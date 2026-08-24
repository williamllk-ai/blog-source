---
title: 【3DV】 计算机视觉第一章-坐标系变换与相机模型
date: 2026-07-10 10:49:44
tags: [SLAM, CV, 3DV]
---
# Computer Vision Chapter1 坐标系变换与几何模型

## 1. 射影几何基础

### 1.1 齐次坐标

二维欧氏点：

$$
(x,y)
$$

对应齐次坐标：

$$
\mathbf{x}=(x,y,1)^T
$$

齐次向量只确定到一个非零尺度：

$$
\mathbf{x}\sim \lambda\mathbf{x},
\qquad \lambda\neq 0
$$

从齐次坐标恢复欧氏坐标：

$$
(x_1,x_2,x_3)^T
\longrightarrow
\left(\frac{x_1}{x_3},\frac{x_2}{x_3}\right)
$$

齐次坐标的作用：

- 将透视投影写成矩阵形式
- 表示无穷远点和无穷远线
- 统一描述点、线、投影和几何变换

---

### 1.2 点与线

二维直线：

$$
ax+by+c=0
$$

齐次表示：

$$
\mathbf{l}=(a,b,c)^T
$$

点在线上的条件：

$$
\mathbf{l}^T\mathbf{x}=0
\Leftrightarrow
\mathbf{x}^T\mathbf{l}=0
$$

过两个点的直线：

$$
\mathbf{l}=\mathbf{x}\times\mathbf{x}'
$$

两条直线的交点：

$$
\mathbf{x}=\mathbf{l}\times\mathbf{l}'
$$

注意：

- $\mathbf{l}$ 是直线方程的系数向量
- $\mathbf{l}$ 不是图像中直线的方向向量
- 叉乘得到的是同时与两个齐次点向量正交的直线系数

---

### 1.3 无穷远点与无穷远线

无穷远点：

$$
\mathbf{x}_\infty=(x_1,x_2,0)^T
$$

无穷远线：

$$
\mathbf{l}_\infty=(0,0,1)^T
$$

平行线在射影平面中相交于同一个无穷远点，所有无穷远点都在无穷远线上。

---

## 2. 二维几何变换

### 2.1 变换层次

| 变换 | 矩阵形式 | 自由度 | 主要不变量 |
|---|---|---:|---|
| 欧氏变换 | $\begin{bmatrix}R&t\\0^T&1\end{bmatrix}$ | 3 | 长度、角度、面积 |
| 相似变换 | $\begin{bmatrix}sR&t\\0^T&1\end{bmatrix}$ | 4 | 角度、长度比、形状 |
| 仿射变换 | $\begin{bmatrix}A&t\\0^T&1\end{bmatrix}$ | 6 | 平行性、平行线段长度比、面积比 |
| 射影变换 | $H$ | 8 | 直线、共线性、交比 |

包含关系：

$$
\text{Euclidean}
\subset
\text{Similarity}
\subset
\text{Affine}
\subset
\text{Projective}
$$

---

### 2.2 欧氏变换

$$
\mathbf{x}'
=
\begin{bmatrix}
R&t\\
0^T&1
\end{bmatrix}
\mathbf{x}
$$

其中：

$$
R^TR=I,
\qquad
\det(R)=1
$$

包含：

- 旋转
- 平移

保持：

- 长度
- 角度
- 面积
- 形状

---

### 2.3 相似变换

$$
\mathbf{x}'
=
\begin{bmatrix}
sR&t\\
0^T&1
\end{bmatrix}
\mathbf{x}
$$

包含：旋转、平移、等比例缩放

保持：角度、长度比、面积比、形状

---

### 2.4 仿射变换

$$
\mathbf{x}'
=
\begin{bmatrix}
A&t\\
0^T&1
\end{bmatrix}
\mathbf{x}
$$

其中 $A$ 是任意非奇异 $2\times2$ 矩阵。

保持：平行关系、平行线段的长度比、面积比

