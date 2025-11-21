"""
LaTeXコードを生成するレンダラー
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.document import Document


class LaTeXRenderer:
    """LaTeXコードを生成するレンダラー"""
    
    def render_document(self, document: 'Document') -> str:
        """ドキュメント全体をLaTeXコードに変換"""
        latex = []
        
        # プリアンブル（余白設定、行間設定、フォントファイル情報を渡す）
        latex.append(document.preamble_manager.generate_preamble(
            margins=document.margins,
            line_spacing=document.line_spacing,
            font_file=document.font_file,
            font_name=document.font_name
        ))
        latex.append("\n")
        
        # ドキュメント開始
        latex.append("\\begin{document}\n")
        
        # フォントファイルが指定されていない場合のみCJK環境を使用
        if document.font_file is None:
            # フォント設定を反映（デフォルト: min=明朝体, goth=ゴシック体）
            latex.append(f"\\begin{{CJK}}{{UTF8}}{{{document.font}}}\n")
        
        # タイトル（titleが設定されている場合のみ）
        title_content = self._render_title(document)
        if title_content:
            latex.append(title_content)
        
        # アブストラクト
        if document.abstract:
            latex.append("\\begin{abstract}\n")
            latex.append(f"{document.abstract}\n")
            latex.append("\\end{abstract}\n\n")
        
        # コンテンツ
        for element in document.content:
            latex.append(element.to_latex())
            latex.append("\n")
        
        # ドキュメント終了
        if document.font_file is None:
            latex.append("\\end{CJK}\n")
        latex.append("\\end{document}\n")
        
        return "".join(latex)
    
    def _render_title(self, document: 'Document') -> str:
        # titleがNoneまたは空文字列の場合は何も表示しない
        if not document.title:
            return ""
        
        result = "\\begin{center}\n"
        result += f"{{\\Large\\bfseries {document.title} }}\\\\[1em]\n"
        if document.author:
            result += f"{document.author} \\\\[0.5em]\n"
        if document.date:
            result += f"{document.date}\n"
        elif document.author:
            result += "\\today\n"
        result += "\\end{center}\n"
        result += "\\vspace{2em}\n\n"
        return result

