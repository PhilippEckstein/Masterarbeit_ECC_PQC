$out_dir = 'build';
$aux_dir = 'build';

$pdf_mode = 1;

$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 %O %S';
$biber = 'biber --input-directory=.. --output-directory=build %O %B';