"""
構造要素 (structure.py) のユニットテスト
"""

import pytest
from pdf_generator.elements.structure import (
    Section, Chapter, TableOfContents, DrawingSpace, Exercise, BlankSpace
)


class TestSection:
    def test_section(self):
        latex = Section("intro").to_latex()
        assert "\\section" in latex
        assert "intro" in latex

    def test_section_unnumbered(self):
        latex = Section("intro", numbered=False).to_latex()
        assert "\\section*" in latex

    def test_section_numbered_no_star(self):
        latex = Section("intro", numbered=True).to_latex()
        assert "\\section*" not in latex

    def test_section_level_2(self):
        latex = Section("sub", level=2).to_latex()
        assert "\\subsection" in latex

    def test_section_with_label(self):
        latex = Section("intro", label="sec:intro").to_latex()
        assert "sec:intro" in latex


class TestChapter:
    def test_chapter(self):
        latex = Chapter("第1章").to_latex()
        assert "\\chapter" in latex
        assert "第1章" in latex


class TestTableOfContents:
    def test_toc(self):
        latex = TableOfContents().to_latex()
        assert "\\tableofcontents" in latex


class TestDrawingSpace:
    def test_drawing_space_has_minipage(self):
        latex = DrawingSpace().to_latex()
        assert "minipage" in latex

    def test_drawing_space_width(self):
        latex = DrawingSpace(width="10cm").to_latex()
        assert "10cm" in latex

    def test_drawing_space_right_margin(self):
        latex = DrawingSpace(right_margin="3cm").to_latex()
        assert "3cm" in latex


class TestExercise:
    def test_exercise_basic(self):
        latex = Exercise("問1", "求めよ").to_latex()
        assert "問1" in latex
        assert "求めよ" in latex

    def test_exercise_with_items(self):
        latex = Exercise("問1", "求めよ", items=["a", "b"], columns=2).to_latex()
        assert "multicols" in latex
        assert "a" in latex
        assert "b" in latex

    def test_exercise_items_single_column_no_multicols(self):
        latex = Exercise("問1", "求めよ", items=["a"], columns=1).to_latex()
        assert "multicols" not in latex

    def test_exercise_bold_title(self):
        latex = Exercise("問1", "内容").to_latex()
        assert "\\textbf" in latex


class TestBlankSpace:
    def test_blank_space(self):
        latex = BlankSpace("5cm").to_latex()
        assert "5cm" in latex

    def test_blank_space_uses_vspace(self):
        latex = BlankSpace("3em").to_latex()
        assert "\\vspace" in latex
        assert "3em" in latex
