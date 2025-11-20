"""
PDF生成のメインクラス
"""

from pathlib import Path
from typing import Optional
from .document import Document
from ..compiler import LaTeXCompiler
from ..config import ConfigManager


class PDFGenerator:
    """PDF生成のメインクラス"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
        """
        self.config_manager = ConfigManager(config_path)
        self.config_manager.load_config()
        self.compiler = LaTeXCompiler(
            engine=self.config_manager.get("compilation.engine", "pdflatex"),
            compile_times=self.config_manager.get("compilation.compile_times", 2),
            interaction_mode=self.config_manager.get("compilation.interaction_mode", "nonstopmode"),
            extra_options=self.config_manager.get("compilation.extra_options", []),
            fallback_encodings=self.config_manager.get("encoding.fallback_encodings", ['utf-8', 'cp932'])
        )
        
        # ディレクトリの作成
        self._ensure_directories()
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        output_dir = self.config_manager.get("directories.output_dir", "output")
        temp_dir = self.config_manager.get("directories.temp_dir")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        if temp_dir:
            Path(temp_dir).mkdir(parents=True, exist_ok=True)
    
    def generate(self, document: Document, output_name: Optional[str] = None) -> str:
        """
        DocumentからPDFを生成
        
        Args:
            document: Documentインスタンス
            output_name: 出力ファイル名（省略時は自動生成）
        
        Returns:
            生成されたPDFファイルのパス
        
        Raises:
            RuntimeError: コンパイルエラー時
        """
        output_dir = Path(self.config_manager.get("directories.output_dir", "output"))
        temp_dir = Path(self.config_manager.get("directories.temp_dir", output_dir))
        
        # 画像の処理
        document.process_images(output_dir)
        
        # フォントファイルの処理
        document.process_fonts(output_dir)
        
        # LaTeXコード生成
        latex_content = document.to_latex()
        
        # 出力ファイル名の決定
        if output_name is None:
            if document.title:
                output_name = f"{document.title.replace(' ', '_')}.pdf"
            else:
                output_name = "document.pdf"
        
        # 一時的な.texファイルを作成
        temp_tex_file = temp_dir / f"{Path(output_name).stem}.tex"
        temp_tex_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_tex_file, "w",
                  encoding=self.config_manager.get("encoding.output_encoding", "utf-8")) as f:
            f.write(latex_content)
        
        # フォントファイルが指定されている場合は、XeLaTeXまたはLuaLaTeXを使用
        original_engine = self.compiler.engine
        if document.font_file:
            # XeLaTeXを優先的に試す（LuaLaTeXも可能）
            preferred_engines = ["xelatex", "lualatex"]
            engine_found = False
            for engine in preferred_engines:
                try:
                    # エンジンの存在確認
                    from ..utils.file_utils import check_command_exists
                    if check_command_exists(engine):
                        self.compiler.engine = engine
                        engine_found = True
                        break
                except FileNotFoundError:
                    continue
            
            if not engine_found:
                import warnings
                warnings.warn(
                    "フォントファイルが指定されていますが、XeLaTeXまたはLuaLaTeXが見つかりません。"
                    "デフォルトのエンジンを使用しますが、フォントが正しく表示されない可能性があります。"
                )
        
        # PDFをコンパイル
        success, error_msg = self.compiler.compile(str(temp_tex_file), output_dir)
        
        # エンジンを元に戻す
        self.compiler.engine = original_engine
        
        if not success:
            raise RuntimeError(f"PDFのコンパイルに失敗しました:\n{error_msg}")
        
        if error_msg:
            import warnings
            warnings.warn(f"PDFは生成されましたが、コンパイル時に警告がありました:\n{error_msg}")
        
        # 生成されたPDFファイルのパスを取得
        compiled_pdf = Path(output_dir) / f"{Path(temp_tex_file).stem}.pdf"
        pdf_file = Path(output_dir) / output_name
        
        if compiled_pdf.exists() and compiled_pdf != pdf_file:
            if pdf_file.exists():
                pdf_file.unlink()
            compiled_pdf.rename(pdf_file)
        elif not pdf_file.exists() and compiled_pdf.exists():
            pdf_file = compiled_pdf
        
        # クリーンアップ
        cleanup = self.config_manager.get("file_management.cleanup", True)
        if cleanup:
            keep_tex = self.config_manager.get("file_management.keep_tex", False)
            keep_log = self.config_manager.get("file_management.keep_log", False)
            
            extensions_to_remove = self.config_manager.get(
                "file_management.cleanup_extensions",
                ['.aux', '.log', '.out', '.synctex.gz']
            )
            
            if not keep_tex:
                extensions_to_remove.append('.tex')
            if not keep_log:
                if '.log' not in extensions_to_remove:
                    extensions_to_remove.append('.log')
            
            self.compiler.cleanup(str(temp_tex_file), extensions_to_remove, output_dir)
        
        return str(pdf_file)

