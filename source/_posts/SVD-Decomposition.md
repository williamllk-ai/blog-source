---
title: 【AI×线性代数】谱分解与奇异值分解(SVD)的原理与数学证明
date: 2026-05-15 12:10:56
tags: [AI_Basics, LA]
---

# 深入浅出矩阵分解：谱分解与奇异值分解 (SVD) 的几何意义与数学证明

> 导读：在探讨了 LU 分解、Cholesky 分解以及 QR 分解之后，本文将介绍最常见的矩阵分解方法——谱分解与奇异值分解（SVD），其中SVD更是重中之重，其普适性与实用性使得它在数据处理中屡见不鲜。本文从半单矩阵（可对角化）的谱分解谈到任意矩阵的SVD分解，这篇也是《深入浅出矩阵分解》的最后一部分。

## 1. 半单矩阵的谱分解

### 1.1 核心概念：半单矩阵与谱

在研究谱分解前，我们需要引入半单矩阵的概念。**可对角化**的矩阵被称为**半单矩阵（semisimple matrix）**。对于一个矩阵 $A$，它的所有特征值构成的集合被称为 $A$ 的谱，通常记为 $\sigma(A) = \{\lambda_1, \ldots, \lambda_s\}$ 。此外，特征值绝对值中的最大值被称为谱半径，记作 $\rho(A) = \max\{|\lambda_1|, \ldots, |\lambda_s|\}$ 。

### 1.2 谱分解定理及其严格证明

> **定理（谱分解定理）**：设 $A$ 为半单矩阵，则存在唯一的一组主幂等矩阵 $P_1, \ldots, P_s$，使得以下条件成立：
> 1. $A = \sum_{i=1}^s \lambda_i P_i$ （即谱分解公式）
> 2. $\sum_{i=1}^s P_i = I$ 
> 3. $P_i^2 = P_i$ （代表投影变换性质）
> 4. 当 $i \neq j$ 时，$P_i P_j = 0$ 
> 5. $\text{rank}(P_i) = n_i$ （其中 $n_i$ 为对应特征值 $\lambda_i$ 的重数）
> 
> 

**证明：**
**存在性与性质证明**：
这份谱分解定理的证明确实需要更严密的结构。为了匹配你博客的专业深度，我将 $P$ 矩阵的列向量分块定义补充完整，并以简洁直观的方式推导完这五条核心性质。

你可以将以下完善后的证明段落直接替换到你的 Markdown 源码中：

---

### 1.2 谱分解定理及其严格证明

> **定理（谱分解定理）**：设 $A$ 为半单矩阵，则存在唯一的一组主幂等矩阵 $P_1, \ldots, P_s$，使得以下五条性质成立：
> 1. $A = \sum_{i=1}^s \lambda_i P_i$ （谱分解公式）
> 2. $\sum_{i=1}^s P_i = I$ （完备性）
> 3. $P_i^2 = P_i$ （幂等性/投影性）
> 4. 当 $i \neq j$ 时，$P_i P_j = 0$ （正交性）
> 5. $\text{rank}(P_i) = n_i$ （其中 $n_i$ 为特征值 $\lambda_i$ 的代数重数）
> 
> 

**存在性与性质证明：**

由于 $A$ 是半单矩阵，存在可逆矩阵 $P$ 满足 $P^{-1} A P = \Lambda = \text{diag}(\lambda_1 I_{n_1}, \ldots, \lambda_s I_{n_s})$。我们将 $P$ 按列向量分块，将 $P^{-1}$ 按行向量分块：

* 令 $P = (\alpha_{11}, \dots, \alpha_{1n_1}, \dots, \alpha_{s1}, \dots, \alpha_{sn_s})$，其中 $\alpha_{ik}$ 是对应 $\lambda_i$ 的线性无关**右特征向量**。
* 令 $P^{-1} = (\beta_{11}, \dots, \beta_{1n_1}, \dots, \beta_{s1}, \dots, \beta_{sn_s})^T$，其中 $\beta_{ik}^T$ 是对应 $\lambda_i$ 的**左特征向量**（读者可尝试自证）。

根据 $P^{-1}P = I$，可直接得出以下关系：$\beta_{ij}^T \alpha_{kl} = \delta_{ij, kl}$。其中$\delta_{ij, kl}$是Kronecker函数，定义如下：
$$\delta_{ij, kl} = \begin{cases} 
1, & \text{当 } i = k \text{ 且 } j = l \\ 
0, & \text{其他情况（即 } i \neq k \text{ 或 } j \neq l \text{）}
\end{cases}$$
在此基础上，定义主幂等矩阵：


