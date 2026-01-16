"""
ドキュメント構造要素
"""

from typing import Optional, List, Union
from pathlib import Path
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
    
    def __init__(self, width: str = "0.7\\textwidth", right_margin: str = "5cm", 
                 margin_content: Optional[Union[str, LaTeXElement]] = None):
        """
        Args:
            width: コンテンツの幅（例: "0.7\\textwidth", "10cm"）
            right_margin: 右側の余白幅（例: "3cm", "5cm"）
            margin_content: 右側の余白に表示するコンテンツ（画像パスまたはLaTeXElement）
        """
        super().__init__()
        self.width = width
        self.right_margin = right_margin
        self.margin_content = margin_content
    
    def to_latex(self) -> str:
        # 左側のコンテンツ用minipageと、右側のマージン用minipageを並べる
        result = "\\noindent\n"
        
        # 左側のminipage
        result += f"\\begin{{minipage}}[t]{{{self.width}}}\n"
        for child in self.children:
            result += child.to_latex() + "\n"
        result += f"\\end{{minipage}}\n"
        
        # 右側のマージン用minipage
        # 左側のminipageとの間に少し隙間を開けるか、ぴったりくっつけるか
        # ここではぴったりくっつけて、マージン幅を確保する
        result += f"\\begin{{minipage}}[t]{{{self.right_margin}}}\n"
        
        if self.margin_content:
            if isinstance(self.margin_content, str):
                # 文字列の場合はそのままLaTeXとして出力（呼び出し側でImage要素などに変換されていることを想定）
                # あるいは単純なテキストとして出力
                result += f"{self.margin_content}\n"
            elif hasattr(self.margin_content, 'to_latex'):
                result += self.margin_content.to_latex()
        else:
            # コンテンツがない場合は、高さ確保のために空のボックスを置くか、単に何もしない
            # minipageの幅は確保される
            result += "\\null\n"
            
        result += f"\\end{{minipage}}\n"
        
        result += "\\par\n"  # 段落を終了
        result += "\\vspace{1em}\n"  # 追加の間隔を確保
        return result

    def process_resources(self, output_dir: Path) -> dict:
        """リソース（画像など）を処理"""
        result = super().process_resources(output_dir)
        if self.margin_content and hasattr(self.margin_content, 'process_resources'):
            result.update(self.margin_content.process_resources(output_dir))
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
        # 修正: 本文（content）は数式を含むためエスケープしない
        content = self.content
        
        # タイトルを太字で表示し、間隔をあけて問題の本文を配置（横並び）
        result = "\\noindent\n"
        # 修正: escaped_content ではなく content を使用
        result += f"\\textbf{{{escaped_title}}}\\quad {content}\n"
        
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
                # 修正: アイテムも数式を含むためエスケープしない
                result += f"  \\item {item}\n"
            result += "\\end{enumerate}\n"
            
            if self.columns > 1:
                result += "\\end{multicols}\n"
            
        result += "\\par\n"
        result += "\\vspace{0.5em}\n"  # 適切な間隔を確保
        
        # 子要素があれば追加
        for child in self.children:
            result += child.to_latex() + "\n"
        
        return result