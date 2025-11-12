"""
テーブル関連の要素
"""

from typing import List, Optional
from .base import LaTeXElement


class Table(LaTeXElement):
    """テーブル要素"""
    
    def __init__(self, headers: List[str], rows: List[List[str]],
                 caption: Optional[str] = None, label: Optional[str] = None,
                 position: str = "h"):
        super().__init__()
        self.headers = headers
        self.rows = rows
        self.caption = caption
        self.label = label
        self.position = position
    
    def to_latex(self) -> str:
        num_cols = len(self.headers)
        result = f"\\begin{{table}}[{self.position}]\n"
        result += "    \\centering\n"
        result += f"    \\begin{{tabular}}{{|{'|'.join(['c'] * num_cols)}|}}\n"
        result += "        \\hline\n"
        result += "        " + " & ".join(self.headers) + " \\\\\n"
        result += "        \\hline\n"
        for row in self.rows:
            if len(row) != num_cols:
                raise ValueError(f"行の列数が一致しません: 期待値={num_cols}, 実際={len(row)}")
            result += "        " + " & ".join(row) + " \\\\\n"
        result += "        \\hline\n"
        result += "    \\end{tabular}\n"
        if self.caption:
            result += f"    \\caption{{{self.caption}}}\n"
        if self.label:
            result += f"    \\label{{{self.label}}}\n"
        result += "\\end{table}\n"
        return result

