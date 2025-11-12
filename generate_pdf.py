# math_generator/generate_pdf.py

import yaml
import random
import subprocess
from jinja2 import Environment, FileSystemLoader

# --- 1. 設定の読み込み ---
def load_config(config_path='config.yaml'):
    """YAML設定ファイルを読み込む"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# --- 2. 問題データの生成 ---
def generate_problem_data(config):
    """一次方程式の問題と解答をランダムに生成する"""
    problems = []
    
    sol_min, sol_max = config['solution_range'].values()
    a_min, a_max = config['coefficient_a_range'].values()
    b_min, b_max = config['coefficient_b_range'].values()

    for _ in range(config['num_problems']):
        # 解 x を先に決める
        x = random.randint(sol_min, sol_max)
        
        # 係数 a, b をランダムに決定 (a は 0 以外とする)
        a = random.randint(a_min, a_max)
        if a == 0: a = 1 # 0になる可能性を回避
        b = random.randint(b_min, b_max)
        
        # 定数項 c を計算: c = ax + b
        c = a * x + b
        
        # 問題を整形（b=0やb<0の場合の表示を簡略化）
        # LaTeXテンプレート側で表示処理を行うため、ここでは計算結果のみ格納
        problem = {
            'a': a,
            'b': b,
            'c': c,
            'x': x, # 解答
        }
        problems.append(problem)
        
    return problems

# --- 3. LaTeXファイルの生成 ---
def create_tex_file(config, problems_data, template_path='template.tex.jinja2', output_tex='output.tex'):
    """Jinja2でLaTeXコードを生成し、ファイルに出力する"""
    
    # Jinja2環境の設定
    file_loader = FileSystemLoader('.') # 現在のディレクトリからテンプレートを読み込む
    env = Environment(loader=file_loader)
    template = env.get_template(template_path)
    
    # テンプレートにデータを渡してレンダリング
    output = template.render(
        title=config['title'],
        problems=problems_data
    )
    
    # .texファイルとして保存
    with open(output_tex, 'w', encoding='utf-8') as f:
        f.write(output)
        
    return output_tex

# --- 4. PDFへのコンパイル ---
def compile_latex_to_pdf(tex_filename):
    """xelatex (日本語対応) を使ってPDFを生成する"""
    
    # .texファイル名から拡張子を除いたベース名を取得
    base_name = tex_filename.replace('.tex', '')
    
    print(f"--- {tex_filename} をxelatexでコンパイル中 ---")
    try:
        # xelatexを2回実行するのは、目次やページ参照などを正しく反映させるため（今回は不要かもしれないが習慣として）
        subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename], check=True, stdout=subprocess.DEVNULL)
        print(f"✅ PDF生成が完了しました: {base_name}.pdf")
        
        # コンパイルで生成される中間ファイル（.aux, .logなど）を削除してフォルダをクリーンに保つ（任意）
        import os
        cleanup_files = ['.aux', '.log', '.out', '.toc', '.gz']
        for ext in cleanup_files:
            try:
                file_path = f'{base_name}{ext}'
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
        
    except subprocess.CalledProcessError:
        print("❌ LaTeXコンパイルに失敗しました。xelatexがインストールされているか、またLaTeXコードにエラーがないか確認してください。")
    except FileNotFoundError:
        print("❌ xelatexコマンドが見つかりません。LaTeX環境が正しく設定されているか確認してください。")


# --- メイン処理 ---
if __name__ == "__main__":
    
    # 1. 設定を読み込む
    config = load_config()
    
    # 2. 問題データを生成する
    problems_data = generate_problem_data(config)
    
    # 3. LaTeXファイルを生成する
    tex_file = create_tex_file(config, problems_data)
    
    # 4. PDFにコンパイルする
    compile_latex_to_pdf(tex_file)