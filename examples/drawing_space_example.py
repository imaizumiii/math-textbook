"""
DrawingSpaceを使用したPDF生成の例

このスクリプトは、特定の部分だけ右側に余白を作って、
手書きでグラフや図を挿入できる領域を確保する方法を示します。
"""

import sys
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_generator import PDFGenerator
from pdf_generator.builder import DocumentBuilder


def main():
    output_name = "drawing_space_example.pdf"
    """メイン関数"""
    # PDFGeneratorの初期化
    print("PDFGeneratorを初期化しています...")
    generator = PDFGenerator()
    
    # DocumentBuilderでドキュメントを構築
    print("ドキュメントを構築しています...")
    doc = (DocumentBuilder(title="手書き用余白の例", author="PDF Generator")
        .set_font_file("fonts/NotoSansJP-Regular.ttf", "Noto Sans JP")
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")
        .set_line_spacing(1.5)
        
        # セクション1: 通常のテキスト
        .add_section("通常のテキスト")
            .add_paragraph("この段落は通常通り、ページ全体の幅を使用します。")
            .add_paragraph("複数の段落を追加することもできます。")
            .end_section()
        
        # セクション2: 手書き用余白を持つ部分
        .add_section("手書き用余白を持つ部分")
            .add_paragraph("以下の部分は、右側に余白が確保されています。")
            # DrawingSpaceを使用して余白を確保
            .add_drawing_space(width="0.7\\textwidth", right_margin="5cm")
                .add_paragraph("この段落は幅が制限され、右側に5cmの余白があります。")
                .add_paragraph("この余白部分に、後から手書きでグラフや図を描くことができます。")
                .add_equation("f(x) = x^2 + 2x + 1")
                .add_text("数式も同じ幅に制限されます。")
                .end_drawing_space()
            .add_paragraph("通常のテキストに戻ります。")
            .end_section()
        
        # セクション3: 異なる幅の余白
        .add_section("異なる幅の余白")
            .add_drawing_space(width="0.6\\textwidth", right_margin="6cm")
                .add_paragraph("より狭い幅（60%）と、より広い余白（6cm）の例です。")
                .add_textbox(
                    title="例題",
                    content="この問題の解答を右側の余白に図示してください。"
                )
                .end_drawing_space()
            .end_section()
        
        # セクション4: セクション内でDrawingSpaceを使用
        .add_section("セクション内での使用例")
            .add_text("セクション内でも使用できます。")
            .add_drawing_space(right_margin="4cm")
                .add_paragraph("デフォルトの幅（70%）と、カスタム余白（4cm）の例です。")
                .add_equation("\\int_0^1 x^2 dx = \\frac{1}{3}")
                .end_drawing_space()
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

