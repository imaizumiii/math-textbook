"""
DocumentBuilderを使用したPDF生成の例

このスクリプトは、PythonコードからLaTeXドキュメントを構築し、
PDFを生成する方法を示します。
"""

import sys
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_generator import PDFGenerator
from pdf_generator.builder import DocumentBuilder


def main():
    """メイン関数"""
    # PDFGeneratorの初期化
    print("PDFGeneratorを初期化しています...")
    generator = PDFGenerator()
    
    # DocumentBuilderでドキュメントを構築
    print("ドキュメントを構築しています...")
    doc = (DocumentBuilder()
        # フォント設定（3つの方法があります）
        # 方法1: CJKutf8を使用（シンプルだが不安定な場合がある）
        # .set_font("goth")  # ゴシック体に設定（デフォルト: "min"=明朝体）
        
        # 方法2: フォントファイルを直接指定（より安定、XeLaTeX/LuaLaTeXが必要）
        # .set_font_file("C:/Windows/Fonts/msgothic.ttc", "MS Gothic")  # Windowsの場合
        # .set_font_file("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")  # Linuxの場合
        .set_font_file("fonts/NotoSansJP-Regular.ttf", "Noto Sans JP")  # ローカルファイル
        
        # 方法3: URLからフォントファイルをダウンロード（推奨）
        # .set_font_from_url(
        #     "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf",
        #     "Noto Sans JP"
        # )
        
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")  # 余白を設定
        # .set_abstract("このレポートでは、PythonとLaTeXの連携について説明します。")
        
        # セクション1: はじめに
        .add_section("はじめに")
            .add_text("このレポートでは、以下の内容について説明します。")
            .add_list([
                "PythonによるLaTeX生成",
                "図の挿入方法",
                "テキストボックスの使用方法"
            ], ordered=True)
            .end_section()
        
        # セクション2: 計算結果
        .add_section("計算結果")
            .add_text("Pythonで計算された円周率を数式として表示します。")
            .add_equation(r"\pi \approx \mathbf{3.141593}")
            .add_note("この結果は実験的に確認されました。")
            .add_warning("数値は近似値です。")
            .add_info("詳細は参考文献を参照してください。")
            .add_align([
                r"a &= b + c \\",
                r"&= y^2 + 1 \\",
                r"&= mc^2"
            ], numbered=False)
            .add_text("テキスト内に数式を書いています。$y = ax + b$")
            .add_textbox("これはテキストボックスです。", title="テキストボックスのタイトル")
            .add_textbox("これはテキストボックスです。タイトルのないテキストボックス。")
            .end_section()
        
        .build())
    
    # PDFを生成
    print("PDFを生成しています...")
    try:
        pdf_path = generator.generate(doc, output_name="math_report.pdf")
        print(f"成功: PDFが生成されました: {pdf_path}")
        return 0
    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません: {e}")
        print("LaTeX環境（TeX LiveまたはMiKTeX）がインストールされているか確認してください。")
        return 1
    except RuntimeError as e:
        print(f"エラー: PDFのコンパイルに失敗しました: {e}")
        return 1
    except Exception as e:
        import traceback
        print(f"予期しないエラーが発生しました: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

