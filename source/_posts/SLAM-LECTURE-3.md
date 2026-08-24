---
title: SLAM LECTURE 3：三维空间刚体运动
date: 2026-01-25 22:10:45
author: williamllk
tags: SLAM
---

# L3 三维空间刚体运动

## 3.1 旋转矩阵

### 3.1.1 内外积Recap

1. 内积：对于$\boldsymbol{a}, \boldsymbol{b} \in \mathbb{R}^3$,
$$\boldsymbol{a}\cdot\boldsymbol{b}=\boldsymbol{a}^\mathrm{T}\boldsymbol{b}=\sum_{i=1}^3a_ib_i=\left|\boldsymbol{a}\right|\left|\boldsymbol{b}\right|\cos\left\langle\boldsymbol{a},\boldsymbol{b}\right\rangle.
\tag{3.1}
$$

2. 外积：

$$\boldsymbol{a}\times\boldsymbol{b}=
\begin{Vmatrix}
\boldsymbol{e}_1 & \boldsymbol{e}_2 & \boldsymbol{e}_3 \\
 \\
a_1 & a_2 & a_3 \\
 \\
b_1 & b_2 & b_3
\end{Vmatrix}=
\begin{bmatrix}
a_2b_3-a_3b_2 \\
 \\
a_3b_1-a_2b_3 \\
 \\
a_1b_2-a_2b_1
\end{bmatrix}=
\begin{bmatrix}
0 & -a_3 & a_2 \\
 \\
a_3 & 0 & -a_1 \\
 \\
-a_2 & a_1 & 0
\end{bmatrix}\boldsymbol{b}\overset{\mathrm{def}}{\operatorname*{=}}\boldsymbol{a}^{\wedge}\boldsymbol{b}.
\tag{3.2}
$$

其中$^\wedge$符号将$\boldsymbol{a}$一一映射成一个反对称矩阵$\boldsymbol{a}^\wedge$，后文将经常用到

### 3.1.2 坐标系间的欧式变换

**旋转**中，设某个单位正交基$(\boldsymbol{e}_1,\boldsymbol{e}_2,\boldsymbol{e}_3)$经过一次旋转变成了$(\boldsymbol{e}_1^{\prime},\boldsymbol{e}_2^{\prime},\boldsymbol{e}_3^{\prime})$，根据坐标的定义有，
$$[\boldsymbol{e}_1,\boldsymbol{e}_2,\boldsymbol{e}_3]
\begin{bmatrix}
a_1 \\
 \\
a_2 \\
 \\
a_3
\end{bmatrix}=[\boldsymbol{e}_1^{\prime},\boldsymbol{e}_2^{\prime},\boldsymbol{e}_3^{\prime}]
\begin{bmatrix}
a_1^{\prime} \\
 \\
a_2^{\prime} \\
 \\
a_3^{\prime}
\end{bmatrix}.
\tag{3.3}
$$
两边同时左乘$[\boldsymbol{e}_1,\boldsymbol{e}_2,\boldsymbol{e}_3]^\top$，得到，
$$\begin{bmatrix}
a_1 \\
\\
a_2 \\
\\
a_3
\end{bmatrix}=
\begin{bmatrix}
e_1^\mathrm{T}e_1^{\prime} & e_1^\mathrm{T}e_2^{\prime} & e_1^\mathrm{T}e_3^{\prime} \\
\\
e_2^\mathrm{T}e_1^{\prime} & e_2^\mathrm{T}e_2^{\prime} & e_2^\mathrm{T}e_3^{\prime} \\
\\
e_3^\mathrm{T}e_1^{\prime} & e_3^\mathrm{T}e_2^{\prime} & e_3^\mathrm{T}e_3^{\prime}
\end{bmatrix}
\begin{bmatrix}
a_1^{\prime} \\
 \\
a_2^{\prime} \\
 \\
a_3^{\prime}
\end{bmatrix}\overset{\mathrm{def}}{\operatorname*{=}}\boldsymbol{R}\boldsymbol{a}^{\prime}.
\tag{3.4}
$$
其中$\boldsymbol{R}$成为**旋转矩阵**（Rotation Matix），且是一个行列式为1的正交矩阵。

