"""
ドキュメントを構築するビルダークラス
"""

from typing import Optional, Dict, List, Union, Any
from ..core.document import Document
from ..elements.structure import Section, DrawingSpace, Exercise, BlankSpace
from ..elements.graphics import Image
from ..elements.boxes import TextBox, Note, Warning, Info
from ..elements.text import Text, Paragraph, List as ListElement, Line, Divider
from ..elements.math import Equation, Align
from ..elements.tables import Table


class DocumentBuilder:
    """ドキュメントを構築するビルダークラス"""
    
    def __init__(self, title: Optional[str] = None, author: str = "", date: Optional[str] = None):
        self.document = Document(title, author, date)
        self.current_section: Optional[Section] = None
    
    def _add_line_to_container(self, container: Any, text: str,
                               line_style: str = "solid",
                               line_thickness: str = "0.4pt",
                               color: Optional[str] = None):
        """
        装飾線付きテキストをコンテナに追加する共通メソッド（例: ----解答----）
        
        Args:
            container: 追加先のコンテナ（document, section, drawing_spaceなど）
            text: 中央に表示するテキスト
            line_style: 線のスタイル
                - "solid": 実線（デフォルト）
                - "dashed": 破線
                - "dotted": 点線
                - "double": 二重線
            line_thickness: 線の太さ（例: "0.4pt", "1pt", "5pt"）
            color: 線の色（例: "gray", "grey", "black", "red"など。Noneの場合は黒）
        """
        # 色が指定されている場合はxcolorパッケージを追加
        if color:
            self.add_package("xcolor")
        line = Line(text, line_style=line_style, line_thickness=line_thickness,
                    color=color)
        container.add(line)
    
    def set_title(self, title: str):
        """
        タイトルを設定
        
        Args:
            title: タイトル文字列
        
        Returns:
            self（メソッドチェーン用）
        """
        self.document.title = title
        return self
    
    def set_abstract(self, abstract: str):
        """アブストラクトを設定"""
        self.document.set_abstract(abstract)
        return self
    
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
    
    def set_line_spacing(self, spacing: float):
        """
        行間を設定
        
        Args:
            spacing: 行間の倍率（例: 1.5 で1.5倍の行間、2.0 で2倍の行間）
        
        Example:
            .set_line_spacing(1.5)  # 1.5倍の行間を設定
        """
        if spacing <= 0:
            raise ValueError("行間の倍率は0より大きい値である必要があります")
        self.document.line_spacing = spacing
        return self
    
    def add_package(self, package: str, options: Optional[str] = None):
        """パッケージを追加"""
        self.document.preamble_manager.add_package(package, options)
        return self
    
    def add_section(self, title: str, level: int = 1, label: Optional[str] = None, numbered: bool = False) -> 'SectionBuilder':
        """
        セクションを追加
        
        Args:
            title: セクションのタイトル
            level: セクションのレベル（1: section, 2: subsection, ...）
            label: 参照用のラベル
            numbered: 番号を振るかどうか（デフォルト: False）
        """
        section = Section(title, level=level, label=label, numbered=numbered)
        self.document.add(section)
        self.current_section = section
        return SectionBuilder(self, section)
    
    def add_text(self, text: str, bold: bool = False):
        """
        テキストを追加
        
        Args:
            text: テキスト文字列
            bold: 太字にするかどうか（デフォルト: False）
        """
        self.document.add(Text(text, bold=bold))
        return self
    
    def add_abstract(self, text: str, bold: bool = True, centered: bool = True):
        """
        アブストラクト（概要）を追加
        
        Args:
            text: 表示するテキスト
            bold: 太字にするかどうか（デフォルト: True）
            centered: 中央寄せにするかどうか（デフォルト: True）
        
        Note:
            呼び出した位置（Document/Sectionの要素列）にそのまま挿入されます。
        """
        formatted_text = text
        if bold:
            formatted_text = f"\\textbf{{{formatted_text}}}"
        if centered:
            formatted_text = f"\\begin{{center}}\n{formatted_text}\n\\end{{center}}"
        self.document.add(Paragraph(formatted_text))
        return self
    
    def add_paragraph(self, text: str, bold: bool = False):
        """
        段落を追加
        
        Args:
            text: 段落のテキスト
            bold: 太字にするかどうか（デフォルト: False）
        """
        self.document.add(Paragraph(text, bold=bold))
        return self
    
    def add_line(self, text: str, 
                 line_style: str = "solid",
                 line_thickness: str = "5pt",
                 color: Optional[str] = "gray"):
        """装飾線付きテキストを追加（例: ----解答----）"""
        self._add_line_to_container(self.document, text, line_style, line_thickness,
                                    color)
        return self
    
    def add_divider(self, symbol: str = "*", spacing: str = "10em",
                    vspace: str = "0.0em", 
                    vspace_before: Optional[str] = None,
                    vspace_after: Optional[str] = None):
        """
        軽い区切りを追加（例: *        *        *）
        
        Args:
            symbol: 区切りに使用する記号（デフォルト: "*"）
            spacing: 記号間の間隔（デフォルト: "10em"、例: "1em", "1.5em", "10em"など）
            vspace: 上下の余白（デフォルト: "-1em"、負の値で余白を減らす）
            vspace_before: 上の余白（指定時はvspaceより優先）
            vspace_after: 下の余白（指定時はvspaceより優先）
        
        Returns:
            self（メソッドチェーン用）
        """
        self.document.add(Divider(symbol=symbol, spacing=spacing, vspace=vspace, 
                                  vspace_before=vspace_before, 
                                  vspace_after=vspace_after))
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
    
    def add_blank_space(self, height: str):
        """
        手書き用の空白スペースを追加
        
        Args:
            height: 空白の高さ（例: "5cm", "50mm", "10em"）
        """
        self.document.add(BlankSpace(height))
        return self
    
    def add_drawing_space(self, width: str = "0.7\\textwidth", 
                         right_margin: str = "5cm") -> 'DrawingSpaceBuilder':
        """
        手書き用の余白を確保する領域を追加
        
        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
        
        Returns:
            DrawingSpaceBuilder（メソッドチェーン用）
        
        Example:
            .add_drawing_space(right_margin="5cm")
                .add_paragraph("この部分だけ右側に余白があります")
                .end_drawing_space()
        """
        drawing_space = DrawingSpace(width=width, right_margin=right_margin)
        self.document.add(drawing_space)
        return DrawingSpaceBuilder(self, drawing_space, parent_builder=self)
    
    def add_exercise(self, title: str, content: str, items: Optional[List[str]] = None, columns: int = 1):
        """
        小問（練習問題）を追加
        
        Args:
            title: 小問のタイトル（例: "練習4"）
            content: 問題の本文
            items: 小問のリスト（例: ["$f(x) = x^2$", "$f(x) = 3x + 1$"]）
            columns: 列数（1: 縦並び, 2以上: 横並び（段組み））
        
        Returns:
            self（メソッドチェーン用）
        
        Example:
            .add_exercise("練習4", "次の関数を微分せよ。", items=["$f(x) = x^2$", "$f(x) = 3x + 1$"], columns=2)
        """
        if columns > 1:
            self.add_package("multicol")
        exercise = Exercise(title=title, content=content, items=items, columns=columns)
        self.document.add(exercise)
        return self
    
    def build(self) -> Document:
        """ドキュメントを構築"""
        return self.document


