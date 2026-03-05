"""
テキスト要素 (text.py) のユニットテスト
"""

from pdf_generator.elements.text import Text, Paragraph, List, Line, Divider


class TestText:
    def test_text_basic(self):
        latex = Text("hello").to_latex()
        assert "hello" in latex

    def test_text_bold(self):
        latex = Text("hello", bold=True).to_latex()
        assert "\\textbf" in latex
        assert "hello" in latex

    def test_text_plain_no_textbf(self):
        latex = Text("hello", bold=False).to_latex()
        assert "\\textbf" not in latex


class TestParagraph:
    def test_paragraph_basic(self):
        latex = Paragraph("test").to_latex()
        assert "test" in latex

    def test_paragraph_bold(self):
        latex = Paragraph("test", bold=True).to_latex()
        assert "\\textbf" in latex
        assert "test" in latex


class TestList:
    def test_list_unordered(self):
        latex = List(["a", "b"]).to_latex()
        assert "itemize" in latex
        assert "a" in latex
        assert "b" in latex

    def test_list_ordered(self):
        latex = List(["a", "b"], ordered=True).to_latex()
        assert "enumerate" in latex
        assert "a" in latex

    def test_list_items_have_item_command(self):
        latex = List(["x"]).to_latex()
        assert "\\item" in latex


class TestLine:
    def test_line_solid(self):
        latex = Line("解答").to_latex()
        assert "解答" in latex

    def test_line_contains_hrule(self):
        latex = Line("解答", line_style="solid").to_latex()
        assert "hrule" in latex

    def test_line_dashed(self):
        latex = Line("解答", line_style="dashed").to_latex()
        assert "解答" in latex

    def test_line_with_color(self):
        latex = Line("解答", color="gray").to_latex()
        assert "gray" in latex


class TestDivider:
    def test_divider(self):
        latex = Divider().to_latex()
        assert "*" in latex
        assert "hspace" in latex

    def test_divider_custom_symbol(self):
        latex = Divider(symbol="—").to_latex()
        assert "—" in latex

    def test_divider_contains_center(self):
        latex = Divider().to_latex()
        assert "center" in latex
