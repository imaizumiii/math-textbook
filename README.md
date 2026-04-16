# Math Textbook Generator

PythonとLaTeXを連携して、高品質な数学テキスト、問題集、レポートを自動生成するライブラリです。**Pythonコードから直接LaTeXドキュメントを構築**できるため、テンプレートファイルへの依存を最小限に抑えられます。

## 特徴

- **数学テキスト作成に特化**: 練習問題、解答スペース、図形配置などの専用機能を提供
- **Python中心の設計**: LaTeXテンプレートを編集せず、Pythonコードでドキュメントを構築
- **ビルダーパターン**: 流れるようなAPIで直感的にドキュメントを記述
- **自動リソース管理**: フォントのダウンロードや画像の配置を自動化
- **柔軟なレイアウト**: `DrawingSpace`により解説と手書き用スペースを並列配置
- **型安全**: `py.typed` マーカー付き、全APIに型ヒント付与済み

## 環境設定

### 1. 仮想環境の作成と有効化

```bash
# 仮想環境を作成
python -m venv .venv

# 有効化（macOS / Linux）
source .venv/bin/activate

# 有効化（Windows）
.venv\Scripts\activate
```

### 2. 依存パッケージのインストール

```bash
# 実行に必要なパッケージ
pip install -r requirements.txt

# 開発・テスト用パッケージ（テストを実行する場合）
pip install -r requirements-dev.txt
```

必要なパッケージ:
- `jinja2>=3.0.0`
- `jsonschema>=4.0.0`
- （開発用）`pytest>=7.0`, `pytest-cov>=4.0`

### 3. LaTeX 環境

LaTeX環境（TeX LiveまたはMiKTeX）がインストールされ、PATHに追加されている必要があります。

### 4. テストの実行

```bash
pytest
```

カバレッジレポートを出力する場合:

```bash
pytest --cov
```

## ディレクトリ構造

```
math-textbook/
├── pdf_generator/              # メインパッケージ（py.typed付き）
│   ├── exceptions.py           # カスタム例外クラス群
│   ├── core/                   # コア機能 (Generator, Document)
│   ├── elements/               # LaTeX要素クラス群
│   │   ├── base.py             # 基底クラス (LaTeXElement)
│   │   ├── text.py             # テキスト要素 (Text, Paragraph, Line, Divider)
│   │   ├── math.py             # 数式要素 (Equation, Align)
│   │   ├── structure.py        # 構造要素 (Section, Exercise, DrawingSpace, BlankSpace)
│   │   ├── graphics.py         # 図形要素 (Image, TikZ)
│   │   ├── boxes.py            # ボックス要素 (TextBox, Note, Warning, Info)
│   │   └── tables.py           # テーブル要素 (Table)
│   ├── builder/                # ビルダーパターン実装
│   │   ├── content_mixin.py    # 共通メソッドMixin (ContentAdderMixin)
│   │   └── document_builder.py # DocumentBuilder / SectionBuilder / DrawingSpaceBuilder
│   ├── renderer/               # LaTeXレンダリング
│   ├── config/                 # 設定管理 (ConfigManager)
│   └── utils/                  # ユーティリティ
│       ├── encoding.py         # 文字コード処理
│       ├── file_utils.py       # ファイル操作
│       └── font_utils.py       # フォント検索ユーティリティ
│
├── config/                     # 設定ファイル
│   ├── default.json            # デフォルト設定
│   └── schema.json             # 設定スキーマ
├── examples/                   # 使用例
│   ├── diff_mogi.py            # 模試・プリント作成の例（推奨）
│   ├── explain_function.py     # 関数の解説作成の例
│   ├── explain_sincos.py       # sin/cos 解説の例
│   ├── mosya_p60.py            # 問題集ページの例
│   ├── proofOfCLT.py           # 中心極限定理の証明ページの例
│   ├── test_drawing_space_image.py  # DrawingSpace + 画像配置の例
│   └── template.py             # 基本テンプレートの例
│
├── output/                     # PDF出力先
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

            # 解説と手書き用スペースを並列配置
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

### スクリプトごとに出力先を分ける

`generate()` の `output_dir` 引数を使うと、設定ファイルとは別に、その呼び出しだけ出力先を変更できます。

```python
from pathlib import Path

script_name = Path(__file__).stem
pdf_path = generator.generate(
    doc,
    output_name=f"{script_name}.pdf",
    output_dir=f"output/{script_name}",
)
print(pdf_path)
```

`docs/mathmatics-1/linear-inequality.py` の場合:

```python
pdf_path = generator.generate(
    doc,
    output_name="linear-inequality.pdf",
    output_dir=str(_dir / "output" / "docs" / "mathmatics-1"),
)
print(pdf_path)
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
| `.add_exercise(title, content, items, columns, line_spacing)` | 練習問題を追加（問題ブロック内だけ行間指定可） |
| `.add_drawing_space(width, right_margin, margin_image)` | 手書きスペースを追加 → `DrawingSpaceBuilder` を返す |
| `.add_blank_space(height)` | 空白スペースを追加 |
| `.add_page_break(use_clearpage)` | 改ページを追加（既定: `\newpage`） |
| `.add_line(text, line_style, color)` | 装飾線付きテキストを追加 |
| `.add_divider(symbol, spacing)` | 区切り記号を追加 |

### ビルダーの終了

| メソッド | 戻り値 |
|---------|------|
| `SectionBuilder.end_section()` | `DocumentBuilder` |
| `DrawingSpaceBuilder.end_drawing_space()` | `DocumentBuilder` または `SectionBuilder` |

## 例外クラス

`pdf_generator.exceptions` モジュールで定義されたカスタム例外を使って、エラー原因を明示的に区別できます。

| 例外クラス | 継承元 | 発生条件 |
|-----------|--------|---------|
| `MathTextbookError` | `Exception` | パッケージ共通の基底例外 |
| `CompilationError` | `MathTextbookError` | LaTeX コンパイル失敗時 |
| `FontNotFoundError` | `MathTextbookError`, `FileNotFoundError` | フォントファイルが見つからない時 |
| `ConfigurationError` | `MathTextbookError` | 設定ファイルの読み込み・バリデーション失敗時 |
| `DependencyError` | `MathTextbookError` | LaTeX エンジン等が見つからない時 |

```python
from pdf_generator import CompilationError, DependencyError

try:
    generator.generate(doc, output_name="output.pdf")
except DependencyError as e:
    print(f"LaTeXエンジンが見つかりません: {e}")
except CompilationError as e:
    print(f"コンパイルエラー: {e}")
```

> `FontNotFoundError` は `FileNotFoundError` を継承しているため、既存の `except FileNotFoundError` でもキャッチできます。

## 設定ファイル (`config/default.json`)

出力ディレクトリやLaTeXエンジンの設定を行えます。
`directories.output_dir` は `generate(..., output_dir=...)` を指定しない場合のデフォルト値です。

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

# 中心極限定理の証明ページの生成
python examples/proofOfCLT.py

# DrawingSpace + 画像配置のテスト
python examples/test_drawing_space_image.py

# 一次不等式の解説ページ（docs配下）を生成
python docs/mathmatics-1/linear-inequality.py
```

## ライセンス

このプロジェクトは個人利用を目的としています。
