"""
ドキュメントを構築するビルダークラス
"""

from typing import Optional, Dict, List
from ..core.document import Document
from ..elements.structure import Section
from ..elements.graphics import Image
from ..elements.boxes import TextBox, Note, Warning, Info
from ..elements.text import Text, Paragraph, List as ListElement
from ..elements.math import Equation, Align
from ..elements.tables import Table


class DocumentBuilder:
    """ドキュメントを構築するビルダークラス"""
    
    def __init__(self, title: str, author: str, date: Optional[str] = None):
        self.document = Document(title, author, date)
        self.current_section: Optional[Section] = None
    
    def set_font(self, font: str):
        """
        フォントを設定（CJKutf8用）
        
        Args:
            font: フォント名（CJKutf8用）
                - "min": 明朝体（デフォルト）
                - "goth": ゴシック体
        
        Note:
            フォントファイルを指定する場合は、set_font_file()を使用してください。
        """
        self.document.font = font
        return self
    
    def set_font_file(self, font_file: str, font_name: Optional[str] = None):
        """
        フォントファイルを設定（XeLaTeX/LuaLaTeX用）
        
        Args:
            font_file: フォントファイルのパス（.ttf, .otfなど）
            font_name: フォント名（省略時はファイル名から自動生成）
        
        Note:
            フォントファイルを指定すると、自動的にXeLaTeXまたはLuaLaTeXが使用されます。
            より安定したフォント表示が可能です。
        
        Example:
            .set_font_file("C:/Windows/Fonts/msgothic.ttc", "MS Gothic")
            .set_font_file("fonts/NotoSansJP-Regular.ttf", "Noto Sans JP")
        """
        from pathlib import Path
        font_path = Path(font_file)
        if not font_path.exists():
            raise FileNotFoundError(f"フォントファイルが見つかりません: {font_file}")
        
        self.document.font_file = str(font_path.absolute())
        self.document.font_name = font_name or font_path.stem
        return self
    
    def set_font_from_url(self, url: str, font_name: Optional[str] = None, 
                         fonts_dir: Optional[str] = None) -> 'DocumentBuilder':
        """
        URLからフォントファイルをダウンロードして設定
        
        Args:
            url: フォントファイルのURL
            font_name: フォント名（省略時はファイル名から自動生成）
            fonts_dir: フォント保存先ディレクトリ（省略時はconfigから取得、デフォルト: fonts）
        
        Returns:
            self（メソッドチェーン用）
        
        Example:
            .set_font_from_url("https://example.com/fonts/NotoSansJP-Regular.ttf", "Noto Sans JP")
        """
        import urllib.request
        import urllib.parse
        from pathlib import Path
        
        # フォント保存先の決定
        if fonts_dir is None:
            # 設定から取得（デフォルト: fonts）
            try:
                from ..config import ConfigManager
                config = ConfigManager()
                config.load_config()
                fonts_dir = config.get("directories.fonts_dir", "fonts")
            except Exception:
                fonts_dir = "fonts"
        
        fonts_path = Path(fonts_dir)
        fonts_path.mkdir(parents=True, exist_ok=True)
        
        # ファイル名をURLから取得
        parsed_url = urllib.parse.urlparse(url)
        filename = Path(parsed_url.path).name
        
        # ファイル名が取得できない場合や拡張子がない場合の処理
        if not filename or not filename.endswith(('.ttf', '.otf', '.ttc', '.woff', '.woff2')):
            # Content-Dispositionヘッダーから取得を試みる
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    content_disposition = response.headers.get('Content-Disposition', '')
                    if 'filename=' in content_disposition:
                        filename = content_disposition.split('filename=')[1].strip('"\'')
                    elif 'filename*=' in content_disposition:
                        # RFC 5987形式の処理
                        filename_part = content_disposition.split('filename*=')[1].split(';')[0]
                        if filename_part.startswith("UTF-8''"):
                            filename = urllib.parse.unquote(filename_part[7:])
                        else:
                            filename = filename_part.strip('"\'')
            except Exception:
                # デフォルト名を使用
                filename = "font.ttf"
        
        font_file_path = fonts_path / filename
        
        # ダウンロード
        print(f"フォントファイルをダウンロード中: {url}")
        try:
            urllib.request.urlretrieve(url, font_file_path)
            print(f"フォントファイルを保存しました: {font_file_path}")
        except Exception as e:
            raise RuntimeError(f"フォントファイルのダウンロードに失敗しました: {e}") from e
        
        # フォントを設定
        return self.set_font_file(str(font_file_path.absolute()), font_name)
    
    def set_margins(self, top: Optional[str] = None, bottom: Optional[str] = None,
                    left: Optional[str] = None, right: Optional[str] = None):
        """
        余白を設定
        
        Args:
            top: 上余白（例: "2cm"）
            bottom: 下余白（例: "2cm"）
            left: 左余白（例: "2cm"）
            right: 右余白（例: "2cm"）
        """
        if top is not None:
            self.document.margins["top"] = top
        if bottom is not None:
            self.document.margins["bottom"] = bottom
        if left is not None:
            self.document.margins["left"] = left
        if right is not None:
            self.document.margins["right"] = right
        return self
    
    def add_package(self, package: str, options: Optional[str] = None):
        """パッケージを追加"""
        self.document.preamble_manager.add_package(package, options)
        return self
    
    def add_section(self, title: str, level: int = 1, label: Optional[str] = None) -> 'SectionBuilder':
        """セクションを追加"""
        section = Section(title, level=level, label=label)
        self.document.add(section)
        self.current_section = section
        return SectionBuilder(self, section)
    
    def add_text(self, text: str):
        """テキストを追加"""
        self.document.add(Text(text))
        return self
    
    def add_paragraph(self, text: str):
        """段落を追加"""
        self.document.add(Paragraph(text))
        return self
    
    def add_image(self, image_path: str, caption: Optional[str] = None,
                  width: str = "0.8", label: Optional[str] = None):
        """画像を追加"""
        img = Image(image_path, caption=caption, width=width, label=label)
        self.document.add(img)
        return self
    
    def add_textbox(self, content: str, title: Optional[str] = None,
                   box_type: str = "tcolorbox", style: Optional[Dict[str, str]] = None):
        """テキストボックスを追加"""
        box = TextBox(content, title=title, box_type=box_type, style=style)
        self.document.add(box)
        return self
    
    def add_note(self, content: str):
        """注意書きを追加"""
        self.document.add(Note(content))
        return self
    
    def add_warning(self, content: str):
        """警告を追加"""
        self.document.add(Warning(content))
        return self
    
    def add_info(self, content: str):
        """情報を追加"""
        self.document.add(Info(content))
        return self
    
    def add_equation(self, equation: str, inline: bool = False, label: Optional[str] = None):
        """数式を追加"""
        eq = Equation(equation, inline=inline, label=label)
        self.document.add(eq)
        return self
    
    def add_table(self, headers: List[str], rows: List[List[str]],
                  caption: Optional[str] = None, label: Optional[str] = None):
        """テーブルを追加"""
        table = Table(headers, rows, caption=caption, label=label)
        self.document.add(table)
        return self
    
    def build(self) -> Document:
        """ドキュメントを構築"""
        return self.document


