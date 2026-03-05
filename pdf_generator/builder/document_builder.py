"""
ドキュメントを構築するビルダークラス
"""

from __future__ import annotations

from typing import Any, Optional, Union
from ..core.document import Document
from ..elements.structure import Section, DrawingSpace
from ..elements.graphics import Image, TikZ
from ..elements.text import Line
from .content_mixin import ContentAdderMixin
from ..exceptions import FontNotFoundError


class DocumentBuilder(ContentAdderMixin):
    """ドキュメントを構築するビルダークラス"""

    def __init__(self, title: Optional[str] = None, author: str = "", date: Optional[str] = None):
        self.document = Document(title, author, date)
        self.current_section: Optional[Section] = None

    @property
    def _container(self) -> Document:
        return self.document

    @property
    def _doc_builder(self) -> DocumentBuilder:
        return self

    def _add_line_to_container(self, container: Any, text: str,
                               line_style: str = "solid",
                               line_thickness: str = "0.4pt",
                               color: Optional[str] = None) -> None:
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
        if color:
            self.add_package("xcolor")
        line = Line(text, line_style=line_style, line_thickness=line_thickness, color=color)
        container.add(line)

    def set_title(self, title: str) -> DocumentBuilder:
        """
        タイトルを設定

        Args:
            title: タイトル文字列

        Returns:
            self（メソッドチェーン用）
        """
        self.document.title = title
        return self

    def set_abstract(self, abstract: str) -> DocumentBuilder:
        """アブストラクトを設定"""
        self.document.set_abstract(abstract)
        return self

    def set_font(self, font: str) -> DocumentBuilder:
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

    def set_font_file(self, font_file: str, font_name: Optional[str] = None) -> DocumentBuilder:
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
            raise FontNotFoundError(f"フォントファイルが見つかりません: {font_file}")

        self.document.font_file = str(font_path.absolute())
        self.document.font_name = font_name or font_path.stem
        return self

    def set_font_from_url(self, url: str, font_name: Optional[str] = None,
                          fonts_dir: Optional[str] = None) -> DocumentBuilder:
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

        if fonts_dir is None:
            try:
                from ..config import ConfigManager
                config = ConfigManager()
                config.load_config()
                fonts_dir = config.get("directories.fonts_dir", "fonts")
            except Exception:
                fonts_dir = "fonts"

        fonts_path = Path(fonts_dir)
        fonts_path.mkdir(parents=True, exist_ok=True)

        parsed_url = urllib.parse.urlparse(url)
        filename = Path(parsed_url.path).name

        if not filename or not filename.endswith(('.ttf', '.otf', '.ttc', '.woff', '.woff2')):
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    content_disposition = response.headers.get('Content-Disposition', '')
                    if 'filename=' in content_disposition:
                        filename = content_disposition.split('filename=')[1].strip('"\'')
                    elif 'filename*=' in content_disposition:
                        filename_part = content_disposition.split('filename*=')[1].split(';')[0]
                        if filename_part.startswith("UTF-8''"):
                            filename = urllib.parse.unquote(filename_part[7:])
                        else:
                            filename = filename_part.strip('"\'')
            except Exception:
                filename = "font.ttf"

        font_file_path = fonts_path / filename

        print(f"フォントファイルをダウンロード中: {url}")
        try:
            urllib.request.urlretrieve(url, font_file_path)
            print(f"フォントファイルを保存しました: {font_file_path}")
        except Exception as e:
            raise FontNotFoundError(f"フォントファイルのダウンロードに失敗しました: {e}") from e

        return self.set_font_file(str(font_file_path.absolute()), font_name)

    def set_margins(self, top: Optional[str] = None, bottom: Optional[str] = None,
                    left: Optional[str] = None, right: Optional[str] = None) -> DocumentBuilder:
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

    def set_line_spacing(self, spacing: float) -> DocumentBuilder:
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

    def add_package(self, package: str, options: Optional[str] = None) -> DocumentBuilder:
        """パッケージを追加"""
        self.document.preamble_manager.add_package(package, options)
        return self

    def add_section(self, title: str, level: int = 1, label: Optional[str] = None,
                    numbered: bool = False) -> SectionBuilder:
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

    def add_drawing_space(self, width: str = "0.7\\textwidth",
                          right_margin: str = "5cm",
                          margin_image: Optional[str] = None,
                          margin_content: Optional[Any] = None) -> DrawingSpaceBuilder:
        """
        手書き用の余白を確保する領域を追加

        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
            margin_image: 右側の余白に表示する画像のパス（オプション）
            margin_content: 右側の余白に表示するコンテンツ（TikZオブジェクトなど。margin_imageより優先度は低い）

        Returns:
            DrawingSpaceBuilder（メソッドチェーン用）

        Example:
            .add_drawing_space(right_margin="5cm", margin_image="fig.png")
                .add_paragraph("この部分だけ右側に余白（図）があります")
                .end_drawing_space()
        """
        final_margin_content = margin_content
        if margin_image:
            final_margin_content = Image(margin_image, width="1.0\\linewidth", inline=True)
        drawing_space = DrawingSpace(width=width, right_margin=right_margin,
                                     margin_content=final_margin_content)
        self.document.add(drawing_space)
        return DrawingSpaceBuilder(self, drawing_space, parent_builder=self)

    def build(self) -> Document:
        """ドキュメントを構築"""
        return self.document


