---
title: 【AI基础】【线性代数】最小二乘法中正规方程的推导
date: 2026-03-15 15:10:27
author: williamllk
tags: [LA, AI_Basics]
---
# 推导正规方程$A^T A \mathbf{x} = A^T \mathbf{b}$

正规方程的推导可以从两个角度理解：一个是几何上的投影，一个是代数上的求导。下面我们从投影的角度出发，展示如何从最小二乘法的 $A\mathbf{x} = \mathbf{b}$ 得到正规方程 $A^T A \mathbf{x} = A^T \mathbf{b}$。

---

### 1. 问题背景
我们有一个线性系统：
$$
A \mathbf{x} = \mathbf{b}
$$
其中 $A$ 是一个 $m \times n$ 的矩阵（通常 $m > n$），$\mathbf{b}$ 是一个 $m$ 维观测向量，$\mathbf{x}$ 是 $n$ 维未知参数向量。由于方程个数多于未知数个数，方程组通常是**超定**的，没有精确解，即 $\mathbf{b}$ 不在 $A$ 的列空间中。

最小二乘法的目标：寻找一个 $\hat{\mathbf{x}}$，使得 $A\hat{\mathbf{x}}$ 尽可能接近 $\mathbf{b}$，即最小化残差 $\|\mathbf{b} - A\mathbf{x}\|^2_2$（右下角的2是**L2范数**的意思，类似常规意义上的欧氏距离）。

### 2. 投影的几何解释
矩阵 $A$ 的列向量张成一个 $n$ 维子空间，称为**列空间** $\mathcal{C}(A)$。对于任意 $\mathbf{x}$，$A\mathbf{x}$ 就是该空间中的一个向量。

我们希望在这个子空间中找到一点 $\mathbf{p} = A\hat{\mathbf{x}}$，使得它到 $\mathbf{b}$ 的距离最短。根据欧几里得空间中的正交投影定理，这个最短距离点就是 $\mathbf{b}$ 在列空间上的**正交投影**。

记投影为 $\mathbf{p}$，那么残差向量 $\mathbf{r} = \mathbf{b} - \mathbf{p}$ 必须垂直于列空间 $\mathcal{C}(A)$。也就是说，$\mathbf{r}$ 与 $A$ 的每一个列向量都正交。

### 3. 用正交条件推导方程
设 $A$ 的列向量为 $\mathbf{a}_1, \mathbf{a}_2, \dots, \mathbf{a}_n$。正交条件意味着：
$$
\mathbf{a}_j^T (\mathbf{b} - A\hat{\mathbf{x}}) = 0, \quad j = 1,2,\dots,n.
$$
将这 $n$ 个等式合并成矩阵形式：
$$
A^T (\mathbf{b} - A\hat{\mathbf{x}}) = \mathbf{0}.
$$
移项即得：
$$
A^T A \hat{\mathbf{x}} = A^T \mathbf{b}.
$$
这就是**正规方程**。

### 4. 代数推导（求导）作为印证
也可以从最小化误差平方和的角度推导。定义目标函数：
$$
f(\mathbf{x}) = \| A\mathbf{x} - \mathbf{b} \|^2 = (A\mathbf{x} - \mathbf{b})^T (A\mathbf{x} - \mathbf{b}).
$$
展开：
$$
f(\mathbf{x}) = \mathbf{x}^T A^T A \mathbf{x} - 2 \mathbf{b}^T A \mathbf{x} + \mathbf{b}^T \mathbf{b}.
$$
对 $\mathbf{x}$ 求梯度并令其为零：
$$
\nabla f(\mathbf{x}) = 2 A^T A \mathbf{x} - 2 A^T \mathbf{b} = \mathbf{0},
$$
同样得到 $A^T A \mathbf{x} = A^T \mathbf{b}$。

### 5. 解的存在性与唯一性
正规方程的解 $\hat{\mathbf{x}}$ 就是最小二乘估计。当 $A$ 列满秩时，$A^T A$ 是可逆矩阵，解唯一：
$$
\hat{\mathbf{x}} = (A^T A)^{-1} A^T \mathbf{b}.
$$
此时投影向量 $\mathbf{p} = A \hat{\mathbf{x}} = A (A^T A)^{-1} A^T \mathbf{b}$，而矩阵 $P = A (A^T A)^{-1} A^T$ 就是到列空间上的投影矩阵。

### 总结
从 $A\mathbf{x} = \mathbf{b}$ 出发，利用**残差与列空间正交**这一几何条件，自然导出了正规方程 $A^T A \mathbf{x} = A^T \mathbf{b}$。它将一个无解的方程组转化为一个有唯一解（在列满秩下）的线性方程组，从而得到最优的近似解。