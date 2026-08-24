---
title: SLAM LECTURE 1
date: 2026-01-23 20:55:42
author: williamllk
tags: SLAM
---

# L1自测题-知识补充

## 数学-Gaussian Distribution

### 一维 (正态分布)

$$ p(x) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{(x-\mu)^2}{2\sigma^2}} $$

- $\mu$为期望/均值
- $\sigma$为标准差

### 高维：状态向量为$\boldsymbol{x}$

$$ p(\boldsymbol{x}) = \frac{1}{\sqrt{(2\pi)^N\det(\boldsymbol{\Sigma})}}e^{-\frac{1}{2}(\boldsymbol{x}-\boldsymbol{\mu})^\top\boldsymbol{\Sigma}^{-1}(\boldsymbol{x}-\boldsymbol{\mu})} $$

- $ \boldsymbol{\Sigma} = \mathbb{E}[(\boldsymbol{x}-\boldsymbol{\mu})(\boldsymbol{x}-\boldsymbol{\mu})^\top] $：协方差矩阵（对称、半正定）

- $ D^2 =  (\boldsymbol{x}-\boldsymbol{\mu})^\top\boldsymbol{\Sigma}^{-1}(\boldsymbol{x}-\boldsymbol{\mu}) $：马哈拉诺比斯距离（考虑了不确定性）

## Linux补充

- 安装：``sudo apt install <>``
- 查询：``sudo apt search <>`` 
- 安装地址：

    | 类型 | 位置 |
    |------|------|
    | 可执行程序 | `/usr/bin/` |
    | 系统库 | `/usr/lib/` |
    | 头文件 | `/usr/include/` |
    | 第三方库（Eigen、OpenCV） | `/usr/include/xxx` |
    | 本地手动安装 | `/usr/local/` |

- Vim