class SectionBuilder(ContentAdderMixin):
    """セクションを構築するビルダー"""

    def __init__(self, doc_builder: DocumentBuilder, section: Section):
        self.doc_builder = doc_builder
        self.section = section

    @property
    def _container(self) -> Section:
        return self.section

    @property
    def _doc_builder(self) -> DocumentBuilder:
        return self.doc_builder

    def add_drawing_space(self, width: str = "0.7\\textwidth",
                          right_margin: str = "5cm",
                          margin_image: Optional[str] = None,
                          margin_content: Optional[Any] = None) -> DrawingSpaceBuilder:
        """
        手書き用の余白を確保する領域を追加

        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
            margin_image: 右側の余白に表示する画像のパス（オプション）
            margin_content: 右側の余白に表示するコンテンツ（TikZオブジェクトなど。margin_imageより優先度は低い）

        Returns:
            DrawingSpaceBuilder（メソッドチェーン用）
        """
        final_margin_content = margin_content
        if margin_image:
            final_margin_content = Image(margin_image, width="1.0\\linewidth", inline=True)
        drawing_space = DrawingSpace(width=width, right_margin=right_margin,
                                     margin_content=final_margin_content)
        self.section.add(drawing_space)
        return DrawingSpaceBuilder(self.doc_builder, drawing_space, parent_builder=self)

    def end_section(self) -> DocumentBuilder:
        """セクションを終了"""
        return self.doc_builder


class DrawingSpaceBuilder(ContentAdderMixin):
    """DrawingSpaceを構築するビルダー"""

    def __init__(self, doc_builder: DocumentBuilder, drawing_space: DrawingSpace,
                 parent_builder: Union[DocumentBuilder, SectionBuilder, None] = None):
        self.doc_builder = doc_builder
        self.drawing_space = drawing_space
        # 親ビルダー（DocumentBuilderまたはSectionBuilder）を保持
        self.parent_builder: Union[DocumentBuilder, SectionBuilder] = (
            parent_builder if parent_builder is not None else doc_builder
        )

    @property
    def _container(self) -> DrawingSpace:
        return self.drawing_space

    @property
    def _doc_builder(self) -> DocumentBuilder:
        return self.doc_builder

    def add_tikz(self, code: str, caption: Optional[str] = None,
                 label: Optional[str] = None,
                 libraries: Optional[list] = None, inline: bool = True) -> DrawingSpaceBuilder:
        """
        TikZ図形を追加

        Note:
            DrawingSpace内ではfigure環境が使えないため、デフォルトでinline=True（非フロート）になります。
        """
        self._doc_builder.add_package("tikz")
        if libraries:
            for lib in libraries:
                cmd = f"\\usetikzlibrary{{{lib}}}"
                if cmd not in self._doc_builder.document.preamble_manager.custom_commands:
                    self._doc_builder.document.preamble_manager.add_command(cmd)
        self.drawing_space.add(TikZ(code, caption=caption, label=label,
                                    libraries=libraries, inline=inline))
        return self

    def end_drawing_space(self) -> Union[DocumentBuilder, SectionBuilder]:
        """DrawingSpaceを終了し、親ビルダーに戻る"""
        return self.parent_builder
