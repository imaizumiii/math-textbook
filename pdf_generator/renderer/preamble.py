"""
LaTeXプリアンブルを管理するクラス
"""

from typing import Dict, Optional, List
from pathlib import Path


class PreambleManager:
    """プリアンブルを管理するクラス"""
    
    def __init__(self):
        self.packages: Dict[str, Optional[str]] = {}
        self.custom_commands: List[str] = []
        self._add_default_packages()
    
    def _add_default_packages(self):
        """デフォルトパッケージを追加"""
        defaults = {
            "amsmath": None,
            "amsfonts": None,
            "amssymb": None,
            "inputenc": "[utf8]",
            "fontenc": "[T1]",
            "graphicx": None,
            "hyperref": None,
            "tcolorbox": None,
            "CJKutf8": None
        }
        self.packages.update(defaults)
    
    def add_package(self, package: str, options: Optional[str] = None):
        """パッケージを追加"""
        self.packages[package] = options
        return self
    
    def add_command(self, command: str):
        """カスタムコマンドを追加"""
        self.custom_commands.append(command)
        return self
    
    def generate_preamble(self, margins: Optional[Dict[str, str]] = None,
                         font_file: Optional[str] = None,
                         font_name: Optional[str] = None) -> str:
        """
        プリアンブルを生成
        
        Args:
            margins: 余白設定の辞書（例: {"top": "2cm", "bottom": "2cm"}）
            font_file: フォントファイルのパス（.ttf, .otfなど）
            font_name: フォント名（フォントファイルが指定された場合に使用）
        """
        latex = []
        latex.append("\\documentclass[a4paper]{article}\n")
        
        # フォントファイルが指定された場合は、fontspecパッケージを使用
        use_fontspec = font_file is not None
        
        if use_fontspec:
            # fontspecパッケージを追加（XeLaTeX/LuaLaTeX用）
            latex.append("\\usepackage{fontspec}\n")
            latex.append("\\usepackage{xeCJK}\n")  # 日本語フォント用
            # CJKutf8は不要なのでスキップ
            packages_to_skip = {"CJKutf8", "inputenc", "fontenc"}
        else:
            packages_to_skip = set()
        
        for package, options in self.packages.items():
            if package in packages_to_skip:
                continue
            if options:
                latex.append(f"\\usepackage{options}{{{package}}}\n")
            else:
                latex.append(f"\\usepackage{{{package}}}\n")
        
        # フォントファイルが指定された場合の設定
        if use_fontspec and font_file:
            font_path = Path(font_file)
            font_filename = font_path.name
            font_display_name = font_name or font_path.stem
            
            # 出力ディレクトリからの相対パスを計算
            # フォントファイルがoutput_dir/fonts/にある場合（process_fontsでコピー後）
            font_abs_path = font_path.absolute()
            font_dir_str = str(font_abs_path.parent).replace("\\", "/")
            
            # fonts/ディレクトリが含まれている場合は相対パスを使用
            if "/fonts" in font_dir_str.lower() or "\\fonts" in font_dir_str.lower():
                # 相対パスを使用（LaTeXの作業ディレクトリから見た相対パス）
                font_dir = "fonts"
            else:
                # 絶対パスを使用（フォントファイルが別の場所にある場合）
                font_dir = font_dir_str
            
            # パスにスペースが含まれている場合は引用符で囲む
            if " " in font_dir and not font_dir.startswith('"'):
                font_dir_quoted = f'"{font_dir}"'
            else:
                font_dir_quoted = font_dir
            
            latex.append("\n% フォント設定\n")
            # フォントファイルを設定（xeCJKを使用）
            latex.append(f"\\setCJKmainfont{{{font_display_name}}}[Path={font_dir_quoted}/, UprightFont={font_filename}]\n")
            latex.append("\n")
        
        # 余白設定がある場合はgeometryパッケージを追加
        if margins:
            margin_options = []
            if "top" in margins:
                margin_options.append(f"top={margins['top']}")
            if "bottom" in margins:
                margin_options.append(f"bottom={margins['bottom']}")
            if "left" in margins:
                margin_options.append(f"left={margins['left']}")
            if "right" in margins:
                margin_options.append(f"right={margins['right']}")
            
            if margin_options:
                # geometryパッケージを追加（パッケージリストには追加しない）
                latex.append(f"\\usepackage[{','.join(margin_options)}]{{geometry}}\n")
        
        if self.custom_commands:
            latex.append("\n")
            latex.extend(self.custom_commands)
            latex.append("\n")
        
        return "".join(latex)

