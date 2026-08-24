---
title: SLAM LECTURE 4：李群与李代数
date: 2026-01-27 11:57:59
author: williamllk
tags: SLAM
---

## 4.1 李群与李代数基础

### 4.1.1 群

1. 定义： “封结幺逆”：封闭性（乘法）、结合律、幺元、逆元
    - 一般线性群 GL(n)：n×n可逆矩阵，对乘法构成群
    - 特殊正交群 SO(n)：旋转矩阵群
    - 特殊欧式群 SE(n)：欧式变换群

2. 李群：具有连续（光滑）性质的群，如SO(n)，SE(n)

### 4.1.2 李代数的定义

李代数由一个集合 $\mathbb{V}$、一个数域 $\mathbb{F}$ 和一个二元运算 $[,]$ 组成。如果它们满足以下几条性质，则称 $(\mathbb{V}, \mathbb{F}, [,])$ 为一个李代数，记作 $\mathfrak{g}$。
1. 封闭性 $\quad \forall X, Y \in \mathbb{V}, [X, Y] \in \mathbb{V}$.
2. 双线性 $\quad \forall X, Y, Z \in \mathbb{V}, a, b \in \mathbb{F}$, 有
$$[aX + bY, Z] = a[X, Z] + b[Y, Z], \quad [Z, aX + bY] = a[Z, X] + b[Z, Y].$$

3. 自反性 $\quad \forall X \in \mathbb{V}, [X, X] = 0$.

4. 雅可比等价 $\quad \forall X, Y, Z \in \mathbb{V}, [X, [Y, Z]] + [Z, [X, Y]] + [Y, [Z, X]] = 0$.

二元运算称作**李括号**，表达的是元素的差异。

### 4.1.3 李代数$\mathfrak{so}(3)$

$SO(3)$对应的李代数$\mathfrak{so}(3)$是定义在$\mathbb{R}^3$上的向量，记作$\phi$，每个$\phi$都可生成一个反对称矩阵：

$$\boldsymbol{\Phi}=\phi^\wedge=
\begin{bmatrix}
0 & -\phi_3 & \phi_2 \\
 \\
\phi_3 & 0 & -\phi_1 \\
 \\
-\phi_2 & \phi_1 & 0
\end{bmatrix}\in\mathbb{R}^{3\times3}.$$

在此定义下，两个向量的李括号为：

$$\left[\phi_1,\phi_2\right]=\left(\boldsymbol{\Phi}_1\boldsymbol{\Phi}_2-\boldsymbol{\Phi}_2\boldsymbol{\Phi}_1\right)^\vee.$$

由于三维向量与三位反对称矩阵一一对应，$\mathfrak{so}(3)$的元素视作三维向量或三维反对称矩阵：

$$\mathfrak{so}(3)=\left\{\phi\in\mathbb{R}^3,\boldsymbol{\Phi}=\phi^\wedge\in\mathbb{R}^{3\times3}\right\}.$$

由此，它与$SO(3)$的关系由指数映射给定：

$$R=\exp(\phi^{\wedge}).$$

### 4.1.4 李代数$\mathfrak{se}(3)$

类似地，$SE(3)$的李代数定义如下：

$$\mathfrak{sc}(3)=\left\{\boldsymbol{\xi}=
\begin{bmatrix}
\boldsymbol{\rho} \\
 \\
\boldsymbol{\phi}
\end{bmatrix}\in\mathbb{R}^6,\boldsymbol{\rho}\in\mathbb{R}^3,\boldsymbol{\phi}\in\mathfrak{so}(3),\boldsymbol{\xi}^\wedge=
\begin{bmatrix}
\boldsymbol{\phi}^\wedge & \boldsymbol{\rho} \\
 \\
\boldsymbol{0}^\mathrm{T} & 0
\end{bmatrix}\in\mathbb{R}^{4\times4}\right\}.$$

其中，前三位为平移，记作$\rho$，但含义与变换矩阵不同。此外，对于$\xi$使用的$^\wedge$符号是讲六位向量转换成四维向量，与先前不同。

此处李括号定义为：

