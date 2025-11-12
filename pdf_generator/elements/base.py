"""
LaTeX要素の基底クラス
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path
import shutil


class LaTeXElement(ABC):
    """LaTeX要素の基底クラス"""
    
    def __init__(self):
        self.parent: Optional['LaTeXElement'] = None
        self.children: List['LaTeXElement'] = []
    
    @abstractmethod
    def to_latex(self) -> str:
        """LaTeXコードに変換"""
        pass
    
    def add(self, element: 'LaTeXElement'):
        """子要素を追加"""
        element.parent = self
        self.children.append(element)
        return self
    
    def process_resources(self, output_dir: Path) -> dict:
        """
        リソース（画像など）を処理
        
        Args:
            output_dir: 出力ディレクトリ
        
        Returns:
            リソースのパスマッピング（元のパス -> 新しいパス）
        """
        result = {}
        for child in self.children:
            result.update(child.process_resources(output_dir))
        return result

