---
title: "凸最適化とは"
description: "凸最適化とは何か，なぜ凸だと扱いやすいか，概要をまとめます．"
date: 2026-09-20
series_id: convex-optimization
order: 1
math: true
toc: true
notebook: null
published: true
---

## この記事の概要
今回は，最適化とは何かを理解し，なぜ凸だと最適化が扱いやすいのか，
コンセプトをまとめます．
ここではイメージをつかむことを目的としており，数式や理論の詳細は後続の記事で扱います．

## 1.1 最適化問題とは何か

最適化問題とは，目的関数の値を最小または最大にする変数を求める問題であり，制約がある場合はその制約範囲内で最も良い解を見つける問題のこと．

一般的に，最適化問題は次のように表される．

$$
\begin{aligned}
    \underset{x}{\operatorname{minimize}} \quad & f_0(x) \\
    \text{subject to} \quad & f_i(x) \le 0, \qquad i=1,\ldots,m, \\
    & h_j(x)=0, \qquad j=1,\ldots,p.
\end{aligned}
$$

ここで，$$x$$は **最適化変数 (optimization variable)**，
$$f_0(x)$$は **目的関数 (objective function)** と呼ばれる．

また，$$f_i(x)$$や$$h_j(x)$$といった**制約関数 (constraint function)**で表される制約を満たす点の集合を，**実行可能領域 (feasible set)**と呼ぶ．

最適化問題は簡単なイメージとして，実行可能領域内の任意の点のうち，
目的地に最も近い点を見つける問題と考えることができる．

最適化問題の解は **最適解 (optimal solution)** と呼ばれ，
一般的には $$x^*$$で表される．
また，そのときの目的関数値は **最適値 (optimal value)** と呼ばれ，$$f_0(x^*)$$ や $$p^*$$で表される．

例えば，目的関数がある目的地への距離だとしたら，
最適解は実行可能領域の中で目的地に最も近い点となる．

<figure class="article-animation">
  <video autoplay loop muted playsinline preload="metadata">
    <source
      src="{{ 'assets/videos/blog/series/convex-optimization/01/01.mp4' | relative_url }}"
      type="video/mp4">
  </video>
  <figcaption>
    実行可能領域の中で目的地に最も近い点を見つける問題とした場合のイメージ
  </figcaption>
</figure>

## 1.2 制約を領域として見る

$$f_i(x) \le 0$$ や $$h_j(x)=0$$といった制約は，実行可能領域を決定する．
2変数でイメージすると，高校数学で学ぶような曲線や直線で囲まれた領域が実行可能領域となる．

例えば，

$$ 
    x_1 \geq 0, \ x_2 \geq 0, \ x_1 + x_2 \leq 4
$$

というような制約は，

$$
    \mathcal{F} = \{(x_1, x_2) \in \mathbb{R}^2 \mid x_1 \geq 0, x_2 \geq 0, x_1 + x_2 \leq 4\}
$$

という三角形の領域を表すことになる．


<figure class="article-animation">
  <video autoplay loop muted playsinline preload="metadata">
    <source
      src="{{ 'assets/videos/blog/series/convex-optimization/01/02.mp4' | relative_url }}"
      type="video/mp4">
  </video>
  <figcaption>
    2変数の制約による実行可能領域の例
  </figcaption>
</figure>

これは変数や次元が増えても同じ．

また，等式の制約は，
その制約を満たす点の集合が，直線や平面などの低次元の部分空間となることを意味する．

## 1.3 目的関数の捉え方

次に，目的関数を数式で考える．
例えば，1.1でイメージした目的地への距離を表す目的関数は，

$$
    f_0(x) = \|x - x_{\text{goal}}\|_2^2
$$

で表せる．そして，この目的関数の値が一定の値 $$c$$ を取る場合，

$$
    f_0(x) = \|x - x_{\text{goal}}\|_2^2 = c
$$

なので，これは $$x_{\text{goal}}$$ を中心とする半径 $$\sqrt{c}$$ の円を表すことになる．

このような目的関数の値が一定の点の集合は **等高線 (level set)** で表すことができる．

このことから，最適化は「実行可能領域内で，より良い等高線に到達できる点を探す問題」と捉えることもできる．

今回の例ではユークリッド距離を用いた目的関数としているため，
等高線は同心円になる．
しかし，目的関数が変わると等高線の形も変わる．

## 1.4 なぜ凸だと扱いやすいのか

このシリーズでは「凸」最適化を扱うが，
なぜ凸にこだわるのか．

### 凸とは何か

まず，凸とは何か．