n为旋转矩阵的集合定义如下：

$$\mathrm{SO}(n)=\{\boldsymbol{R}\in\mathbb{R}^{n\times n}|\boldsymbol{R}^\mathrm{T}\boldsymbol{R}=\boldsymbol{I},\det(\boldsymbol{R})=1\}
\tag{3.5}
$$

其中SO(n)是**特殊正交群**（Special Orthogonal Group）的意思。

<br>

**平移**中，直接相加即可，记作$\boldsymbol{t}$，称为平移向量。

<br>

因此，把旋转和平移合到一起，有

$$
\boldsymbol{a}^\prime = 
\boldsymbol{R}\boldsymbol{a} + \boldsymbol{t}
\tag{3.6}
$$

完整地描述了一个欧氏空间的坐标变换关系。

实际上，对于坐标系1、坐标系2，你们向量$\boldsymbol{a}$在两个坐标系下的坐标为$\boldsymbol{a}_1$，$\boldsymbol{a}_2$，它们之间的关系应该是：

$$
\boldsymbol{a}_1 = 
\boldsymbol{R}_{12}\boldsymbol{a}_2 + \boldsymbol{t}_{12}
\tag{3.7}
$$

其中，$\boldsymbol{R}_{12}$是指“**把坐标系2的向量变换到坐标系**1”中，$\boldsymbol{t}_{12}$对应的是**坐标系1原点指向坐标系2原点的向量，在坐标系1下取的坐标**，下标需尤其注意。

### 3.1.3 变换矩阵与齐次坐标

考虑到变换关系非线性，多次变换后数学式会很复杂，因此引入齐次坐标和变换矩阵，重写式(3.6)：

$$\begin{bmatrix}
a^{\prime} \\
1
\end{bmatrix}=
\begin{bmatrix}
R & t \\
\mathbf{0}^\mathrm{T} & 1
\end{bmatrix}
\begin{bmatrix}
a \\
 \\
1
\end{bmatrix}\overset{\mathrm{def}}{\operatorname*{=}}\;\boldsymbol{T}
\begin{bmatrix}
a \\
 \\
1
\end{bmatrix}.
\tag{3.8}
$$

在三维向量的末尾添加1，变成了四维向量，成为**齐次坐标**，从而将变换变成线性关系，矩阵$\boldsymbol{T}$称为**变换矩阵**(Transform Matrix)，后续在不引起歧义的情况下，写成$\boldsymbol{b} = \boldsymbol{T}\boldsymbol{a}$时，默认进行了齐次坐标的变换。

<bf>

关于变换矩阵$\boldsymbol{T}$，左上角为旋转矩阵，右上角为平移向量，左下角为$\mathbf{0}$，右下角为1，这种矩阵又称为**特殊欧式群**(Special Euclidean Group):

$$\mathrm{SE}(3)=\left\{\boldsymbol{T}=
\begin{bmatrix}
\boldsymbol{R} & \boldsymbol{t} \\
\boldsymbol{0}^\mathrm{T} & 1
\end{bmatrix}\in\mathbb{R}^{4\times4}|\boldsymbol{R}\in\mathrm{SO}(3),\boldsymbol{t}\in\mathbb{R}^3\right\}.
\tag{3.9}
$$

该矩阵的逆表示一个反向的变换：

$$\boldsymbol{T}^{-1}=
\begin{bmatrix}
\boldsymbol{R}^\mathrm{T} & -\boldsymbol{R}^\mathrm{T}\boldsymbol{t} \\
\mathbf{0}^\mathrm{T} & 1
\end{bmatrix}.
\tag{3.10}
$$

同样，我们用$\boldsymbol{T}_{12}$来表示从2到1的变换。

## 3.3 旋转向量和欧拉角

### 3.3.1 旋转向量

旋转矩阵用9个参数和一些限制条件来表示仅有3个自由度的旋转，不够紧凑，因而提出使用一个三维向量来表示旋转，其方向与旋转轴一致，而长度等于旋转角，这种向量被成为**旋转向量**（Axis-Angle）

