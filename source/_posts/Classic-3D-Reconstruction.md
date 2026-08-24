---
title: 【3DV】 经典三维重建知识总结
date: 2026-07-10 16:37:38
tags: [SLAM, 3DV]
---

# 经典三维重建知识总结

## 坐标系变换与相机模型

相机模型描述三维空间点如何经过坐标系变换和透视投影，最终得到二维像素坐标。

完整过程为：

> 世界坐标  
> → 相机坐标  
> → 归一化像平面  
> → 像素坐标

---

### 1. 世界坐标系与相机坐标系

设三维点在世界坐标系中为：

$$
\mathbf X_w=
\begin{bmatrix}
X_w\\
Y_w\\
Z_w
\end{bmatrix}.
$$

经过相机位姿变换后，在相机坐标系中为：

$$
\boxed{
\mathbf X_c=R\mathbf X_w+t
}
$$

其中：

- $R$：旋转矩阵；
- $t$：平移向量；
- $R,t$ 合称相机外参。

需要注意，若该式表示世界坐标到相机坐标，则 $t$ 不等于相机在世界坐标系中的位置。

相机光心在世界坐标系中的位置为：

$$
\boxed{
\mathbf C_w=-R^Tt
}
$$

---

### 2. 齐次变换矩阵

旋转和平移可以统一写成齐次变换：

$$
T_{cw}
=
\begin{bmatrix}
R & t\\
\mathbf 0^T & 1
\end{bmatrix}.
$$

于是：

$$
\boxed{
\widetilde{\mathbf X}_c
=
T_{cw}\widetilde{\mathbf X}_w
}
$$

逆变换为：

$$
\boxed{
T_{wc}
=
T_{cw}^{-1}
=
\begin{bmatrix}
R^T & -R^Tt\\
\mathbf 0^T & 1
\end{bmatrix}
}
$$

因此：

$$
\boxed{
\mathbf X_w=R^T(\mathbf X_c-t)
}
$$

---

### 3. 针孔相机模型

设三维点在相机坐标系中为：

$$
\mathbf X_c=
\begin{bmatrix}
X_c\\
Y_c\\
Z_c
\end{bmatrix}.
$$

经过透视投影，得到归一化像平面坐标：

$$
\boxed{
x_n=\frac{X_c}{Z_c},
\qquad
y_n=\frac{Y_c}{Z_c}
}
$$

齐次形式为：

$$
\mathbf x_n=
\begin{bmatrix}
x_n\\
y_n\\
1
\end{bmatrix}.
$$

其中 $Z_c$ 表示点的深度。可见点通常满足：

$$
Z_c>0.
$$

---

### 4. 相机内参

归一化坐标通过内参矩阵变换到像素坐标：

$$
\boxed{
K=
\begin{bmatrix}
f_x & 0 & c_x\\
0 & f_y & c_y\\
0 & 0 & 1
\end{bmatrix}
}
$$

其中：

- $f_x,f_y$：以像素为单位的焦距；
- $(c_x,c_y)$：主点坐标。

像素坐标为：

$$
\mathbf p=
\begin{bmatrix}
u\\
v\\
1
\end{bmatrix}
=
K\mathbf x_n.
$$

展开得到：

$$
\boxed{
u=f_x\frac{X_c}{Z_c}+c_x
}
$$

$$
\boxed{
v=f_y\frac{Y_c}{Z_c}+c_y
}
$$

---

### 5. 三维点到二维像素的完整投影

世界点先经过外参变换，再经过内参投影：

$$
\boxed{
\lambda\mathbf p
=
K(R\mathbf X_w+t)
}
$$

使用齐次坐标可写为：

$$
\boxed{
\lambda\mathbf p
=
K[R\mid t]\widetilde{\mathbf X}_w
}
$$

定义摄像机投影矩阵：

$$
\boxed{
P=K[R\mid t]
}
$$

则：

$$
\boxed{
\lambda\mathbf p=P\widetilde{\mathbf X}_w
}
$$

其中：

