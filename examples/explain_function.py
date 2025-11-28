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
        .set_font_file(
            str(Path(__file__).parent.parent /
                "fonts" / "NotoSansJP-Regular.ttf"),
            "Noto Sans JP",
        )  # ローカルファイル
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")  # 余白を設定
        .set_line_spacing(1.8)  # 行間を1.8倍に設定
        
        # ここから内容を追加
        .add_section("Theme: 関数$f(x)$とは？（中学生、高校生向け）")
        
        .add_text(r"\quad \textbf{”関数”} という言葉がなじみ始めるのは、中学二年生の「一次関数」という単元ではないでしょうか。高校生なんかは、もっといろんなところでこの言葉を耳にしていますよね。ここでは、「関数」について小学生でも理解できるように簡単に説明していきますので、ぜひ見ていってください。")
        
        .add_divider()
        
        .add_text(r"\quad 「関数」という言葉ですが、数学以外でも、\textbf{プログラミングの世界で良く出現するんです。} そちらの世界の説明のほうがわかりやすいので、少しお借りすることとします。\\")

        .add_blank_space("4cm")
        
        .add_text(r"\quad 関数はよく、\textbf{「数字の工場」}と表現されます。何かを作るにはまず材料が必要ですよね。工場に入れる材料のことを、\textbf{変数}だとか\textbf{引数}、\textbf{入力値} とか言ったりもします。\\")
        
        .add_text(r"すると、工場は製品を作ってくれます。この出来上がった製品のことを、\textbf{出力値}とか\textbf{返り値}といいます。\\")
        
        .add_text(r"\quad それでは、なじみの深いであろう$\boldsymbol{y = 2x + 1}$という一次関数について見ていきましょうか。")

        .add_divider()
        
        .add_drawing_space(width="0.6\\textwidth", right_margin="2cm")
            .add_text(r"数学の世界では、\textbf{入力値を} $\boldsymbol{x}$、\textbf{出力値を} $\boldsymbol{y}$や $\boldsymbol{f(x)}$とすることが多いです。 ")
            .add_text(r"せっかくなので中学生の皆さんも$f(x)$という書き方で見ていきましょうか。")
            .add_text(r"$f(x) = 2x + 1$と数式で書くと、皆さんアレルギー反応が出てしまう可能性があるので、\begin{center}$f$(入力値) $= 2\times$(入力値) $+$ $1$\end{center} としましょうか。")
            .add_text(r"見てわかるように、入力値に2を入れれば5が、3を入れれば7が出力されるというわけです。数式で書くと、")
            .add_text(r"\begin{center}$f(2) = 5$ \qquad $f(3) = 7$ \qquad $f(-1) = -1$\end{center}")
            .add_text(r"これを一目でわかるようにしたのが、\textbf{グラフ}なのです。（右図）")
        .end_drawing_space()
        
        .add_divider()
        
        .add_text(r"関数は英語で\textbf{function}というので、$f(x)$の$f$はそこから来てるんですね。")
        
        .add_text(r"ちなみに、教科書の関数の説明ではこのように書いてあります。\\")
        
        .add_text(r"\quad 「２つの変数$x$と$y$があって、$x$ の値を定めると、それにともなって $y$ の値がただ 1 つ定まるとき、$y$ は $x$ の関数であるという。」\\")
        
        .add_text(r"まぁ、正しいといえば正しいですが、ちょっとわかりにくいですね。慣れるまでは、\textbf{「数字の工場」}というイメージを持っておくことをお勧めします。裏面に少しだけ問題を載せておくので、いろんな関数をみていってください。")
        
        .add_line("問題")
        
        .add_exercise("問題1", r"関数 $y = 5x $ について、$x=2$のときの$y$の値を求めよ。（比例）\\")
        
        .add_exercise("問題2", r"関数 $y =\dfrac{24}{x}$ について、$x=6$のときの$y$の値を求めよ。（反比例）\\")
        
        .add_exercise("問題3", r"関数 $y = -2x + 7$ について、$y=1$となるような$x$の値を求めよ。（一次関数）\\")
        
        .add_exercise("問題4", r"原点を通る二次関数について、$x=-2$のとき、$y=12$となるような関数を求めよ。（二次関数）\\")
        
        .add_line("ここから高校", line_style="dashed", line_thickness="1pt")

        .add_exercise("問題5", r"関数$x^3 -1$について、$y=26$となるような$x$の値を求めよ。（三次関数）\\")
        
        .add_exercise("問題6", r"関数 $y = \sqrt{x}$ について、$y=4$となるような$x$の値を求めよ。（平方根）\\")

        .add_exercise("問題7", r"関数 $y = 2^x$について、$x=5$のときの$y$の値を求めよ。（指数関数）\\")
        
        .add_exercise("問題8", r"関数 $y = \log_3 x$ について、$y=4$となるような$x$の値を求めよ。（対数関数）\\")
        
        .add_exercise("問題9", r"関数$y = \sin x$について、$y = \dfrac{1}{2}$のときの$x$の値を求めよ。（三角関数）\\")
        
        
        
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
