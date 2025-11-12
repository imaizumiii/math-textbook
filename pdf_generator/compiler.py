"""
LaTeXコンパイル処理を担当するモジュール
"""

import subprocess
import os
import time
from pathlib import Path
from typing import Optional, List, Tuple
from .utils.encoding import safe_decode
from .utils.file_utils import check_command_exists


class LaTeXCompiler:
    """
    LaTeXコンパイル処理を担当
    
    機能:
    - LaTeXファイルのコンパイル
    - 依存関係の確認
    - エラーハンドリングとログ出力
    """
    
    def __init__(self, engine: str = "pdflatex", 
                 compile_times: int = 2,
                 interaction_mode: str = "nonstopmode",
                 extra_options: Optional[List[str]] = None,
                 fallback_encodings: Optional[List[str]] = None):
        """
        Args:
            engine: LaTeXエンジン（pdflatex, xelatex, lualatex）
            compile_times: コンパイル回数
            interaction_mode: インタラクションモード
            extra_options: 追加のLaTeXオプション
            fallback_encodings: フォールバック用エンコーディング
        """
        self.engine = engine
        self.compile_times = compile_times
        self.interaction_mode = interaction_mode
        self.extra_options = extra_options or []
        self.fallback_encodings = fallback_encodings or ['utf-8', 'cp932', 'shift_jis']
    
    def check_dependencies(self) -> bool:
        """
        必要なLaTeXコマンドの存在確認
        
        Returns:
            bool: コマンドが存在する場合True
        
        Raises:
            FileNotFoundError: コマンドが見つからない場合
        """
        if not check_command_exists(self.engine):
            raise FileNotFoundError(
                f"'{self.engine}'コマンドが見つかりません。\n"
                f"  -> TeX Live/MiKTeXがインストールされ、PATHに追加されているか確認してください。"
            )
        return True
    
    def compile(self, tex_file: str, output_dir: Optional[str] = None) -> Tuple[bool, str]:
        """
        PDFをコンパイル
        
        Args:
            tex_file: コンパイルする.texファイルのパス
            output_dir: 出力ディレクトリ（Noneの場合はtex_fileと同じディレクトリ）
        
        Returns:
            Tuple[bool, str]: (成功フラグ, エラーメッセージ)
        
        Raises:
            FileNotFoundError: tex_fileが見つからない場合
            RuntimeError: コンパイルエラー時
        """
        tex_path = Path(tex_file)
        if not tex_path.exists():
            raise FileNotFoundError(f"LaTeXファイルが見つかりません: {tex_file}")
        
        # 出力ディレクトリの設定
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            work_dir = output_path
            # tex_fileをwork_dirにコピー（または同じディレクトリの場合はそのまま）
            if tex_path.parent != work_dir:
                import shutil
                target_tex = work_dir / tex_path.name
                shutil.copy2(tex_path, target_tex)
                tex_file_to_compile = target_tex
            else:
                tex_file_to_compile = tex_path
        else:
            work_dir = tex_path.parent
            tex_file_to_compile = tex_path
        
        # 依存関係の確認
        self.check_dependencies()
        
        # コンパイルコマンドの構築
        cmd = [
            self.engine,
            f'-interaction={self.interaction_mode}',
            *self.extra_options,
            str(tex_file_to_compile.name)
        ]
        
        errors = []
        
        # 指定回数コンパイル
        for i in range(self.compile_times):
            try:
                result = subprocess.run(
                    cmd,
                    cwd=str(work_dir),
                    capture_output=True,
                    check=False,
                    timeout=60  # タイムアウト60秒
                )
                
                # 出力をデコード
                stdout = safe_decode(result.stdout, self.fallback_encodings)
                stderr = safe_decode(result.stderr, self.fallback_encodings)
                
                # エラーの記録
                if result.returncode != 0:
                    error_msg = f"{i+1}回目のコンパイルでエラーが発生しました:\n"
                    if stderr:
                        error_msg += f"stderr: {stderr}\n"
                    if stdout:
                        # LaTeXのエラーメッセージは通常stdoutに出力される
                        error_msg += f"stdout: {stdout[-2000:]}\n"  # 最後の2000文字
                    errors.append(error_msg)
                
            except subprocess.TimeoutExpired:
                raise RuntimeError(
                    f"コンパイルがタイムアウトしました（60秒）。"
                    f"大きなファイルや複雑なLaTeXファイルの可能性があります。"
                )
            except Exception as e:
                raise RuntimeError(f"コンパイル中に予期しないエラーが発生しました: {e}") from e
        
        # PDFファイルが作成されたか確認
        pdf_file = work_dir / f"{tex_file_to_compile.stem}.pdf"
        if not pdf_file.exists():
            # 別の場所を確認（元のtex_fileと同じディレクトリ）
            pdf_file = tex_path.with_suffix('.pdf')
        
        if not pdf_file.exists():
            error_summary = "\n".join(errors) if errors else "不明なエラー"
            raise RuntimeError(
                f"PDFファイルが作成されませんでした。\n"
                f"コンパイルログ:\n{error_summary}"
            )
        
        # PDFが作成された場合は成功（警告があっても続行）
        # エラーメッセージは警告として返す
        return True, "\n".join(errors) if errors else ""
    
    def cleanup(self, tex_file: str, extensions: List[str], 
                output_dir: Optional[str] = None) -> None:
        """
        中間ファイルを削除
        
        Args:
            tex_file: .texファイルのパス
            extensions: 削除する拡張子のリスト
            output_dir: 出力ディレクトリ
        """
        tex_path = Path(tex_file)
        base_name = tex_path.stem
        
        if output_dir:
            work_dir = Path(output_dir)
        else:
            work_dir = tex_path.parent
        
        time.sleep(0.5)  # ファイルが完全に閉じられるまで少し待つ
        
        for ext in extensions:
            temp_file = work_dir / f"{base_name}{ext}"
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except (PermissionError, FileNotFoundError):
                    # ファイルが使用中または既に削除されている場合はスキップ
                    pass
