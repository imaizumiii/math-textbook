"""
数式要素 (math.py) のユニットテスト
"""

from pdf_generator.elements.math import Equation, Align


class TestEquation:
    def test_equation_display(self):
        latex = Equation("x^2").to_latex()
        assert "\\[" in latex
        assert "x^2" in latex

    def test_equation_inline(self):
        latex = Equation("x^2", inline=True).to_latex()
        assert "$x^2$" in latex

    def test_equation_display_no_dollar(self):
        latex = Equation("x^2", inline=False).to_latex()
        assert "$x^2$" not in latex

    def test_equation_with_label(self):
        latex = Equation("x^2", label="eq:test").to_latex()
        assert "eq:test" in latex


class TestAlign:
    def test_align_basic(self):
        latex = Align(["a &= b"]).to_latex()
        assert "align" in latex
        assert "a &= b" in latex

    def test_align_unnumbered(self):
        latex = Align(["a &= b"], numbered=False).to_latex()
        assert "align*" in latex

    def test_align_numbered_no_star(self):
        latex = Align(["a &= b"], numbered=True).to_latex()
        assert "\\begin{align}" in latex
        assert "\\begin{align*}" not in latex

    def test_align_multiple_equations(self):
        latex = Align(["a &= b", "c &= d"]).to_latex()
        assert "a &= b" in latex
        assert "c &= d" in latex

    def test_align_with_vspace(self):
        latex = Align(["a &= b"], vspace="-1em").to_latex()
        assert "vspace" in latex
        assert "-1em" in latex
