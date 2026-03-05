"""
PDF生成パッケージ
"""

# 新しいAPI（推奨）
from .core import PDFGenerator, Document
from .builder import DocumentBuilder, SectionBuilder

# 要素クラス
from .elements import (
    LaTeXElement,
    Text, Paragraph, List,
    Equation, Align,
    Image, Figure,
    TextBox, Note, Warning, Info,
    Section, Chapter, TableOfContents,
    Table
)

# 例外クラス
from .exceptions import (
    MathTextbookError,
    CompilationError,
    FontNotFoundError,
    ConfigurationError,
    DependencyError,
)

# レガシーAPI（後方互換性のため）
from .compiler import LaTeXCompiler
from .config import ConfigManager

__all__ = [
    # 新しいAPI
    'PDFGenerator',
    'Document',
    'DocumentBuilder',
    'SectionBuilder',
    # 要素クラス
    'LaTeXElement',
    'Text', 'Paragraph', 'List',
    'Equation', 'Align',
    'Image', 'Figure',
    'TextBox', 'Note', 'Warning', 'Info',
    'Section', 'Chapter', 'TableOfContents',
    'Table',
    # 例外クラス
    'MathTextbookError',
    'CompilationError',
    'FontNotFoundError',
    'ConfigurationError',
    'DependencyError',
    # レガシーAPI
    'LaTeXCompiler',
    'ConfigManager',
]

__version__ = "2.0.0"
