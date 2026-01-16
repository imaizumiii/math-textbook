import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent))

from pdf_generator.builder.document_builder import DocumentBuilder
from pdf_generator.core.generator import PDFGenerator
from pdf_generator.elements.graphics import TikZ

def main():
    try:
        builder = DocumentBuilder(title="TikZ Test")
        
        builder.add_section("TikZ Basic Shape Test")
        
        builder.add_paragraph("以下はTikZを使用して描画した円です。")
        
        # 基本的なTikZ図形
        tikz_circle = r"""
        \draw[red, fill=red!20] (0,0) circle (1cm);
        \draw[blue] (1.5,0) circle (1cm);
        """
        builder.add_tikz(tikz_circle, caption="TikZ Circle", label="fig:circle")
        
        builder.add_section("TikZ Library Test")
        builder.add_paragraph("以下はarrowsライブラリを使用した矢印です。")
        
        # ライブラリを使用したTikZ図形
        tikz_arrows = r"""
        \draw[>=stealth, ->, ultra thick] (0,0) -- (2,0);
        \draw[>=latex, <->, dashed] (0,-1) -- (2,-1);
        """
        builder.add_tikz(tikz_arrows, caption="TikZ Arrows", libraries=["arrows"])

        builder.add_section("Inline TikZ Test")
        builder.add_paragraph("文中に")
        # インラインTikZ
        builder.add_tikz(r"\draw[fill=green] (0,0) circle (2pt);", inline=True)
        builder.add_text("緑色の点を描画しました。")
        
        builder.add_section("Complex TikZ Example")
        builder.add_paragraph("関数グラフの描画例：")
        
        tikz_graph = r"""
        \draw[->] (-0.5,0) -- (4.5,0) node[right] {$x$};
        \draw[->] (0,-0.5) -- (0,4.5) node[above] {$y$};
        \draw[scale=0.5,domain=0:4,smooth,variable=\x,blue] plot ({\x},{\x*\x});
        """
        builder.add_tikz(tikz_graph, caption="Function Graph", label="fig:graph")

        # DrawingSpace内でのTikZテスト
        builder.add_section("TikZ in DrawingSpace")
        builder.add_drawing_space(width="0.6\\textwidth", right_margin="5cm") \
            .add_paragraph("DrawingSpace内にもTikZ図形を描画できます。") \
            .add_tikz(r"\draw[orange, thick] (0,0) rectangle (2,1);", caption="Orange Rectangle in DrawingSpace") \
            .end_drawing_space()

        builder.add_section("TikZ in Margin")
        
        # マージン用のTikZ図形を定義（inline=Trueにしてフロートさせないことが重要）
        margin_tikz = TikZ(
            r"\draw[blue, thick] (0,0) -- (2,2) node[right] {Margin};", 
            inline=True
        )

        builder.add_drawing_space(
            width="0.6\\textwidth", 
            right_margin="5cm", 
            margin_content=TikZ(tikz_graph, inline=True)
        ).add_paragraph("右側の余白にTikZで描いた図が表示されます。") \
         .end_drawing_space()
        
        # ビルド
        output_dir = Path("examples/output")
        output_dir.mkdir(exist_ok=True, parents=True)
        
        doc = builder.build()
        generator = PDFGenerator()
        
        pdf_path = generator.generate(doc, "text_drawing_space_image.pdf")
        print(f"PDF generated at: {pdf_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
