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
        # フォント設定（3つの方法があります）
        # 方法1: CJKutf8を使用（シンプルだが不安定な場合がある）
        # .set_font("goth")  # ゴシック体に設定（デフォルト: "min"=明朝体）
        # 方法2: フォントファイルを直接指定（より安定、XeLaTeX/LuaLaTeXが必要）
        # .set_font_file("C:/Windows/Fonts/msgothic.ttc", "MS Gothic")  # Windowsの場合
        # .set_font_file("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")  # Linuxの場合
        .set_font_file(
            str(Path(__file__).parent.parent /
                "fonts" / "NotoSansJP-Regular.ttf"),
            "Noto Sans JP",
        )  # ローカルファイル
        # 方法3: URLからフォントファイルをダウンロード（推奨）
        # .set_font_from_url(
        #     "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf",
        #     "Noto Sans JP"
        # )
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")  # 余白を設定
        .set_line_spacing(1.8)  # 行間を1.5倍に設定
        # .set_abstract("このレポートでは、PythonとLaTeXの連携について説明します。")
        # セクション2: 計算結果
        .add_section("Theme: 微分積分とは？")
        # 導入
        .add_paragraph(
            r"みなさん、\textbf{”微分積分”}って聞いたことありますか？ 「難しそう」という感想を持つ人がほとんどだと思いますが、実はすごくシンプルで便利なツールなんですよ。"
        )
        # 変化の割合の復習
        .add_paragraph(
            r"まずは、復習から。\textbf{”変化の割合”}という言葉はきいたことあると思います。$\text{変化の割合}=\frac{\text{$y$の増加量}}{\text{$x$の増加量}}$とかいうやつです。具体例を用いながら思い出していきましょう。"
        )
        .add_divider()
        # 具体例　グラフ挿入
        .add_drawing_space(width="0.65\\textwidth", right_margin="20cm")
        .add_paragraph(
            r"$y=x^2$というグラフを考えてみましょう。$x=1$から$x=2$に変化したときの変化の割合は、次のような式から求められます。"
        )
        .add_text(
            r"\begin{center}$\dfrac{\text{$y$の増加量}}{\text{$x$の増加量}} =\dfrac{f(2) - f(1)}{2 - 1} =\dfrac{2^2 - 1^2}{2 - 1} = 3$\end{center}"
        )
        .add_text(
            r"さて、ここからは文字にしていきます。文字にしたとたんにわからない人が急増するのでお気を付けを。"
        )
        .add_text(
            r"\begin{center}$\dfrac{\text{$y$の増加量}}{\text{$x$の増加量}} =\dfrac{f(x+h) - f(x)}{(x+h) - x} =\dfrac{f(x+h) - f(x)}{h}$\end{center}"
        )
        .add_text(
            r"具体例では\textbf{「} $\boldsymbol{1 \rightarrow 2}$ \textbf{」}という変化でしたが、これを\textbf{「} $\boldsymbol{x \rightarrow x+h}$ \textbf{」}という変化にしてみました。グラフからよく確認しておいてください。"
        )
        .end_drawing_space()
        # 公式紹介
        .add_text(
            "このタイミングで微分係数を求める公式（定義）を紹介することにします。"
        )
        .add_textbox(
            title="微分係数の求め方（定義）",
            content=r"関数$f(x)$の微分係数$f'(x)$は以下のように定義される。\[ f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} \]",
            style=math_box_style,
        )
        .add_text(
            r"{\centering\textbf{さっき作った式にすごく似ていることがわかりますね？}\par}"
        )
        .add_text(
            r"さっきの図をでは、\textbf{幅を} $\boldsymbol{h}$としていたので、「\textbf{その幅をごくごく小さくすれば、瞬間の変化率がわかるんじゃね？」}という発想になります。実際にさっきの例で計算してみましょうか。"
        )
        .add_align(
            [
                r"\begin{aligned}",
                r"f'(x)      & = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} \\",
                r"           & = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h} \\",
                r"           & = \lim_{h \to 0} \frac{x^2 + 2xh + h^2 - x^2}{h} \\",
                r"           & = \lim_{h \to 0} \frac{2xh + h^2}{h} \\",
                r"           & = \lim_{h \to 0} (2x + h) \\",
                r"           & = 2x",
                r"\end{aligned}",
            ]
        )
        
        
        .add_text(
            r"よって、$\boldsymbol{f'(x) = 2x}$となります。実際に、「$f(x) = x^2$の\textbf{導関数}を求めよ」と言われたら、これが答えになります。「$x=2$における$f(x) = x^2$の\textbf{微分係数}を求めよ」とか言われたら、$x=2$を代入して、$f'(2) = 4$が答えになります。少しだけ単語が複雑ですが、問題を解くときにはあまり困らないので、あまり気にしないでおくことにしましょう。\\"
        )

        .add_paragraph(
            r"\textbf{これがとても便利なんですよ。}今回はこれで終わりですが、この分野は物理や数学以外にも、経済学や社会学でもよく使われるんですよ。では、少しだけ教科書の問題を解いて終わることとしましょう。"
        )
        
        .add_line("練習4, 5（教科書P.195,199）", line_thickness="5pt")

        .add_exercise("練習4","関数$f(x) = x^3+2$の$x=1$における微分係数$f'(1)$を求めよ。")
        
        .add_exercise("練習5", "導関数の定義に従って、次の関数の導関数を求めよ。", items=[
            "$f(x) = 3x^2$",
            "$f(x) = -x^2$",
        ], columns=2)
        
        # .add_line("")
        
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
