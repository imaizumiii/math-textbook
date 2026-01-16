# Math Textbook Generator

PythonとLaTeXを連携して、高品質な数学テキスト、問題集、レポートを自動生成するライブラリです。**Pythonコードから直接LaTeXドキュメントを構築**できるため、テンプレートファイルへの依存を最小限に抑えられます。

## 特徴

- **数学テキスト作成に特化**: 練習問題、解答スペース、図形配置などの専用機能を提供
- **Python中心の設計**: LaTeXテンプレートを編集せず、Pythonコードでドキュメントを構築
- **ビルダーパターン**: 流れるようなAPIで直感的にドキュメントを記述
- **自動リソース管理**: フォントのダウンロードや画像の配置を自動化
- **柔軟なレイアウト**: `DrawingSpace`により解説と手書き用スペースを並列配置

## インストール

```bash
pip install -r requirements.txt
```

必要なパッケージ:
- `jinja2>=3.0.0`
- `jsonschema>=4.0.0`

また、LaTeX環境（TeX LiveまたはMiKTeX）がインストールされ、PATHに追加されている必要があります。

## ディレクトリ構造

```
math-textbook/
├── pdf_generator/              # メインパッケージ
│   ├── core/                  # コア機能 (Generator, Document)
│   ├── elements/              # LaTeX要素クラス群
│   │   ├── text.py            # テキスト要素
│   │   ├── math.py            # 数式要素 (Equation, Align)
│   │   ├── structure.py       # 構造要素 (Section, Exercise, DrawingSpace)
│   │   ├── boxes.py           # テキストボックス要素
│   │   └── ...
│   ├── builder/               # ビルダーパターン実装 (DocumentBuilder)
│   └── renderer/              # LaTeXレンダリング
│
├── config/                    # 設定ファイル
├── examples/                  # 使用例
│   ├── diff_mogi.py           # 模試・プリント作成の例（推奨）
│   ├── explain_function.py    # 関数の解説作成の例
│   └── ...
│
├── output/                    # PDF出力先
└── requirements.txt
```

## 基本的な使い方

### 数学プリントの作成例

```python
import sys
from pathlib import Path
from pdf_generator import PDFGenerator, DocumentBuilder

def main():
    generator = PDFGenerator()
    
    doc = (DocumentBuilder("微分積分入門", "数学 太郎")
        # フォント設定（URLから自動ダウンロードして設定）
        .set_font_from_url(
            "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf",
            "Noto Sans JP"
        )
        
        .add_section("微分の基礎")
            .add_paragraph("導関数の定義は以下の通りです。")
            
            # 定義などの重要なポイントをボックスで表示
            .add_textbox(
                title="導関数の定義",
                content=r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}"
            )
            
            # 解説と余白を確保するスペース
            .add_drawing_space(width="0.6\\textwidth", right_margin="5cm")
                .add_text("この定義式に基づいて計算を行います。")
                .add_equation(r"f(x) = x^2")
                .add_align([
                    r"f'(x) &= \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h} \\",
                    r"      &= \lim_{h \to 0} (2x + h) = 2x"
                ])
            .end_drawing_space()
            
            # 練習問題の追加
            .add_exercise("練習1", "次の関数を微分せよ。", items=[
                r"f(x) = x^3",
                r"f(x) = \sin x",
                r"f(x) = e^x"
            ], columns=2)  # 2列で表示
            
        .end_section()
        .build())

    # PDF生成
    generator.generate(doc, output_name="math_print.pdf")

if __name__ == "__main__":
    main()
```

## DocumentBuilder API

ドキュメント構築のための主要なメソッドです。

### ドキュメント設定
- `.set_font_from_url(url, name)` - フォントを自動ダウンロードして設定
- `.set_font_file(path, name)` - ローカルのフォントファイルを設定
- `.set_margins(top, bottom, left, right)` - 余白の設定

### コンテンツ追加
- `.add_section(title)` - セクションの開始（SectionBuilderを返す）
- `.add_paragraph(text)` - 段落の追加
- `.add_equation(latex_str)` - 数式の追加
- `.add_align([eq1, eq2])` - 複数行数式の追加
- `.add_textbox(content, title)` - 装飾ボックスの追加
- `.add_image(path, caption)` - 画像の追加

### 数学テキスト特化機能
- `.add_drawing_space(width, right_margin)` - 解説エリアと手書き用余白を作成
- `.add_exercise(title, content, items, columns)` - 練習問題を追加
- `.add_divider()` - 区切り線を追加
- `.add_line(text)` - 見出し線を追加
- `.add_note/warning/info(content)` - 各種アイコン付きボックスを追加

## 設定ファイル (`config/default.json`)

出力ディレクトリやLaTeXエンジンの設定を行えます。

```json
{
  "directories": {
    "output_dir": "output",
    "temp_dir": "temp",
    "fonts_dir": "fonts"
  },
  "compilation": {
    "engine": "pdflatex",
    "compile_times": 2
  }
}
```

## 実行方法

付属のサンプルスクリプトを実行して動作を確認できます。

```bash
# 模試風プリントの生成
python examples/diff_mogi.py

# 関数解説の生成
python examples/explain_function.py
```

## ライセンス

このプロジェクトは個人利用を目的としています。
