"""
ドキュメント構造要素
"""

from typing import Optional
from .base import LaTeXElement


class Section(LaTeXElement):
    """セクション要素"""
    
    def __init__(self, title: str, level: int = 1, label: Optional[str] = None):
        super().__init__()
        self.title = title
        self.level = level
        self.label = label
    
    def to_latex(self) -> str:
        commands = {
            1: "\\section",
            2: "\\subsection",
            3: "\\subsubsection",
            4: "\\paragraph",
            5: "\\subparagraph"
        }
        
        cmd = commands.get(self.level, "\\section")
        result = f"{cmd}{{{self.title}}}\n"
        
        if self.label:
            result += f"\\label{{{self.label}}}\n"
        
        result += "\n"
        
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result


class Chapter(LaTeXElement):
    """章要素（bookクラス用）"""
    
    def __init__(self, title: str, label: Optional[str] = None):
        super().__init__()
        self.title = title
        self.label = label
    
    def to_latex(self) -> str:
        result = f"\\chapter{{{self.title}}}\n"
        if self.label:
            result += f"\\label{{{self.label}}}\n"
        result += "\n"
        
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result


class TableOfContents(LaTeXElement):
    """目次要素"""
    
    def to_latex(self) -> str:
        return "\\tableofcontents\n\\newpage\n"