- $K$：相机内参；
- $[R\mid t]$：相机外参；
- $P$：$3\times4$ 摄像机投影矩阵。

---

### 6. 像素点反投影

已知像素坐标：

$$
\mathbf p=
\begin{bmatrix}
u\\
v\\
1
\end{bmatrix},
$$

通过内参逆矩阵得到归一化相机射线：

$$
\boxed{
\mathbf x_n=K^{-1}\mathbf p
}
$$

展开为：

$$
\boxed{
x_n=\frac{u-c_x}{f_x},
\qquad
y_n=\frac{v-c_y}{f_y}
}
$$

因此：

$$
\mathbf x_n=
\begin{bmatrix}
(u-c_x)/f_x\\
(v-c_y)/f_y\\
1
\end{bmatrix}.
$$

单个像素点不能确定唯一三维点，只能确定一条射线：

$$
\boxed{
\mathbf X_c=sK^{-1}\mathbf p
}
$$

其中 $s$ 是未知深度。

---

### 7. 已知深度时恢复三维点

若深度 $Z_c$ 已知，则：

$$
\boxed{
\mathbf X_c
=
Z_cK^{-1}\mathbf p
}
$$

展开为：

$$
\boxed{
X_c=\frac{(u-c_x)Z_c}{f_x}
}
$$

$$
\boxed{
Y_c=\frac{(v-c_y)Z_c}{f_y}
}
$$

再通过逆位姿变换得到世界坐标：

$$
\boxed{
\mathbf X_w=R^T(\mathbf X_c-t)
}
$$

---

### 8. 未知深度时恢复三维点

单张图像只能得到射线，无法确定深度。恢复三维点还需要额外信息，例如：

- 已知深度；
- 已知点位于某个平面；
- 双目或多视图三角测量；
- RGB-D 深度传感器。

两视图三角测量中，若归一化坐标为 $\mathbf x_1,\mathbf x_2$，相对位姿为 $R,t$，则：

$$
\boxed{
s_2\mathbf x_2
=
R(s_1\mathbf x_1)+t
}
$$

求出 $s_1,s_2$ 后即可恢复三维点。

也即单个像素只能反投影为一条三维射线，必须结合深度或多视图信息才能恢复唯一三维点。


## 图像特征提取与匹配

### ORB（Oriented FAST and Rotated BRIEF）

ORB 将 FAST 角点检测器与改进后的 BRIEF 二进制描述子结合起来，并通过图像金字塔和方向校正获得一定的尺度与旋转适应能力。

ORB 的完整流程为：

> 构建图像金字塔  
> → 每层使用 FAST 检测角点  
> → 筛选稳定角点  
> → 使用灰度质心法计算角点方向  
> → 根据方向旋转 BRIEF 采样模板  
> → 生成二进制描述子  
> → 使用汉明距离进行特征匹配  
> → 使用几何模型与 RANSAC 剔除误匹配

#### 1. 图像金字塔与尺度适应性

FAST 和 BRIEF 本身使用固定大小的局部邻域，因此不能直接处理明显的尺度变化。ORB 首先对原始图像进行多次降采样，构建图像金字塔：

$$
I_0,\ I_1,\ I_2,\ldots,I_{L-1}.
$$

若相邻层之间的尺度因子为 $s>1$，则第 $l$ 层相对于原图的缩放比例约为：

$$
\frac{1}{s^l}.
$$

ORB 在每个金字塔层中分别检测和描述特征点。同一物体在不同图像中大小发生变化时，可能在不同金字塔层中呈现相近的局部像素尺度，因此仍有机会生成相似描述子。

#### 2. FAST 角点检测

FAST 用于快速检测图像中的角点。对于候选像素 $p$，考察以其为中心、半径通常为 3 像素的圆周上的 16 个像素。

设中心灰度为 $I_p$，阈值为 $t$。如果圆周上存在连续若干个像素同时满足：

$$
I_x>I_p+t,
$$

或者：

$$
I_x<I_p-t,
$$

