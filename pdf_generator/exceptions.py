"""
pdf_generator パッケージ共通の例外クラス
"""


class MathTextbookError(Exception):
    """pdf_generator パッケージの基底例外クラス"""


class CompilationError(MathTextbookError):
    """LaTeX コンパイルが失敗した場合に送出される例外"""


class FontNotFoundError(MathTextbookError, FileNotFoundError):
    """フォントファイルが見つからない場合に送出される例外"""


class ConfigurationError(MathTextbookError):
    """設定ファイルの読み込みまたはバリデーションが失敗した場合に送出される例外"""


class DependencyError(MathTextbookError):
    """LaTeX エンジン等の必須コマンドが見つからない場合に送出される例外"""
