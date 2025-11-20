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
                         line_spacing: Optional[float] = None,
                         font_file: Optional[str] = None,
                         font_name: Optional[str] = None) -> str:
        """
        プリアンブルを生成
        
        Args:
            margins: 余白設定の辞書（例: {"top": "2cm", "bottom": "2cm"}）
            line_spacing: 行間の倍率（例: 1.5 で1.5倍の行間）
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
            
            # 太字フォントを自動検出
            bold_font_filename = None
            font_stem = font_path.stem
            font_parent = font_path.parent
            
            # 一般的な太字フォント名のパターンをチェック
            bold_patterns = [
                font_stem.replace("Regular", "Bold"),
                font_stem.replace("-Regular", "-Bold"),
                font_stem.replace("_Regular", "_Bold"),
                font_stem + "Bold",
                font_stem + "-Bold",
                font_stem + "_Bold",
            ]
            
            # 既存のパターンから重複を除去
            bold_patterns = list(dict.fromkeys(bold_patterns))
            
            # まず、フォントファイルと同じディレクトリ内を検索
            for pattern in bold_patterns:
                bold_font_path = font_parent / f"{pattern}{font_path.suffix}"
                if bold_font_path.exists():
                    bold_font_filename = bold_font_path.name
                    break
            
            # 太字フォントが見つからない場合、同じディレクトリ内の他の太字フォントを検索
            if bold_font_filename is None:
                for bold_file in font_parent.glob("*Bold*.ttf"):
                    if bold_file.exists():
                        bold_font_filename = bold_file.name
                        break
                # Bold.otfも検索
                if bold_font_filename is None:
                    for bold_file in font_parent.glob("*Bold*.otf"):
                        if bold_file.exists():
                            bold_font_filename = bold_file.name
                            break
            
            # 出力ディレクトリのfontsフォルダも確認（process_fontsでコピーされた後）
            # font_dirが"fonts"の場合、出力ディレクトリのfontsフォルダを確認
            if bold_font_filename is None and font_dir == "fonts":
                # font_abs_pathから出力ディレクトリを推測
                # font_abs_pathがoutput_dir/fonts/にある場合
                output_fonts_dir = font_abs_path.parent
                if output_fonts_dir.exists() and output_fonts_dir.name == "fonts":
                    for pattern in bold_patterns:
                        bold_font_path = output_fonts_dir / f"{pattern}{font_path.suffix}"
                        if bold_font_path.exists():
                            bold_font_filename = bold_font_path.name
                            break
                    
                    if bold_font_filename is None:
                        for bold_file in output_fonts_dir.glob("*Bold*.ttf"):
                            if bold_file.exists():
                                bold_font_filename = bold_file.name
                                break
                        if bold_font_filename is None:
                            for bold_file in output_fonts_dir.glob("*Bold*.otf"):
                                if bold_file.exists():
                                    bold_font_filename = bold_file.name
                                    break
            
            latex.append("\n% フォント設定\n")
            # フォントファイルを設定（xeCJKを使用）
            if bold_font_filename:
                # 太字フォントが存在する場合はBoldFontオプションを追加
                latex.append(f"\\setCJKmainfont{{{font_display_name}}}[Path={font_dir_quoted}/, UprightFont={font_filename}, BoldFont={bold_font_filename}]\n")
            else:
                # 太字フォントが見つからない場合は通常フォントのみ設定
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
        
        # 行間設定がある場合はsetspaceパッケージを追加
        if line_spacing is not None:
            latex.append("\\usepackage{setspace}\n")
            latex.append(f"\\setstretch{{{line_spacing}}}\n")
        
        if self.custom_commands:
            latex.append("\n")
            latex.extend(self.custom_commands)
            latex.append("\n")
        
        return "".join(latex)

