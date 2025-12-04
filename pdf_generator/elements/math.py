"""
数式関連の要素
"""

from typing import Optional, List
from .base import LaTeXElement


class Equation(LaTeXElement):
    """数式要素"""
    
    def __init__(self, equation: str, inline: bool = False, label: Optional[str] = None):
        super().__init__()
        self.equation = equation
        self.inline = inline
        self.label = label
    
    def to_latex(self) -> str:
        if self.inline:
            result = f"${self.equation}$"
        else:
            result = "\\[\n"
            result += f"    {self.equation}\n"
            result += "\\]"
            if self.label:
                result += f"\n\\label{{{self.label}}}"
        
        return result


class Align(LaTeXElement):
    """複数行の数式（align環境）"""
    
    def __init__(self, equations: List[str], label: Optional[str] = None, numbered: bool = True, vspace: Optional[str] = None):
        super().__init__()
        self.equations = equations
        self.label = label
        self.numbered = numbered
        self.vspace = vspace
    
    def to_latex(self) -> str:
        env_name = "align" if self.numbered else "align*"
        result = ""
        if self.vspace:
            result += f"\\vspace{{{self.vspace}}}\n"
            
        result += f"\\begin{{{env_name}}}\n"
        for eq in self.equations:
            result += f"    {eq}\n"
        if self.label:
            result += f"    \\label{{{self.label}}}\n"
        result += f"\\end{{{env_name}}}\n"
        return result