$$[\boldsymbol{\xi}_1,\boldsymbol{\xi}_2]=(\boldsymbol{\xi}_1^\wedge\boldsymbol{\xi}_2^\wedge-\boldsymbol{\xi}_2^\wedge\boldsymbol{\xi}_1^\wedge)^\vee.$$

## 4.2 对数与指数映射

![SO(3), SE(3)及其李代数的对应关系](slam4-1.png)

## 4.3 李代数求导与扰动模型   

### 4.3.1 BCH公式及其近似形式

现考察李群上两个矩阵乘法时李代数发生的变化，得到BCH公式。当其中一个$\phi$为小量时，高次可忽略，此时，BCH拥有线性近似表达：

$$\ln\left(\exp\left(\phi_1^\wedge\right)\exp\left(\phi_2^\wedge\right)\right)^\vee\approx
\begin{cases}
J_l(\phi_2)^{-1}\phi_1+\phi_2 & \text{当}\phi_1\text{为小量}, \\
J_r(\phi_1)^{-1}\phi_2+\phi_1 & \text{当}\phi_2\text{为小量}. & 
\end{cases}$$

其中，左乘BCH近似雅可比$\boldsymbol{J}_l$形式为：

$$\boldsymbol{J}_{l}=\boldsymbol{J}=\frac{\sin\theta}{\theta}\boldsymbol{I}+\left(1-\frac{\sin\theta}{\theta}\right)\boldsymbol{aa}^{\mathrm{T}}+\frac{1-\cos\theta}{\theta}\boldsymbol{a}^{\wedge}.$$

其逆为：

$$\boldsymbol{J}_{l}^{-1}=\frac{\theta}{2}\cot\frac{\theta}{2}\boldsymbol{I}+\left(1-\frac{\theta}{2}\cot\frac{\theta}{2}\right)\boldsymbol{aa}^{\mathrm{T}}-\frac{\theta}{2}\boldsymbol{a}^{\wedge}.$$

而右乘雅可比仅需对自变量取负号即可：

$$\boldsymbol{J}_r(\phi)=\boldsymbol{J}_l(-\boldsymbol{\phi}).$$

由以上可得李群乘法与李代数加法之间的关系。

对于旋转$\boldsymbol{R}$及其李代数$\phi$，给它左乘一个微小旋转$\Delta\boldsymbol{R}$，其对应的李代数为$\Delta\phi$。那么，在李群上得到的结果就是$\Delta\boldsymbol{R}\cdot\boldsymbol{R}$，而在李代数上，根据BCH近似，为$J_l^{-1}(\phi)\,\Delta\phi + \phi$。合并起来可以写成：

$$\exp\left(\Delta\phi^{\wedge}\right)\exp\left(\phi^{\wedge}\right)=\exp\left(\left(\phi+J_{l}^{-1}\left(\phi\right)\Delta\phi\right)^{\wedge}\right).$$

反之，在李代数上做加法，可以写成李群上的乘法：

$$\exp\left(\left(\phi+\Delta\phi\right)^{\wedge}\right)=\exp\left(\left(\boldsymbol{J}_{l}\Delta\phi\right)^{\wedge}\right)\exp\left(\boldsymbol{\phi}^{\wedge}\right)=\exp\left(\boldsymbol{\phi}^{\wedge}\right)\exp\left(\left(\boldsymbol{J}_{r}\Delta\phi\right)^{\wedge}\right).$$

同样地，对于$SE(3)$，也有类似的BCH近似：

$$
\begin{aligned}
\exp\left(\Delta\boldsymbol{\xi}^{\wedge}\right)\exp\left(\boldsymbol{\xi}^{\wedge}\right)\approx\exp\left(\left(\mathcal{J}_{l}^{-1}\Delta\boldsymbol{\xi}+\boldsymbol{\xi}\right)^{\wedge}\right), \\
\exp\left(\boldsymbol{\xi}^{\wedge}\right)\exp\left(\Delta\boldsymbol{\xi}^{\wedge}\right)\approx\exp\left(\left(\mathcal{J}_{r}^{-1}\Delta\boldsymbol{\xi}+\boldsymbol{\xi}\right)^{\wedge}\right).
\end{aligned}$$

### 4.3.2 两种求导方法

1. 利用李代数表示姿态，然后根据李代数加法对**李代数求导**：