class SectionBuilder:
    """セクションを構築するビルダー"""
    
    def __init__(self, doc_builder: DocumentBuilder, section: Section):
        self.doc_builder = doc_builder
        self.section = section
    
    def add_text(self, text: str, bold: bool = False):
        """
        テキストを追加
        
        Args:
            text: テキスト文字列
            bold: 太字にするかどうか（デフォルト: False）
        """
        self.section.add(Text(text, bold=bold))
        return self
    
    def add_paragraph(self, text: str, bold: bool = False):
        """
        段落を追加
        
        Args:
            text: 段落のテキスト
            bold: 太字にするかどうか（デフォルト: False）
        """
        self.section.add(Paragraph(text, bold=bold))
        return self
    
    def add_line(self, text: str, 
                 line_style: str = "solid",
                 line_thickness: str = "5pt",
                 color: Optional[str] = "gray"):
        """装飾線付きテキストを追加（例: ----解答----）"""
        self.doc_builder._add_line_to_container(self.section, text, line_style, line_thickness,
                                                 color)
        return self
    
    def add_divider(self, symbol: str = "*", spacing: str = "10em",
                    vspace: str = "0.0em", 
                    vspace_before: Optional[str] = None,
                    vspace_after: Optional[str] = None):
        """
        軽い区切りを追加（例: *        *        *）
        
        Args:
            symbol: 区切りに使用する記号（デフォルト: "*"）
            spacing: 記号間の間隔（デフォルト: "10em"、例: "1em", "1.5em", "10em"など）
            vspace: 上下の余白（デフォルト: "-1em"、負の値で余白を減らす）
            vspace_before: 上の余白（指定時はvspaceより優先）
            vspace_after: 下の余白（指定時はvspaceより優先）
        
        Returns:
            self（メソッドチェーン用）
        """
        self.section.add(Divider(symbol=symbol, spacing=spacing, vspace=vspace, 
                                 vspace_before=vspace_before, 
                                 vspace_after=vspace_after))
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
    
    def add_align(self, equations: List[str], label: Optional[str] = None, numbered: bool = False, vspace: Optional[str] = None):
        """
        複数行の数式を追加
        
        Args:
            equations: 数式のリスト
            label: ラベル
            numbered: 番号を振るかどうか
            vspace: 直前の余白調整（例: "-1em", "5pt"）
        """
        align = Align(equations, label=label, numbered=numbered, vspace=vspace)
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

    def add_abstract(self, text: str, bold: bool = True, centered: bool = True):
        """
        セクション内に概要を追加
        """
        formatted_text = text
        if bold:
            formatted_text = f"\\textbf{{{formatted_text}}}"
        if centered:
            formatted_text = f"\\begin{{center}}\n{formatted_text}\n\\end{{center}}"
        self.section.add(Paragraph(formatted_text))
        return self
    
    def add_blank_space(self, height: str):
        """
        手書き用の空白スペースを追加
        
        Args:
            height: 空白の高さ（例: "5cm", "50mm", "10em"）
        """
        self.section.add(BlankSpace(height))
        return self
    
    def add_drawing_space(self, width: str = "0.7\\textwidth", 
                         right_margin: str = "5cm") -> 'DrawingSpaceBuilder':
        """
        手書き用の余白を確保する領域を追加
        
        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
        
        Returns:
            DrawingSpaceBuilder（メソッドチェーン用）
        """
        drawing_space = DrawingSpace(width=width, right_margin=right_margin)
        self.section.add(drawing_space)
        return DrawingSpaceBuilder(self.doc_builder, drawing_space, parent_builder=self)
    
    def add_exercise(self, title: str, content: str, items: Optional[List[str]] = None, columns: int = 1):
        """
        小問（練習問題）を追加
        
        Args:
            title: 小問のタイトル（例: "練習4"）
            content: 問題の本文
            items: 小問のリスト（例: ["$f(x) = x^2$", "$f(x) = 3x + 1$"]）
            columns: 列数（1: 縦並び, 2以上: 横並び（段組み））
        
        Returns:
            self（メソッドチェーン用）
        
        Example:
            .add_exercise("練習4", "次の関数を微分せよ。", items=["$f(x) = x^2$", "$f(x) = 3x + 1$"], columns=2)
        """
        if columns > 1:
            self.doc_builder.add_package("multicol")
        exercise = Exercise(title=title, content=content, items=items, columns=columns)
        self.section.add(exercise)
        return self
    
    def end_section(self) -> DocumentBuilder:
        """セクションを終了"""
        return self.doc_builder


