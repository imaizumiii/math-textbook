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
                r"\textbf{方程式}：「＝」（等号）を使う式 --- 例 \( 2x + 3 = 7 \) ",
                r"\textbf{不等式}：「＜」や「＞」などの記号（不等号）を使う式 --- 例 \( 2x + 3 > 7 \) ",
            ]
        )
        .add_text("不等式は等式と同じように「移項」や「定数倍」などの操作ができます。")
        .add_blank_space(height="1.2cm") 
        # 移項と定数倍の例を手書きで追加
        
        .add_text("ただし、定数倍の操作では注意が必要です。")
        .add_text("不等式の両辺を負の数で定数倍すると、不等号の向きが逆になります。")
        .add_blank_space(height="1.2cm")
        # 定数倍の例を手書きで追加
        
        .add_textbox(title="例27", content=r"不等式\( 2x - 7 < 5x -1 \)を解く。")
        .add_text("解答")
        .add_blank_space(height="2.4cm")
        # 例27の解答を手書きで追加
        
        .add_exercise(title="練習42", content=r"次の１次不等式を解け。", items=[
            r" \( 5x - 2 < 2x + 4 \)",
            r" \( 6x - 3 \geqq 8x + 7 \)",
            r" \( 2(4x-1) \geqq 5x -11 \)",
            r" \( 3(3-2x) < 4-3x \)",
        ], columns=2)
        .end_section()
        .build()
    )

    # PDFを生成
    print("PDFを生成しています...")
    try:
        pdf_path = generator.generate(
            doc,
            output_name=output_name,
            output_dir=str(_dir / "output" / "docs" / "mathmatics-1"),
        )
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
