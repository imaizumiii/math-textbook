"""
テキスト関連の要素
"""

from typing import List
from .base import LaTeXElement


class Text(LaTeXElement):
    """テキスト要素"""
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text
    
    def to_latex(self) -> str:
        result = self.text
        for child in self.children:
            result += "\n" + child.to_latex()
        return result
    
    def process_resources(self, output_dir):
        result = {}
        for child in self.children:
            result.update(child.process_resources(output_dir))
        return result


class Paragraph(LaTeXElement):
    """段落要素"""
    
    def __init__(self, text: str):
        super().__init__()
        self.text = text
    
    def to_latex(self) -> str:
        result = f"{self.text}\n\n"
        for child in self.children:
            result += child.to_latex() + "\n"
        return result


class List(LaTeXElement):
    """リスト要素"""
    
    def __init__(self, items: List[str], ordered: bool = False):
        super().__init__()
        self.items = items
        self.ordered = ordered
    
    def to_latex(self) -> str:
        env = "enumerate" if self.ordered else "itemize"
        result = f"\\begin{{{env}}}\n"
        for item in self.items:
            result += f"    \\item {item}\n"
        result += f"\\end{{{env}}}\n"
        return result