则将 $p$ 判断为角点。

FAST 检测速度很快，但原始 FAST 存在两个主要问题：

1. 不提供特征方向；
2. 不具备尺度不变性。

ORB 分别通过灰度质心法和图像金字塔解决这两个问题。

在实际实现中，还会对 FAST 候选点进行**非极大值抑制**和响应值排序，以保留更稳定、分布更均匀的角点。

#### 3. 灰度质心法与特征方向

FAST 只给出角点位置，不给出方向。ORB 在每个角点周围取一个局部图像块，将像素灰度视为对应位置的“质量”，利用灰度分布的质心确定主方向。

定义图像矩：

$$
m_{pq}
=
\sum_{x,y\in B}
x^p y^q I(x,y),
\qquad
p,q\in\{0,1\}.
$$

其中：

- $B$ 表示角点周围的局部图像块；
- $I(x,y)$ 表示位置 $(x,y)$ 的灰度值；
- 坐标原点通常取在当前角点中心。

零阶矩为：

$$
m_{00}
=
\sum_{x,y\in B}I(x,y),
$$

表示图像块的灰度总和。

一阶矩为：

$$
m_{10}
=
\sum_{x,y\in B}xI(x,y),
$$

$$
m_{01}
=
\sum_{x,y\in B}yI(x,y).
$$

灰度质心为：

$$
C=
\left(
\frac{m_{10}}{m_{00}},
\frac{m_{01}}{m_{00}}
\right).
$$

以角点中心为 $O$，向量 $\overrightarrow{OC}$ 的方向作为角点主方向：

$$
\theta
=
\arctan(m_{01}/m_{10}).
$$

当图像发生旋转时，角点周围的灰度分布和灰度质心也会随之旋转，因此主方向 $\theta$ 能够反映局部图像块的旋转变化。

由此，普通 FAST 角点被赋予方向，形成 Oriented FAST。

#### 4. BRIEF 二进制描述子

BRIEF 在角点周围预先设置若干组采样点对：

$$
(p_1,q_1),
(p_2,q_2),
\ldots,
(p_n,q_n).
$$

对于每一组点对，比较两点的灰度值：

$$
\tau(p_i,q_i)
=
\begin{cases}
1, & I(p_i)<I(q_i),\\
0, & I(p_i)\ge I(q_i).
\end{cases}
$$

将所有比较结果依次排列，得到二进制描述子：

$$
d=
\left[
\tau(p_1,q_1),
\tau(p_2,q_2),
\ldots,
\tau(p_n,q_n)
\right].
$$

例如，进行 256 次灰度比较，就可以得到一个 256 位的二进制描述子。

BRIEF 中的点对并不是在每个角点处重新随机生成。通常是在描述子设计阶段生成或筛选出一套固定的采样模板，之后每个角点都使用同一套相对坐标模板。

设角点图像坐标为：

$$
O=(u_0,v_0),
$$

某个模板点为：

$$
p_i=(\Delta u_i,\Delta v_i),
$$

则实际采样位置为：

$$
O+p_i
=
(u_0+\Delta u_i,\ v_0+\Delta v_i).
$$

#### 5. Rotated BRIEF 与旋转不变性

原始 BRIEF 的采样模板方向固定。当图像发生旋转时，固定模板会采样到局部结构中的不同位置，因此描述子会发生较大变化。

ORB 根据灰度质心法得到的主方向 $\theta$，将整个 BRIEF 采样模板旋转：

$$
p_i^\theta
=
R(\theta)p_i,
$$

$$
q_i^\theta
=
R(\theta)q_i,
$$

旋转后的实际采样位置为：

$$
O+p_i^\theta,
\qquad
O+q_i^\theta.
$$

这样，当局部图像结构旋转时，BRIEF 点对模板也会按相同方向旋转，从而仍然比较局部结构中相近的对应位置。

这类根据主方向调整采样模板的描述子称为 Steered BRIEF 或 Rotated BRIEF。

#### 6. ORB 特征匹配

