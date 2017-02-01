import sys
import re

args = sys.argv
if len(args) != 2:
    print('Please type a input file name')
    exit()
f = open(args[1], 'r', encoding='utf-8')
text = f.read()
# modify parts #############################
text = text.replace('\\begin{figure}', '\\begin{figure}[ht]')

text = text.replace('\\begin{longtable}', '\\begin{table}[ht]\n\n\\centering\n\\begin{tabular}')
text = text.replace('\\end{longtable}', '\\end{tabular}\n\n\\end{table}')
text = text.replace('\\tabularnewline', '\\\\')
text = text.replace('\\endhead', '')

text = text.replace('\\[', '\\begin{align}')
text = text.replace('\\]', '\\end{align}')

text = text.replace('。', '．')
text = text.replace('、', '，')
############################################

# convert to tabular environment ###########
line_text = text.split('\n')
tab_begin = r'\\begin{table}.*'
tab_end = r'\\end{table}.*'
tab_top = r'\\toprule'
tab_mid = r'\\midrule'
tab_bottom = r'\\bottomrule'
tab_firsthead = r'\\endfirsthead'
tab_caption = r'\\caption.*'
tab_figure = r'Figure:.*'
fig_begin = '\\begin{figure}[ht]'
fig_end = '\\end{figure}'
tab2figure = False
for i in range(len(line_text)):
    # print(line_text[i])
    line_text[i] += '\n'
    # detect table to figure
    if re.match(tab_figure, line_text[i]) is not None:
        tab2figure = True
        caption = '\\caption{' + line_text[i].replace('Figure:', '') + '}'
        caption = caption.replace('\n','')
        line_text[i] = ''
    # detect table begin
    if re.match(tab_begin, line_text[i]) is not None:
        if tab2figure:
            line_text[i] = fig_begin
        for j in range(i+1, len(line_text)):
            # detect table end
            if re.match(tab_end, line_text[j]) is not None:
                if tab2figure:
                    line_text[j-1] = caption
                    line_text[j] = fig_end
                break
            # move caption above '\begin{tabular}'
            if re.match(tab_caption, line_text[j]) is not None:
                line_text[i+1] = line_text[j].replace('\\\\', '') # delete \caption'\\'
                line_text[j] = ''
            # delete between toprule and endfirsthead
            if re.match(tab_top, line_text[j]) is not None:
                if tab2figure:
                    line_text[j] = ''
                topruline = j
            if re.match(tab_firsthead, line_text[j]) is not None:
                for deleteline in range(topruline, j+1):
                    line_text[deleteline] = ''
            # delete table line when use figure environment
            if tab2figure:
                if re.match(tab_bottom, line_text[j]) is not None or\
                re.match(tab_mid, line_text[j]) is not None:
                    line_text[j] = ''
        tab2figure = False
#############################################
# for i in range(len(line_text)):
#     print(line_text[i])
f = open(args[1], 'w', encoding='utf-8')
f.writelines(line_text)
f.close()
