"""
ドキュメント全体を管理するクラス
"""

from typing import List, Optional, Dict
from pathlib import Path
from ..elements.base import LaTeXElement
from ..renderer.latex_renderer import LaTeXRenderer
from ..renderer.preamble import PreambleManager


class Document:
    """LaTeXドキュメント全体を表現するクラス"""
    
    def __init__(self, title: str, author: str, date: Optional[str] = None,
                 font: str = "min", margins: Optional[Dict[str, str]] = None,
                 font_file: Optional[str] = None, font_name: Optional[str] = None):
        self.title = title
        self.author = author
        self.date = date
        self.abstract: Optional[str] = None
        
        # フォント設定（CJKutf8用: min=明朝体, goth=ゴシック体）
        # font_fileが指定された場合は、XeLaTeX/LuaLaTeX + fontspecを使用
        self.font = font
        
        # フォントファイルパス（.ttf, .otfなど）
        # 指定された場合は、CJKutf8の代わりにfontspecを使用
        self.font_file = font_file
        
        # フォント名（システムフォント名またはフォントファイルの内部名）
        # font_fileが指定されている場合は、この名前でフォントを参照
        self.font_name = font_name or (Path(font_file).stem if font_file else None)
        
        # 余白設定（デフォルト: None = LaTeXのデフォルト）
        # 例: {"top": "2cm", "bottom": "2cm", "left": "2cm", "right": "2cm"}
        self.margins = margins or {}
        
        self.preamble_manager = PreambleManager()
        self.content: List[LaTeXElement] = []
        self.renderer = LaTeXRenderer()
    
    def add(self, element: LaTeXElement):
        """要素を追加"""
        self.content.append(element)
        return self
    
    def to_latex(self) -> str:
        """LaTeXコードに変換"""
        return self.renderer.render_document(self)
    
    def process_images(self, output_dir: Path) -> dict:
        """
        画像などのリソースを処理
        
        Args:
            output_dir: 出力ディレクトリ
        
        Returns:
            リソースのパスマッピング
        """
        result = {}
        for element in self.content:
            result.update(element.process_resources(output_dir))
        return result
    
    def process_fonts(self, output_dir: Path) -> Optional[str]:
        """
        フォントファイルを出力ディレクトリにコピー
        
        Args:
            output_dir: 出力ディレクトリ
        
        Returns:
            コピー後のフォントファイルの相対パス、またはNone
        """
        if not self.font_file:
            return None
        
        import shutil
        font_path = Path(self.font_file)
        if not font_path.exists():
            raise FileNotFoundError(f"フォントファイルが見つかりません: {self.font_file}")
        
        fonts_dir = output_dir / "fonts"
        fonts_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = fonts_dir / font_path.name
        shutil.copy2(font_path, dest_path)
        
        # 相対パスを保存（LaTeXで使用するため）
        self.font_file = str(dest_path.absolute())
        return f"fonts/{font_path.name}"

