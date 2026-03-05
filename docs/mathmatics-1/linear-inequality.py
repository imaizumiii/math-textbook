"""
一次不等式について解説：part1
"""

import sys
from pathlib import Path

# プロジェクトルート（pdf_generator/ を含むディレクトリ）を自動検出
_dir = Path(__file__).resolve().parent
while _dir != _dir.parent:
    if (_dir / "pdf_generator").is_dir():
        sys.path.insert(0, str(_dir))
        break
    _dir = _dir.parent

from pdf_generator.builder import DocumentBuilder
from pdf_generator import PDFGenerator


def main():
    output_name = Path(__file__).stem + ".pdf"
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
        
        ###ドキュメント全体の設定###

        .set_font_file(     
            str(_dir /
                "fonts" / "NotoSansJP-Regular.ttf"),
            "Noto Sans JP",
        )  

        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")  # 余白を設定
        .set_line_spacing(1.5)  # 行間を1.5倍に設定
        
        
        ###要素の追加###
        .add_section("Thema: 一次不等式")
        .add_list(
            [
                r"\textbf{方程式}：「＝」（等号）を使う式    - 例 \( 2x + 3 = 7 \) ",
                r"\textbf{不等式}：「＜」や「＞」などの記号（不等号）を使う式    - 例 \( 2x + 3 > 7 \) ",
            ]
        )
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
