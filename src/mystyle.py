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

text = text.replace('にゃーん', 'まだ十分に検討されておらず，今後研究が必要な課題である')

# けものフレンズのじかんだよ！
text = text.replace('フレンズなんだね！', '関係がある．')
text = text.replace('なにこれー？', 'まだ知られていない．')
text = text.replace('フレンズ？', '関係性が確かめられていない．')
text = text.replace('フレンズ！', '関係性が確かめられた．')
text = text.replace('をみてみてー！', 'に示す．')
text = text.replace('すごーい！', '大幅に改善されている．')
text = text.replace('たのしー！', '非常に興味深い．')
text = text.replace('えらいね！', '有効であることが確かめられた．')
text = text.replace('たいへーん！', '課題として挙げられる．')
text = text.replace('してね！', 'する．')
text = text.replace('ね！', 'である．')
text = text.replace('なんだ！', 'である．')
text = text.replace('んだ！', '．')
text = text.replace('よ！', '．')
text = text.replace('よね？', '．')
text = text.replace('でも，', 'しかし，')
text = text.replace('いて，', 'おり，')
text = text.replace('だから，', 'よって，')
text = text.replace('から，', 'ため，')
text = text.replace('けど', 'が')
text = text.replace('ごはん！', '結論である．')
text = text.replace('としょかん', '参考文献')
text = text.replace('！', '．')
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
label_figure = r'Figure:.*'
label_page = r'Page:.*'
include_graphic = r'\\includegraphics.*';
fig_begin = r'\\begin{figure}.*'
fig_end = '\\end{figure}'
tab2figure = False
add_page = False
for i in range(len(line_text)):
    # print(line_text[i])
    line_text[i] += '\n'
    # detect table to figure
    if re.match(label_figure, line_text[i]) is not None:
        tab2figure = True
        caption = '\\caption{' + line_text[i].replace('Figure:', '') + '}'
        caption = caption.replace('\n','')
        line_text[i] = ''
    # detect number of page
    if re.match(label_page, line_text[i]) is not None:
        add_page = True
        num_page = int(line_text[i].replace('Page:',''));
        line_text[i] = ''
    # detect figure begin
    if re.match(fig_begin, line_text[i]) is not None and add_page:
        for j in range(i+1, len(line_text)):
            # detect includegraphic
            if re.match(include_graphic, line_text[j]) is not None:
                dir_figure = line_text[j].replace('\\includegraphics[','');
                line_text[j] = '\\includegraphics[page=' + str(num_page) + ', ' + dir_figure
                add_page = False        
                break
    # detect table begin
    if re.match(tab_begin, line_text[i]) is not None:
        if tab2figure:
            line_text[i] = '\\begin{figure}[ht]'
        for j in range(i+1, len(line_text)):
            # detect includegraphic
            if re.match(include_graphic, line_text[j]) is not None:
                if add_page:
                    dir_figure = line_text[j].replace('\\includegraphics[','');
                    line_text[j] = '\\includegraphics[page=' + str(num_page) + ', ' + dir_figure
                    num_page += 1
            # detect table end
            if re.match(tab_end, line_text[j]) is not None:
                if tab2figure:
                    line_text[j-1] = caption
                    line_text[j] = fig_end
                add_page = False
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