两张图像首先分别独立完成 ORB 特征提取：

> 图像 1  
> → 图像金字塔  
> → FAST 角点  
> → 主方向 $\theta$  
> → rBRIEF 描述子  
>
> 图像 2  
> → 图像金字塔  
> → FAST 角点  
> → 主方向 $\theta$  
> → rBRIEF 描述子

由于 ORB 描述子是二进制向量，因此通常使用**汉明距离**比较两个描述子。

设两个描述子为 $d_1,d_2$，则汉明距离为：

$$
d_H(d_1,d_2)
=
\operatorname{popcount}(d_1\oplus d_2).
$$

其中：

- $\oplus$ 表示按位异或；
- $\operatorname{popcount}$ 表示统计结果中 1 的数量。

汉明距离等于两个描述子中不同二进制位的数量。距离越小，两个局部特征越相似。

然而仅依赖描述子距离通常会产生误匹配，因此需要进一步筛选。常见方法包括距离阈值筛选、最近邻比值检验、RANSAC 几何验证等。

### SIFT（Scale Invariant Feature Transform）


SIFT 是一种具有较强尺度不变性和旋转不变性的局部图像特征。它不仅检测关键点的位置，还会为每个关键点确定合适的尺度和主方向，并生成一个 128 维浮点描述子。

一个完整的 SIFT 特征可以表示为：

$$
(x,\ y,\ \sigma,\ \theta,\ d),
$$

其中：

- $(x,y)$ 表示关键点位置；
- $\sigma$ 表示关键点对应的尺度；
- $\theta$ 表示关键点主方向；
- $d$ 表示 128 维描述子。

SIFT 的完整流程为：

> 构建高斯尺度空间  
> → 计算相邻高斯图像之差，得到 DoG  
> → 在 DoG 尺度空间中寻找极值点  
> → 精确定位并剔除不稳定关键点  
> → 根据局部梯度分配主方向  
> → 构造 128 维梯度描述子  
> → 使用欧氏距离和最近邻比值进行匹配  
> → 使用 RANSAC 剔除误匹配

#### 1. 高斯尺度空间

为了检测不同大小的局部结构，SIFT 不只在原始图像上寻找特征，而是在不同模糊尺度下观察同一张图像。

高斯尺度空间定义为：

$$
L(x,y,\sigma)
=
G(x,y,\sigma)*I(x,y),
$$

其中：

$$
G(x,y,\sigma)
=
\frac{1}{2\pi\sigma^2}
\exp
\left(
-\frac{x^2+y^2}{2\sigma^2}
\right).
$$

$I(x,y)$ 表示原始图像，$*$ 表示卷积，$\sigma$ 控制高斯模糊程度。

- $\sigma$ 较小时，图像保留较多细节，适合观察较小结构；
- $\sigma$ 较大时，细小纹理被平滑，主要保留较大结构。

因此，SIFT 不仅要确定特征点的位置，还要确定该特征在哪个尺度下最明显。

#### 2. Octave 与 Gaussian 层级

SIFT 的尺度空间由多个 Octave 组成，每个 Octave 内包含多张尺寸相同、模糊程度不同的 Gaussian 图像。

例如：

> Octave 0：原始分辨率，多张不同 $\sigma$ 的 Gaussian 图  
> Octave 1：宽高缩小一半，多张不同 $\sigma$ 的 Gaussian 图  
> Octave 2：宽高再次缩小一半，继续构建 Gaussian 图

因此：

- 同一个 Octave 内，图像尺寸不变，只改变高斯模糊程度；
- 相邻 Octave 之间，图像宽高通常各缩小一半。

若当前图像为 $I_o$，下一 Octave 的基础图像可以近似表示为：

$$
I_{o+1}(x,y)
=
I_o(2x,2y).
$$

这里的 $I_o$ 已经经过适当的高斯平滑。先模糊再降采样，可以减少图像缩小时产生的混叠。

#### 3. DoG 高斯差分

