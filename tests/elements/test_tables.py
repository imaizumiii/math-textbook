"""
テーブル要素 (tables.py) のユニットテスト
"""

import pytest
from pdf_generator.elements.tables import Table


class TestTable:
    def test_table_basic(self):
        table = Table(["名前", "点数"], [["Alice", "90"], ["Bob", "80"]])
        latex = table.to_latex()
        assert "tabular" in latex
        assert "名前" in latex
        assert "点数" in latex
        assert "Alice" in latex
        assert "90" in latex

    def test_table_row_mismatch(self):
        table = Table(["A", "B"], [["a", "b", "c"]])  # 列数が合わない
        with pytest.raises(ValueError):
            table.to_latex()

    def test_table_has_hline(self):
        table = Table(["X"], [["1"]])
        latex = table.to_latex()
        assert "\\hline" in latex

    def test_table_with_caption(self):
        table = Table(["X"], [["1"]], caption="テスト表")
        latex = table.to_latex()
        assert "caption" in latex
        assert "テスト表" in latex

    def test_table_with_label(self):
        table = Table(["X"], [["1"]], label="tab:test")
        latex = table.to_latex()
        assert "tab:test" in latex

    def test_table_multiple_rows(self):
        table = Table(["A", "B"], [["1", "2"], ["3", "4"], ["5", "6"]])
        latex = table.to_latex()
        assert "1" in latex
        assert "6" in latex
