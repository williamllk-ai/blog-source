---
title: "【AI×线性代数】QR分解的原理与两种实现"
date: 2026-05-01 14:54:51
tags:
  - "AI_Basics"
  - "LA"
---
# 深入浅出矩阵分解：QR 分解的几何意义、数学证明与两种实用算法推导实现

> 导读：本文深入探讨了矩阵的 QR 分解。从欧氏空间中 Gram-Schmidt 正交化的几何本源出发，逐步推导出矩阵形式的分解过程，并详细剖析了基于 Householder 镜像变换和 Givens 旋转变换的算法实现方案及其数学原理。

在[《深入浅出矩阵分解：LU分解 与 Cholesky分解》](https://williamllk-ai.github.io/2026/04/04/LU-Decomposition-and-Cholesky-Decomposition/)一文中，我们探讨了基于高斯消元的矩阵分解方法。然而，在数值计算中（尤其是求解最小二乘问题或特征值问题时），我们往往追求更高的**数值稳定性**。**QR 分解** 正是基于这一需求而诞生的强大工具。它将一个矩阵分解为一个正交矩阵 $Q$ 和一个上三角矩阵 $R$ 。本文将从几何直觉出发，揭示其背后的数学奥秘。

---
## 1. 来源：Gram-Schmidt 正交化

QR分解的本质思想，其实源自线性代数中的**Gram-Schmidt（施密特）正交化方法**。

### 1.1 几何解释与推导

设 $\alpha_{1},\alpha_{2},\ldots,\alpha_{m}$ 是欧氏空间中的一组线性无关向量。我们的目标是寻找一组两两正交的向量 $b_{1},b_{2},\ldots,b_{m}$ ，它们能张成与原向量组相同的子空间。

根据投影的几何意义：

1.  **第一个基向量**：我们直接选取 $b_{1} = \alpha_{1}$ 。
2.  **第二个基向量**：我们从 $\alpha_{2}$ 中减去它在 $b_{1}$ 上的投影分量 $c_{2}$ 。  
    投影向量 $c_{2} = \frac{(\alpha_{2},b_{1})}{||b_{1}||^{2}}b_{1} = \frac{(\alpha_{2},b_{1})}{(b_{1},b_{1})}b_{1}$  
    则 $b_{2} = \alpha_{2} - c_{2}$ 。
3.  **第三个基向量**：同理，从 $\alpha_{3}$ 中减去它在 $b_{1}$ 和 $b_{2}$ 上的投影（由三垂线定理，这两个投影是相互独立的）。  
    $b_{3} = \alpha_{3} - \frac{(\alpha_{3},b_{1})}{(b_{1},b_{1})}b_{1} - \frac{(\alpha_{3},b_{2})}{(b_{2},b_{2})}b_{2}$

以此类推，对于第 $m$ 个向量：

$$b_{m} = \alpha_{m} - \sum\limits_{i = 1}^{m - 1}\frac{(\alpha_{m},b_{i})}{(b_{i},b_{i})}b_{i}$$

最后，对这组正交向量进行**单位化**，令 $\eta_{i} = \frac{b_{i}}{|b_{i}|}$ ，即可得到一组标准正交基 $\eta_{1},\eta_{2},\ldots,\eta_{m}$ 。

### 1.2 转化为矩阵的 QR 分解形式

如果我们把上述过程反转过来，用新生成的标准正交基 $\eta_{i}$ 来表示原来的向量 $\alpha_{i}$ ：

$$\begin{matrix}
\alpha_{1} & {= |b_{1}|\eta_{1}} \\
\alpha_{2} & {= (\alpha_{2},\eta_{1})\eta_{1} + |b_{2}|\eta_{2}} \\
 & {\ldots}
\end{matrix}$$

将其写成矩阵分块的形式：

$$(\alpha_{1},\alpha_{2},\ldots,\alpha_{m}) = (\eta_{1},\eta_{2},\ldots,\eta_{m})\begin{pmatrix}
{|b_{1}|} & {(\alpha_{2},\eta_{1})} & \cdots & {(\alpha_{m},\eta_{1})} \\
0 & {|b_{2}|} & \cdots & \ast \\
 \vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & {|b_{m}|}
\end{pmatrix}$$

令左侧矩阵为 $A$ ，中间的单位正交矩阵为 $Q$ ，右侧的上三角矩阵为 $R$ ，我们就自然地得出了 $A = QR$ 分解的直观雏形。

---
## 2. QR 分解的严格定义与存在唯一性

### 2.1 定义与定理

**定义**：设 $A \in \mathbb{R}^{n \times n}$ (A可以不是方阵，分解成方阵Q和非方阵R的乘积，思路类似)，且 $r(A) = n$ （即 $A$ 满秩）。若 $A = QR$ ，其中 $Q$ 为正交矩阵（ $Q^{T}Q = I$ ）， $R$ 为**对角元大于零**的上三角矩阵，则称此等式为矩阵 $A$ 的 QR 分解。

> **定理**：若方阵 $A$ 可逆，则 $A$ 存在唯一的 QR 分解。

**证明：**  
**存在性：** 由上述计算过程知显然存在。  
**唯一性：**  
假设存在两种分解： $A = Q_{1}R_{1} = Q_{2}R_{2}$ 。  
由于 $A$ 可逆， $R_{1},R_{2}$ 均可逆，等式两边进行移项操作：

$$Q_{2}^{- 1}Q_{1} = R_{2}R_{1}^{- 1}$$

由于 $Q$ 是正交矩阵，其逆等于其转置，故 $Q_{2}^{T}Q_{1}$ 是两个正交矩阵的乘积，必定仍为**正交矩阵**。  
而右侧 $R_{2}R_{1}^{- 1}$ 是两个上三角矩阵的乘积，必定仍为**上三角矩阵**。

一个矩阵既是正交矩阵又是对角元全为正的上三角矩阵，它必然是单位矩阵 $E$ 。  
因此推出 $Q_{1} = Q_{2}$ 且 $R_{1} = R_{2}$ ，得证唯一性。

---
## 3. 进阶算法Ⅰ：Householder 镜像变换（反射）

虽然 Gram-Schmidt 方法在理论上非常优雅，但在计算机浮点运算中，它容易受到舍入误差的累积影响，导致生成的 $Q$ 矩阵不够正交。为此，数值代数中更常使用 **Householder 变换**。

### 3.1 几何意义：镜面反射

在线性空间中，设有一超平面 $U = L(a)^{\bot}$ （法向量为 $a$ ， $L(a)$ 表示由向量 $a$ 张成的空间）。向量 $\gamma$ 关于该超平面的镜面反射像为 $H\gamma$ 。  
通过正交投影推导，镜面上的投影为 $\gamma - \frac{(\gamma,a)}{(a,a)}a$ 。反射像相当于减去两倍的法向分量：

$$H\gamma = \gamma - 2\frac{aa^{T}}{a^{T}a}\gamma = \left( E - 2\frac{aa^{T}}{a^{T}a} \right)\gamma$$

### 3.2 Householder 矩阵的定义与性质

**定义**：设 $u$ 为 $\mathbb{R}^{n}$ 中的单位向量（ $||u|| = 1$ ），矩阵 $H = E - 2uu^{T}$ 称为 Householder 矩阵。

它具有极佳的代数性质：

- **对称性**： $H^{T} = H$
- **正交性**： $H^{T}H = H^{2} = E$ （即它是一个对合矩阵）
- **保长性**：作为一种正交变换，它保持向量的长度不变。

### 3.3 构造 QR 分解的过程

对于矩阵 $A$ ，我们可以构造一系列的 Householder 反射矩阵 $H_{1},H_{2},\ldots$ 。

- 第 1 步：构造 $H_{1}$ ，将 $A$ 的第一列向量 $\alpha_{1}$ 反射到 $e_{1}$ (即坐标轴)的方向上，使得第一列主对角线下方全为 0。
- 第 2 步：构造 $H_{2}$ ，作用于右下角的子矩阵，将第二列的对应部分清零。  
  最终：

$$H_{n - 1}\ldots H_{2}H_{1}A = R$$

由于 $H_{i}$ 是正交对称的，令 $Q = H_{1}H_{2}\ldots H_{n - 1}$ ，即得到 $A = QR$ 。这种方法具有极高的数值稳定性。

### 3.4 Householder QR 分解伪代码

以下为Householder QR分解的伪代码，完整python代码见文末github仓库。

---
**Algorithm 1: Householder QR Decomposition**

---
**Input:** 矩阵 $A \in \mathbb{R}^{m \times n}$  
**Output:** 正交矩阵 $Q \in \mathbb{R}^{m \times m}$ 与上三角矩阵 $R \in \mathbb{R}^{m \times n}$ ，满足 $A = QR$  
**Initialization:** 令 $R\leftarrow A,Q\leftarrow I_{m}$  
**for** $k = 1,2,\ldots,\min(m - 1,n)$ **do**  
  └─ $x\leftarrow R_{k:m,k}$  
  └─ $v\leftarrow x + \text{sgn}(x_{1}) \parallel x \parallel_{2}e_{1}$  
  └─ $u\leftarrow\frac{v}{\parallel v \parallel_{2}}$  
  └─ ${\hat{H}}_{k}\leftarrow I_{m - k + 1} - 2uu^{T}$  
  └─ $H_{k}\leftarrow\begin{pmatrix}
I_{k - 1} & 0 \\
0 & {\hat{H}}_{k}
\end{pmatrix}$  
  └─ $R\leftarrow H_{k}R$  
  └─ $Q\leftarrow QH_{k}^{T}$  
**end for**  
**return** $Q,R$

---
---
## 4. 进阶算法Ⅱ：Givens 旋转变换

不同于 Householder 变换（一次性清零一列），**Givens 变换**是一种更为精细的操作，它通过旋转矩阵一次只消去一个特定位置的非零元素。

### 4.1 Givens 矩阵的形式

Givens 旋转矩阵 $G(i,j,\theta)$ 是一个在第 $i$ 和 $j$ 个坐标构成的二维平面内旋转角度 $\theta$ 的正交矩阵：

$$G(i,j) = \begin{pmatrix}
1 & & & & & & \\
 & \ddots & & & & & \\
 & & c & \cdots & s & & \\
 & & \vdots & \ddots & \vdots & & \\
 & & {- s} & \cdots & c & & \\
 & & & & & \ddots & \\
 & & & & & & 1
\end{pmatrix}$$

其中 $c^{2} + s^{2} = 1$ （代表 $\cos\theta$ 和 $\sin\theta$ ）。

### 4.2 核心思想

若要利用 $x_{i}$ 消去向量 $x$ 中的 $x_{j}$ 分量，只需令：

$$c = \frac{x_{i}}{\sqrt{x_{i}^{2} + x_{j}^{2}}},\quad s = \frac{x_{j}}{\sqrt{x_{i}^{2} + x_{j}^{2}}}$$

通过连续左乘一系列这样的旋转矩阵，我们可以逐点将矩阵主对角线下方的值清零，最终化为上三角矩阵 $R$ 。  
Givens 旋转特别适合用于**稀疏矩阵**的分解，因为它能精准清零而不破坏已经产生的零元素。

### 4.3 Givens QR 分解伪代码

以下为Givens QR分解的伪代码，完整python代码见文末github仓库。

---
**Algorithm 2: Givens QR Decomposition**

---
**Input:** 矩阵 $A \in \mathbb{R}^{m \times n}$  
**Output:** 正交矩阵 $Q \in \mathbb{R}^{m \times m}$ 与上三角矩阵 $R \in \mathbb{R}^{m \times n}$ ，满足 $A = QR$  
**Initialization:** 令 $R\leftarrow A,Q\leftarrow I_{m}$  
**for** $j = 1,2,\ldots,n$ **do**  
  **for** $i = m,m - 1,\ldots,j + 1$ **do**  
    **if** $R_{ij} \neq 0$ **then**  
      └─ $r\leftarrow\sqrt{R_{jj}^{2} + R_{ij}^{2}}$  
      └─ $c\leftarrow\frac{R_{jj}}{r},\quad s\leftarrow\frac{R_{ij}}{r}$  
      └─ $G_{ij}\leftarrow I_{m}$  
      └─ $G_{ij}\begin{bmatrix}
{j,j} & {j,i} \\
{i,j} & {i,i}
\end{bmatrix}\leftarrow\begin{bmatrix}
c & s \\
{- s} & c
\end{bmatrix}$  
      └─ $R\leftarrow G_{ij}R$  
      └─ $Q\leftarrow QG_{ij}^{T}$  
    **end if**  
  **end for**  
**end for**  
**return** $Q,R$

---
---
## 5. Python 实现（项目源码）

关于高斯消元求阶梯形、以及 Householder 和 Givens 两种方法求解 QR 分解的完整 Python 面向对象代码实现（包含详细的边界条件处理与注释），已上传至我的 GitHub 仓库，欢迎 Star 与交流探讨：

👉 **[GitHub 仓库：AI-Linear-Algebra(SJTU)](https://github.com/williamllk-ai/AI-Linear-Algebra)**

也欢迎参观Github个人主页和个人博客，有更多算法和底层逻辑的干货仓库：

👉 **[GitHub Profile：williamllk-ai](https://github.com/williamllk-ai)**

👉 **[Personal Blog：williamllk-ai.github.io](https://williamllk-ai.github.io/)**

---
## 6. 总结

- **Gram-Schmidt 正交化**提供了 QR 分解的最初始的几何与代数直觉。
- **Householder 变换**利用超平面的镜面反射性质，是求解稠密矩阵 QR 分解的主流且稳定的算法。
- **Givens 旋转**利用局部平面的正交旋转，为稀疏矩阵的分解提供了高度灵活的定点清零方案。
- 两种正交变换是常见的代码实现思路。
