"""
ビルダー (DocumentBuilder / SectionBuilder / DrawingSpaceBuilder) のユニットテスト
"""

import pytest
from pdf_generator.builder.document_builder import (
    DocumentBuilder, SectionBuilder, DrawingSpaceBuilder
)
from pdf_generator.core.document import Document


class TestDocumentBuilderBasic:
    def test_document_builder_basic(self):
        doc = DocumentBuilder("title", "author").build()
        assert isinstance(doc, Document)

    def test_build_sets_title(self):
        doc = DocumentBuilder("my title").build()
        assert doc.title == "my title"

    def test_build_sets_author(self):
        doc = DocumentBuilder("t", "author name").build()
        assert doc.author == "author name"

    def test_builder_no_args(self, builder):
        doc = builder.build()
        assert isinstance(doc, Document)


class TestMethodChain:
    def test_method_chain(self, builder):
        result = (builder
                  .add_text("a")
                  .add_paragraph("b")
                  .add_equation("x"))
        assert isinstance(result, DocumentBuilder)

    def test_add_text_returns_builder(self, builder):
        result = builder.add_text("hello")
        assert isinstance(result, DocumentBuilder)

    def test_add_paragraph_returns_builder(self, builder):
        result = builder.add_paragraph("hello")
        assert isinstance(result, DocumentBuilder)

    def test_add_equation_returns_builder(self, builder):
        result = builder.add_equation("x^2")
        assert isinstance(result, DocumentBuilder)

    def test_add_align_returns_builder(self, builder):
        result = builder.add_align(["a &= b"])
        assert isinstance(result, DocumentBuilder)

    def test_add_list_returns_builder(self, builder):
        result = builder.add_list(["a", "b"])
        assert isinstance(result, DocumentBuilder)

    def test_add_blank_space_returns_builder(self, builder):
        result = builder.add_blank_space("5cm")
        assert isinstance(result, DocumentBuilder)

    def test_add_page_break_returns_builder(self, builder):
        result = builder.add_page_break()
        assert isinstance(result, DocumentBuilder)

    def test_add_page_break_adds_page_break_element(self, builder):
        builder.add_page_break(use_clearpage=True)
        assert "\\clearpage" in builder.document.content[-1].to_latex()

    def test_add_divider_returns_builder(self, builder):
        result = builder.add_divider()
        assert isinstance(result, DocumentBuilder)

    def test_add_note_returns_builder(self, builder):
        result = builder.add_note("注意")
        assert isinstance(result, DocumentBuilder)

    def test_add_warning_returns_builder(self, builder):
        result = builder.add_warning("警告")
        assert isinstance(result, DocumentBuilder)

    def test_add_info_returns_builder(self, builder):
        result = builder.add_info("情報")
        assert isinstance(result, DocumentBuilder)

    def test_add_exercise_returns_builder(self, builder):
        result = builder.add_exercise("問1", "求めよ")
        assert isinstance(result, DocumentBuilder)

    def test_add_exercise_with_line_spacing_adds_setspace_package(self, builder):
        builder.add_exercise("問1", "求めよ", line_spacing=1.2)
        assert "setspace" in builder.document.preamble_manager.packages
        assert builder.document.content[-1].line_spacing == 1.2

    def test_add_table_returns_builder(self, builder):
        result = builder.add_table(["A", "B"], [["1", "2"]])
        assert isinstance(result, DocumentBuilder)


class TestSectionChain:
    def test_add_section_returns_section_builder(self, builder):
        result = builder.add_section("セクション")
        assert isinstance(result, SectionBuilder)

    def test_section_chain(self, builder):
        result = (builder
                  .add_section("s")
                  .add_text("t")
                  .end_section())
        assert isinstance(result, DocumentBuilder)

    def test_section_content_chain(self, builder):
        result = (builder
                  .add_section("s")
                  .add_paragraph("p")
                  .add_equation("x^2")
                  .add_list(["a", "b"])
                  .end_section())
        assert isinstance(result, DocumentBuilder)

    def test_end_section_returns_doc_builder(self, builder):
        sb = builder.add_section("s")
        result = sb.end_section()
        assert result is builder


class TestDrawingSpaceChain:
    def test_drawing_space_chain(self, builder):
        result = (builder
                  .add_drawing_space()
                  .add_text("t")
                  .end_drawing_space())
        assert isinstance(result, DocumentBuilder)

    def test_add_drawing_space_returns_drawing_space_builder(self, builder):
        result = builder.add_drawing_space()
        assert isinstance(result, DrawingSpaceBuilder)

    def test_end_drawing_space_returns_doc_builder(self, builder):
        dsb = builder.add_drawing_space()
        result = dsb.end_drawing_space()
        assert isinstance(result, DocumentBuilder)

    def test_drawing_space_from_section_returns_section_builder(self, builder):
        sb = builder.add_section("s")
        dsb = sb.add_drawing_space()
        result = dsb.end_drawing_space()
        assert isinstance(result, SectionBuilder)

    def test_drawing_space_chain_from_section(self, builder):
        result = (builder
                  .add_section("s")
                  .add_drawing_space()
                  .add_text("t")
                  .end_drawing_space()
                  .end_section())
        assert isinstance(result, DocumentBuilder)


class TestFullChain:
    def test_full_chain(self):
        doc = (DocumentBuilder("微分積分入門", "数学 太郎")
               .add_section("微分の基礎")
               .add_paragraph("導関数の定義は以下の通りです。")
               .add_textbox(
                   title="導関数の定義",
                   content=r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}"
               )
               .add_drawing_space(width="0.6\\textwidth", right_margin="5cm")
               .add_text("この定義式に基づいて計算を行います。")
               .add_equation(r"f(x) = x^2")
               .end_drawing_space()
               .add_exercise("練習1", "次の関数を微分せよ。",
                             items=[r"f(x) = x^3", r"f(x) = \sin x"],
                             columns=2)
               .end_section()
               .build())
        assert isinstance(doc, Document)

    def test_to_latex_runs_without_error(self):
        doc = (DocumentBuilder("テスト")
               .add_section("節")
               .add_paragraph("本文")
               .add_equation("E = mc^2")
               .end_section()
               .build())
        latex = doc.to_latex()
        assert isinstance(latex, str)
        assert len(latex) > 0
