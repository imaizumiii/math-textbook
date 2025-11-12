"""
画像・図表関連の要素
"""

from pathlib import Path
from typing import Optional
import shutil
from .base import LaTeXElement


class Image(LaTeXElement):
    """画像要素"""
    
    def __init__(self, image_path: str, caption: Optional[str] = None,
                 width: str = "0.8", height: Optional[str] = None,
                 label: Optional[str] = None, position: str = "h"):
        super().__init__()
        self.image_path = Path(image_path)
        self.caption = caption
        self.width = width
        self.height = height
        self.label = label
        self.position = position
        self.processed_path: Optional[str] = None
    
    def to_latex(self) -> str:
        path = self.processed_path or str(self.image_path)
        result = f"\\begin{{figure}}[{self.position}]\n"
        result += "    \\centering\n"
        
        # オプションの構築
        opts = []
        if self.width:
            opts.append(f"width={self.width}\\textwidth")
        if self.height:
            opts.append(f"height={self.height}\\textheight")
        
        opt_str = f"[{', '.join(opts)}]" if opts else ""
        result += f"    \\includegraphics{opt_str}{{{path}}}\n"
        
        if self.caption:
            result += f"    \\caption{{{self.caption}}}\n"
        if self.label:
            result += f"    \\label{{{self.label}}}\n"
        result += "\\end{figure}\n"
        return result
    
    def process_resources(self, output_dir: Path) -> dict:
        """画像ファイルをコピー"""
        if not self.image_path.exists():
            raise FileNotFoundError(f"画像ファイルが見つかりません: {self.image_path}")
        
        images_dir = output_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = images_dir / self.image_path.name
        shutil.copy2(self.image_path, dest_path)
        
        self.processed_path = f"images/{self.image_path.name}"
        return {str(self.image_path): self.processed_path}


class Figure(Image):
    """Figure要素（Imageのエイリアス）"""
    pass

