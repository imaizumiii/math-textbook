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
    output_name = "mosya_p60.pdf"
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
        .set_line_spacing(1.5)  # 行間を1.5倍に設定
        # .set_abstract("このレポートでは、PythonとLaTeXの連携について説明します。")

        # セクション2: 計算結果
        .add_section("【無限大も特別な値の候補の１つ】")
        
            .add_textbox(title="例題", content=r"どのような実数$x$に対しても、不等式\\\[|x^3 + ax^2 + bx + c| \leqq |x^3|\]\\が成り立つように、実数$a, b, c$を定めよ")

            .add_paragraph("お次は阪大の問題から。これは標準的な問題なんですけど、")
            .add_equation(r"\textbf{「グラフをイメージして大雑把に答だけ追いかける」}")
            .add_text("って姿勢がないと結構な難問に見える。どうやら数学が苦手な人は「字面だけ」でモノゴトを処理しようとしているんですね。")

            .add_paragraph(r"数学は物理や化学とは違って、特に緻密さを強調される科目だから勘違いされやすいんですけど、\textbf{ある程度のイメージをもってぼんやり答の見当をつける}のはとても有効な手段です。")

            .add_paragraph("本問ならば、")

            .add_text(r"\begin{center}「$y = | x^3 |$ と $y = | x^3 + ax^2 + bx + c |$ のグラフを比較して、\\前者のほうが後者よりも（境界も含めて）常に上側にありなさいよ」\end{center}")

            .add_text(r"ということで、$a = b = c = 0$なら「常に一致する」という状況で題意が満たされるのは自明の理。そして、")

            .add_text(r"\begin{center} \textbf{「$a, b, c$ のどれか1つでも0からずれてたら無理ちゃうの？」}\end{center}")

            .add_drawing_space(width="0.7\\textwidth", right_margin="5cm")
                .add_text(r"という感覚を持てるようになってほしい。（右図参照）\\これを目指して解答を完成させるのが数学が得意な人の頭の中なわけです。")
            .end_drawing_space()
            
            .add_paragraph("前問を扱った直後ですから、おそらく")
            .add_text(r"\begin{center}\textbf{「必要性からせめて$x = 0$を代入しようかな？」}\end{center}")
            .add_line("解答", line_thickness="10pt")
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