仿射矩阵可分解为：

$$
A=R(\theta)R(-\phi)DR(\phi)
$$

其中：

$$
D=
\begin{bmatrix}
\lambda_1&0\\
0&\lambda_2
\end{bmatrix}
$$

几何过程：

1. 将坐标轴旋转到主拉伸方向
2. 在两个正交方向分别缩放
3. 将坐标轴旋转回来
4. 进行整体旋转

相对相似变换，仿射变换新增的核心是非等比例缩放。

---

### 2.5 射影变换与单应矩阵

二维平面间的射影变换：

$$
\mathbf{x}'\sim H\mathbf{x}
$$

其中：

$$
H\in\mathbb{R}^{3\times3},
\qquad
\det(H)\neq 0
$$

术语关系：

- 射影变换：Projective Transformation
- 单应：Homography
- $H$：单应矩阵

$H$ 有 9 个元素，但整体尺度无意义，因此有 8 个自由度。

最少需要 4 对点对应：

$$
\mathbf{x}_i\leftrightarrow\mathbf{x}_i'
$$

---

## 3. DLT 直接线性变换

### 3.1 单应矩阵 DLT

由：

$$
\mathbf{x}_i'\sim H\mathbf{x}_i
$$

利用叉乘消除齐次尺度：

$$
\mathbf{x}_i'\times H\mathbf{x}_i=0
$$

整理为：

$$
A_i\mathbf{h}=0
$$

将所有点对应堆叠：

$$
A\mathbf{h}=0
$$

其中 $\mathbf{h}$ 是矩阵 $H$ 的 9 个元素组成的向量。

由于齐次方程存在平凡解 $\mathbf{h}=0$，增加约束：

$$
\|\mathbf{h}\|=1
$$

于是求解：

$$
\min_{\|\mathbf{h}\|=1}\|A\mathbf{h}\|^2
$$

利用SVD分解：

$$
A=U\Sigma V^T
$$

则 $\mathbf{h}$ 为 $V$ 中对应最小奇异值的右奇异向量。

---

### 3.2 归一化 DLT

DLT 对坐标尺度和原点选择敏感，因此需要归一化。

对第一组点计算相似变换 $T$，使：

- 点集中心位于原点
- 点到原点的平均距离为 $\sqrt{2}$

对第二组点计算相似变换 $T'$。

在归一化坐标下求得：

$$
\bar H
$$

解除归一化：

$$
H=T'^{-1}\bar HT
$$

归一化的作用：

- 改善矩阵条件数
- 提高数值稳定性
- 减少坐标尺度差异的影响

---

### 3.3 误差类型

#### 代数误差

$$
\|A\mathbf{h}\|^2
$$

特点：

- 线性
- 计算快
- 几何意义较弱
- 适合作为非线性优化初值

#### 单向转移误差

$$
\sum_i
d\left(
\mathbf{x}_i',
\pi(H\mathbf{x}_i)
\right)^2
$$

#### 对称转移误差

