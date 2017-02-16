# section
ここに文章書く
*斜体*
**太字**
***太字斜体***

## subsection
* 箇条書き
  * 箇条書き

### subsubsection
1. 数字の箇条書き
  1. 数字の箇条書き

# 図の貼り方
図\ref{fig:sample}にサンプル図を示す。

![Sample\label{fig:sample}](./fig/sample.png){width=12cm}

## 図を横に並べる

Figure:test2

|||
|:-:|:-:|
|![](./fig/sample.png){width=8cm}|![](./fig/sample.png){width=8cm}|
|(a)|(b)|

# 数式
スクリプトにてalign環境へ変換済み。
文中でも数式$y=ax^2$は使える。

$$
y=ax^2
$$

# 表
表\ref{tab:test}にテスト結果を示す。

Table:テスト結果\label{tab:test}

|たかし|ひろし|
|:-:|:-:|
|67|86|
|72|66|