$$P_i = \sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T$$

下证五条性质：

1. （性质1）利用 $A = P \Lambda P^{-1}$ 的分块展开：

$$A = P \begin{pmatrix} \lambda_1 I_{n_1} & & \\ & \ddots & \\ & & \lambda_s I_{n_s} \end{pmatrix} P^{-1} = \sum_{i=1}^s \lambda_i \left( \sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T \right) = \sum_{i=1}^s \lambda_i P_i$$


2. （性质2）由 $I = P P^{-1}$ 展开：

$$I = (\alpha_{11}, \dots, \alpha_{sn_s}) \begin{pmatrix} \beta_{11}^T \\ \vdots \\ \beta_{sn_s}^T \end{pmatrix} = \sum_{i=1}^s \sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T = \sum_{i=1}^s P_i$$


3. （性质3与4）利用 $\beta_{ik}^T \alpha_{jl} = \delta_{ij, kl}$：

$$P_i P_j = \left( \sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T \right) \left( \sum_{l=1}^{n_j} \alpha_{jl} \beta_{jl}^T \right) = \sum_{k=1}^{n_i} \sum_{l=1}^{n_j} \alpha_{ik} (\beta_{ik}^T \alpha_{jl}) \beta_{jl}^T$$


* 若 $i \neq j$，则 $\beta_{ik}^T \alpha_{jl} = 0$，故 $P_i P_j = 0$。
* 若 $i = j$，则只有当 $k=l$ 时内积为 1，故 $P_i^2 = \sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T = P_i$。


4. （性质5）：
首先，考察 $P_i$ 的秩的上限。由 $P_i = \sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T$ 且秩关于矩阵加法有不等式 $\text{rank}(A+B) \le \text{rank}(A) + \text{rank}(B)$，可得：
$$\text{rank}(P_i) = \text{rank}\left(\sum_{k=1}^{n_i} \alpha_{ik} \beta_{ik}^T\right) \le \sum_{k=1}^{n_i} \text{rank}(\alpha_{ik} \beta_{ik}^T) = n_i$$
其次，利用性质 2 中的完备性 $\sum_{i=1}^s P_i = I$。两边同时取秩，并再次应用秩的次可加性：

$$
n = \text{rank}(I) = \text{rank}\left(\sum_{i=1}^s P_i\right) \le \sum_{i=1}^s \text{rank}(P_i)
$$

由于 $A$ 是可对角化，其各特征值重数之和必定等于方阵的维度，即 $\sum_{i=1}^s n_i = n$。综合上述两个不等式，我们得到一个严密的夹逼关系：

$$
n \le \sum_{i=1}^s \text{rank}(P_i) \le \sum_{i=1}^s n_i = n
$$

这意味着 $\sum_{i=1}^s \text{rank}(P_i) = \sum_{i=1}^s n_i$ 必须严格成立。又因为对于每一个 $i$ 都有 $\text{rank}(P_i) \le n_i$，要使其总和相等，唯一的可能是每一项都取到等号。故严格得证：$\text{rank}(P_i) = n_i$。



**唯一性**：

假设存在另一种满足所有性质的分解 $A = \sum_{i=1}^s \lambda_i Q_i$。我们需要证明对于所有的 $i$，都有 $P_i = Q_i$。

首先，根据假设，有：


$$\sum_{k=1}^s \lambda_k P_k = \sum_{k=1}^s \lambda_k Q_k$$


对等式两边同时**右乘**某个 $Q_j$。由于 $Q_k$ 也满足正交性（当 $k \neq j$ 时 $Q_k Q_j = 0$）和幂等性（$Q_j^2 = Q_j$），等式右边所有项均消去，仅剩 $\lambda_j Q_j$：


$$\sum_{k=1}^s \lambda_k P_k Q_j = \lambda_j Q_j \quad \text{--- (1)}$$

接着，对等式 (1) 两边同时**左乘**某个 $P_i$（此时设定 $i \neq j$）。同理，利用 $P_i$ 的正交性（当 $i \neq k$ 时 $P_i P_k = 0$）和幂等性（$P_i^2 = P_i$），等式 (1) 的左边坍缩为 $\lambda_i P_i Q_j$。于是得到：


$$\lambda_i P_i Q_j = \lambda_j P_i Q_j$$


