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
        .add_section("Theme: $\sin$, $\cos$とは？")
        
        .add_text(r"今回は、$\boldsymbol{\sin}$, $\boldsymbol{\cos}$とは何かについて説明します。$\sin$, $\cos$, $\tan$はまとめて\textbf{三角関数}と呼ばれます。$\tan$だけ、少し種類が違うので、今回は$\sin$と$\cos$のみ説明します。")
        .add_text(r"まずは、$\boldsymbol{\sin}$, $\boldsymbol{\cos}$\textbf{を使いたくなるシチュエーションを紹介したいと思います。}今回は物理分野の力学からお借りします。次の図を見てください。")

        .add_blank_space("4cm")
        
        .add_text(r"日常生活でもよく目にしそうな光景ですね。荷物を斜めに引っ張っている様子です。")
        .add_text(r"このとき、おそらく皆さんを悩ませる原因は、\textbf{紐が斜めであること}じゃないでしょうか。仮に紐がまっすぐだったら、どれくらいの力で引っ張っているかがすぐに計算できそうです。しかし、今回は紐が斜めなので、すぐには計算できません。そこで、頭のいい人はこう考えました。")

        .add_text(r"{\centering\textbf{「斜めの矢印を、縦と横に分けたらいいんじゃね？」}\par}")
        
        .add_text(r"一応、中学の理科で\textbf{力の分解}なるものを習ったと思います。それを使って斜めの矢印を縦と横に分解するという発想になります。")
        
        .add_text(r"{\centering\textbf{そのときに使うものこそが、} $\boldsymbol{\sin}$ \textbf{と} $\boldsymbol{\cos}$ \textbf{なんです。}\par}") 
        
        .add_text(r"下の図を見てください。斜めに向いている力を縦と横に分解してみました。角度を$\boldsymbol{\theta}$という文字で表しています。")

        .add_blank_space("4cm")
        
        .add_text(r"このとき、縦方向の力が$\boldsymbol{T \sin \theta}$、横方向の力が$\boldsymbol{T \cos \theta}$となります。")
        
        .add_text(r"皆さんの頭の上についたハテナを一度無視して、$\boldsymbol{T}$ \textbf{の大きさを} $\boldsymbol{1}$ にしてみます。この\textbf{「１」}というのがミソなんですよ。")
        
        .add_blank_space("4cm")
        
        .add_text(r"{\centering\textbf{$\boldsymbol{\sin\theta}$は縦方向の力、$\boldsymbol{\cos\theta}$は横方向の力}\par}")
        
        .add_text(r"このイメージをしっかり持つようにしてください。そうすれば、皆さんが苦手な\textbf{90度以上のときの三角関数}もすぐに理解できるようになります。\\")
        
        .add_drawing_space(width="0.6\\textwidth", right_margin="2cm")
        
        .add_text(r"右の図は、$\theta = 90^\circ$のときです。横方向は矢印が伸びていないのが一目瞭然ですよね。なので、$\boldsymbol{\cos 90^\circ = 0}$となります。")
        
        .add_text(r"一方、縦方向の矢印はそのまま引っ張る力と同じになっていますよね？ひもを引っ張る力は「１」と設定していたので、$\boldsymbol{\sin 90^\circ = 1}$となります。\\")
        
        .add_text(r"いろんなパターンで確認していきましょう！次は$\theta = 150^\circ$のときでも考えてみましょうか。")
        
        .add_text(r"$\sin$の値はわかりますかね？$\sin$は縦方向の力だったので、縦方向の矢印の長さを見ればいいですよね。すると、$\boldsymbol{\sin 150^\circ = \frac{1}{2}}$となります。")
        
        .add_text(r"次は$\cos$の値です。横方向の力が、運ぶ方向と逆に向いているのがわかりますか？逆に向いているということはつまり、\textbf{マイナスの値をとる}ということになります。よって、$\boldsymbol{\cos 150^\circ = -\frac{\sqrt{3}}{2}}$となります。")
        
        .end_drawing_space()        
        
        
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
