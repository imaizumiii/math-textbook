# PDF Generator

PythonとLaTeXを連携してPDFを自動生成するライブラリです。**Pythonコードから直接LaTeXドキュメントを構築**できるため、テンプレートファイルへの依存を最小限に抑えられます。

## 特徴

- **Python中心の設計**: LaTeXテンプレートを編集せず、Pythonコードでドキュメントを構築
- **ビルダーパターン**: 流れるようなAPIでドキュメントを構築
- **拡張性**: 新しい要素クラスを簡単に追加可能
- **型安全**: メソッドチェーンで構造を明確に定義
- **柔軟性**: JSON設定ファイルによる柔軟な設定管理
- **エラーハンドリング**: 詳細なエラーメッセージと例外処理

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
│   ├── __init__.py            # パブリックAPIのエクスポート
│   │
│   ├── core/                  # コア機能
│   │   ├── __init__.py
│   │   ├── generator.py       # PDFGenerator（メインクラス）
│   │   └── document.py        # Documentクラス（ドキュメント全体を管理）
│   │
│   ├── elements/              # LaTeX要素クラス群
│   │   ├── __init__.py
│   │   ├── base.py            # LaTeXElement基底クラス
│   │   ├── text.py            # Text, Paragraph, List
│   │   ├── math.py            # Equation, Align
│   │   ├── graphics.py        # Image, Figure
│   │   ├── boxes.py           # TextBox, Note, Warning, Info
│   │   ├── structure.py       # Section, Chapter, TableOfContents
│   │   └── tables.py          # Table
│   │
│   ├── builder/               # ビルダーパターン実装
│   │   ├── __init__.py
│   │   └── document_builder.py # DocumentBuilder, SectionBuilder
│   │
│   ├── renderer/              # LaTeXレンダリング
│   │   ├── __init__.py
│   │   ├── latex_renderer.py  # LaTeXコード生成
│   │   └── preamble.py         # プリアンブル管理
│   │
│   ├── config/                # 設定管理
│   │   ├── __init__.py
│   │   └── config_manager.py  # 設定読み込み・管理
│   │
│   ├── utils/                 # ユーティリティ
│   │   ├── __init__.py
│   │   ├── file_utils.py      # ファイル操作
│   │   └── encoding.py        # エンコーディング処理
│   │
│   └── compiler.py            # LaTeXコンパイラ
│
├── config/                    # 設定ファイル
│   ├── default.json
│   └── schema.json
│
├── examples/                  # 使用例
│   ├── builder_example.py     # Builderパターンの例（推奨）
│   └── usage_example.py       # レガシーAPIの例
│
├── templates/                 # テンプレート（レガシー、オプション）
│   └── report.tex
│
├── output/                    # PDF出力先
├── temp/                      # 一時ファイル
│
├── requirements.txt
└── README.md
```

## 基本的な使い方

### 1. 簡単な例

```python
from pdf_generator import PDFGenerator, DocumentBuilder

# PDFGeneratorを初期化
generator = PDFGenerator()

# DocumentBuilderでドキュメントを構築
doc = (DocumentBuilder("タイトル", "著者名", "2024年1月1日")
    
    # セクションを追加
    .add_section("はじめに")
        .add_text("テキストを追加")
        .add_equation(r"E = mc^2")
        .end_section()
    
    .build())

# PDFを生成
pdf_path = generator.generate(doc, output_name="output.pdf")
print(f"PDFが生成されました: {pdf_path}")
```

### 2. より詳細な例

```python
from pdf_generator import PDFGenerator, DocumentBuilder

generator = PDFGenerator()

