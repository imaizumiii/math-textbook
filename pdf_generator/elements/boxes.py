"""
テキストボックス関連の要素
"""

from typing import Optional, Dict
from .base import LaTeXElement


class TextBox(LaTeXElement):
    """テキストボックス要素"""
    
    def __init__(self, content: str, title: Optional[str] = None,
                 box_type: str = "tcolorbox",
                 style: Optional[Dict[str, str]] = None):
        super().__init__()
        self.content = content
        self.title = title
        self.box_type = box_type
        self.style = style or {}
    
    def to_latex(self) -> str:
        if self.box_type == "tcolorbox":
            return self._to_tcolorbox()
        elif self.box_type == "fancybox":
            return self._to_fancybox()
        else:
            return self._to_simple()
    
    def _to_tcolorbox(self) -> str:
        opts = []
        if self.style:
            opts.extend([f"{k}={v}" for k, v in self.style.items()])
        if self.title:
            opts.append(f"title={{{self.title}}}")
        
        opt_str = f"[{', '.join(opts)}]" if opts else ""
        result = f"\\begin{{tcolorbox}}{opt_str}\n"
        result += f"{self.content}\n"
        for child in self.children:
            result += child.to_latex()
        result += "\\end{tcolorbox}\n"
        return result
    
    def _to_fancybox(self) -> str:
        result = "\\fbox{\n"
        result += "    \\parbox{0.9\\textwidth}{\n"
        if self.title:
            result += f"        \\textbf{{{self.title}}}\\\\\n"
        result += f"        {self.content}\n"
        for child in self.children:
            child_latex = child.to_latex()
            result += "        " + child_latex.replace("\n", "\n        ")
        result += "    }\n"
        result += "}\n"
        return result
    
    def _to_simple(self) -> str:
        return f"\\fbox{{\\parbox{{0.9\\textwidth}}{{{self.content}}}}}\n"


class Note(TextBox):
    """注意書きボックス"""
    def __init__(self, content: str):
        super().__init__(
            content,
            title="注意",
            box_type="tcolorbox",
            style={"colback": "yellow!5!white", "colframe": "yellow!75!black"}
        )


class Warning(TextBox):
    """警告ボックス"""
    def __init__(self, content: str):
        super().__init__(
            content,
            title="警告",
            box_type="tcolorbox",
            style={"colback": "red!5!white", "colframe": "red!75!black"}
        )


class Info(TextBox):
    """情報ボックス"""
    def __init__(self, content: str):
        super().__init__(
            content,
            title="情報",
            box_type="tcolorbox",
            style={"colback": "blue!5!white", "colframe": "blue!75!black"}
        )