class DrawingSpaceBuilder:
    """DrawingSpaceを構築するビルダー"""
    
    def __init__(self, doc_builder: DocumentBuilder, drawing_space: DrawingSpace, 
                 parent_builder: Any = None):
        self.doc_builder = doc_builder
        self.drawing_space = drawing_space
        # 親ビルダー（DocumentBuilderまたはSectionBuilder）を保持
        self.parent_builder = parent_builder if parent_builder is not None else doc_builder
    
    def add_text(self, text: str, bold: bool = False):
        """
        テキストを追加
        
        Args:
            text: テキスト文字列
            bold: 太字にするかどうか（デフォルト: False）
        """
        self.drawing_space.add(Text(text, bold=bold))
        return self
    
    def add_paragraph(self, text: str, bold: bool = False):
        """
        段落を追加
        
        Args:
            text: 段落のテキスト
            bold: 太字にするかどうか（デフォルト: False）
        """
        self.drawing_space.add(Paragraph(text, bold=bold))
        return self
    
    def add_line(self, text: str, 
                 line_style: str = "solid",
                 line_thickness: str = "5pt",
                 color: Optional[str] = "gray"):
        """装飾線付きテキストを追加（例: ----解答----）"""
        self.doc_builder._add_line_to_container(self.drawing_space, text, line_style, line_thickness,
                                                color)
        return self
    
    def add_divider(self, symbol: str = "*", spacing: str = "10em",
                    vspace: str = "0.0em", 
                    vspace_before: Optional[str] = None,
                    vspace_after: Optional[str] = None):
        """
        軽い区切りを追加（例: *        *        *）
        
        Args:
            symbol: 区切りに使用する記号（デフォルト: "*"）
            spacing: 記号間の間隔（デフォルト: "10em"、例: "1em", "1.5em", "10em"など）
            vspace: 上下の余白（デフォルト: "-1em"、負の値で余白を減らす）
            vspace_before: 上の余白（指定時はvspaceより優先）
            vspace_after: 下の余白（指定時はvspaceより優先）
        
        Returns:
            self（メソッドチェーン用）
        """
        self.drawing_space.add(Divider(symbol=symbol, spacing=spacing, vspace=vspace, 
                                       vspace_before=vspace_before, 
                                       vspace_after=vspace_after))
        return self
    
    def add_image(self, image_path: str, caption: Optional[str] = None,
                  width: str = "0.8", label: Optional[str] = None):
        """画像を追加"""
        img = Image(image_path, caption=caption, width=width, label=label)
        self.drawing_space.add(img)
        return self
    
    def add_textbox(self, content: str, title: Optional[str] = None,
                   box_type: str = "tcolorbox", style: Optional[Dict[str, str]] = None):
        """テキストボックスを追加"""
        box = TextBox(content, title=title, box_type=box_type, style=style)
        self.drawing_space.add(box)
        return self
    
    def add_note(self, content: str):
        """注意書きを追加"""
        self.drawing_space.add(Note(content))
        return self
    
    def add_warning(self, content: str):
        """警告を追加"""
        self.drawing_space.add(Warning(content))
        return self
    
    def add_info(self, content: str):
        """情報を追加"""
        self.drawing_space.add(Info(content))
        return self
    
    def add_equation(self, equation: str, inline: bool = False, label: Optional[str] = None):
        """数式を追加"""
        eq = Equation(equation, inline=inline, label=label)
        self.drawing_space.add(eq)
        return self
    
    def add_align(self, equations: List[str], label: Optional[str] = None, numbered: bool = False, vspace: Optional[str] = None):
        """
        複数行の数式を追加
        
        Args:
            equations: 数式のリスト
            label: ラベル
            numbered: 番号を振るかどうか
            vspace: 直前の余白調整（例: "-1em", "5pt"）
        """
        align = Align(equations, label=label, numbered=numbered, vspace=vspace)
        self.drawing_space.add(align)
        return self
    
    def add_list(self, items: List[str], ordered: bool = False):
        """リストを追加"""
        lst = ListElement(items, ordered=ordered)
        self.drawing_space.add(lst)
        return self
    
    def add_table(self, headers: List[str], rows: List[List[str]],
                  caption: Optional[str] = None, label: Optional[str] = None):
        """テーブルを追加"""
        table = Table(headers, rows, caption=caption, label=label)
        self.drawing_space.add(table)
        return self
    
    def add_blank_space(self, height: str):
        """
        手書き用の空白スペースを追加
        
        Args:
            height: 空白の高さ（例: "5cm", "50mm", "10em"）
        """
        self.drawing_space.add(BlankSpace(height))
        return self
    
    def add_exercise(self, title: str, content: str, items: Optional[List[str]] = None, columns: int = 1):
        """
        小問（練習問題）を追加
        
        Args:
            title: 小問のタイトル（例: "練習4"）
            content: 問題の本文
            items: 小問のリスト（例: ["$f(x) = x^2$", "$f(x) = 3x + 1$"]）
            columns: 列数（1: 縦並び, 2以上: 横並び（段組み））
        
        Returns:
            self（メソッドチェーン用）
        
        Example:
            .add_exercise("練習4", "次の関数を微分せよ。", items=["$f(x) = x^2$", "$f(x) = 3x + 1$"], columns=2)
        """
        if columns > 1:
            self.doc_builder.add_package("multicol")
        exercise = Exercise(title=title, content=content, items=items, columns=columns)
        self.drawing_space.add(exercise)
        return self
    
    def end_drawing_space(self):
        """DrawingSpaceを終了し、親ビルダーに戻る"""
        # parent_builderがNoneでないことを確認
        if self.parent_builder is None:
            return self.doc_builder
        return self.parent_builder