class SectionBuilder:
    """セクションを構築するビルダー"""
    
    def __init__(self, doc_builder: DocumentBuilder, section: Section):
        self.doc_builder = doc_builder
        self.section = section
    
    def add_text(self, text: str):
        """テキストを追加"""
        self.section.add(Text(text))
        return self
    
    def add_paragraph(self, text: str):
        """段落を追加"""
        self.section.add(Paragraph(text))
        return self
    
    def add_image(self, image_path: str, caption: Optional[str] = None,
                  width: str = "0.8", label: Optional[str] = None):
        """画像を追加"""
        img = Image(image_path, caption=caption, width=width, label=label)
        self.section.add(img)
        return self
    
    def add_textbox(self, content: str, title: Optional[str] = None,
                   box_type: str = "tcolorbox", style: Optional[Dict[str, str]] = None):
        """テキストボックスを追加"""
        box = TextBox(content, title=title, box_type=box_type, style=style)
        self.section.add(box)
        return self
    
    def add_note(self, content: str):
        """注意書きを追加"""
        from ..elements.boxes import Note
        self.section.add(Note(content))
        return self
    
    def add_warning(self, content: str):
        """警告を追加"""
        from ..elements.boxes import Warning
        self.section.add(Warning(content))
        return self
    
    def add_info(self, content: str):
        """情報を追加"""
        from ..elements.boxes import Info
        self.section.add(Info(content))
        return self
    
    def add_equation(self, equation: str, inline: bool = False, label: Optional[str] = None):
        """数式を追加"""
        eq = Equation(equation, inline=inline, label=label)
        self.section.add(eq)
        return self
    
    def add_align(self, equations: List[str], label: Optional[str] = None, numbered: bool = True):
        """複数行の数式を追加"""
        align = Align(equations, label=label, numbered=numbered)
        self.section.add(align)
        return self
    
    def add_list(self, items: List[str], ordered: bool = False):
        """リストを追加"""
        lst = ListElement(items, ordered=ordered)
        self.section.add(lst)
        return self
    
    def add_table(self, headers: List[str], rows: List[List[str]],
                  caption: Optional[str] = None, label: Optional[str] = None):
        """テーブルを追加"""
        table = Table(headers, rows, caption=caption, label=label)
        self.section.add(table)
        return self
    
    def end_section(self) -> DocumentBuilder:
        """セクションを終了"""
        return self.doc_builder

