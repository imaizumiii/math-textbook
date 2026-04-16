"""
ビルダークラス共通のコンテンツ追加メソッドを提供するMixin
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypeVar

from ..elements.structure import Exercise, BlankSpace, DrawingSpace, PageBreak
from ..elements.graphics import Image, TikZ
from ..elements.boxes import TextBox, Note, Warning, Info
from ..elements.text import Text, Paragraph, List as ListElement, Divider
from ..elements.math import Equation, Align
from ..elements.tables import Table

if TYPE_CHECKING:
    from .document_builder import DocumentBuilder, DrawingSpaceBuilder

_Self = TypeVar("_Self", bound="ContentAdderMixin")


class ContentAdderMixin(ABC):
    """ビルダークラス共通のコンテンツ追加メソッドを提供するMixin"""

    @property
    @abstractmethod
    def _container(self) -> Any:
        """コンテンツの追加先を返す（Document / Section / DrawingSpace）"""
        ...

    @property
    @abstractmethod
    def _doc_builder(self) -> DocumentBuilder:
        """DocumentBuilder インスタンスへの参照を返す（パッケージ追加等に使用）"""
        ...

    def add_text(self: _Self, text: str, bold: bool = False) -> _Self:
        """
        テキストを追加

        Args:
            text: テキスト文字列
            bold: 太字にするかどうか（デフォルト: False）
        """
        self._container.add(Text(text, bold=bold))
        return self

    def add_paragraph(self: _Self, text: str, bold: bool = False) -> _Self:
        """
        段落を追加

        Args:
            text: 段落のテキスト
            bold: 太字にするかどうか（デフォルト: False）
        """
        self._container.add(Paragraph(text, bold=bold))
        return self

    def add_line(self: _Self, text: str,
                 line_style: str = "solid",
                 line_thickness: str = "5pt",
                 color: Optional[str] = "gray") -> _Self:
        """装飾線付きテキストを追加（例: ----解答----）"""
        self._doc_builder._add_line_to_container(
            self._container, text, line_style, line_thickness, color
        )
        return self

    def add_divider(self: _Self, symbol: str = "*", spacing: str = "10em",
                    vspace: str = "0.0em",
                    vspace_before: Optional[str] = None,
                    vspace_after: Optional[str] = None) -> _Self:
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
        self._container.add(Divider(symbol=symbol, spacing=spacing, vspace=vspace,
                                    vspace_before=vspace_before,
                                    vspace_after=vspace_after))
        return self

    def add_image(self: _Self, image_path: str, caption: Optional[str] = None,
                  width: str = "0.8", label: Optional[str] = None) -> _Self:
        """画像を追加"""
        self._container.add(Image(image_path, caption=caption, width=width, label=label))
        return self

    def add_tikz(self: _Self, code: str, caption: Optional[str] = None,
                 label: Optional[str] = None,
                 libraries: Optional[List[str]] = None, inline: bool = False) -> _Self:
        """
        TikZ図形を追加

        Args:
            code: TikZコード
            caption: キャプション
            label: ラベル
            libraries: 必要なTikZライブラリのリスト
            inline: インライン表示するかどうか
        """
        self._doc_builder.add_package("tikz")
        if libraries:
            for lib in libraries:
                cmd = f"\\usetikzlibrary{{{lib}}}"
                if cmd not in self._doc_builder.document.preamble_manager.custom_commands:
                    self._doc_builder.document.preamble_manager.add_command(cmd)
        self._container.add(TikZ(code, caption=caption, label=label,
                                 libraries=libraries, inline=inline))
        return self

    def add_textbox(self: _Self, content: str, title: Optional[str] = None,
                    box_type: str = "tcolorbox",
                    style: Optional[Dict[str, str]] = None) -> _Self:
        """テキストボックスを追加"""
        self._container.add(TextBox(content, title=title, box_type=box_type, style=style))
        return self

    def add_note(self: _Self, content: str) -> _Self:
        """注意書きを追加"""
        self._container.add(Note(content))
        return self

    def add_warning(self: _Self, content: str) -> _Self:
        """警告を追加"""
        self._container.add(Warning(content))
        return self

    def add_info(self: _Self, content: str) -> _Self:
        """情報を追加"""
        self._container.add(Info(content))
        return self

    def add_equation(self: _Self, equation: str, inline: bool = False,
                     label: Optional[str] = None) -> _Self:
        """数式を追加"""
        self._container.add(Equation(equation, inline=inline, label=label))
        return self

    def add_align(self: _Self, equations: List[str], label: Optional[str] = None,
                  numbered: bool = False, vspace: Optional[str] = None) -> _Self:
        """
        複数行の数式を追加

        Args:
            equations: 数式のリスト
            label: ラベル
            numbered: 番号を振るかどうか
            vspace: 直前の余白調整（例: "-1em", "5pt"）
        """
        self._container.add(Align(equations, label=label, numbered=numbered, vspace=vspace))
        return self

    def add_list(self: _Self, items: List[str], ordered: bool = False) -> _Self:
        """リストを追加"""
        self._container.add(ListElement(items, ordered=ordered))
        return self

    def add_table(self: _Self, headers: List[str], rows: List[List[str]],
                  caption: Optional[str] = None, label: Optional[str] = None) -> _Self:
        """テーブルを追加"""
        self._container.add(Table(headers, rows, caption=caption, label=label))
        return self

    def add_blank_space(self: _Self, height: str) -> _Self:
        """
        手書き用の空白スペースを追加

        Args:
            height: 空白の高さ（例: "5cm", "50mm", "10em"）
        """
        self._container.add(BlankSpace(height))
        return self

    def add_page_break(self: _Self, use_clearpage: bool = False) -> _Self:
        """
        改ページを追加

        Args:
            use_clearpage: True の場合は \\clearpage（保留中のフロートも出力）を使用
        """
        self._container.add(PageBreak(use_clearpage=use_clearpage))
        return self

    def add_abstract(self: _Self, text: str, bold: bool = True,
                     centered: bool = True) -> _Self:
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
        self._container.add(Paragraph(formatted_text))
        return self

    def add_drawing_space(self, width: str = "0.7\\textwidth",
                          right_margin: str = "5cm",
                          margin_image: Optional[str] = None,
                          margin_content: Any = None) -> "DrawingSpaceBuilder":
        """
        手書き用の余白を確保する領域を追加

        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
            margin_image: 右側の余白に表示する画像のパス（オプション）
            margin_content: 右側の余白に表示するコンテンツ（TikZオブジェクトなど）

        Returns:
            DrawingSpaceBuilder（メソッドチェーン用）
        """
        from .document_builder import DrawingSpaceBuilder
        final_margin_content = margin_content
        if margin_image:
            final_margin_content = Image(margin_image, width="1.0\\linewidth", inline=True)
        drawing_space = DrawingSpace(width=width, right_margin=right_margin,
                                     margin_content=final_margin_content)
        self._container.add(drawing_space)
        return DrawingSpaceBuilder(self._doc_builder, drawing_space, parent_builder=self)

    def add_exercise(self: _Self, title: str, content: str,
                     items: Optional[List[str]] = None, columns: int = 1,
                     line_spacing: Optional[float] = None) -> _Self:
        """
        小問（練習問題）を追加

        Args:
            title: 小問のタイトル（例: "練習4"）
            content: 問題の本文
            items: 小問のリスト（例: ["$f(x) = x^2$", "$f(x) = 3x + 1$"]）
            columns: 列数（1: 縦並び, 2以上: 横並び（段組み））
            line_spacing: この練習問題ブロック内だけに適用する行間倍率（例: 1.2）

        Returns:
            self（メソッドチェーン用）

        Example:
            .add_exercise("練習4", "次の関数を微分せよ。", items=["$f(x) = x^2$", "$f(x) = 3x + 1$"], columns=2, line_spacing=1.2)
        """
        if columns > 1:
            self._doc_builder.add_package("multicol")
        if line_spacing is not None:
            self._doc_builder.add_package("setspace")
        self._container.add(
            Exercise(
                title=title,
                content=content,
                items=items,
                columns=columns,
                line_spacing=line_spacing
            )
        )
        return self
