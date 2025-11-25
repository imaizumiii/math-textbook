
from pdf_generator.builder.document_builder import DocumentBuilder
from pdf_generator.config.config_manager import ConfigManager

def main():
    # ビルダーの初期化
    builder = DocumentBuilder(title="番号なしセクションテスト", author="Test Author", date="2023-10-27")
    
    # コンテンツの追加（デフォルトで番号なしになるはず）
    builder.add_section("はじめに") \
           .add_paragraph("このセクションには番号がつかないはずです。")
    
    builder.add_section("番号なしセクション", numbered=False) \
           .add_paragraph("これも明示的に番号なしです。")
           
    builder.add_section("番号付きセクション", numbered=True) \
           .add_paragraph("これには番号がつくはずです。")
           
    # PDF生成
    doc = builder.build()
    from pdf_generator.core.generator import PDFGenerator
    generator = PDFGenerator()
    output_path = "test_no_number.pdf"
    generated_path = generator.generate(doc, output_path)
    print(f"Generated: {generated_path}")

if __name__ == "__main__":
    main()

