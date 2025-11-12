"""
PDF生成の使用例
"""

import sys
from pathlib import Path

# 親ディレクトリをパスに追加
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from pdf_generator import PDFGenerator

# 1. デフォルト設定で初期化
generator = PDFGenerator()

# 2. レポート用PDFを生成
report_data = {
    "title": "数学レポート",
    "author": "あなたの名前",
    "date": "2024年1月1日",
    "abstract": "このレポートでは、PythonとLaTeXの連携について説明します。"
}

try:
    pdf_path = generator.generate(
        template_name="report",
        variables=report_data,
        output_name="math_report.pdf"
    )
    print(f"PDFが正常に生成されました: {pdf_path}")
except Exception as e:
    print(f"エラーが発生しました: {e}")

# 3. カスタム設定で初期化（設定を上書き）
custom_generator = PDFGenerator(
    config_path="config/default.json",
    override_config={
        "directories": {
            "output_dir": "custom_output"
        }
    }
)

# 4. テンプレート一覧を取得
templates = generator.list_templates()
print("\n利用可能なテンプレート:")
for name, config in templates.items():
    print(f"  - {name}: {config.get('description', '')}")