$$\frac{\partial\left(\boldsymbol{Rp}\right)}{\partial\boldsymbol{\phi}}=\left(-\boldsymbol{Rp}\right)^{\wedge}\boldsymbol{J}_{l}.$$

2. 对李群左乘或右乘**微小扰动**，然后对该**扰动求导**

左扰动模型求导：

$$\begin{aligned}
\frac{\partial\left(Rp\right)}{\partial\varphi} & =\lim_{\varphi\to0}\frac{\exp\left(\varphi^{\wedge}\right)\exp\left(\phi^{\wedge}\right)p-\exp\left(\phi^{\wedge}\right)p}{\varphi} \\
 & =\lim_{\varphi\to0}\frac{\left(\boldsymbol{I}+\boldsymbol{\varphi}^\wedge\right)\exp\left(\boldsymbol{\phi}^\wedge\right)\boldsymbol{p}-\exp\left(\boldsymbol{\phi}^\wedge\right)\boldsymbol{p}}{\varphi} \\
 & =\lim_{\varphi\to0}\frac{\varphi^{\wedge}Rp}{\varphi}=\lim_{\varphi\to0}\frac{-(Rp)^{\wedge}\varphi}{\varphi}=-(Rp)^{\wedge}.
\end{aligned}$$

相比于直接对李代数求导，扰动模型更简洁实用。

## 4.5 相似变换群和李代数

由于单目相机存在尺度不确定性与尺度漂移，需要尺度因子来表示，因此相机坐标系需要经过一个**相似变换**，而非欧式变换：

$$\boldsymbol{p}^{\prime}= \begin{bmatrix} s\boldsymbol{R} & \boldsymbol{t} \\ \\ \boldsymbol{0}^\mathrm{T} & 1 \end{bmatrix}\boldsymbol{p}=s\boldsymbol{R}\boldsymbol{p}+\boldsymbol{t}.$$

类似地，相似变换也对矩阵乘法构成群，称为相似变换群：

$$\mathrm{Sim}(3)=\left\{\boldsymbol{S}=
\begin{bmatrix}
s\boldsymbol{R} & \boldsymbol{t} \\
\boldsymbol{0}^\mathrm{T} & 1
\end{bmatrix}\in\mathbb{R}^{4\times4}\right\}.$$

对应李代数为：

$$\mathfrak{sim}(3)=\left\{\boldsymbol{\zeta}|\boldsymbol{\zeta}=
\begin{bmatrix}
\boldsymbol{\rho} \\
 \\
\boldsymbol{\phi} \\
 \\
\boldsymbol{\sigma}
\end{bmatrix}\in\mathbb{R}^7,\boldsymbol{\zeta}^\wedge=
\begin{bmatrix}
\sigma\boldsymbol{I}+\boldsymbol{\phi}^\wedge & \boldsymbol{\rho} \\
 \\
\boldsymbol{0}^\mathrm{T} & 0
\end{bmatrix}\in\mathbb{R}^{4\times4}\right\}.$$

指数映射为：
$$\exp\left(\boldsymbol{\zeta}^{\wedge}\right)=
\begin{bmatrix}
\mathrm{e}^{\sigma}\exp\left(\boldsymbol{\phi}^{\wedge}\right) & \boldsymbol{J}_{s}\boldsymbol{\rho} \\
 \\
\mathbf{0}^{\mathrm{T}} & 1
\end{bmatrix}.$$

其中，

$$\begin{aligned}
\boldsymbol{J}_{s} & =\frac{\mathrm{e}^\sigma-1}{\sigma}\boldsymbol{I}+\frac{\sigma\mathrm{e}^\sigma\sin\theta+\left(1-\mathrm{e}^\sigma\cos\theta\right)\theta}{\sigma^2+\theta^2}\boldsymbol{a}^\wedge \\
 & +\left(\frac{\mathrm{e}^\sigma-1}{\sigma}-\frac{(\mathrm{e}^\sigma\cos\theta-1)\sigma+(\mathrm{e}^\sigma\sin\theta)\theta}{\sigma^2+\theta^2}\right)\boldsymbol{a}^\wedge\boldsymbol{a}^\wedge.
\end{aligned}$$