"""
通分の練習問題プリント
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
    print("PDFGeneratorを初期化しています...")
    generator = PDFGenerator()

    print("ドキュメントを構築しています...")
    doc = (
        DocumentBuilder()
        .set_font_file(
            str(_dir / "docs" / "mathmatics-1" / "fonts" / "NotoSansJP-Regular.ttf"),
            "Noto Sans JP",
        )
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")
        .set_line_spacing(1.5)
        .add_section("Theme: 通分")
        # .add_blank_space(height="0.6cm")
        .add_exercise(
            title="問題1",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{1}{2} \) + \( \dfrac{1}{3} \) ",
                r" \( \dfrac{2}{3} \) + \( \dfrac{1}{4} \) ",
                r" \( \dfrac{3}{4} \) + \( \dfrac{5}{6} \) ",
                r" \( \dfrac{2}{5} \) + \( \dfrac{1}{10} \) ",
                r" \( \dfrac{7}{8} \) + \( \dfrac{3}{4} \) ",
                r" \( \dfrac{4}{9} \) + \( \dfrac{5}{6} \) ",
            ],
            columns=2,
        )
        .add_blank_space(height="0.4cm")
        .add_exercise(
            title="基本問題",
            content=r"次の2つの分数を通分し、同じ分母で表しなさい。",
            items=[
                r" \( \frac{5}{12} \) と \( \frac{7}{18} \) ",
                r" \( \frac{3}{14} \) と \( \frac{2}{21} \) ",
                r" \( \frac{11}{15} \) と \( \frac{4}{9} \) ",
                r" \( \frac{5}{16} \) と \( \frac{3}{20} \) ",
                r" \( \frac{7}{24} \) と \( \frac{5}{36} \) ",
                r" \( \frac{13}{18} \) と \( \frac{2}{27} \) ",
                r" \( \frac{5}{22} \) と \( \frac{9}{33} \) ",
                r" \( \frac{4}{25} \) と \( \frac{7}{30} \) ",
            ],
            columns=2,
        )
        .add_blank_space(height="0.4cm")
        .add_exercise(
            title="発展問題",
            content=r"次の3つの分数を通分しなさい。",
            items=[
                r" \( \frac{1}{2},\ \frac{1}{3},\ \frac{1}{4} \) ",
                r" \( \frac{2}{5},\ \frac{1}{6},\ \frac{3}{10} \) ",
                r" \( \frac{3}{8},\ \frac{5}{12},\ \frac{7}{18} \) ",
                r" \( \frac{4}{9},\ \frac{5}{12},\ \frac{1}{18} \) ",
                r" \( \frac{7}{15},\ \frac{11}{20},\ \frac{13}{30} \) ",
                r" \( \frac{3}{14},\ \frac{5}{21},\ \frac{4}{6} \) ",
            ],
            columns=1,
        )
        .end_section()
        .build()
    )

    print("PDFを生成しています...")
    try:
        pdf_path = generator.generate(
            doc,
            output_name=output_name,
            output_dir=str(_dir / "output" / "docs" / "problem"),
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