DoG 全称为 Difference of Gaussian，即高斯差分。它由同一个 Octave 内相邻两张 Gaussian 图像相减得到：

$$
D(x,y,\sigma)
=
L(x,y,k\sigma)-L(x,y,\sigma).
$$

例如，一个 Octave 内有多张 Gaussian 图像：

$$
L_0,\ L_1,\ L_2,\ L_3,\ L_4,
$$

则可以得到：

$$
D_0=L_1-L_0,
$$

$$
D_1=L_2-L_1,
$$

$$
D_2=L_3-L_2,
$$

$$
D_3=L_4-L_3.
$$

如果一个区域在相邻模糊尺度下变化很小，相减结果就接近 0；如果某个局部结构在某个尺度附近变化明显，则会在 DoG 图像中产生较大的正响应或负响应。

因此，DoG 的作用是寻找：

> 在某个图像位置和某个尺度下特别明显的局部结构。

#### 4. 尺度空间极值检测

SIFT 在 DoG 图像中同时沿着图像位置和尺度方向寻找极值。

对于某个候选像素，需要与周围共 26 个邻点比较：

- 当前 DoG 层中的 8 个邻点；
- 上一 DoG 层中的 9 个邻点；
- 下一 DoG 层中的 9 个邻点。

如果当前点比这 26 个邻点都大，或者比这 26 个邻点都小，就将其视为候选关键点。

因此，SIFT 检测到的关键点不仅具有位置：

$$
(x,y),
$$

还具有对应尺度：

$$
\sigma.
$$

也就是说，关键点是在三维尺度空间中检测到的：

$$
(x,y,\sigma).
$$

不同 Octave、不同 Gaussian 层都可能产生关键点，但并不是每一层都会产生固定数量的关键点。

#### 5. 关键点精确定位与筛选

DoG 极值点只是离散像素和离散尺度上的候选点，真实极值可能位于像素之间或相邻尺度之间。因此，SIFT 会在候选点附近进行局部函数拟合，以获得更精确的位置和尺度。

同时，还需要剔除两类不稳定关键点。

第一类是**低对比度点**。这类点的 DoG 响应较弱，容易受到图像噪声影响，因此需要删除。

第二类是**边缘响应点**。边缘上的点虽然可能有较强响应，但沿着边缘方向的位置不容易准确确定，因此不适合作为稳定特征点。

SIFT 使用 DoG 图像的 Hessian 矩阵判断边缘响应：

$$
H=
\begin{bmatrix}
D_{xx} & D_{xy}\\
D_{xy} & D_{yy}
\end{bmatrix}.
$$

通过比较两个方向上的曲率，可以剔除只在一个方向上变化明显的边缘点，保留在两个方向上都具有稳定变化的局部结构。

#### 6. 主方向分配

为了获得旋转不变性，SIFT 会在关键点对应尺度的 Gaussian 图像上计算局部梯度。

水平方向和竖直方向的梯度可近似表示为：

$$
g_x
=
L(x+1,y)-L(x-1,y),
$$

$$
g_y
=
L(x,y+1)-L(x,y-1).
$$

梯度幅值为：

$$
m(x,y)
=
\sqrt{g_x^2+g_y^2},
$$

梯度方向为：

$$
\theta(x,y)
=
\operatorname{atan2}(g_y,g_x).
$$

SIFT 在关键点邻域内建立梯度方向直方图。经典实现通常将 $360^\circ$ 划分为 36 个方向区间，每个像素按照梯度幅值进行加权投票。

方向直方图的最高峰作为关键点主方向：

$$
\theta_{\text{keypoint}}
=
\arg\max_{\theta} h(\theta).
$$

如果还有其他方向峰值接近最高峰，SIFT 可能在同一个位置和尺度上生成多个方向不同的关键点。

#### 7. SIFT 描述子

确定关键点位置、尺度和方向后，SIFT 在对应 Gaussian 图像上构造局部描述子。

首先，以关键点主方向为参考，将局部坐标系旋转到统一方向。这样，即使图像发生旋转，对应特征也能在相同方向下进行描述。

