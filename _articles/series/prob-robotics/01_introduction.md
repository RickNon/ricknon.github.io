---
title: "移動ロボットと確率ロボティクス・SLAM"
description: "移動ロボットが観測・推定・計画・制御を通して動く仕組みの全体像を整理します."
date: 2026-09-09
series_id: prob-robotics
order: 1
math: true
notebook: null
---

## この記事で学ぶこと

目的

## 確認用のPythonコード

一定の速度で直進したときの位置を計算

```python
# Update the position using a constant velocity.
position = 0.0
velocity = 0.5
dt = 0.1

position += velocity * dt

print(position)
```

実行結果は `0.05` になるはず
