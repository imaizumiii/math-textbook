"""
自動プレビュー機能のテストスクリプト
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
_dir = Path(__file__).resolve().parent
while _dir != _dir.parent:
    if (_dir / "pdf_generator").is_dir():
        sys.path.insert(0, str(_dir))
        break
    _dir = _dir.parent

from pdf_generator import PDFGenerator, DocumentBuilder

def main():
    print("PDF生成とプレビューのテストを開始します...")
    
    generator = PDFGenerator()
    
    # シンプルなドキュメントを作成
    doc = (
        DocumentBuilder("プレビューテスト", "テスト太郎")
        .add_section("テストセクション")
        .add_paragraph("このPDFが自動的に開けば成功です。")
        .add_equation(r"E = mc^2")
        .build()
    )
    
    try:
        # preview=True を指定して生成
        print("PDFを生成し、プレビューを起動します...")
        pdf_path = generator.generate(doc, output_name="preview_test.pdf", preview=True)
        print(f"PDFが生成されました: {pdf_path}")
        print("プレビューが起動したか確認してください。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