然后，在关键点周围取一个局部区域，并将其划分为：

$$
4\times4
$$

个小区域，共 16 个单元。

每个单元统计 8 个方向上的梯度分布，因此描述子维度为：

$$
4\times4\times8=128.
$$

最终得到：

$$
d\in\mathbb{R}^{128}.
$$

这 128 个数记录了关键点邻域内不同位置、不同方向上的梯度分布，因此能够描述局部边缘、纹理和轮廓结构。

为了减小光照和对比度变化的影响，还会对描述子进行归一化：

$$
d
\leftarrow
\frac{d}{\lVert d\rVert_2}.
$$

SIFT 描述子是浮点向量，与 ORB 的二进制描述子不同。

#### 8. 不同尺度关键点的统一匹配

一张图像中会在多个 Octave 和多个尺度层中检测到关键点。每个关键点都在其对应的 Gaussian 尺度上计算主方向和描述子。

需要注意：

- DoG 图像主要用于检测关键点；
- Gaussian 图像用于计算梯度、主方向和描述子；
- 各层得到的关键点和描述子最终会汇总到同一个集合中。

图像 1 的描述子集合记为：

$$
D_1
=
\left\{
d_1^{(1)},
d_2^{(1)},
\ldots,
d_{N_1}^{(1)}
\right\},
$$

图像 2 的描述子集合记为：

$$
D_2
=
\left\{
d_1^{(2)},
d_2^{(2)},
\ldots,
d_{N_2}^{(2)}
\right\}.
$$

匹配时，图像 1 中的每个描述子会与图像 2 中所有 Octave、所有尺度层汇总后的描述子进行比较。

不同 Octave 和不同尺度层的特征也可以互相匹配，因为描述子构造过程中已经根据关键点尺度调整了邻域大小，并根据主方向进行了旋转归一化。

#### 9. SIFT 特征匹配

由于 SIFT 描述子是 128 维浮点向量，通常使用欧氏距离衡量两个描述子的差异：

$$
d(d_i,d_j)
=
\lVert d_i-d_j\rVert_2.
$$

对于图像 1 中的某个描述子，在图像 2 的所有描述子中寻找距离最小的最近邻。

仅使用最近邻可能会产生误匹配，因此通常还会使用 **Lowe 最近邻比值检验**。

设最近邻距离为 $d_1$，次近邻距离为 $d_2$，若满足：

$$
\frac{d_1}{d_2}<\tau,
$$

则接受该匹配。

常用阈值为：

$$
\tau=0.7\sim0.8.
$$

比值较小说明最佳匹配明显优于第二最佳匹配，匹配歧义较小；如果两个距离接近，则说明存在多个相似特征，应当删除该匹配。

还可以使用双向匹配，只保留两张图像中互为最近邻的特征点。

#### 10. 几何验证

描述子匹配只表示两个局部区域外观相似，并不能保证它们符合真实的相机几何关系。因此，还需要使用 **RANSAC** 估计几何模型并剔除错误匹配。

根据场景和相机条件，可以选择：

- 平面场景或纯旋转：估计单应矩阵 $H$；
- 一般未标定两视图：估计基本矩阵 $F$；
- 已知相机内参：估计本质矩阵 $E$。

对应约束分别为：

$$
x'\sim Hx,
$$

$$
x'^T F x=0,
$$

$$
\hat{x}'^T E\hat{x}=0.
$$

最终保留下来的匹配应同时满足：

$$
\boxed{
\text{描述子相似}
+
\text{几何关系一致}
}
$$

#### 11. SIFT 核心总结

SIFT 可以概括为：

$$
\boxed{
\text{SIFT}
=
\text{高斯尺度空间}
+
\text{DoG 极值检测}
+
\text{梯度方向归一化}
+
\text{128 维梯度描述子}
}
$$

各部分功能分别为：

