:loop

if "%~1" == "" goto end
pdfcrop %1 %~dpn1_bb.pdf
echo %1

shift

goto loop

:end
