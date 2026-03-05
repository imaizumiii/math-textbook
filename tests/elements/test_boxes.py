"""
ボックス要素 (boxes.py) のユニットテスト
"""

from pdf_generator.elements.boxes import TextBox, Note, Warning, Info


class TestTextBox:
    def test_textbox_with_title(self):
        latex = TextBox("content", title="Title").to_latex()
        assert "tcolorbox" in latex
        assert "Title" in latex
        assert "content" in latex

    def test_textbox_no_title(self):
        latex = TextBox("content only").to_latex()
        assert "tcolorbox" in latex
        assert "content only" in latex

    def test_textbox_fancybox(self):
        latex = TextBox("content", box_type="fancybox").to_latex()
        assert "fbox" in latex

    def test_textbox_simple(self):
        latex = TextBox("content", box_type="simple").to_latex()
        assert "content" in latex


class TestNote:
    def test_note(self):
        latex = Note("msg").to_latex()
        assert "yellow" in latex
        assert "msg" in latex

    def test_note_has_title(self):
        latex = Note("msg").to_latex()
        assert "注意" in latex


class TestWarning:
    def test_warning(self):
        latex = Warning("msg").to_latex()
        assert "red" in latex
        assert "msg" in latex

    def test_warning_has_title(self):
        latex = Warning("msg").to_latex()
        assert "警告" in latex


class TestInfo:
    def test_info(self):
        latex = Info("msg").to_latex()
        assert "blue" in latex
        assert "msg" in latex

    def test_info_has_title(self):
        latex = Info("msg").to_latex()
        assert "情報" in latex