- 高斯尺度空间：观察不同大小的局部结构；
- DoG：寻找空间和尺度方向上的稳定极值点；
- 主方向分配：处理图像旋转；
- 128 维描述子：描述关键点周围的梯度分布；
- 欧氏距离和比值检验：完成特征匹配；
- RANSAC：利用几何关系剔除错误匹配。

与 ORB 相比，SIFT 的计算量更大、描述子占用空间更多，但它对尺度变化、旋转、光照变化和一定程度的视角变化通常更加稳定，因此常用于离线三维重建、SfM 和图像检索。

## 三角化算法（match + pose -> 3D point）

### 概念

三角化用于根据**同一个空间点在两张图像中的匹配位置**，以及两台相机的已知位姿，恢复该点的三维坐标。

已知：

- 两张图像中的匹配点 $\mathbf{x}_1=(u_1,v_1)$ 和 $\mathbf{x}_2=(u_2,v_2)$
- 相机内参矩阵 $K$
- 两台相机的位姿 $T_{cw}^{(1)}$ 和 $T_{cw}^{(2)}$

目标是求空间点：

$$
\mathbf{X}_w=
\begin{bmatrix}
X\\
Y\\
Z
\end{bmatrix}
$$

直观上，可以从两个相机中心分别经过对应像素点发出一条空间射线。理想情况下，两条射线的交点就是该空间点。

### 核心计算思路

相机投影矩阵为：

$$
P=K
\begin{bmatrix}
R & t
\end{bmatrix}
$$

三维点和像素点满足投影关系：

$$
\tilde{\mathbf{x}}\sim P\tilde{\mathbf{X}}
$$

其中：

$$
\tilde{\mathbf{x}}=
\begin{bmatrix}
u\\
v\\
1
\end{bmatrix},
\qquad
\tilde{\mathbf{X}}=
\begin{bmatrix}
X\\
Y\\
Z\\
1
\end{bmatrix}
$$

根据两张图像中的对应点，可以建立齐次线性方程：

$$
A\tilde{\mathbf{X}}=0
$$

求解后得到齐次三维坐标：

$$
\tilde{\mathbf{X}}=
\begin{bmatrix}
X'\\
Y'\\
Z'\\
W
\end{bmatrix}
$$

再进行齐次除法：

$$
\mathbf{X}_w=
\begin{bmatrix}
X'/W\\
Y'/W\\
Z'/W
\end{bmatrix}
$$

三角化后通常还要过滤：

- $W$ 接近零的点
- 位于相机后方的点
- 重投影误差过大的点
- 视差角过小的点

### 核心调包代码

```python
P1 = K @ Tcw1[:3, :]
P2 = K @ Tcw2[:3, :]

points4d = cv2.triangulatePoints(P1, P2, points1.T, points2.T)
points3d = (points4d[:3] / points4d[3]).T
```

---

## PnP算法（match + 3D point -> pose）

### 概念

PnP，即 Perspective-$n$-Point，用于根据一组三维地图点及其在当前图像中的二维像素位置，求当前相机位姿。

已知：

- 三维地图点 $\mathbf{X}_i$
- 对应的二维像素点 $\mathbf{x}_i$
- 相机内参矩阵 $K$

目标是求相机的旋转矩阵 $R$ 和平移向量 $t$，即：

$$
T_{cw}=
\begin{bmatrix}
R & t\\
0 & 1
\end{bmatrix}
$$

在增量三维重建中，PnP 用于将一张新图像注册到已有三维地图中。

### 核心计算思路

三维点从世界坐标系变换到相机坐标系：

$$
\mathbf{X}_{c,i}
=
R\mathbf{X}_{w,i}+t
$$

然后投影到图像平面：

$$
\tilde{\mathbf{x}}_i
\sim
K\left(R\mathbf{X}_{w,i}+t\right)
$$

设相机坐标为：

$$
\mathbf{X}_{c,i}=
\begin{bmatrix}
X_{c,i}\\
Y_{c,i}\\
Z_{c,i}
\end{bmatrix}
$$

对应的像素坐标为：

