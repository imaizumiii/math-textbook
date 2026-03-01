# Math Textbook Generator

PythonとLaTeXを連携して、高品質な数学テキスト、問題集、レポートを自動生成するライブラリです。**Pythonコードから直接LaTeXドキュメントを構築**できるため、テンプレートファイルへの依存を最小限に抑えられます。

## 特徴

- **数学テキスト作成に特化**: 練習問題、解答スペース、図形配置などの専用機能を提供
- **Python中心の設計**: LaTeXテンプレートを編集せず、Pythonコードでドキュメントを構築
- **ビルダーパターン**: 流れるようなAPIで直感的にドキュメントを記述
- **自動リソース管理**: フォントのダウンロードや画像の配置を自動化
- **柔軟なレイアウト**: `DrawingSpace`により解説と手書き用スペースを並列配置
- **型安全**: `py.typed` マーカー付き、全APIに型ヒント付与済み

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
├── pdf_generator/              # メインパッケージ（py.typed付き）
│   ├── core/                  # コア機能 (Generator, Document)
│   ├── elements/              # LaTeX要素クラス群
│   │   ├── base.py            # 基底クラス (LaTeXElement)
│   │   ├── text.py            # テキスト要素 (Text, Paragraph, Line, Divider)
│   │   ├── math.py            # 数式要素 (Equation, Align)
│   │   ├── structure.py       # 構造要素 (Section, Exercise, DrawingSpace)
│   │   ├── graphics.py        # 図形要素 (Image, TikZ)
│   │   ├── boxes.py           # ボックス要素 (TextBox, Note, Warning, Info)
│   │   └── tables.py          # テーブル要素 (Table)
│   ├── builder/               # ビルダーパターン実装
│   │   ├── content_mixin.py   # 共通メソッドMixin (ContentAdderMixin)
│   │   └── document_builder.py # DocumentBuilder / SectionBuilder / DrawingSpaceBuilder
│   ├── renderer/              # LaTeXレンダリング
│   ├── config/                # 設定管理 (ConfigManager)
│   └── utils/                 # ユーティリティ
│
├── config/                    # 設定ファイル
│   ├── default.json           # デフォルト設定
│   └── schema.json            # 設定スキーマ
├── examples/                  # 使用例
│   ├── diff_mogi.py           # 模試・プリント作成の例（推奨）
│   ├── explain_function.py    # 関数の解説作成の例
│   ├── explain_sincos.py      # sin/cos 解説の例
│   ├── mosya_p60.py           # 問題集ページの例
│   └── template.py            # 基本テンプレートの例
│
├── output/                    # PDF出力先
└── requirements.txt
```

## 基本的な使い方

### 数学プリントの作成例

```python
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
        .build()
    )

    generator.generate(doc, output_name="math_print.pdf")

if __name__ == "__main__":
    main()
```

## DocumentBuilder API

`DocumentBuilder` / `SectionBuilder` / `DrawingSpaceBuilder` の3クラスは `ContentAdderMixin` を継承しており、以下のコンテンツ追加メソッドを共有しています。

### ドキュメント設定（DocumentBuilder のみ）

| メソッド | 説明 |
|---------|------|
| `.set_font_from_url(url, name)` | フォントを自動ダウンロードして設定 |
| `.set_font_file(path, name)` | ローカルのフォントファイルを設定 |
| `.set_font(font)` | CJKフォントを設定（`"min"` / `"goth"`） |
| `.set_margins(top, bottom, left, right)` | 余白を設定 |
| `.set_line_spacing(spacing)` | 行間倍率を設定（例: `1.5`） |
| `.add_package(package, options)` | LaTeXパッケージを追加 |

### 構造（DocumentBuilder のみ）

| メソッド | 説明 |
|---------|------|
| `.add_section(title, level, numbered)` | セクション追加 → `SectionBuilder` を返す |
| `.add_drawing_space(width, right_margin, margin_image)` | 手書きスペース追加 → `DrawingSpaceBuilder` を返す |
| `.build()` | `Document` オブジェクトを返す |

### コンテンツ追加（全ビルダー共通）

| メソッド | 説明 |
|---------|------|
| `.add_text(text, bold)` | テキストを追加 |
| `.add_paragraph(text, bold)` | 段落を追加 |
| `.add_abstract(text, bold, centered)` | 中央寄せ概要を追加 |
| `.add_equation(latex_str, inline)` | 数式を追加 |
| `.add_align([eq1, eq2, ...], numbered)` | 複数行数式を追加 |
| `.add_textbox(content, title, box_type)` | 装飾ボックスを追加 |
| `.add_note/warning/info(content)` | 各種アイコン付きボックスを追加 |
| `.add_image(path, caption, width)` | 画像を追加 |
| `.add_tikz(code, caption, libraries, inline)` | TikZ図形を追加 |
| `.add_list(items, ordered)` | 箇条書きリストを追加 |
| `.add_table(headers, rows, caption)` | テーブルを追加 |
| `.add_exercise(title, content, items, columns)` | 練習問題を追加 |
| `.add_drawing_space(width, right_margin)` | 手書きスペースを追加 |
| `.add_blank_space(height)` | 空白スペースを追加 |
| `.add_line(text, line_style, color)` | 装飾線付きテキストを追加 |
| `.add_divider(symbol, spacing)` | 区切り記号を追加 |

### ビルダーの終了

| メソッド | 戻り値 |
|---------|------|
| `SectionBuilder.end_section()` | `DocumentBuilder` |
| `DrawingSpaceBuilder.end_drawing_space()` | `DocumentBuilder` または `SectionBuilder` |

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

# sin/cos 解説の生成
python examples/explain_sincos.py

# 問題集ページの生成
python examples/mosya_p60.py
```

## ライセンス

このプロジェクトは個人利用を目的としています。