考虑某个旋转对应的旋转矩阵为$\boldsymbol{R}$，其旋转轴为一个单位长度的向量$\boldsymbol{n}$，旋转角为$\theta$，那么向量$\theta\boldsymbol{n}$即是描述这个旋转的旋转向量，下面给出两种表达方式之间的转换关系。

从旋转向量到旋转矩阵的转换过程由**罗德里格斯公式**(Rodrigues's Formula)表明，公式如下：

$$\boldsymbol{R}=\cos\theta\boldsymbol{I}+(1-\cos\theta)\boldsymbol{n}\boldsymbol{n}^\mathrm{T}+\sin\theta\boldsymbol{n}^\mathrm{\wedge}.
\tag{3.11}
$$

从一个旋转矩阵到旋转向量的计算过程分两步走。对于转角$\theta$，取两边的trace，得到：

$$\begin{aligned}
\operatorname{tr}\left(R\right) & =\cos\theta\operatorname{tr}\left(\boldsymbol{I}\right)+\left(1-\cos\theta\right)\operatorname{tr}\left(\boldsymbol{n}\boldsymbol{n}^\mathrm{T}\right)+\sin\theta\operatorname{tr}(\boldsymbol{n}^\wedge) \\
 & =3\cos\theta+(1-\cos\theta) \\
 & =1+2\cos\theta \\
\end{aligned}
\tag{3.12}$$

因此：
$$\theta=\arccos\frac{\operatorname{tr}(\boldsymbol{R})-1}{2}.\tag{3.13}$$

关于转轴$\boldsymbol{n}$，旋转轴上的向量在旋转后不发生变化，说明：

$$\boldsymbol{R}\boldsymbol{n}=\boldsymbol{n}.\tag{3.14}$$

因此，$\boldsymbol{n}$是矩阵$\boldsymbol{R}$特征值1对应的特征向量，求解后再归一化得到转轴。

tip：旋转向量具有奇异性，$\theta = 90^\circ$时旋转轴不唯一，丢失自由度

### 3.3.2 欧拉角

以ZYX为例，将任意旋转分解成以下3个轴的转角：

1. 绕物体Z轴旋转，得到偏航角yaw
2. 绕旋转之后的Y轴旋转，得到俯仰角pitch
3. 绕旋转之后的X轴旋转，得到滚转角roll

此时可以使用$[r, p, y]^\mathrm{T}$来描述仍以旋转。

但是存在一个重大缺点，会出现**万向锁问题**（Gimbal Lock），即当俯仰角pitch = ±90°时第一次旋转与第三次旋转将使用同一个轴，从而丢失了一个自由度，这被称为奇异性问题。

## 3.4 四元数

### 3.4.1 定义

一个四元数$\boldsymbol{q}$拥有一个实部和三个虚部，
$$\boldsymbol{q}=q_0+q_1\mathrm{i}+q_2\mathrm{j}+q_3\mathrm{k}
\tag{3.15}$$

其中$\mathrm{i}$, $\mathrm{j}$, $\mathrm{k}$为三个虚部，且满足关系式：

$$\begin{cases}
\mathrm{i}^2=\mathrm{j}^2=\mathrm{k}^2=-1 \\
\mathrm{i}\mathrm{j}=\mathrm{k},\mathrm{j}\mathrm{i}=-\mathrm{k} \\
\mathrm{j}\mathrm{k}=\mathrm{i},\mathrm{k}\mathrm{j}=-\mathrm{i} \\
\mathrm{k}\mathrm{i}=\mathrm{j},\mathrm{i}\mathrm{k}=-\mathrm{j} & 
\end{cases}\tag{3.16}$$

有时，四元数也可以用一个标量和一个向量来表示，

$$\boldsymbol{q}=\left[s,\boldsymbol{v}\right]^\mathrm{T},\quad s=q_0\in\mathbb{R},\quad\boldsymbol{v}=\left[q_1,q_2,q_3\right]^\mathrm{T}\in\mathbb{R}^3.\tag{3.17}$$

其中，$s$成为四元数的实部，而$\boldsymbol{v}$称为虚部。可以用**单位四元数**来表示三维空间中任意一个旋转。

### 3.4.2 运算

现有两个四元数$\boldsymbol{q}_a$，$\boldsymbol{q}_b$，它们的向量表示为$[s_a,\boldsymbol{v}_a]^\mathrm{T}$，$[s_b,\boldsymbol{v}_b]^\mathrm{T}$，运算可表示如下。

1. 加减法（数乘类似）

$$\boldsymbol{q}_a\pm\boldsymbol{q}_b=\left[s_a\pm s_b,\boldsymbol{v}_a\pm\boldsymbol{v}_b\right]^\mathrm{T}.\tag{3.18}$$

2. 乘法：每项相乘相加，整理可得

$$\boldsymbol{q}_a\boldsymbol{q}_b=
\begin{bmatrix}
s_as_b-\boldsymbol{v}_a^\mathrm{T}\boldsymbol{v}_b,s_a\boldsymbol{v}_b+s_b\boldsymbol{v}_a+\boldsymbol{v}_a\times\boldsymbol{v}_b
\end{bmatrix}^\mathrm{T}.\tag{3.19}$$

需注意，不满足交换律

3. 模长

$$\|q_a\|=\sqrt{s_a^2+x_a^2+y_a^2+z_a^2}.\tag{3.20}$$

且满足

$$\|\boldsymbol{q}_a\boldsymbol{q}_b\|=\|\boldsymbol{q}_a\|\|\boldsymbol{q}_b\|.\tag{3.21}$$

4. 共轭

$$\boldsymbol{q}_a^*=[\mathrm{s}_\mathrm{a},-\mathrm{v}_\mathrm{a}]^\mathrm{T}.\tag{3.22}$$

四元数共轭与自身相乘，会得到一个实四元数，其实部为模长的平方：

$$\boldsymbol{q}^*\boldsymbol{q} = \boldsymbol{q}\boldsymbol{q}^* = \left[s_a^2 + \boldsymbol{v}^\mathrm{T}\boldsymbol{v}, \boldsymbol{0} \right]^\mathrm{T}.\tag{3.23}$$

5. 逆

$$\boldsymbol{q}^{-1}=\boldsymbol{q}^*/\|\boldsymbol{q}\|^2.$$

因此，四元数和自己的逆的成绩为实四元数$\boldsymbol{1}$

$$\boldsymbol{q}^{-1}\boldsymbol{q} = \boldsymbol{q}\boldsymbol{q}^{-1} = \boldsymbol{1}.\tag{3.24}$$

对于单位四元数，其逆和共轭是一个量。

同时，乘积的逆具有和矩阵的相似性质：

$$\left(\boldsymbol{q}_a\boldsymbol{q}_b\right)^{-1}=\boldsymbol{q}_b^{-1}\boldsymbol{q}_a^{-1}.\tag{3.25}$$

### 3.4.3 用四元数表示旋转

我们可以用四元数表达对一个点的旋转。假设有一个空间三维点$\boldsymbol{p}=[x, y, z] \in \mathbb{R}^3$，以及一个**单位四元数**$\boldsymbol{q}$来指定将$\boldsymbol{p}$旋转至$\boldsymbol{p}^\prime$。

首先，把三维空间点用一个虚四元数来描述：

$$\boldsymbol{p}=[0, x, y, z]^\mathrm{T} = [0, \boldsymbol{v}]^\mathrm{T}.\tag{3.26}$$

则旋转后的$\boldsymbol{p}^\prime$可以表示为：

$$\boldsymbol{p}' = \boldsymbol{q}\boldsymbol{p}\boldsymbol{q}^{-1}.\tag{3.27}$$

### 3.4.4 四元数到其他旋转表示的转换

设$\boldsymbol{q}=[s, \boldsymbol{v}]^\mathrm{T}$，定义如下符号：

$$\boldsymbol{q}^+=
\begin{bmatrix}
s & -\boldsymbol{v}^\mathrm{T} \\
 \\
\boldsymbol{v} & s\boldsymbol{I}+\boldsymbol{v}^\wedge
\end{bmatrix},\quad\boldsymbol{q}^\oplus=
\begin{bmatrix}
s & -\boldsymbol{v}^\mathrm{T} \\
 \\
\boldsymbol{v} & s\boldsymbol{I}-\boldsymbol{v}^\wedge
\end{bmatrix}\tag{3.28}.$$

可证明

$$\boldsymbol{q}_1\boldsymbol{q}_2=\boldsymbol{q}_1^+\boldsymbol{q}_2=\boldsymbol{q}_2^\oplus\boldsymbol{q}_1\tag{3.29}.$$

于是可以得到

$$\begin{aligned}
\boldsymbol{p}^{\prime} & =\boldsymbol{qpq}^{-1}=\boldsymbol{q}^+\boldsymbol{p}^+\boldsymbol{q}^{-1} \\
 & =\boldsymbol{q}^+\boldsymbol{q}^{-1^\oplus}\boldsymbol{p}.
\end{aligned}.\tag{3.30}$$

代入矩阵可得

$$\boldsymbol{q}^+(\boldsymbol{q}^{-1})^\oplus=
\begin{bmatrix}
1 & \boldsymbol{0} \\
\mathbf{0}^\mathrm{T} & \boldsymbol{v}\boldsymbol{v}^\mathrm{T}+s^2\boldsymbol{I}+2s\boldsymbol{v}^\mathrm{\wedge}+\left(\boldsymbol{v}^\mathrm{\wedge}\right)^2
\end{bmatrix}\tag{3.31}.$$

矩阵的右下角即给出了**从四元数到旋转矩阵**的关系：

$$\boldsymbol{R}=\boldsymbol{v}\boldsymbol{v}^\mathrm{T}+s^2\boldsymbol{I}+2s\boldsymbol{v}^\wedge+\left(\boldsymbol{v}^\wedge\right)^2.\tag{3.32}$$

要求**四元数到旋转向量**的转换公式，类似地可求得：

$$\begin{cases}
\theta=2\arccos q_0 \\
[n_x,n_y,n_z]^\mathrm{T}=[q_1,q_2,q_3]^\mathrm{T}/\sin\frac{\theta}{2}
\end{cases}\tag{3.33}$$

## 3.5 相似、仿射、射影变换

欧式变换保持了向量的长度和夹角，而下面几种变换会改变外形。

### 3.5.1 相似变换

比欧式变换多了一个自由度，允许物体进行缩放，其矩阵表示为

$$\boldsymbol{T}_S=
\begin{bmatrix}
s\boldsymbol{R} & \boldsymbol{t} \\
\boldsymbol{0}^\mathrm{T} & 1
\end{bmatrix}\tag{3.34}.$$

旋转部分多了一个缩放因子$s$，三维相似变换的集合叫做**相似变换群**，记作$\mathrm{Sim}(3)$

### 3.5.2 仿射变换

$$\boldsymbol{T}_A=
\begin{bmatrix}
\boldsymbol{A} & \boldsymbol{t} \\
\boldsymbol{0}^\mathrm{T} & 1
\end{bmatrix}\tag{3.34}.$$

仿射变换只要求$\boldsymbol{A}$是一个可逆矩阵，而不必是正交矩阵。仿射变换也叫正交投影，经过仿射变换，直线仍为直线，保持平行关系。

三维的仿射变换有12个自由度：$3$个平移，$3×3=9$个线性变换

### 3.5.3 射影变换

$$T_P=
\begin{bmatrix}
\boldsymbol{A} & \boldsymbol{t} \\
 \\
\boldsymbol{a}^\mathrm{T} & v
\end{bmatrix}\tag{3.35}.$$

左上角$\boldsymbol{A}$是一个可逆矩阵，左下角为缩放$\boldsymbol{a}^\mathrm{T}$，是最一般的变换。由于采用了齐次坐标，矩阵乘以任何非零常数，代表的变换是完全一样的，因此二维的射影变换自由度为8，三维的自由度为15。