doc = (DocumentBuilder("数学レポート", "あなたの名前", "2024年1月1日")
    
    # セクション1: はじめに
    .add_section("はじめに")
        .add_text("このレポートでは、以下の内容について説明します。")
        .add_list([
            "PythonによるLaTeX生成",
            "図の挿入方法",
            "テキストボックスの使用方法"
        ], ordered=True)
        .end_section()
    
    # セクション2: 計算結果
    .add_section("計算結果")
        .add_text("Pythonで計算された円周率を数式として表示します。")
        .add_equation(r"\pi \approx \mathbf{3.141593}")
        .end_section()
    
    # セクション3: 図の挿入
    .add_section("図表")
        .add_image(
            image_path="path/to/image.png",
            caption="関数のグラフ",
            width="0.6",
            label="fig:graph1"
        )
        .end_section()
    
    # セクション4: テキストボックス
    .add_section("補足説明")
        .add_note("この結果は実験的に確認されました。")
        .add_warning("数値は近似値です。")
        .add_info("詳細は参考文献を参照してください。")
        .end_section()
    
    .build())

# PDFを生成
pdf_path = generator.generate(doc, output_name="math_report.pdf")
```

### 3. 実行

```bash
python examples/builder_example.py
```

## 利用可能な要素

### テキスト要素

- `Text(text)` - テキストを追加
- `Paragraph(text)` - 段落を追加
- `List(items, ordered=False)` - リストを追加

### 数式要素

- `Equation(equation, inline=False, label=None)` - 数式を追加
- `Align(equations, label=None)` - 複数行の数式を追加

### 画像要素

- `Image(image_path, caption=None, width="0.8", label=None)` - 画像を追加
- `Figure(...)` - Imageのエイリアス

### テキストボックス要素

- `TextBox(content, title=None, box_type="tcolorbox", style=None)` - カスタムテキストボックス
- `Note(content)` - 注意書きボックス（黄色）
- `Warning(content)` - 警告ボックス（赤色）
- `Info(content)` - 情報ボックス（青色）

### 構造要素

- `Section(title, level=1, label=None)` - セクションを追加
- `Chapter(title, label=None)` - 章を追加（bookクラス用）
- `TableOfContents()` - 目次を追加

### テーブル要素

- `Table(headers, rows, caption=None, label=None)` - テーブルを追加

## DocumentBuilderのメソッド

### DocumentBuilderのメソッド

- `.set_font(font)` - フォントを設定（CJKutf8用: "min"=明朝体, "goth"=ゴシック体）
- `.set_font_file(font_file, font_name=None)` - フォントファイルを設定（XeLaTeX/LuaLaTeX用）
- `.set_font_from_url(url, font_name=None, fonts_dir=None)` - URLからフォントファイルをダウンロードして設定
- `.set_margins(top=None, bottom=None, left=None, right=None)` - 余白を設定
- `.add_package(package, options=None)` - LaTeXパッケージを追加
- `.add_section(title, level=1, label=None)` - セクションを追加（SectionBuilderを返す）
- `.add_text(text)` - テキストを追加
- `.add_paragraph(text)` - 段落を追加
- `.add_image(...)` - 画像を追加
- `.add_textbox(...)` - テキストボックスを追加
- `.add_note(content)` - 注意書きボックスを追加
- `.add_warning(content)` - 警告ボックスを追加
- `.add_info(content)` - 情報ボックスを追加
- `.add_equation(...)` - 数式を追加
- `.add_table(...)` - テーブルを追加
- `.build()` - Documentオブジェクトを構築

### SectionBuilderのメソッド

- `.add_text(text)` - テキストを追加
- `.add_paragraph(text)` - 段落を追加
- `.add_image(...)` - 画像を追加
- `.add_textbox(...)` - テキストボックスを追加
- `.add_note(content)` - 注意書きを追加
- `.add_warning(content)` - 警告を追加
- `.add_info(content)` - 情報を追加
- `.add_equation(...)` - 数式を追加
- `.add_align(equations, label=None, numbered=True)` - 複数行の数式を追加
- `.add_list(items, ordered=False)` - リストを追加
- `.add_table(...)` - テーブルを追加
- `.end_section()` - セクションを終了してDocumentBuilderに戻る

## 設定ファイル

設定は`config/default.json`で管理されます：

```json
{
  "directories": {
    "output_dir": "output",
    "temp_dir": "temp",
    "fonts_dir": "fonts"
  },
  "compilation": {
    "engine": "pdflatex",
    "compile_times": 2,
    "interaction_mode": "nonstopmode"
  },
  "file_management": {
    "cleanup": true,
    "keep_tex": false,
    "keep_log": false
  }
}
```

### 設定項目の説明

#### directories
- `output_dir`: PDF出力先ディレクトリ（デフォルト: `output`）
- `temp_dir`: 一時ファイルの保存ディレクトリ（デフォルト: `temp`）

#### compilation
- `engine`: LaTeXエンジン（`pdflatex`, `xelatex`, `lualatex`）
- `compile_times`: コンパイル回数（通常は2回）
- `interaction_mode`: インタラクションモード（`nonstopmode`, `batchmode`など）

#### file_management
- `cleanup`: 中間ファイルを削除するか
- `keep_tex`: `.tex`ファイルを残すか
- `keep_log`: `.log`ファイルを残すか
- `cleanup_extensions`: 削除する拡張子のリスト

## フォントの設定

フォントの設定には3つの方法があります：

### 方法1: CJKutf8を使用（シンプル）

```python
doc = (DocumentBuilder("タイトル", "著者")
    .set_font("goth")  # ゴシック体（"min"=明朝体）
    .build())
