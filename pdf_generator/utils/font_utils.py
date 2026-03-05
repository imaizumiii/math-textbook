"""フォント関連のユーティリティ"""
from pathlib import Path
from typing import Optional, List


def get_bold_font_patterns(font_stem: str) -> List[str]:
    """フォント名からBold版の候補名リストを生成する（重複除去済み）"""
    patterns = [
        font_stem.replace("Regular", "Bold"),
        font_stem.replace("-Regular", "-Bold"),
        font_stem.replace("_Regular", "_Bold"),
        font_stem + "Bold",
        font_stem + "-Bold",
        font_stem + "_Bold",
    ]
    return list(dict.fromkeys(patterns))


def find_bold_font(font_path: Path,
                   additional_search_dirs: Optional[List[Path]] = None) -> Optional[Path]:
    """フォントファイルのパスから、同ディレクトリ内のBoldフォントを検索する。
    見つからない場合はNoneを返す。

    Args:
        font_path: 通常フォントファイルのパス
        additional_search_dirs: 同ディレクトリで見つからない場合に追加で検索するディレクトリ一覧

    Returns:
        Boldフォントファイルのパス、または None
    """
    def _search_in_dir(search_dir: Path) -> Optional[Path]:
        for pattern in get_bold_font_patterns(font_path.stem):
            candidate = search_dir / f"{pattern}{font_path.suffix}"
            if candidate.exists():
                return candidate
        for glob_pattern in ("*Bold*.ttf", "*Bold*.otf"):
            for bold_file in search_dir.glob(glob_pattern):
                if bold_file.exists():
                    return bold_file
        return None

    result = _search_in_dir(font_path.parent)
    if result is not None:
        return result

    if additional_search_dirs:
        for search_dir in additional_search_dirs:
            if search_dir.exists():
                result = _search_in_dir(search_dir)
                if result is not None:
                    return result

    return None
