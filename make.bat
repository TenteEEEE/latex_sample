REM Thesis compile start
move .\tex\main_thesis.tex .\
pandoc .\src\test.md -o test.tex
python .\src\mystyle.py test.tex
latexmk -pdfdvi main_thesis.tex
latexmk -c main_thesis.tex
del main_thesis.dvi
del main_thesis.synctex.gz
REM Abst compile start
move .\tex\main_abst.tex .\
pandoc .\src\abst.md -o abst.tex
python .\src\mystyle.py abst.tex
latexmk -pdfdvi main_abst.tex
latexmk -c main_abst.tex
del main_abst.dvi
del main_abst.synctex.gz
move *.tex .\tex\
