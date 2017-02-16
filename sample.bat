move .\tex\sample.tex .\
pandoc .\src\friends.md -o friends.tex
python .\src\mystyle.py friends.tex
latexmk -pdfdvi sample.tex
latexmk -c sample.tex
del sample.dvi
del sample.synctex.gz
move *.tex .\tex\
