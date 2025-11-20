"""
エンコーディング関連のユーティリティ
"""

from typing import Optional, List


def safe_decode(byte_data: Optional[bytes], 
                encodings: Optional[List[str]] = None) -> str:
    """
    バイト列を安全にデコード
    
    Args:
        byte_data: デコードするバイト列
        encodings: 試行するエンコーディングのリスト
    
    Returns:
        デコードされた文字列
    """
    if byte_data is None:
        return ""
    
    if encodings is None:
        encodings = ['utf-8', 'cp932', 'shift_jis', 'latin-1']
    
    for encoding in encodings:
        try:
            return byte_data.decode(encoding, errors='ignore')
        except (UnicodeDecodeError, LookupError):
            continue
    
    # すべてのエンコーディングが失敗した場合
    return str(byte_data)


def escape_latex_special_chars(text: str) -> str:
    """
    LaTeXの特殊文字をエスケープする（\textbf{}コマンド内で使用する場合）
    
    Args:
        text: エスケープするテキスト
    
    Returns:
        エスケープされたテキスト
    
    Note:
        \textbf{}コマンド内で使用する場合、{ と } をエスケープする必要があります。
        これにより、テキスト内に含まれる中括弧がLaTeXの構文エラーを引き起こすことを防ぎます。
        バックスラッシュは既存のLaTeXコマンドを壊さないように、そのままにします。
    """
    # \textbf{}コマンド内で使用する場合、{ と } をエスケープする必要がある
    # これにより、テキスト内の中括弧がLaTeXの構文エラーを引き起こすことを防ぐ
    # バックスラッシュは既存のLaTeXコマンドを壊さないように、そのままにする
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    
    return text