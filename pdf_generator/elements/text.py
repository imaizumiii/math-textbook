"""
テキスト関連の要素
"""

from typing import List, Optional
from .base import LaTeXElement
from ..utils.encoding import escape_latex_special_chars


class Text(LaTeXElement):
    """テキスト要素"""
    
    def __init__(self, text: str, bold: bool = False):
        super().__init__()
        self.text = text
        self.bold = bold
    
    def to_latex(self) -> str:
        if self.bold:
            # LaTeXの特殊文字をエスケープしてから\textbfコマンドで囲む
            escaped_text = escape_latex_special_chars(self.text)
            result = f"\\textbf{{{escaped_text}}}"
        else:
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
    
    def __init__(self, text: str, bold: bool = False):
        super().__init__()
        self.text = text
        self.bold = bold
    
    def to_latex(self) -> str:
        if self.bold:
            # LaTeXの特殊文字をエスケープしてから\textbfコマンドで囲む
            escaped_text = escape_latex_special_chars(self.text)
            text_content = f"\\textbf{{{escaped_text}}}"
        else:
            text_content = self.text
        result = f"{text_content}\n\n"
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


class Line(LaTeXElement):
    """装飾線付きテキスト要素（例: ----解答----）"""
    
    def __init__(self, text: str, 
                 line_style: str = "solid",
                 line_thickness: str = "0.4pt",
                 color: Optional[str] = None):
        """
        Args:
            text: 中央に表示するテキスト
            line_style: 線のスタイル
                - "solid": 実線（デフォルト）
                - "dashed": 破線
                - "dotted": 点線
                - "double": 二重線
            line_thickness: 線の太さ（例: "0.4pt", "1pt"）
            color: 線の色（例: "gray", "grey", "black", "red"など。Noneの場合は黒）
        """
        super().__init__()
        self.text = text
        self.line_style = line_style
        self.line_thickness = line_thickness
        self.color = color
    
    def to_latex(self) -> str:
        # テキストをエスケープ
        escaped_text = escape_latex_special_chars(self.text)
        
        # 線のスタイルに応じたLaTeXコマンドを生成
        # シンプルで確実な方法: \hrulefill または \dotfill を使用
        if self.line_style == "solid":
            # 実線: \hrulefill を使用（自動的に横いっぱいに伸びる）
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\hrulefill}}"
            else:
                line_cmd = "\\hrulefill"
        elif self.line_style == "dashed":
            # 破線: \dotfill を使用
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\dotfill}}"
            else:
                line_cmd = "\\dotfill"
        elif self.line_style == "dotted":
            # 点線: \dotfill を使用
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\dotfill}}"
            else:
                line_cmd = "\\dotfill"
        elif self.line_style == "double":
            # 二重線: \hrulefill を2回使用
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\hrulefill\\vspace{{-0.2pt}}\\hrulefill}}"
            else:
                line_cmd = "\\hrulefill\\vspace{-0.2pt}\\hrulefill"
        else:
            # デフォルトは実線
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\hrulefill}}"
            else:
                line_cmd = "\\hrulefill"
        
        # テキスト領域の端まで線を引くレイアウト
        # \makebox[\textwidth] を使ってテキスト領域の幅に合わせる
        # テキストは中央に配置し、左右に線を引く
        result = "\\begin{center}\n"
        result += "\\makebox[\\textwidth][s]{"
        result += line_cmd
        result += f"\\quad\\textbf{{{escaped_text}}}\\quad"
        result += line_cmd
        result += "}\n"
        result += "\\end{center}\n"
        result += "\\vspace{0.5em}\n"  # 適切な間隔
        
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result