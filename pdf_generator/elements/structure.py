"""
ドキュメント構造要素
"""

from typing import Optional, List
from .base import LaTeXElement
from ..utils.encoding import escape_latex_special_chars


class BlankSpace(LaTeXElement):
    """
    手書き用の空白スペース要素
    
    指定された高さの空白を作ります。
    """
    
    def __init__(self, height: str):
        """
        Args:
            height: 空白の高さ（例: "5cm", "50mm", "10em"）
        """
        super().__init__()
        self.height = height
    
    def to_latex(self) -> str:
        return f"\\vspace{{{self.height}}}\n"


class Section(LaTeXElement):
    """セクション要素"""
    
    def __init__(self, title: str, level: int = 1, label: Optional[str] = None, numbered: bool = True):
        super().__init__()
        self.title = title
        self.level = level
        self.label = label
        self.numbered = numbered
    
    def to_latex(self) -> str:
        commands = {
            1: "\\section",
            2: "\\subsection",
            3: "\\subsubsection",
            4: "\\paragraph",
            5: "\\subparagraph"
        }
        
        cmd = commands.get(self.level, "\\section")
        if not self.numbered:
            cmd += "*"
            
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
        # minipage環境を使用して幅を制限し、右側に余白を確保
        # \makebox[\textwidth][l]{...}を使用して、minipageとhspaceを同じ行に配置
        result = "\\noindent\n"
        result += f"\\makebox[\\textwidth][l]{{%\n"
        result += f"\\begin{{minipage}}[t]{{{self.width}}}\n"
        for child in self.children:
            result += child.to_latex() + "\n"
        result += f"\\end{{minipage}}\n"
        result += f"\\hspace{{{self.right_margin}}}\n"
        result += "}%\n"
        result += "\\par\n"  # 段落を終了して適切な間隔を確保
        result += "\\vspace{1em}\n"  # 追加の間隔を確保
        return result


class Exercise(LaTeXElement):
    """
    小問（練習問題）要素
    
    タイトルと問題の本文を持つ小問を表現します。
    """
    
    def __init__(self, title: str, content: str, items: Optional[List[str]] = None, columns: int = 1):
        """
        Args:
            title: 小問のタイトル（例: "練習4"）
            content: 問題の本文
            items: 小問のリスト（例: ["$f(x) = x^2$", "$f(x) = 3x + 1$"]）
            columns: 列数（1: 縦並び, 2以上: 横並び（段組み））
        """
        super().__init__()
        self.title = title
        self.content = content
        self.items = items or []
        self.columns = columns
    
    def to_latex(self) -> str:
        # タイトルと本文をエスケープ
        escaped_title = escape_latex_special_chars(self.title)
        escaped_content = escape_latex_special_chars(self.content)
        
        # タイトルを太字で表示し、間隔をあけて問題の本文を配置（横並び）
        result = "\\noindent\n"
        result += f"\\textbf{{{escaped_title}}}\\quad {escaped_content}\n"
        
        # 小問リストがある場合
        if self.items:
            # 余白を調整
            result += "\\vspace{-1.5em}\n"

            # 列数が2以上の場合はmulticol環境を使用
            if self.columns > 1:
                result += f"\\begin{{multicols}}{{{self.columns}}}\n"
            
            result += "\\begin{enumerate}\n"
            # ラベルを (1), (2)... の形式に変更
            result += "  \\renewcommand{\\labelenumi}{(\\arabic{enumi})}\n"
            for item in self.items:
                escaped_item = escape_latex_special_chars(item)
                result += f"  \\item {escaped_item}\n"
            result += "\\end{enumerate}\n"
            
            if self.columns > 1:
                result += "\\end{multicols}\n"
            
        result += "\\par\n"
        result += "\\vspace{0.5em}\n"  # 適切な間隔を確保
        
        # 子要素があれば追加
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result