数式による定義は後の記事で扱うが，
ここでは，「同じ集合内の2点を結ぶ線分が，その集合内に含まれる」というイメージで捉える．

直感的には凹みや穴がない集合だと考えればよい．

![Convex and nonconvex sets]({{ 'assets\images\blog\series\convex-optimization\01\convex_vs_nonconvex_examples.svg' | relative_url }})

今回の例では集合を二次元的な領域で表しているが，
このような凸領域を表す関数は，凸関数と呼ばれる．

変数が増えても同じことが言えるが，
変数が1つの場合，凸関数は下に凸な二次関数などを表す．
（反対に，一般的な四次関数のように下に凸の部分と上に凸の部分が混在する関数は非凸関数となる．）

### 凸最適化の解はグローバル最適解

なぜ凸最適化が扱いやすいのか．
それは，凸最適化問題では局所最適解と大域最適解が一致するためである．

例えば，最適化を1変数の関数上で行うことを考えてみる．
曲線で描かれる関数上の点のうち，最も低い点が最適解となる．

最も低い点を探すには，まず関数上の点を適当に選び，
その点より低い点がある方向へ移動することを繰り返せばよい．

例えば，左右から1つずつ関数上の点を選び，この作業をしてみる．
非凸の四次関数と，凸の二次関数でこれを行った場合を比較すると，
四次関数では片方の点が全体では最適ではない谷に留まってしまう．

このような局所的に見れば最適な点を局所最適点というが，
非凸関数では局所最適点と大域最適点が異なる場合がある．
一方で，凸関数では，最適な方向に谷は一つしか存在しえないため，
局所最適点と大域最適点が一致する．

<figure class="article-animation">
  <video autoplay loop muted playsinline preload="metadata">
    <source
      src="{{ 'assets/videos/blog/series/convex-optimization/01/03.mp4' | relative_url }}"
      type="video/mp4">
  </video>
  <figcaption>
    非凸問題では局所最適解と大域最適解が異なる場合がある一方，
    凸最適化問題では局所最適解と大域最適解が一致する．
  </figcaption>
</figure>

このように，局所最適であっても全体の最適であることが保証されるため，
凸最適化は解きやすく，広く好まれて扱われている．

## 1.6 最も代表的な二つの凸最適化
参考文献（Boyd, Convex Optimization, Cambridge University Press, 2004）では，凸最適化の中でも特に代表的な二つの凸最適化問題として，
最小二乗問題（Least squares）と，線形計画問題（Linear programming）を扱っている．

### Least squares
最小二乗問題は，観測データとモデルの差の二乗和を最小化する問題である．

$$
    \operatorname{minimize} \quad f_0(x) = \|Ax - b\|_2^2
    = \Sigma_{i=1}^{k} (a_i^Tx - b_i)^2
$$

### Linear programming
線形計画問題は，目的関数と制約がすべて線形（一次式）で表される最適化問題である．

$$
    \begin{aligned}
        \underset{x}{\operatorname{minimize}} \quad & c^Tx \\
        \text{subject to} \quad & a_i^Tx \le b_i, \ i=1,\ldots,m, \\
    \end{aligned}
$$

## 1.7 このシリーズで扱う共通の最適化問題

この記事シリーズでは，

$$
\begin{aligned}
    \underset{x}{\operatorname{minimize}} \quad & f_0(x) \\
    \text{subject to} \quad & a_i^Tx \le b_i, \ i=1,\ldots,m, \\
\end{aligned}
$$

を共通の最適化問題の例として扱う．

今後は，
- 第2回：$$a_i^Tx \le b_i$$
- 第3回：$$\underset{x}{\operatorname{minimize}} \quad f_0(x)$$
- 第4回：問題全体
- 第5回：最適になる条件を別の形で表す
というように，同じ問題を異なる視点から見て理解を深めていく．

基本的には参考文献（Boyd, Convex Optimization, Cambridge University Press, 2004）に沿う．

なお，参考文献では，凸最適化の問題を一般に以下のように定式化している．

$$
\begin{aligned}
    \operatorname{minimize} \quad & f_0(x) \\
    \text{subject to} \quad & f_i(x) \le b_i, \qquad i=1,\ldots,m
\end{aligned}
$$

## 1.8 まとめ

- 最適化は目的関数を最小または最大にする変数を求める問題である．
- 制約を満たす点の集合をfeasible setとして幾何学的に見ることができる．
- 一般の非凸問題ではlocal optimumとglobal optimumが異なる可能性がある．
- 凸最適化ではすべてのlocal optimumがglobal optimumである．
