"""
通分の練習問題プリント
"""

from pdb import line_prefix
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
            line_spacing=3.0,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題2",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{5}{12} \) + \( \dfrac{7}{18} \) ",
                r" \( \dfrac{3}{14} \) + \( \dfrac{2}{21} \) ",
                r" \( \dfrac{11}{15} \) + \( \dfrac{4}{9} \) ",
                r" \( \dfrac{5}{16} \) + \( \dfrac{3}{20} \) ",
                r" \( \dfrac{7}{24} \) + \( \dfrac{5}{36} \) ",
                r" \( \dfrac{13}{18} \) + \( \dfrac{2}{27} \) ",
                r" \( \dfrac{5}{22} \) + \( \dfrac{9}{33} \) ",
                r" \( \dfrac{4}{25} \) + \( \dfrac{7}{30} \) ",
            ],
            line_spacing=3.0,
            columns=2,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題3",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{1}{2} \) + \( \dfrac{1}{3} \) + \( \dfrac{1}{4} \) ",
                r" \( \dfrac{2}{5} \) + \( \dfrac{1}{6} \) + \( \dfrac{3}{10} \) ",
                r" \( \dfrac{3}{8} \) + \( \dfrac{5}{12} \) + \( \dfrac{7}{18} \) ",
                r" \( \dfrac{4}{9} \) + \( \dfrac{5}{12} \) + \( \dfrac{1}{18} \) ",
                r" \( \dfrac{7}{15} \) + \( \dfrac{11}{20} \) + \( \dfrac{13}{30} \) ",
                r" \( \dfrac{3}{14} \) + \( \dfrac{5}{21} \) + \( \dfrac{4}{6} \) ",
            ],
            line_spacing=3.0,
            columns=1,
        )
        .add_page_break()
        .add_exercise(
            title="問題4",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{5}{6} \) - \( \dfrac{1}{4} \) ",
                r" \( \dfrac{7}{10} \) - \( \dfrac{2}{5} \) ",
                r" \( \dfrac{11}{12} \) - \( \dfrac{1}{3} \) ",
                r" \( \dfrac{9}{14} \) - \( \dfrac{3}{7} \) ",
                r" \( \dfrac{13}{15} \) - \( \dfrac{2}{9} \) ",
                r" \( \dfrac{17}{18} \) - \( \dfrac{5}{12} \) ",
            ],
            columns=2,
            line_spacing=3.0,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題5",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{3}{8} \) + \( \dfrac{5}{12} \) - \( \dfrac{1}{6} \) ",
                r" \( \dfrac{7}{9} \) - \( \dfrac{1}{6} \) + \( \dfrac{2}{3} \) ",
                r" \( \dfrac{5}{14} \) + \( \dfrac{3}{7} \) - \( \dfrac{1}{2} \) ",
                r" \( \dfrac{11}{20} \) - \( \dfrac{3}{10} \) + \( \dfrac{1}{4} \) ",
                r" \( \dfrac{7}{18} \) + \( \dfrac{5}{12} \) - \( \dfrac{1}{9} \) ",
                r" \( \dfrac{13}{24} \) - \( \dfrac{1}{8} \) + \( \dfrac{5}{6} \) ",
                r" \( \dfrac{9}{16} \) + \( \dfrac{7}{20} \) - \( \dfrac{3}{10} \) ",
                r" \( \dfrac{4}{15} \) - \( \dfrac{1}{10} \) + \( \dfrac{2}{3} \) ",
            ],
            line_spacing=3.0,
            columns=2,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題6",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{1}{3} \) + \( \dfrac{1}{4} \) + \( \dfrac{1}{6} \) ",
                r" \( \dfrac{5}{8} \) - \( \dfrac{1}{6} \) - \( \dfrac{1}{12} \) ",
                r" \( \dfrac{7}{10} \) + \( \dfrac{3}{5} \) - \( \dfrac{1}{4} \) ",
                r" \( \dfrac{11}{15} \) - \( \dfrac{2}{9} \) + \( \dfrac{1}{6} \) ",
                r" \( \dfrac{13}{18} \) + \( \dfrac{5}{12} \) - \( \dfrac{7}{24} \) ",
                r" \( \dfrac{4}{7} \) - \( \dfrac{3}{14} \) + \( \dfrac{5}{21} \) ",
            ],
            line_spacing=3.0,
            columns=1,
        )
        .add_page_break()
        .add_exercise(
            title="問題7",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{5}{9} \) + \( \dfrac{7}{12} \) ",
                r" \( \dfrac{11}{18} \) + \( \dfrac{1}{4} \) ",
                r" \( \dfrac{3}{10} \) + \( \dfrac{5}{6} \) ",
                r" \( \dfrac{7}{16} \) + \( \dfrac{3}{8} \) ",
                r" \( \dfrac{13}{20} \) + \( \dfrac{2}{15} \) ",
                r" \( \dfrac{17}{24} \) + \( \dfrac{5}{18} \) ",
            ],
            columns=2,
            line_spacing=3.0,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題8",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{7}{12} \) - \( \dfrac{1}{8} \) ",
                r" \( \dfrac{9}{14} \) - \( \dfrac{2}{7} \) ",
                r" \( \dfrac{11}{15} \) - \( \dfrac{1}{6} \) ",
                r" \( \dfrac{5}{18} \) - \( \dfrac{1}{9} \) ",
                r" \( \dfrac{13}{16} \) - \( \dfrac{3}{10} \) ",
                r" \( \dfrac{19}{20} \) - \( \dfrac{7}{12} \) ",
                r" \( \dfrac{5}{21} \) - \( \dfrac{1}{14} \) ",
                r" \( \dfrac{17}{30} \) - \( \dfrac{2}{9} \) ",
            ],
            line_spacing=3.0,
            columns=2,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題9",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{1}{2} \) + \( \dfrac{2}{3} \) - \( \dfrac{1}{4} \) ",
                r" \( \dfrac{3}{5} \) + \( \dfrac{1}{6} \) - \( \dfrac{1}{10} \) ",
                r" \( \dfrac{7}{8} \) - \( \dfrac{1}{3} \) + \( \dfrac{1}{12} \) ",
                r" \( \dfrac{11}{12} \) + \( \dfrac{1}{4} \) - \( \dfrac{1}{6} \) ",
                r" \( \dfrac{5}{14} \) + \( \dfrac{2}{7} \) - \( \dfrac{1}{3} \) ",
                r" \( \dfrac{13}{18} \) - \( \dfrac{1}{9} \) + \( \dfrac{5}{12} \) ",
            ],
            line_spacing=3.0,
            columns=1,
        )
        .add_page_break()
        .add_exercise(
            title="問題10",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{4}{9} \) + \( \dfrac{5}{18} \) ",
                r" \( \dfrac{7}{15} \) + \( \dfrac{11}{30} \) ",
                r" \( \dfrac{3}{14} \) + \( \dfrac{5}{21} \) ",
                r" \( \dfrac{9}{20} \) + \( \dfrac{7}{25} \) ",
                r" \( \dfrac{13}{24} \) + \( \dfrac{1}{8} \) ",
                r" \( \dfrac{17}{28} \) + \( \dfrac{3}{7} \) ",
            ],
            columns=2,
            line_spacing=3.0,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題11",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{5}{12} \) + \( \dfrac{1}{3} \) - \( \dfrac{1}{8} \) ",
                r" \( \dfrac{7}{10} \) - \( \dfrac{1}{4} \) + \( \dfrac{2}{5} \) ",
                r" \( \dfrac{11}{18} \) + \( \dfrac{1}{6} \) - \( \dfrac{1}{9} \) ",
                r" \( \dfrac{13}{20} \) - \( \dfrac{3}{10} \) + \( \dfrac{1}{5} \) ",
                r" \( \dfrac{17}{24} \) + \( \dfrac{1}{12} \) - \( \dfrac{5}{18} \) ",
                r" \( \dfrac{19}{30} \) - \( \dfrac{1}{6} \) + \( \dfrac{2}{15} \) ",
                r" \( \dfrac{5}{16} \) + \( \dfrac{3}{8} \) - \( \dfrac{1}{4} \) ",
                r" \( \dfrac{7}{22} \) + \( \dfrac{9}{33} \) - \( \dfrac{2}{11} \) ",
            ],
            line_spacing=3.0,
            columns=2,
        )
        .add_blank_space(height="-0.4cm")
        .add_exercise(
            title="問題12",
            content=r"次の計算をしなさい。",
            items=[
                r" \( \dfrac{1}{3} \) + \( \dfrac{1}{4} \) + \( \dfrac{1}{5} \) ",
                r" \( \dfrac{2}{7} \) + \( \dfrac{3}{14} \) + \( \dfrac{1}{2} \) ",
                r" \( \dfrac{5}{12} \) + \( \dfrac{7}{18} \) - \( \dfrac{1}{6} \) ",
                r" \( \dfrac{11}{20} \) - \( \dfrac{1}{4} \) + \( \dfrac{3}{10} \) ",
                r" \( \dfrac{13}{30} \) + \( \dfrac{1}{6} \) + \( \dfrac{2}{5} \) ",
                r" \( \dfrac{17}{24} \) - \( \dfrac{1}{3} \) + \( \dfrac{5}{12} \) ",
            ],
            line_spacing=3.0,
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
