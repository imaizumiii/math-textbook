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
    output_name = "diff_mogi.pdf"
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
        .set_font_file(str(Path(__file__).parent.parent / "fonts" / "NotoSansJP-Regular.ttf"), "Noto Sans JP")  # ローカルファイル
        
        # 方法3: URLからフォントファイルをダウンロード（推奨）
        # .set_font_from_url(
        #     "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf",
        #     "Noto Sans JP"
        # )
        
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")  # 余白を設定
        .set_line_spacing(1.8)  # 行間を1.5倍に設定
        # .set_abstract("このレポートでは、PythonとLaTeXの連携について説明します。")

        # セクション2: 計算結果
        .add_section("微分積分とは？")
            
            .add_paragraph(r"みなさん、\textbf{”微分積分”}って聞いたことありますか？ 「難しそう」という感想を持つ人がほとんどだと思いますが、実はすごくシンプルで便利なツールなんですよ。")
            .add_divider()
            
            .add_paragraph(r"では、復習。\textbf{”変化の割合”}という言葉はきいたことあると思います。$\text{変化の割合}=\frac{\text{$y$の増加量}}{\text{$x$の増加量}}$とかいうやつです。具体例を用いながら思い出していきましょう♪")

            .add_drawing_space(width="0.6\\textwidth", right_margin="20cm")

            .add_text(r'$y=x^2$というグラフを考えてみましょう。$x=1$から$x=2$に変化したときの変化の割合は、次のような式から求められます。')

            .add_text(r"\begin{center}$\dfrac{\text{$y$の増加量}}{\text{$x$の増加量}} =\dfrac{f(2) - f(1)}{2 - 1} =\dfrac{2^2 - 1^2}{2 - 1} = 3$\end{center}")
            
            .add_text(r"さて、ここからは文字にしていきます。文字にしたとたんにわからない人が急増するのでお気を付けを。")

            .add_text(r"\begin{center}$\dfrac{\text{$y$の増加量}}{\text{$x$の増加量}} =\dfrac{f(x+h) - f(x)}{(x+h) - x} =\dfrac{f(x+h) - f(x)}{h}$\end{center}")
            
            .add_text(r"具体例では「$\boldsymbol{1 \rightarrow 2}$」という変化でしたが、これを「$\boldsymbol{x \rightarrow x+h}$」という変化にしてみました。")

            .end_drawing_space()
            
            .add_textbox(title="例題", content=r"どのような実数$x$に対しても、不等式\\\[|x^3 + ax^2 + bx + c| \leqq |x^3|\]\\が成り立つように、実数$a, b, c$を定めよ")

            .add_text(r"\begin{center} \textbf{「$a, b, c$ のどれか1つでも0からずれてたら無理ちゃうの？」}\end{center}")

            .add_drawing_space(width="0.7\\textwidth", right_margin="5cm")
                .add_text(r"という感覚を持てるようになってほしい。（右図参照）\\これを目指して解答を完成させるのが数学が得意な人の頭の中なわけです。")
            .end_drawing_space()
            
            .add_paragraph("前問を扱った直後ですから、おそらく")
            .add_line("解答", line_thickness="5pt")
            .end_section()
        
        .build())
    
    # PDFを生成
    print("PDFを生成しています...")
    try:
        pdf_path = generator.generate(doc, output_name=output_name)
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