移项可得 $(\lambda_i - \lambda_j) P_i Q_j = 0$。由于 $\lambda_i$ 和 $\lambda_j$ 是不同的特征值（即 $\lambda_i \neq \lambda_j$），故必然有：


$$P_i Q_j = 0 \quad (i \neq j)$$

现在，我们利用性质 2。已知两组分解的主幂等矩阵之和均为单位阵，即 $\sum_{k=1}^s P_k = I = \sum_{k=1}^s Q_k$：
对等式 $I = \sum_{k=1}^s Q_k$ 两边分别**左乘** $P_i$，由于当 $k \neq i$ 时 $P_i Q_k = 0$，展开后可得：


$$P_i = P_i Q_i$$


同理，对等式 $\sum_{k=1}^s P_k = I$ 两边分别**右乘** $Q_i$，由于当 $k \neq i$ 时 $P_k Q_i = 0$，展开后可得：


$$Q_i = P_i Q_i$$

综合上述两个结果，显然有：


$$P_i = Q_i \quad (i = 1, 2, \dots, s)$$


这就严密地证明了符合该五条性质的谱分解是唯一的。

谱分解得证！

### 1.3 几何意义与实对称矩阵的特化

在这个分解过程中，由特征向量性质可知，$\beta_{ij}^T$ 被称为 $A$ 的**左特征向量**，而 $\alpha_{ij}$ 则是**右特征向量** 。
从几何意义上看，谱分解相当于将矩阵 $A$ 拆分成了多个投影向量的和，而特征值 $\lambda_i$ 则描述了在这些特征向量对应方向上的伸缩因子 。
特别地，如果 $A$ 是实对称矩阵，那么存在正交矩阵 $Q$ 使得 $A = Q \Lambda Q^T = \sum_{i=1}^s \lambda_i P_i$ 。此时，$P_i$ 满足对称性（$P_i^T = P_i$），普通的投影变换就升级成了**正交投影** 。
这一过程的几何意义非常直观：先通过 $Q^T$ 进行旋转操作，接着在正交特征向量方向上进行独立的伸缩（由 $\Lambda$ 决定），最后通过 $Q$ 逆旋转复原 。

---

## 2. 奇异值分解 (SVD)

谱分解要求矩阵必须是方阵且可对角化。对于那些不能进行特征值分解的矩阵（例如非方阵或非半单矩阵），我们就需要引入更强大且极其普适的奇异值分解（SVD）。

### 2.1 引入引理

在推导 SVD 之前，我们先明确两个引理（读者自证不难）：

1. $AA^T$ 与 $A^TA$ 这两个矩阵拥有完全相同的非零特征值 。


2. 如果 $\alpha_i$ 是 $A^TA$ 对应于非零特征值 $\lambda_i$ 的单位正交特征向量，那么 $A\alpha_i$ 彼此之间互为正交向量，并且它们都是 $AA^T$ 的特征向量 。



### 2.2 SVD 定理与数学证明

> 
> **定理**：设 $A \in \mathbb{R}^{m \times n}$，且 $\text{rank}(A)=r$，必定存在正交矩阵 $U \in \mathbb{R}^{m \times m}$ 和 $V \in \mathbb{R}^{n \times n}$ 使得 $A = U \Sigma V^T$ 。这是全奇异值分解，其中 $\Sigma$ 为广义对角阵，其对角线上的元素 $\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_r > 0$ 称为矩阵 $A$ 的奇异值 。
> 
> 

**证明：**
根据矩阵性质，$A^TA$ 的非零特征值可以写为 $\sigma_1^2 \ge \sigma_2^2 \ge \cdots \ge \sigma_r^2 > 0$ 。
我们设 $v_1, \ldots, v_n$ 为 $A^TA$ 的一组标准正交特征向量 。
对于 $1 \le i \le r$，我们构造向量 $u_i = \frac{1}{\sigma_i} A v_i$ 。此时计算它们的内积：


$$(u_i, u_j) = u_i^T u_j = \frac{1}{\sigma_i \sigma_j} v_i^T A^T A v_j = \frac{\sigma_j^2}{\sigma_i \sigma_j} v_i^T v_j = \delta_{ij}$$

这说明 $u_i$ 是一组标准正交向量集合。我们将其扩充为 $\mathbb{R}^m$ 空间下的标准正交基，从而构造出正交矩阵 $U$ 。
因为满足等式 $A V = U \Sigma$，等式两边同时右乘 $V^T$（正交矩阵性质），即可得出：$A = U \Sigma V^T$ 。定理得证。