```

### 方法2: フォントファイルを直接指定（推奨）

```python
doc = (DocumentBuilder("タイトル", "著者")
    .set_font_file("fonts/NotoSansJP-Regular.ttf", "Noto Sans JP")
    # またはシステムフォント
    # .set_font_file("C:/Windows/Fonts/msgothic.ttc", "MS Gothic")
    .build())
```

### 方法3: URLからダウンロード（最も便利）

```python
doc = (DocumentBuilder("タイトル", "著者")
    .set_font_from_url(
        "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP-Regular.ttf",
        "Noto Sans JP"
    )
    .build())
```

フォントファイルは自動的に`fonts/`ディレクトリにダウンロードされ、PDF生成時に`output/fonts/`にコピーされます。

## 画像の処理

画像ファイルは自動的に`output/images/`ディレクトリにコピーされ、相対パスに変換されます：

```python
doc = (DocumentBuilder("タイトル", "著者")
    .add_section("図表")
        .add_image("path/to/image.png", caption="説明")
        .end_section()
    .build())

# 画像は自動的に output/images/image.png にコピーされる
generator.generate(doc)
```

## エラーハンドリング

すべてのエラーは例外として投げられます：

- `FileNotFoundError`: 設定ファイルや画像ファイルが見つからない場合
- `ValidationError`: 設定ファイルのバリデーションエラー
- `RuntimeError`: LaTeXコンパイルエラー

```python
try:
    pdf_path = generator.generate(doc, output_name="output.pdf")
except FileNotFoundError as e:
    print(f"ファイルが見つかりません: {e}")
except RuntimeError as e:
    print(f"コンパイルエラー: {e}")
```

## 拡張方法

### カスタム要素の作成

新しい要素クラスを作成するには、`LaTeXElement`を継承します：

```python
from pdf_generator.elements.base import LaTeXElement

class CustomElement(LaTeXElement):
    def __init__(self, content: str):
        super().__init__()
        self.content = content
    
    def to_latex(self) -> str:
        return f"\\customcommand{{{self.content}}}\n"
```

### カスタムパッケージの追加

```python
doc = (DocumentBuilder("タイトル", "著者")
    .add_package("tikz")
    .add_package("babel", options="[english]")
    .build())
```

## レガシーAPI（非推奨）

旧バージョンのテンプレートベースのAPIも利用可能ですが、非推奨です：

```python
# 非推奨: テンプレートベースのAPI
generator = PDFGenerator()
pdf_path = generator.generate(
    template_name="report",
    variables={"title": "タイトル", "author": "著者"},
    output_name="output.pdf"
)
```

新しいプロジェクトでは`DocumentBuilder`を使用することを推奨します。

## 使用例

詳細な使用例は`examples/builder_example.py`を参照してください。

```bash
python examples/builder_example.py
```

## ライセンス

このプロジェクトは個人利用を目的としています。
