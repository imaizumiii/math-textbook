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
    
    def __init__(self, title: Optional[str], author: str, date: Optional[str] = None,
                 font: str = "min", margins: Optional[Dict[str, str]] = None,
                 font_file: Optional[str] = None, font_name: Optional[str] = None,
                 line_spacing: Optional[float] = None):
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
        
        # 行間設定（デフォルト: None = LaTeXのデフォルト）
        # 例: 1.5 で1.5倍の行間
        self.line_spacing = line_spacing
        
        self.preamble_manager = PreambleManager()
        self.content: List[LaTeXElement] = []
        self.renderer = LaTeXRenderer()
    
    def add(self, element: LaTeXElement):
        """要素を追加"""
        self.content.append(element)
        return self
    
    def set_abstract(self, abstract: str):
        """アブストラクトを設定"""
        self.abstract = abstract
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
        フォントファイルを出力ディレクトリにコピー（太字フォントも自動的にコピー）
        
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
        
        # 太字フォントを自動検出してコピー
        font_stem = font_path.stem
        font_parent = font_path.parent
        
        # 一般的な太字フォント名のパターンをチェック
        bold_patterns = [
            font_stem.replace("Regular", "Bold"),
            font_stem.replace("-Regular", "-Bold"),
            font_stem.replace("_Regular", "_Bold"),
            font_stem + "Bold",
            font_stem + "-Bold",
            font_stem + "_Bold",
        ]
        
        # 既存のパターンから重複を除去
        bold_patterns = list(dict.fromkeys(bold_patterns))
        
        bold_font_copied = False
        for pattern in bold_patterns:
            bold_font_path = font_parent / f"{pattern}{font_path.suffix}"
            if bold_font_path.exists():
                bold_dest_path = fonts_dir / bold_font_path.name
                shutil.copy2(bold_font_path, bold_dest_path)
                bold_font_copied = True
                break
        
        # 太字フォントが見つからない場合、同じディレクトリ内の他の太字フォントを検索
        if not bold_font_copied:
            for bold_file in font_parent.glob("*Bold*.ttf"):
                if bold_file.exists():
                    bold_dest_path = fonts_dir / bold_file.name
                    shutil.copy2(bold_file, bold_dest_path)
                    bold_font_copied = True
                    break
            if not bold_font_copied:
                for bold_file in font_parent.glob("*Bold*.otf"):
                    if bold_file.exists():
                        bold_dest_path = fonts_dir / bold_file.name
                        shutil.copy2(bold_file, bold_dest_path)
                        break
        
        # 相対パスを保存（LaTeXで使用するため）
        self.font_file = str(dest_path.absolute())
        return f"fonts/{font_path.name}"

