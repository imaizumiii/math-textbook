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


class DrawingSpace(LaTeXElement):
    """
    手書き用の余白を確保するためのラッパー要素
    
    この要素内のすべてのコンテンツは、指定された幅に制限され、
    右側に手書き用の余白が確保されます。
    """
    
    def __init__(self, width: str = "0.7\\textwidth", right_margin: str = "5cm"):
        """
        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
        """
        super().__init__()
        self.width = width
        self.right_margin = right_margin
    
    def to_latex(self) -> str:
        # minipage環境を使用して幅を制限
        result = f"\\begin{{minipage}}[t]{{{self.width}}}\n"
        for child in self.children:
            result += child.to_latex() + "\n"
        result += f"\\end{{minipage}}\n"
        result += f"\\hspace{{{self.right_margin}}}\n"
        result += "\\par\n"  # 段落を終了して適切な間隔を確保
        result += "\\vspace{1em}\n"  # 追加の間隔を確保
        return result