$$
u_i=f_x\frac{X_{c,i}}{Z_{c,i}}+c_x
$$

$$
v_i=f_y\frac{Y_{c,i}}{Z_{c,i}}+c_y
$$

PnP 的目标是寻找 $R$ 和 $t$，使三维点的预测投影位置尽量接近实际像素位置：

$$
\min_{R,t}
\sum_i
\left\|
\mathbf{x}_i-
\pi(K,R,t,\mathbf{X}_i)
\right\|_2^2
$$

其中，$\pi(\cdot)$ 表示三维点到图像平面的投影过程。

实际匹配中可能包含错误对应，因此通常使用 PnP 与 RANSAC 结合，筛除重投影误差过大的外点。

### 核心调包代码

```python
success, rvec, tvec, inliers = cv2.solvePnPRansac(
    points3d,
    points2d,
    K,
    None,
)

R, _ = cv2.Rodrigues(rvec)
```

构造世界坐标到相机坐标的变换矩阵：

```python
Tcw = np.eye(4)
Tcw[:3, :3] = R
Tcw[:3, 3] = tvec.reshape(3)
```

---

## BA (Bundle Adjustment) 优化

### 概念

Bundle Adjustment，简称 BA，用于联合优化：

- 所有相机位姿
- 所有三维地图点

PnP 和三角化通常是逐帧计算的，因此误差可能逐渐累积。BA 利用多个相机对多个三维点的二维观测，对整个重建结果进行统一优化。

一条观测包含：

- 相机编号 $i$
- 三维点编号 $j$
- 三维点在相机 $i$ 中的实际像素坐标 $\mathbf{x}_{ij}$

### 核心计算思路

第 $j$ 个三维点在第 $i$ 台相机中的预测像素位置为：

$$
\hat{\mathbf{x}}_{ij}
=
\pi(K,R_i,t_i,\mathbf{X}_j)
$$

该观测的重投影残差为：

$$
\mathbf{r}_{ij}
=
\hat{\mathbf{x}}_{ij}
-
\mathbf{x}_{ij}
$$

BA 的目标是同时调整所有相机位姿和三维点，使总重投影误差最小：

$$
\min_{\{R_i,t_i,\mathbf{X}_j\}}
\sum_{(i,j)\in\mathcal{O}}
\left\|
\pi(K,R_i,t_i,\mathbf{X}_j)
-
\mathbf{x}_{ij}
\right\|_2^2
$$

其中，$\mathcal{O}$ 表示全部有效二维观测的集合。

每台相机通常使用六个参数表示：

$$
\mathbf{p}_i=
\begin{bmatrix}
r_x &
r_y &
r_z &
t_x &
t_y &
t_z
\end{bmatrix}^{T}
$$

其中：

- $r_x,r_y,r_z$ 是 Rodrigues 旋转向量
- $t_x,t_y,t_z$ 是平移向量

所有相机参数和三维点坐标共同组成优化变量：

$$
\mathbf{z}
=
\begin{bmatrix}
\mathbf{p}_1,\ldots,\mathbf{p}_M,
\mathbf{X}_1,\ldots,\mathbf{X}_N
\end{bmatrix}
$$

为了消除单目重建中的坐标系和尺度自由度，通常固定第一台或前两台相机。

### 核心调包代码

```python
result = scipy.optimize.least_squares(
    residual_function,
    initial_parameters,
    jac_sparsity=jacobian_sparsity,
    method="trf",
    loss="soft_l1",
)
```

其中，残差函数的核心计算为：

```python
residual = projected_point - observed_point
```

BA 前后通常使用重投影均方根误差评价优化效果：

$$
\mathrm{RMSE}
=
\sqrt{
\frac{1}{2|\mathcal{O}|}
\sum_{(i,j)\in\mathcal{O}}
\left\|
\mathbf{r}_{ij}
\right\|_2^2
}
$$

理想情况下应满足：

$$
\mathrm{RMSE}_{\mathrm{after}}
<
\mathrm{RMSE}_{\mathrm{before}}
$$