$$
\sum_i
d\left(
\mathbf{x}_i',
\pi(H\mathbf{x}_i)
\right)^2
+
d\left(
\mathbf{x}_i,
\pi(H^{-1}\mathbf{x}_i')
\right)^2
$$

#### 黄金标准误差

引入满足精确几何约束的理想点：

$$
\hat{\mathbf{x}}_i'\sim H\hat{\mathbf{x}}_i
$$

最小化：

$$
\sum_i
d(\mathbf{x}_i,\hat{\mathbf{x}}_i)^2
+
d(\mathbf{x}_i',\hat{\mathbf{x}}_i')^2
$$

同时优化$\mathbf{x}_i$和$H$矩阵。

---

## 4. 摄像机模型

### 4.1 小孔相机模型

相机坐标系中的三维点：

$$
\mathbf{X}_c=(X,Y,Z)^T
$$

投影到归一化平面：

$$
\hat{\mathbf{x}}
=
\begin{pmatrix}
X/Z\\
Y/Z\\
1
\end{pmatrix}
$$

理想投影：

$$
u=f\frac{X}{Z},
\qquad
v=f\frac{Y}{Z}
$$

透视投影的特征：

- 近大远小
- 平行线可能在图像中相交
- 一条空间射线上的点投影为同一个图像点
- 单张图像无法恢复点的深度

---

### 4.2 相机内参矩阵

$$
K=
\begin{bmatrix}
f_x&s&c_x\\
0&f_y&c_y\\
0&0&1
\end{bmatrix}
$$

参数含义：

- $f_x,f_y$：像素单位焦距
- $(c_x,c_y)$：主点
- $s$：偏斜参数，通常近似为 0

像素坐标与归一化坐标关系：

$$
\mathbf{x}=K\hat{\mathbf{x}}
$$

$$
\hat{\mathbf{x}}=K^{-1}\mathbf{x}
$$

$\hat{\mathbf{x}}$ 表示相机坐标系中的一条空间射线方向。

---

### 4.3 相机外参

世界坐标点变换到相机坐标系：

$$
\mathbf{X}_c=R\mathbf{X}_w+t
$$

其中：

- $R$：世界坐标系到相机坐标系的旋转
- $t$：世界坐标原点在相机坐标系中的坐标

完整投影：

$$
\mathbf{x}\sim K[R\mid t]\mathbf{X}_w
$$

定义相机投影矩阵：

$$
P=K[R\mid t]
$$

---

### 4.4 相机中心与平移向量

设相机中心在世界坐标系中的坐标为 $C$，则：

$$
\mathbf{X}_c=R(\mathbf{X}_w-C)
$$

展开：

$$
\mathbf{X}_c=R\mathbf{X}_w-RC
$$

因此：

$$
t=-RC
$$

相机矩阵也可写成：

$$
P=KR[I\mid -C]
$$

---

### 4.5 相机矩阵分块

将相机矩阵写成：

$$
P=[M\mid p_4]
$$

其中：

$$
M=KR
$$

$$
p_4=Kt
$$

已知 $P$ 时：

- 对 $M$ 做 RQ 分解可得到 $K,R$
- 相机中心满足

$$
PC=0
$$

因此相机中心是 $P$ 的右零空间向量，可通过 SVD 求得。

---

## 5. 摄像机标定

标定的目标是估计：

$$
K,\ R,\ t
$$

或先估计完整投影矩阵：

$$
P
$$

给定 3D-2D 点对应：

$$
\mathbf{X}_i\leftrightarrow\mathbf{x}_i
$$

满足：

$$
\mathbf{x}_i\sim P\mathbf{X}_i
$$

利用叉乘消除尺度：

$$
\mathbf{x}_i\times P\mathbf{X}_i=0
$$

整理为：

$$
A_i\mathbf{p}=0
$$

堆叠所有点：

$$
A\mathbf{p}=0
$$

其中 $\mathbf{p}$ 为 $P$ 的 12 个元素组成的向量。

$P$ 有 12 个元素，但整体尺度无意义，因此有 11 个自由度。

理论上至少需要 6 对非退化的 3D-2D 点对应。

---

## 6. 消影点与消影线

空间中方向为 $\mathbf{d}$ 的平行线，其消影点满足：

$$
\mathbf{v}\sim K\mathbf{d}
$$

性质：

- 所有同方向的空间直线投影后经过同一消影点
- 消影点只与方向有关，与直线位置无关
- 与图像平面平行的方向，其消影点位于无穷远处

同一空间平面内不同方向的消影点位于同一直线上，该直线称为该平面的消影线。

---

## 7. 对极几何

### 7.1 基本概念

- 基线：两个相机中心 $C,C'$ 的连线
- 对极点：另一相机中心在当前图像中的投影
- 对极平面：包含 $C,C'$ 和空间点 $X$ 的平面
- 对极线：对极平面与图像平面的交线

给定第一幅图像中的点 $\mathbf{x}$，它在第二幅图像中的对应点 $\mathbf{x}'$ 必须位于一条对极线上。

对极约束将匹配搜索从二维区域缩小为一维直线。

---

### 7.2 基本矩阵定义

基本矩阵实现第一幅图像中的点到第二幅图像中对极线的映射：

$$
\mathbf{l}'=F\mathbf{x}
$$

由于匹配点 $\mathbf{x}'$ 位于 $\mathbf{l}'$ 上：

$$
\mathbf{x}'^T\mathbf{l}'=0
$$

因此：

$$
\boxed{
\mathbf{x}'^TF\mathbf{x}=0
}
$$

这称为对极约束。

---

### 7.3 基本矩阵性质

$$
F\in\mathbb{R}^{3\times3}
$$

$$
\operatorname{rank}(F)=2
$$

左右对极点满足：

$$
F\mathbf{e}=0
$$

$$
F^T\mathbf{e}'=0
$$

原因：

- 所有右图对极线都经过 $\mathbf{e}'$
- 所有左图对极线都经过 $\mathbf{e}$

$F$ 的自由度：

$$
9-1-1=7
$$

其中：

- 减去 1：整体尺度无意义
- 减去 1：秩为 2，即 $\det(F)=0$

---

### 7.4 $F=[e']_\times H_\pi$

$H_\pi$ 是空间平面 $\pi$ 诱导的两视图单应矩阵：

$$
\mathbf{x}_\pi'=H_\pi\mathbf{x}
$$

右图对极线经过：

- 右图对极点 $\mathbf{e}'$
- 平面转移点 $\mathbf{x}_\pi'$

因此：

$$
\mathbf{l}'
=
\mathbf{e}'\times\mathbf{x}_\pi'
$$

写成矩阵形式：

$$
\mathbf{l}'
=
[\mathbf{e}']_\times H_\pi\mathbf{x}
$$

与 $\mathbf{l}'=F\mathbf{x}$ 比较：

$$
F=[\mathbf{e}']_\times H_\pi
$$

$H_\pi$ 在这里主要用于理论解释，普通三维重建通常直接估计 $F$ 或 $E$。

---

### 7.5 本质矩阵定义

若内参已知，将像素坐标变为归一化相机坐标：

$$
\hat{\mathbf{x}}=K^{-1}\mathbf{x}
$$

$$
\hat{\mathbf{x}}'=K'^{-1}\mathbf{x}'
$$

本质矩阵满足：

$$
\boxed{
\hat{\mathbf{x}}'^TE\hat{\mathbf{x}}=0
}
$$

若选择第一台相机为参考：

$$
P=[I\mid0]
$$

$$
P'=[R\mid t]
$$

则：

$$
\boxed{
E=[t]_\times R
}
$$

其中：

$$
[t]_\times=
\begin{bmatrix}
0&-t_z&t_y\\
t_z&0&-t_x\\
-t_y&t_x&0
\end{bmatrix}
$$

满足：

$$
[t]_\times\mathbf{a}=t\times\mathbf{a}
$$

---

### 7.6 本质矩阵性质

$$
E\in\mathbb{R}^{3\times3}
$$

$$
\operatorname{rank}(E)=2
$$

理想本质矩阵的奇异值形式：

$$
E=
U
\operatorname{diag}(\sigma,\sigma,0)
V^T
$$

即：

- 两个非零奇异值相等
- 第三个奇异值为 0

$E$ 有 5 个自由度：

- 旋转 $R$：3 个自由度
- 平移方向 $t/\|t\|$：2 个自由度

两视图单目重建不能恢复平移的绝对尺度。

---

### 7.7 $F$ 与 $E$ 的关系

$$
F=K'^{-T}EK^{-1}
$$

反过来：

$$
E=K'^TFK
$$

若两幅图像由同一台相机拍摄：

$$
K'=K
$$

则：

$$
E=K^TFK
$$

---

### 7.9 8 点法估计基本矩阵

给定匹配点：

$$
\mathbf{x}_i=(x_i,y_i,1)^T
$$

$$
\mathbf{x}_i'=(x_i',y_i',1)^T
$$

对极约束：

$$
\mathbf{x}_i'^TF\mathbf{x}_i=0
$$

展开：

$$
x_i'x_i f_{11}
+x_i'y_i f_{12}
+x_i'f_{13}
+y_i'x_i f_{21}
+y_i'y_i f_{22}
+y_i'f_{23}
+x_i f_{31}
+y_i f_{32}
+f_{33}
=0
$$

每对匹配点产生矩阵 $A$ 的一行：

$$
\begin{bmatrix}
x_i'x_i&
x_i'y_i&
x_i'&
y_i'x_i&
y_i'y_i&
y_i'&
x_i&
y_i&
1
\end{bmatrix}
$$

所有匹配点构成：

$$
A\mathbf{f}=0
$$

求解：

$$
\min_{\|\mathbf{f}\|=1}\|A\mathbf{f}\|^2
$$

算法步骤：

1. 归一化两组匹配点
2. 构造矩阵 $A$
3. 对 $A$ 做 SVD
4. 取最小奇异值对应的右奇异向量
5. reshape 得到初始 $F$
6. 强制 $F$ 满足秩为 2
7. 解除归一化

---

### 7.10 奇异性约束

直接线性求得的 $F$ 一般可能是满秩矩阵，但真实基本矩阵必须满足：

$$
\operatorname{rank}(F)=2
$$

对初始 $F$ 做 SVD：

$$
F=
U
\operatorname{diag}(\sigma_1,\sigma_2,\sigma_3)
V^T
$$

令最小奇异值为 0：

$$
\sigma_3=0
$$

得到修正后的基本矩阵：

$$
F'=
U
\operatorname{diag}(\sigma_1,\sigma_2,0)
V^T
$$

几何意义：

- 所有右图对极线存在公共交点 $\mathbf{e}'$
- 所有左图对极线存在公共交点 $\mathbf{e}$

实际中通常将 8 点法与 RANSAC 结合，以剔除错误匹配。

---

## 8. 三角化

### 8.1 问题定义

已知：

$$
\mathbf{x}\leftrightarrow\mathbf{x}'
$$

以及相机矩阵：

$$
P,\ P'
$$

求三维点：

$$
\mathbf{X}
$$

满足：

$$
\mathbf{x}\sim P\mathbf{X}
$$

$$
\mathbf{x}'\sim P'\mathbf{X}
$$

---

### 8.2 线性三角化

利用叉乘消除齐次尺度：

$$
\mathbf{x}\times P\mathbf{X}=0
$$

设：

$$
\mathbf{x}=(u,v,1)^T
$$

且 $P$ 的三行为：

$$
p_1^T,\ p_2^T,\ p_3^T
$$

则可取两个独立方程：

$$
(up_3^T-p_1^T)\mathbf{X}=0
$$

$$
(vp_3^T-p_2^T)\mathbf{X}=0
$$

第二台相机同理，组合成：

$$
A\mathbf{X}=0
$$

通过 SVD 求最小奇异值对应的右奇异向量。

---

### 8.3 线性与非线性三角化

线性三角化最小化代数误差：

$$
\|A\mathbf{X}\|^2
$$

非线性三角化最小化重投影误差：

$$
\min_{\mathbf{X}}
\left\|
\mathbf{x}-\pi(P\mathbf{X})
\right\|^2
+
\left\|
\mathbf{x}'-\pi(P'\mathbf{X})
\right\|^2
$$

线性三角化：

- 计算快
- 可直接用 SVD
- 适合作为初值

非线性三角化：

- 几何意义更正确
- 精度更高
- 需要迭代优化

---

## 9. PnP

PnP 的输入：

- 已知世界三维点 $\mathbf{X}_j$
- 已知它们在新图像中的二维观测 $\mathbf{x}_j$

目标：

$$
\mathbf{x}_j
\sim
K[R\mid t]\mathbf{X}_j
$$

求新相机位姿：

$$
R,t
$$

三维重建中的作用：

- 两视图初始化后加入新图像
- 利用已有 3D-2D 对应估计新相机位姿
- 常与 RANSAC 结合排除错误对应

---

## 10. 重投影误差

第 $j$ 个三维点在第 $i$ 个相机中的预测投影：

$$
\hat{\mathbf{x}}_{ij}
=
\pi\left(
K_i(R_i\mathbf{X}_j+t_i)
\right)
$$

其中投影函数 $\pi$ 表示透视除法：

$$
\pi
\begin{pmatrix}
X\\Y\\Z
\end{pmatrix}
=
\begin{pmatrix}
X/Z\\
Y/Z
\end{pmatrix}
$$

重投影残差：

$$
\mathbf{r}_{ij}
=
\mathbf{x}_{ij}
-
\hat{\mathbf{x}}_{ij}
$$

重投影误差：

$$
\|\mathbf{r}_{ij}\|^2
$$

---

## 11. Bundle Adjustment

### 11.1 定义

BA 的目标是同时优化：

- 相机位姿 $R_i,t_i$
- 三维点 $\mathbf{X}_j$
- 必要时也可优化内参和畸变参数

目标函数：

$$
\min_{\{R_i,t_i,\mathbf{X}_j\}}
\sum_{(i,j)\in\mathcal{O}}
\left\|
\mathbf{x}_{ij}
-
\pi\left(
K_i(R_i\mathbf{X}_j+t_i)
\right)
\right\|^2
$$

其中 $\mathcal{O}$ 为实际存在的相机—三维点观测集合。

---

### 11.2 BA 为什么是非线性的

非线性来源：

1. 透视除法

$$
u=\frac{X}{Z},
\qquad
v=\frac{Y}{Z}
$$

2. 旋转矩阵 $R$ 不是普通线性变量

3. 相机位姿和三维点同时参与投影

因此 BA 不能通过一次 SVD 求解，需要迭代优化。

---

### 11.3 Gauss-Newton 与 LM

设所有待优化参数组成向量 $p$，残差为 $r(p)$。

在当前参数附近进行一阶近似：

$$
r(p+\Delta p)
\approx
r(p)+J\Delta p
$$

Gauss-Newton 方程：

$$
J^TJ\Delta p=-J^Tr
$$

Levenberg-Marquardt 方程：

$$
(J^TJ+\lambda I)\Delta p=-J^Tr
$$

其中：

- $J$：残差对参数的 Jacobian
- $\Delta p$：当前迭代的参数增量
- $\lambda$：阻尼系数

BA 需要较好的初值，初值通常来自：

- $F/E$ 估计
- 位姿恢复
- 三角化
- PnP

---

## 12. 关键算法对比

| 问题 | 输入 | 输出 | 典型算法 |
|---|---|---|---|
| 单应估计 | 平面上的 2D-2D 点 | $H$ | 归一化 DLT |
| 相机标定 | 3D-2D 点 | $P$ 或 $K,R,t$ | DLT、非线性优化 |
| 两视图几何 | 2D-2D 点 | $F$ 或 $E$ | 8 点法、5 点法 |
| 相对位姿恢复 | $E$ | $R,t$ | SVD 分解 |
| 三角化 | $\mathbf{x},\mathbf{x}',P,P'$ | $\mathbf{X}$ | 线性 SVD、非线性优化 |
| 新相机定位 | 3D-2D 点 | $R,t$ | PnP |
| 全局精修 | 位姿和点云初值 | 优化后的位姿和点云 | BA |


## 参考资料
[1] 上海交通大学. AI4701《计算机视觉》课程课件[Z]. 2024.
[2] 高翔, 张涛, 刘毅, 等. 视觉SLAM十四讲：从理论到实践[M]. 2版. 北京: 电子工业出版社, 2019.