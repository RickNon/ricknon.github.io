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

最適化問題とは，所定の制約を満たす領域の中から，最も良い解を見つける問題のこと．

一般的な最適化問題は次のように表される．

$$
\begin{aligned}
    \underset{x}{\operatorname{minimize}} \quad & f_0(x) \\
    \text{subject to} \quad & f_i(x) \le 0, \qquad i=1,\ldots,m, \\
    & h_j(x)=0, \qquad j=1,\ldots,p.
\end{aligned}
$$

ここで，$$x$$は **最適化変数 (optimization variable)**，
$$f_0(x)$$は **目的関数 (objective function)** と呼ばれる．

また，$$f_i(x)$$や$$h_j(x)$$といった**制約関数 (constraint function)**で表される制約を満たす点の集合を，**実行可能領域 (feasible region)**と呼ぶ．

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
      src="{{ 'assets/videos/convex-optimization/01/01.mp4' | relative_url }}"
      type="video/mp4">
  </video>
  <figcaption>
    実行可能領域の中で目的地に最も近い点を見つける問題とした場合のイメージ
  </figcaption>
</figure>

## 1.2 制約を領域として見る


## 1.3 目的関数の見方


## 1.4 なぜ凸だと扱いやすいのか

### 一般的な最適化

### 凸最適化


## 1.5 凸集合と凸関数


## 1.6 最も代表的な二つの凸最適化


## 1.7 このシリーズで扱う共通の最適化問題


## 1.8 まとめ

