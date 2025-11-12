#!/usr/bin/env perl

# Force latexmk to use LuaLaTeX to make PDF
$pdf_mode = 4;  # 4 = lualatex, 5 = xelatex, 1 = pdflatex

$latex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
$max_repeat = 5;

# Quiet some noise while keeping errors
$silent = 0;

# Clean up extra junk files if -c is used
@clean_ext = (@clean_ext, 'synctex.gz', 'run.xml', 'nav', 'snm');


