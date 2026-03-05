"""
PDFプレビュー用ユーティリティ
"""

import os
import subprocess
import platform
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class Previewer(ABC):
    """プレビューアの基底クラス"""
    
    @abstractmethod
    def preview(self, pdf_path: str):
        """PDFをプレビューする"""
        pass


class OSPreviewer(Previewer):
    """OS標準のビューアでPDFを開くプレビューア"""
    
    def preview(self, pdf_path: str):
        """
        OS標準のアプリケーションでPDFを開く
        
        Args:
            pdf_path: PDFファイルのパス
        """
        path = Path(pdf_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
            
        system = platform.system()
        try:
            if system == "Windows":
                # Windowsのstartfileは非ブロッキング
                os.startfile(str(path))
            else:
                # macOS (Darwin) または Linux (xdg-open)
                cmd = ["open", str(path)] if system == "Darwin" else ["xdg-open", str(path)]
                
                # 非ブロッキングで起動。
                # start_new_session=True により、Pythonスクリプト終了後もビューアを維持する。
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
        except Exception as e:
            print(f"プレビューの起動に失敗しました: {e}")


class LivePreviewer(Previewer):
    """
    (将来的な拡張用) ライブプレビューアのプレースホルダ
    
    ファイルを監視し、変更があれば再読み込みするなどの処理を想定
    """
    
    def __init__(self, generator, document, output_name: Optional[str] = None):
        self.generator = generator
        self.document = document
        self.output_name = output_name
        self._is_running = False
    
    def preview(self, pdf_path: str):
        """
        初回起動と監視の開始
        """
        # ここに watchdog 等を使った監視ロジックを実装可能
        print(f"Live preview started for {pdf_path}. (Not fully implemented yet)")
        OSPreviewer().preview(pdf_path)


def get_previewer(preview_type: str = "os", **kwargs) -> Previewer:
    """
    プレビューアのインスタンスを取得する
    
    Args:
        preview_type: 'os' または 'live'
        **kwargs: プレビューアの初期化引数
        
    Returns:
        Previewer インスタンス
    """
    if preview_type == "os":
        return OSPreviewer()
    elif preview_type == "live":
        return LivePreviewer(**kwargs)
    else:
        raise ValueError(f"未知のプレビュータイプです: {preview_type}")