### 2.3 奇异值的四个性质

奇异值在数值计算和分析中极其重要，它具有以下四个核心性质 ：

1. 若矩阵是对称矩阵，其奇异值就是其对应特征值的绝对值 。


2. 矩阵行列式的绝对值等于其所有奇异值的乘积，即 $|\det (A)|= \sigma_1 \sigma_2 \cdots \sigma_n$ 。


3. 最大奇异值的平方 $\sigma_1^2 = \max_{\|x\|=1} x^T A^T A x$，$\sigma_2^2 = \min_{\|x\|=1} x^T A^T A x$ 。


4. 如果方阵 $A$ 可逆，那么 $A^{-1}$ 的奇异值即为原奇异值的倒数反序：$1/\sigma_n, \ldots, 1/\sigma_1$ 。

其中性质3在**范数理论**中也有应用，四个性质读者自证不难。



---

## 3. 极分解与 SVD 的应用

### 3.1 极分解 (Polar Decomposition)

利用 SVD，我们可以引申出另一种具有优美几何意义的分解方法。

> 
> **定理**：设 $A \in \mathbb{R}^{n \times n}$，则必定存在一个正交矩阵 $Q$ 和唯一的一个半正定矩阵 $P$，使得 $A = PQ$ 。这就是矩阵 $A$ 的极分解 。
> 
> 

**证明：**
根据奇异值分解，我们有 $A = U \Sigma V^T$ 。
通过在中间插入 $U^T U = I$，我们可以将其改写为 $A = (U \Sigma U^T)(U V^T)$ 。
此时，我们令 $P = U \Sigma U^T$，显然这是一个半正定对称矩阵 。同时令 $Q = U V^T$，因为 $U$ 和 $V^T$ 都是正交矩阵，它们的乘积 $Q$ 必然也是正交矩阵 。至此极分解证明成立 。

**几何意义**：极分解非常类似于复数系统中的极坐标表示 $re^{i\theta}$ 。公式 $A = PQ$ 意味着线性变换可以被拆解为两步：先通过正交矩阵 $Q$ 进行一次不改变长度的保距旋转，接着通过半正定矩阵 $P$ 沿着一组正交方向进行拉伸 。

### 3.2 SVD 应用

SVD 是数据科学中降维和去噪的底层核心算法。假设我们有一个评分矩阵 $A$，其中行代表不同的被评分物品，列代表不同的评分者 。
根据 SVD，该矩阵可以被分解为多个秩为 1 的矩阵的叠加形式：$A = \sum_{i=1}^r \sigma_i u_i v_i^T$ 。

在这个叠加过程中：

* 第一层 $A(1) = \sigma_1 u_1 v_1^T$ 由最大的奇异值主导，它可能提取出了数据中最核心的特征 。


* 第二层 $A(2) = \sigma_2 u_2 v_2^T$ 则可能提取了第二关键特征，后续以此类推 。


* 在实际应用中，往往伴随大量微小的奇异值，它们代表了数据的随机噪声 。通过**截断奇异值**，我们可以利用少数几个最大的奇异值实现对原矩阵的高精度低秩重构，从而达到过滤噪声和数据降维的目的 。



---

## 4. 总结

* **谱分解**展示了可对角化矩阵可以被拆解为多个投影变换的叠加，为计算矩阵的高次幂和矩阵函数提供了捷径，也可以用来遍历的计算矩阵多项式，例如$e^A$。
* **奇异值分解 (SVD)** 是最普适的矩阵分解法，其构造出的正交基和奇异值在几何变换中对应着空间的正交旋转与伸缩。
* 无论是求矛盾方程组的最小二乘解，还是进行矩阵的低秩近似以实现数据降维，SVD 都是连接纯数学理论与实际数据处理和AI的关键桥梁。

关于线性代数底层逻辑与算法推导的完整代码库及其他资源，已上传至我的 GitHub，欢迎交流探讨：

👉 **[GitHub 仓库：AI-Linear-Algebra(SJTU)](https://github.com/williamllk-ai/AI-Linear-Algebra)**

也欢迎参观Github个人主页和个人博客，有更多CS和数学的博客笔记：

👉 **[GitHub Profile：williamllk-ai](https://github.com/williamllk-ai)**

👉 **[Personal Blog：williamllk-ai.github.io](https://williamllk-ai.github.io/)**