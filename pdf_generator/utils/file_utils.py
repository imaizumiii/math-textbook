"""
ファイル操作関連のユーティリティ
"""

import subprocess
import shutil
import platform


def check_command_exists(command: str) -> bool:
    """
    コマンドが存在するか確認
    
    Args:
        command: 確認するコマンド名
    
    Returns:
        bool: コマンドが存在する場合True
    """
    import shutil
    import platform
    
    # shutil.whichを使用（クロスプラットフォーム）
    if shutil.which(command) is not None:
        return True
    
    # Windowsの場合、追加の確認
    if platform.system() == "Windows":
        try:
            # whereコマンドで確認
            result = subprocess.run(
                ["where", command],
                capture_output=True,
                timeout=5,
                check=False
            )
            if result.returncode == 0 and result.stdout:
                return True
        except Exception:
            pass
    
    # 最後の手段：直接実行を試みる
    try:
        # --versionや-hなどのオプションで確認
        result = subprocess.run(
            [command, '--version'],
            capture_output=True,
            timeout=5,
            check=False
        )
        # リターンコードが0でなくても、コマンドが見つかればOK
        if result.returncode != 127:  # 127は"command not found"
            return True
    except FileNotFoundError:
        return False
    except Exception:
        pass
    
    return False

