"""
DocumentBuilderを使用したPDF生成の例

このスクリプトは、PythonコードからLaTeXドキュメントを構築し、
PDFを生成する方法を示します。
"""

import sys
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_generator.builder import DocumentBuilder
from pdf_generator import PDFGenerator


def main():
    output_name = "diff_mogi.pdf"
    """メイン関数"""
    # PDFGeneratorの初期化
    print("PDFGeneratorを初期化しています...")
    generator = PDFGenerator()

    # 数式の上下余白を調整するスタイル
    math_box_style = {
        "before upper": r"{\setlength{\abovedisplayskip}{5pt}\setlength{\belowdisplayskip}{5pt}\setlength{\abovedisplayshortskip}{0pt}\setlength{\belowdisplayshortskip}{0pt}}"
    }

    # DocumentBuilderでドキュメントを構築
    print("ドキュメントを構築しています...")
    doc = (
        DocumentBuilder()
        .set_font_file(
            str(Path(__file__).parent.parent /
                "fonts" / "NotoSansJP-Regular.ttf"),
            "Noto Sans JP",
        )  # ローカルファイル
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")  # 余白を設定
        .set_line_spacing(1.8)  # 行間を1.8倍に設定
        
        # ここから内容を追加
        .add_section("Theme: 関数$f(x)$とは？（中学、高校生向け）")
        
        .add_text(r"\textbf{”関数”}という言葉がなじみ始める、中学二年生の「一次関数」という単元ではないでしょうか。高校生なんかはもっといろんなところでこの言葉を耳にしていますよね。")
        
        .end_section()
        .build()
    )

    # PDFを生成
    print("PDFを生成しています...")
    try:
        pdf_path = generator.generate(doc, output_name=output_name)
        print(f"成功: PDFが生成されました: {pdf_path}")
        return 0
    except FileNotFoundError as e:
        print(f"エラー: ファイルが見つかりません: {e}")
        print(
            "LaTeX環境（TeX LiveまたはMiKTeX）がインストールされているか確認してください。"
        )
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
