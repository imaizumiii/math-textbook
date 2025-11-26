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
            result = f"\\noindent \\textbf{{{escaped_text}}}"
        else:
            result = f"\\noindent {self.text}"
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
        result = f"\\noindent {text_content}\n\n"
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
        # \leadersを使用して太さを制御可能にする
        thickness = self.line_thickness
        
        if self.line_style == "solid":
            # 実線: \leaders\hrule height {thickness} \hfill を使用
            # \hrulefill は \leaders\hrule height 0.4pt \hfill のショートカット
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\leaders\\hrule height {thickness} \\hfill}}"
            else:
                line_cmd = f"\\leaders\\hrule height {thickness} \\hfill"
        elif self.line_style == "dashed":
            # 破線: \leaders を使って破線パターンを生成
            # 破線のパターン: 線の長さと間隔を調整
            dash_length = "0.5em"
            dash_gap = "0.3em"
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\leaders\\hbox to {dash_length}{{\\hss\\rule[-0.2pt]{{0.4em}}{{{thickness}}}\\hss}}\\hfill}}"
            else:
                line_cmd = f"\\leaders\\hbox to {dash_length}{{\\hss\\rule[-0.2pt]{{0.4em}}{{{thickness}}}\\hss}}\\hfill"
        elif self.line_style == "dotted":
            # 点線: \leaders を使って点のパターンを生成
            dot_spacing = "0.5em"
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\leaders\\hbox to {dot_spacing}{{\\hss\\rule[-0.2pt]{{0.1pt}}{{{thickness}}}\\hss}}\\hfill}}"
            else:
                line_cmd = f"\\leaders\\hbox to {dot_spacing}{{\\hss\\rule[-0.2pt]{{0.1pt}}{{{thickness}}}\\hss}}\\hfill"
        elif self.line_style == "double":
            # 二重線: 2本の線を適切な間隔で配置
            # 線の間隔は太さに応じて調整（太さの1.5倍程度）
            gap = f"{-float(thickness.replace('pt', '')) * 1.5}pt" if 'pt' in thickness else "-0.6pt"
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\leaders\\hrule height {thickness} \\hfill\\vspace{{{gap}}}\\leaders\\hrule height {thickness} \\hfill}}"
            else:
                line_cmd = f"\\leaders\\hrule height {thickness} \\hfill\\vspace{{{gap}}}\\leaders\\hrule height {thickness} \\hfill"
        else:
            # デフォルトは実線
            if self.color:
                line_cmd = f"\\textcolor{{{self.color}}}{{\\leaders\\hrule height {thickness} \\hfill}}"
            else:
                line_cmd = f"\\leaders\\hrule height {thickness} \\hfill"
        
        # テキスト領域の端まで線を引くレイアウト
        # \makebox[\textwidth] を使ってテキスト領域の幅に合わせる
        # テキストは中央に配置し、左右に線を引く
        # center環境は上下に大きな余白を作るため、\noindentを使用
        result = "\\par\\noindent\n"
        result += "\\makebox[\\textwidth][s]{"
        result += line_cmd
        result += f"\\quad\\textbf{{{escaped_text}}}\\quad"
        result += line_cmd
        result += "}\n"
        result += "\\par\n"
        
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result


class Divider(LaTeXElement):
    """軽い区切り要素（例: *        *        *）"""
    
    def __init__(self, symbol: str = "*", spacing: str = "10em", 
                 vspace: str = "-1em", vspace_before: Optional[str] = None,
                 vspace_after: Optional[str] = None):
        """
        Args:
            symbol: 区切りに使用する記号（デフォルト: "*"）
            spacing: 記号間の間隔（デフォルト: "2em"、例: "1em", "2em", "3em"など）
            vspace: 上下の余白（デフォルト: "-1em"、負の値で余白を減らす）
            vspace_before: 上の余白（指定時はvspaceより優先）
            vspace_after: 下の余白（指定時はvspaceより優先）
        """
        super().__init__()
        self.symbol = symbol
        self.spacing = spacing
        self.vspace_before = vspace_before if vspace_before is not None else vspace
        self.vspace_after = vspace_after if vspace_after is not None else vspace
    
    def to_latex(self) -> str:
        # 記号をエスケープ
        escaped_symbol = escape_latex_special_chars(self.symbol)
        
        # 3つの記号を指定された間隔で配置
        result = f"\\vspace{{{self.vspace_before}}}\n"  # 上の余白
        result += "\\begin{center}\n"
        result += f"{escaped_symbol}\\hspace{{{self.spacing}}} {escaped_symbol}\\hspace{{{self.spacing}}} {escaped_symbol}"
        result += "\n"
        result += "\\end{center}\n"
        result += f"\\vspace{{{self.vspace_after}}}\n"  # 下の余白
        
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result
    
    def process_resources(self, output_dir):
        result = {}
        for child in self.children:
            result.update(child.process_resources(output_dir))
        return result