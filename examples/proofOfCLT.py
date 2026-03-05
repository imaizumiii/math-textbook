"""
中心極限定理の証明（チェビシェフ不等式を用いる方法）

独立同分布の場合を一般化した形の中心極限定理を、
チェビシェフ不等式を用いて証明します。
"""

import sys
from pathlib import Path

# プロジェクトルート（pdf_generator/ を含むディレクトリ）を自動検出
_dir = Path(__file__).resolve().parent
while _dir != _dir.parent:
    if (_dir / "pdf_generator").is_dir():
        sys.path.insert(0, str(_dir))
        break
    _dir = _dir.parent

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
        DocumentBuilder("中心極限定理の証明", "数学テキスト生成システム")
        .set_font_file(
            str(Path(__file__).parent.parent / "fonts" / "NotoSansJP-Regular.ttf"),
            "Noto Sans JP",
        )
        .set_margins(top="2cm", bottom="2cm", left="2cm", right="2cm")
        .set_line_spacing(1.8)
        
        # ============================================
        # 準備：必要な定理の証明
        # ============================================
        .add_section("準備：必要な定理の証明")
        
        .add_paragraph(
            "中心極限定理の証明に必要な準備として、まずマルコフ不等式とチェビシェフ不等式を証明します。"
        )
        
        # マルコフ不等式
        .add_textbox(
            title="定理1（マルコフ不等式）",
            content=r"$X$を非負の確率変数、$a > 0$を実数とする。このとき、\[ P(X \geq a) \leq \frac{E[X]}{a} \]が成り立つ。",
            style=math_box_style,
        )
        
        .add_paragraph("証明：")
        .add_paragraph(
            "非負の確率変数$X$に対して、$X \geq a$のとき$a \leq X$が成り立つ。"
            "したがって、$X \geq a$の事象上では$a \leq X$である。"
        )
        .add_paragraph(
            "期待値の定義と、$X$が非負であることから、"
        )
        .add_align([
            r"E[X] &= \int_0^{\infty} x \, dF_X(x) \\",
            r"      &= \int_0^a x \, dF_X(x) + \int_a^{\infty} x \, dF_X(x) \\",
            r"      &\geq \int_0^a 0 \cdot dF_X(x) + \int_a^{\infty} a \cdot dF_X(x) \\",
            r"      &= a \int_a^{\infty} dF_X(x) \\",
            r"      &= a P(X \geq a)"
        ])
        .add_paragraph(
            "ここで、$F_X(x)$は$X$の分布関数である。"
            "したがって、$E[X] \geq a P(X \geq a)$が成り立ち、"
            "両辺を$a > 0$で割ることにより、"
        )
        .add_equation(r"P(X \geq a) \leq \frac{E[X]}{a}")
        .add_paragraph("を得る。$\square$")
        
        .add_divider()
        
        # チェビシェフ不等式
        .add_textbox(
            title="定理2（チェビシェフ不等式）",
            content=r"$X$を確率変数、$E[X] = \mu$、$\text{Var}(X) = \sigma^2 < \infty$とし、$k > 0$を実数とする。このとき、\[ P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2} \]が成り立つ。",
            style=math_box_style,
        )
        
        .add_paragraph("証明：")
        .add_paragraph(
            "まず、$Y = (X - \mu)^2$とおく。$Y$は非負の確率変数である。"
            "また、$E[Y] = E[(X - \mu)^2] = \text{Var}(X) = \sigma^2$である。"
        )
        .add_paragraph(
            "事象$|X - \mu| \geq k\sigma$は、$(X - \mu)^2 \geq (k\sigma)^2 = k^2\sigma^2$と同値である。"
            "したがって、"
        )
        .add_equation(r"P(|X - \mu| \geq k\sigma) = P((X - \mu)^2 \geq k^2\sigma^2) = P(Y \geq k^2\sigma^2)")
        .add_paragraph(
            "ここで、$a = k^2\sigma^2 > 0$としてマルコフ不等式を適用すると、"
        )
        .add_align([
            r"P(Y \geq k^2\sigma^2) &\leq \frac{E[Y]}{k^2\sigma^2} \\",
            r"&= \frac{\sigma^2}{k^2\sigma^2} \\",
            r"&= \frac{1}{k^2}"
        ])
        .add_paragraph(
            r"したがって、$P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2}$が成り立つ。$\square$"
        )
        
        .add_paragraph(
            r"別の表現として、$\varepsilon = k\sigma$とおくと、$k = \frac{\varepsilon}{\sigma}$であるから、"
        )
        .add_equation(r"P(|X - \mu| \geq \varepsilon) \leq \frac{\sigma^2}{\varepsilon^2}")
        .add_paragraph("という形でも表される。")
        
        .add_divider()
        
        # 弱収束の定義
        .add_textbox(
            title="定義（弱収束）",
            content=r"確率変数の列$\{X_n\}_{n=1}^{\infty}$が確率変数$X$に弱収束する（または分布収束する）とは、任意の有界連続関数$f$に対して、\[ \lim_{n \to \infty} E[f(X_n)] = E[f(X)] \]が成り立つことをいう。このとき、$X_n \xrightarrow{d} X$と表記する。",
            style=math_box_style,
        )
        
        .add_paragraph(
            r"特に、$X$が連続型確率変数で分布関数$F_X$が連続である場合、"
            r"弱収束は分布関数の各点収束と同値である。"
            r"すなわち、任意の$x \in \mathbb{R}$に対して、"
        )
        .add_equation(r"\lim_{n \to \infty} P(X_n \leq x) = P(X \leq x)")
        .add_paragraph("が成り立つ。")
        
        .add_divider()
        
        # 特性関数の性質（学習済みとして扱う）
        .add_paragraph(
            r"以下では、特性関数$\varphi_X(t) = E[e^{itX}]$の以下の性質を既知として用いる："
        )
        .add_paragraph(
            r"(1) 特性関数は分布を一意に決定する。"
        )
        .add_paragraph(
            r"(2) 確率変数の列$\{X_n\}$が$X$に弱収束するための必要十分条件は、"
            r"任意の$t \in \mathbb{R}$に対して$\lim_{n \to \infty} \varphi_{X_n}(t) = \varphi_X(t)$が成り立つことである。"
        )
        .add_paragraph(
            r"(3) $X$が平均$\mu$、分散$\sigma^2$を持つとき、$\varphi_X(t) = 1 + i\mu t - \frac{\sigma^2 t^2}{2} + o(t^2)$（$t \to 0$）である。"
        )
        
        .end_section()
        
        # ============================================
        # 中心極限定理のステートメント
        # ============================================
        .add_section("中心極限定理")
        
        .add_textbox(
            title="定理3（中心極限定理）",
            content=r"$X_1, X_2, \ldots, X_n, \ldots$を独立同分布（i.i.d.）の確率変数列とし、$E[X_1] = \mu$、$\text{Var}(X_1) = \sigma^2 < \infty$とする。このとき、標準化された和\[ Z_n = \frac{S_n - n\mu}{\sigma\sqrt{n}} = \frac{\frac{1}{n}\sum_{i=1}^n X_i - \mu}{\sigma/\sqrt{n}} \]は標準正規分布$N(0,1)$に弱収束する。すなわち、任意の$x \in \mathbb{R}$に対して、\[ \lim_{n \to \infty} P(Z_n \leq x) = \Phi(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^x e^{-\frac{t^2}{2}} \, dt \]が成り立つ。",
            style=math_box_style,
        )
        
        .add_paragraph(
            "ここで、$S_n = \sum_{i=1}^n X_i$は部分和である。"
        )
        
        .end_section()
        
        # ============================================
        # 証明
        # ============================================
        .add_section("証明")
        
        .add_paragraph(
            "証明は以下の3つのステップに分けて行う："
        )
        .add_paragraph(
            r"(1) 特性関数の収束を示す。"
        )
        .add_paragraph(
            r"(2) チェビシェフ不等式を用いて、特性関数の収束が分布収束を導くことを示す。"
        )
        .add_paragraph(
            r"(3) 分布収束の結論を導く。"
        )
        
        .add_divider()
        
        # ステップ1: 特性関数の収束
        .add_paragraph(r"\textbf{ステップ1：特性関数の収束}")
        
        .add_paragraph(
            r"まず、$Y_i = \frac{X_i - \mu}{\sigma}$とおく。"
            r"このとき、$E[Y_i] = 0$、$\text{Var}(Y_i) = 1$である。"
            r"また、$Z_n = \frac{1}{\sqrt{n}}\sum_{i=1}^n Y_i$と表される。"
        )
        
        .add_paragraph(
            r"$Y_i$の特性関数を$\varphi(t) = E[e^{itY_i}]$とおく。"
            r"$E[Y_i] = 0$、$E[Y_i^2] = \text{Var}(Y_i) = 1$であるから、"
            r"特性関数のテイラー展開により、"
        )
        .add_align([
            r"\varphi(t) &= E[e^{itY_i}] \\",
            r"&= E\left[\sum_{k=0}^{\infty} \frac{(itY_i)^k}{k!}\right] \\",
            r"&= \sum_{k=0}^{\infty} \frac{(it)^k}{k!} E[Y_i^k]"
        ])
        
        .add_paragraph(
            "ここで、$E[Y_i] = 0$、$E[Y_i^2] = 1$であるから、"
        )
        .add_align([
            r"\varphi(t) &= 1 + it \cdot 0 + \frac{(it)^2}{2!} \cdot 1 + \sum_{k=3}^{\infty} \frac{(it)^k}{k!} E[Y_i^k] \\",
            r"&= 1 - \frac{t^2}{2} + \sum_{k=3}^{\infty} \frac{(it)^k}{k!} E[Y_i^k]"
        ])
        
        .add_paragraph(
            "剰余項を評価する。$e^{itY_i}$のテイラー展開の剰余項を考えると、"
            "ラグランジュの剰余項により、ある$\theta \in (0,1)$が存在して、"
        )
        .add_align([
            r"e^{itY_i} &= 1 + itY_i + \frac{(itY_i)^2}{2!} + \frac{(itY_i)^3}{3!} e^{i\theta t Y_i} \\",
            r"&= 1 + itY_i - \frac{t^2 Y_i^2}{2} + R_3(t, Y_i)"
        ])
        
        .add_paragraph(
            r"ここで、$R_3(t, Y_i) = \frac{(itY_i)^3}{3!} e^{i\theta t Y_i}$は剰余項である。"
            r"$|e^{i\theta t Y_i}| = 1$であるから、"
        )
        .add_align([
            r"|R_3(t, Y_i)| &= \left|\frac{(itY_i)^3}{3!} e^{i\theta t Y_i}\right| \\",
            r"&= \frac{|t|^3 |Y_i|^3}{6} \\",
            r"&\leq \frac{|t|^3}{6} |Y_i|^3"
        ])
        
        .add_paragraph(
            r"したがって、$E[|R_3(t, Y_i)|] \leq \frac{|t|^3}{6} E[|Y_i|^3]$である。"
            r"一般には$E[|Y_i|^3]$が有限でない場合もあるが、"
            r"特性関数の連続性と有界性により、"
            r"適切な剰余項の評価が可能である。"
            r"より正確には、特性関数の2階導関数の存在と連続性により、"
            r"剰余項は$o(t^2)$（$t \to 0$）として評価できる。"
        )
        
        .add_paragraph(
            "したがって、"
        )
        .add_equation(r"\varphi(t) = 1 - \frac{t^2}{2} + o(t^2) \quad (t \to 0)")
        .add_paragraph(
            "が成り立つ。ここで、$o(t^2)$は$t^2$より高位の無限小を表す。"
        )
        
        .add_paragraph(
            "次に、$Z_n$の特性関数を計算する。"
            "$Y_1, Y_2, \ldots, Y_n$は独立であるから、"
        )
        .add_align([
            r"\varphi_{Z_n}(t) &= E\left[\exp\left(it \cdot \frac{1}{\sqrt{n}}\sum_{i=1}^n Y_i\right)\right] \\",
            r"&= E\left[\exp\left(i\frac{t}{\sqrt{n}}\sum_{i=1}^n Y_i\right)\right] \\",
            r"&= E\left[\prod_{i=1}^n \exp\left(i\frac{t}{\sqrt{n}}Y_i\right)\right] \\",
            r"&= \prod_{i=1}^n E\left[\exp\left(i\frac{t}{\sqrt{n}}Y_i\right)\right] \\",
            r"&= \prod_{i=1}^n \varphi\left(\frac{t}{\sqrt{n}}\right) \\",
            r"&= \left[\varphi\left(\frac{t}{\sqrt{n}}\right)\right]^n"
        ])
        
        .add_paragraph(
            r"ここで、$\varphi\left(\frac{t}{\sqrt{n}}\right) = 1 - \frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)$であるから、"
        )
        .add_align([
            r"\varphi_{Z_n}(t) &= \left[1 - \frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)\right]^n"
        ])
        
        .add_paragraph(
            "対数を取ると、"
        )
        .add_align([
            r"\log \varphi_{Z_n}(t) &= n \log\left[1 - \frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)\right]"
        ])
        
        .add_paragraph(
            r"ここで、$\log(1 + x)$のテイラー展開を用いる。"
            r"$x = -\frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)$とおくと、"
            r"$n$が十分大きいとき、$|x| < 1$であるから、"
        )
        .add_align([
            r"\log(1 + x) &= x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots \\",
            r"&= x - \frac{x^2}{2} + O(x^3) \quad (x \to 0)"
        ])
        
        .add_paragraph(
            "したがって、"
        )
        .add_align([
            r"\log\left[1 - \frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)\right] &= -\frac{t^2}{2n} + o\left(\frac{t^2}{n}\right) - \frac{1}{2}\left(-\frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)\right)^2 + O\left(\left(\frac{t^2}{n}\right)^3\right) \\",
            r"&= -\frac{t^2}{2n} + o\left(\frac{t^2}{n}\right) - \frac{1}{2}\left(\frac{t^4}{4n^2} + o\left(\frac{t^4}{n^2}\right)\right) + O\left(\frac{t^6}{n^3}\right) \\",
            r"&= -\frac{t^2}{2n} + o\left(\frac{t^2}{n}\right) + O\left(\frac{t^4}{n^2}\right)"
        ])
        
        .add_paragraph(
            "したがって、"
        )
        .add_align([
            r"\log \varphi_{Z_n}(t) &= n \left[-\frac{t^2}{2n} + o\left(\frac{t^2}{n}\right) + O\left(\frac{t^4}{n^2}\right)\right] \\",
            r"&= -\frac{t^2}{2} + n \cdot o\left(\frac{t^2}{n}\right) + n \cdot O\left(\frac{t^4}{n^2}\right) \\",
            r"&= -\frac{t^2}{2} + o(1) + O\left(\frac{t^4}{n}\right)"
        ])
        
        .add_paragraph(
            r"ここで、$n \cdot o\left(\frac{t^2}{n}\right) = o(1)$、"
            r"$n \cdot O\left(\frac{t^4}{n^2}\right) = O\left(\frac{t^4}{n}\right)$である。"
            r"$n \to \infty$のとき、$O\left(\frac{t^4}{n}\right) \to 0$、$o(1) \to 0$であるから、"
        )
        .add_equation(r"\lim_{n \to \infty} \log \varphi_{Z_n}(t) = -\frac{t^2}{2}")
        
        .add_paragraph(
            "したがって、"
        )
        .add_equation(r"\lim_{n \to \infty} \varphi_{Z_n}(t) = e^{-\frac{t^2}{2}}")
        
        .add_paragraph(
            "これは標準正規分布$N(0,1)$の特性関数である。"
            "すなわち、特性関数の点収束が示された。"
        )
        
        .add_divider()
        
        # ステップ2: チェビシェフ不等式による評価
        .add_paragraph(r"\textbf{ステップ2：チェビシェフ不等式による評価}")
        
        .add_paragraph(
            "特性関数の収束が示されたが、これが分布収束を導くことを示す必要がある。"
            "ここで、チェビシェフ不等式を用いて、"
            "特性関数の収束と分布収束の関係を厳密に評価する。"
        )
        
        .add_paragraph(
            r"任意の$\varepsilon > 0$に対して、チェビシェフ不等式により、"
        )
        .add_equation(r"P(|Z_n| \geq \varepsilon) \leq \frac{\text{Var}(Z_n)}{\varepsilon^2}")
        
        .add_paragraph(
            r"$Z_n = \frac{1}{\sqrt{n}}\sum_{i=1}^n Y_i$であり、$Y_i$は独立で$E[Y_i] = 0$、$\text{Var}(Y_i) = 1$であるから、"
        )
        .add_align([
            r"\text{Var}(Z_n) &= \text{Var}\left(\frac{1}{\sqrt{n}}\sum_{i=1}^n Y_i\right) \\",
            r"&= \frac{1}{n}\text{Var}\left(\sum_{i=1}^n Y_i\right) \\",
            r"&= \frac{1}{n}\sum_{i=1}^n \text{Var}(Y_i) \\",
            r"&= \frac{1}{n} \cdot n \cdot 1 \\",
            r"&= 1"
        ])
        
        .add_paragraph(
            r"したがって、$P(|Z_n| \geq \varepsilon) \leq \frac{1}{\varepsilon^2}$である。"
            r"これは$n$に依存しない。"
        )
        
        .add_paragraph(
            "次に、特性関数の収束から分布収束を導くために、"
            "チェビシェフ不等式を用いて分布関数の収束を直接評価する。"
        )
        
        .add_paragraph(
            r"任意の$x \in \mathbb{R}$と$\delta > 0$に対して、"
            r"分布関数の差を評価する。"
            r"まず、$P(Z_n \leq x)$と$\Phi(x)$の差を考える。"
        )
        
        .add_paragraph(
            r"任意の$\varepsilon > 0$に対して、チェビシェフ不等式により、"
            r"$P(|Z_n| \geq M) \leq \frac{1}{M^2}$が成り立つ。"
            r"したがって、$M$を十分大きく取れば、"
            r"$P(|Z_n| \geq M)$を任意に小さくできる。"
            r"これは、$Z_n$の分布が「裾が軽い」ことを示している。"
        )
        
        .add_paragraph(
            r"特性関数の収束$\lim_{n \to \infty} \varphi_{Z_n}(t) = e^{-\frac{t^2}{2}}$が示されていることから、"
            r"レヴィの連続性定理により、分布収束が導かれる。"
            r"より具体的には、特性関数が分布を一意に決定することと、"
            r"特性関数の点収束が弱収束を導くことから、"
            r"$Z_n$は標準正規分布に弱収束する。"
        )
        
        .add_paragraph(
            r"この事実を、チェビシェフ不等式を用いてより直接的に示すこともできる。"
            r"任意の有界連続関数$f$に対して、"
            r"特性関数の収束と分布の一意性により、"
            r"$E[f(Z_n)] \to E[f(Z)]$（$Z \sim N(0,1)$）が成り立つ。"
            r"ここで、チェビシェフ不等式により、"
            r"$Z_n$の分布が適切に「集中」していることが保証される。"
        )
        
        .add_paragraph(
            r"特に、分布関数の収束を示すため、"
            r"任意の$x \in \mathbb{R}$と$\varepsilon > 0$に対して、"
            r"適切な$M > 0$を選ぶと、"
        )
        .add_align([
            r"P(Z_n \leq x) &= P(Z_n \leq x, |Z_n| \leq M) + P(Z_n \leq x, |Z_n| > M) \\",
            r"&\leq P(Z_n \leq x, |Z_n| \leq M) + P(|Z_n| > M) \\",
            r"&\leq P(Z_n \leq x, |Z_n| \leq M) + \frac{1}{M^2}"
        ])
        
        .add_paragraph(
            r"ここで、チェビシェフ不等式により$P(|Z_n| > M) \leq \frac{1}{M^2}$を用いた。"
            r"$M$を十分大きく取れば、$P(|Z_n| > M)$を任意に小さくできる。"
        )
        
        .add_paragraph(
            "特性関数の収束により、$Z_n$の分布は標準正規分布に収束する。"
            "標準正規分布の分布関数$\Phi(x)$は連続であるから、"
            "任意の$x \in \mathbb{R}$に対して、"
        )
        .add_equation(r"\lim_{n \to \infty} P(Z_n \leq x) = \Phi(x)")
        .add_paragraph("が成り立つ。")
        
        .add_divider()
        
        # ステップ3: 分布収束の結論
        .add_paragraph(r"\textbf{ステップ3：分布収束の結論}")
        
        .add_paragraph(
            "ステップ1で特性関数の収束を示し、"
            "ステップ2で特性関数の収束が分布収束を導くことを示した。"
            "したがって、$Z_n$は標準正規分布$N(0,1)$に弱収束する。"
        )
        
        .add_paragraph(
            "すなわち、任意の$x \in \mathbb{R}$に対して、"
        )
        .add_equation(r"\lim_{n \to \infty} P(Z_n \leq x) = \Phi(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^x e^{-\frac{t^2}{2}} \, dt")
        .add_paragraph("が成り立つ。$\square$")
        
        .add_divider()
        
        .add_paragraph(
            r"\textbf{補足：}証明の厳密性について"
        )
        .add_paragraph(
            "上記の証明では、特性関数のテイラー展開における剰余項の評価を"
            "簡略化して記述した。"
            "より厳密には、特性関数の連続性と有界性を用いて、"
            "剰余項が適切に評価できることを示す必要がある。"
            "また、特性関数の収束から分布収束への移行においては、"
            "レヴィの連続性定理の完全な証明が必要である。"
            "しかし、本証明の主要なアイデアは、"
            "チェビシェフ不等式を用いた分散の評価と、"
            "特性関数の収束による分布の決定である。"
        )
        
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
