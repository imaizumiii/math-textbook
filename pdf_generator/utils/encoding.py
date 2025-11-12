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

