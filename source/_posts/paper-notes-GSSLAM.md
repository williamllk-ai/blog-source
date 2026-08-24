---
title: 【Paper Notes】- GS-SLAM
date: 2026-07-28 17:40:02
tags: [3DV, SLAM, CV]
---

# GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting

## 一、论文信息

- **论文名称**：GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting
- **任务类型**：RGB-D 稠密视觉 SLAM
- **输入**：连续 RGB-D 图像、已知相机内参
- **输出**：
  - 每一帧的相机位姿
  - 全局 3D Gaussian 地图
- **核心思想**：利用可微 Gaussian Splatting 同时完成相机位姿估计、在线地图扩展和稠密场景重建，即完整SLAM系统。

系统输入为：

$$
\left\{ C_t, D_t \right\}_{t=1}^{T}
$$

其中：

- $C_t$：第 $t$ 帧 RGB 图像
- $D_t$：第 $t$ 帧深度图

系统最终估计：

$$
\left\{ P_t \right\}_{t=1}^{T}
$$

以及 Gaussian 地图：

$$
\mathcal{G} = \left\{ G_i \right\}_{i=1}^{N}
$$

---

## 二、创新点

### 1. 基于 3D Gaussian Splatting 的 RGB-D SLAM

将 3D Gaussian 场景表示和可微光栅化引入在线 RGB-D SLAM，通过渲染误差优化：

- 当前相机位姿
- Gaussian 地图参数

### 2. Adaptive 3D Gaussian Expansion

根据累计 opacity 和深度误差：

- 为新观测区域添加 Gaussian
- 抑制漂浮在真实表面前方的错误 Gaussian
- 配合 clone、split 和 pruning 管理地图密度

### 3. Coarse-to-Fine Tracking

相机跟踪分为：

$$
\text{低分辨率粗定位}
\rightarrow
\text{深度筛选可靠 Gaussian}
\rightarrow
\text{全分辨率精定位}
$$

### 4. Differentiable Pose Estimation 与 Bundle Adjustment

推导 Gaussian Rasterization 对相机位姿的梯度，并在关键帧上联合优化：

$$
\text{Gaussian 地图}
+
\text{关键帧相机位姿}
$$

---

# 三、3D Gaussian 场景表示

场景表示为：

$$
\mathcal{G}
=
\left\{
G_i =
\left(
X_i,
\Sigma_i,
\Lambda_i,
Y_i
\right)
\right\}_{i=1}^{N}
$$

其中：

| 参数 | 含义 |
|---|---|
| $X_i \in \mathbb{R}^3$ | Gaussian 三维中心 |
| $\Sigma_i \in \mathbb{R}^{3 \times 3}$ | 三维各向异性协方差 |
| $\Lambda_i$ | Gaussian 的 opacity 参数 |
| $Y_i \in \mathbb{R}^{12}$ | 一阶球谐颜色系数 |

一阶球谐包含 $4$ 个基函数，每个基函数分别具有 RGB 三个系数，因此：

$$
4 \times 3 = 12
$$

此为 3DGS 的简化版本，以下是与3DGS类似的处理。

## 3.1 协方差参数化

为保证协方差矩阵有效，将其表示为：

$$
\Sigma_i
=
R_i S_i S_i^{T} R_i^{T}
$$

其中：

- $S_i$：三个方向上的尺度
- $R_i$：由四元数表示的旋转矩阵

## 3.2 Gaussian 投影

三维 Gaussian 在相机位姿 $P$ 下投影到图像平面。

Gaussian 中心的二维投影为：

$$
m_i
=
\pi(PX_i)
$$

其中 $\pi(\cdot)$ 是针孔相机投影函数。

二维投影协方差为：

$$
\Sigma_i'
=
J P^{-1} \Sigma_i P^{-T} J^{T}
$$

其中 $J$ 是透视投影函数在 Gaussian 中心位置处的 Jacobian。


## 3.3 RGB 渲染

将当前像素处的 Gaussian 按深度从前到后排列，渲染颜色为：

$$
\hat{C}(p)
=
\sum_{i \in \mathcal{N}(p)}
c_i
\alpha_i(p)
\prod_{j<i}
\left(
1-\alpha_j(p)
\right)
$$

其中：

- $c_i$：第 $i$ 个 Gaussian 的颜色
- $\alpha_i(p)$：Gaussian 在像素 $p$ 上的实际 alpha
- $\mathcal{N}(p)$：覆盖像素 $p$ 的 Gaussian 集合

Gaussian 在像素上的 alpha 可以理解为：

$$
\alpha_i(p)
=
\operatorname{opacity}_i
\cdot
\exp
\left[
-\frac{1}{2}
(p-m_i)^T
(\Sigma_i')^{-1}
(p-m_i)
\right]
$$

注意：

$$
\alpha_i(p) \neq \Lambda_i
$$

$\Lambda_i$ 是 Gaussian 自身保存的 opacity 参数，而 $\alpha_i(p)$ 还取决于 Gaussian 的二维投影中心和二维协方差。


## 3.4 Depth 渲染

将颜色 $c_i$ 替换为 Gaussian 中心在相机坐标系中的深度 $d_i$：

$$
\hat{D}(p)
=
\sum_{i \in \mathcal{N}(p)}
d_i
\alpha_i(p)
\prod_{j<i}
\left(
1-\alpha_j(p)
\right)
$$

---

# 四、论文 Pipeline

GS-SLAM 的整体流程可以重新整理为：

$$
\boxed{
\text{初始化}
\rightarrow
\text{逐帧 Tracking}
\rightarrow
\text{关键帧判定}
\rightarrow
\text{Gaussian Expansion}
\rightarrow
\text{Mapping}
\rightarrow
\text{Bundle Adjustment}
}
$$

---

## 模块 1：第一帧初始化

第一帧没有历史地图，因此将第一帧相机坐标系定义为世界坐标系：

$$
P_1 = I
$$

从第一张 RGB-D 图像中均匀采样一半像素：

$$
M = \frac{HW}{2}
$$

对于像素 $(u,v)$，利用深度反投影：

$$
X_i
=
D(u,v)
K^{-1}
\begin{bmatrix}
u \\
v \\
1
\end{bmatrix}
$$

利用反投影点初始化 Gaussian：

$$
G_i
=
\left(
X_i,
\Sigma_{\mathrm{init}},
\Lambda_{\mathrm{init}},
C_i
\right)
$$

初始化方式：

- Gaussian 中心来自深度反投影
- 零阶球谐颜色由像素 RGB 初始化
- opacity 使用预设初值
- 协方差根据局部点密度初始化

只采样一半像素的原因是为后续 Gaussian 的 clone、split 和在线扩展保留空间。


## 模块 2：位姿初值预测

对于新帧，系统利用前两帧相机运动进行恒速预测。

设上一段相对运动为：

$$
\Delta P_{t-1}
=
P_{t-1} P_{t-2}^{-1}
$$

则当前帧初始位姿可表示为：

$$
P_t^{(0)}
\approx
\Delta P_{t-1} P_{t-1}
$$



## 模块 3：Coarse-to-fine Tracking

Tracking 阶段固定 Gaussian 地图，只优化当前相机位姿。

主文中的 Tracking Loss 为颜色 $L_1$ 损失：

$$
L_{\mathrm{track}}
=
\sum_{m=1}^{M}
\left|
C_m
-
\hat{C}_m
\right|_1
$$

优化目标为：

$$
P_t^{*}
=
\arg\min_{P_t}
L_{\mathrm{track}}
$$

Coarse 阶段在半分辨率下渲染：

$$
\frac{H}{2}
\times
\frac{W}{2}
$$

经过 $T_c$ 次优化得到粗位姿：

$$
P_c
$$

接着利用粗位姿 $P_c$，将当前视野中的 Gaussian 投影到输入深度图。

比较：

- Gaussian 投影深度 $d_i$
- 对应像素的传感器深度 $D_i$

只保留满足以下条件的 Gaussian：

$$
\mathcal{G}_{\mathrm{selected}}
=
\left\{
G_i \in \mathcal{G}
\mid
\left|
D_i-d_i
\right|
\leq
\varepsilon
\right\}
$$

该步骤可以排除：

- 漂浮在表面前方的 floater
- 深度位置错误的 Gaussian
- 历史建图中的局部伪影

在Fine阶段，只使用筛选后的可靠 Gaussian：

$$
\mathcal{G}_{\mathrm{selected}}
$$

在完整分辨率下渲染：

$$
\hat{I}_f
=
F
\left(
u,
v,
\mathcal{G}_{\mathrm{selected}},
P
\right)
$$

然后继续优化相机位姿，得到最终结果：

$$
P_t
$$

未被 selected Gaussian 覆盖的像素不会产生有效的 pose gradient，因此 Fine Tracking 实际只利用可靠历史地图覆盖的区域。

因此 GS-SLAM 的 Coarse-to-Fine Tracking 是：

$$
\boxed{
\text{低分辨率粗定位}
\rightarrow
\text{深度筛选可靠 Gaussian}
\rightarrow
\text{全分辨率精定位}
}
$$

它不仅是图像分辨率由低到高，也将参与优化的地图从全部 Gaussian 变为可靠 Gaussian 子集。


## 模块 4：关键帧判定

当前帧完成 Tracking 后，系统根据以下因素判断是否加入关键帧数据库：

1. 当前图像中 reliable region 所占比例
2. 当前帧与最近关键帧之间的差异是否超过阈值 $\mu_k$

非关键帧主要用于 Tracking，关键帧还会触发：

- Gaussian Expansion
- Mapping
- Bundle Adjustment

---

## 模块 5：Adaptive Gaussian Expansion

对于选中的关键帧，系统首先使用历史 Gaussian 地图渲染：

$$
\hat{C},
\quad
\hat{D},
\quad
T
$$

其中累计 opacity 为：

$$
T(p)
=
\sum_i
\alpha_i(p)
\prod_{j<i}
\left(
1-\alpha_j(p)
\right)
$$

$T(p)$ 表示当前 Gaussian 地图对像素 $p$ 的覆盖程度。

### 5.1 Gaussian Adding

像素满足以下任意条件时，被认为无法由当前地图可靠解释：

$$
T(p) < \tau_T
$$

或：

$$
\left|
D(p)-\hat{D}(p)
\right|
>
\tau_D
$$

两个条件分别表示：

1. 当前地图在该像素覆盖不足
2. 当前地图渲染的几何与真实深度不一致

系统利用真实深度将这些像素反投影到三维空间，并创建新的 Gaussian：

$$
\mathcal{G}
\leftarrow
\mathcal{G}
\cup
\mathcal{G}_{\mathrm{new}}
$$


### 5.2 Floater Suppression

对于当前相机视锥内的 Gaussian，系统比较其三维位置与输入深度对应的真实表面。

若 Gaussian 漂浮在真实表面前方，则降低其 opacity：

$$
\Lambda_i
\leftarrow
\eta
\Lambda_i
$$

其中：

$$
\eta \ll 1
$$

该操作不是立即从数组中删除 Gaussian，而是先让其变得近乎透明，之后再通过低 opacity pruning 移除。

因此 Adaptive Expansion 可以概括为：

$$
\boxed{
\text{Adding 解决地图缺失}
+
\text{Floater Suppression 解决错误几何}
}
$$


## 模块 6：Keyframe Mapping

完成 Gaussian 的添加和抑制后，固定关键帧位姿，优化 Gaussian 地图参数。

颜色损失为：

$$
L_c
=
\sum_{m=1}^{HW}
\left|
C_m
-
\hat{C}_m
\right|
$$

深度损失为：

$$
L_d
=
\sum_{m=1}^{HW}
\left|
D_m
-
\hat{D}_m
\right|
$$

优化的 Gaussian 参数包括：

$$
X_i,
\quad
\Sigma_i,
\quad
\Lambda_i,
\quad
Y_i
$$

分别对应：

- 三维位置
- Gaussian 尺度和旋转
- opacity
- 球谐颜色

这一阶段可以概括为：

$$
\boxed{
\text{固定关键帧位姿}
\rightarrow
\text{优化 Gaussian 地图}
}
$$


## 模块 7：Bundle Adjustment

系统从关键帧数据库中随机选择 $K$ 个关键帧，对 Gaussian 地图和关键帧位姿进行联合优化。

BA 损失为：

$$
L_{\mathrm{BA}}
=
\frac{1}{K}
\sum_{k=1}^{K}
\sum_{m=1}^{HW}
\left[
\left|
D_{k,m}
-
\hat{D}_{k,m}
\right|_1
+
\lambda_m
\left|
C_{k,m}
-
\hat{C}_{k,m}
\right|_1
\right]
$$

优化目标为：

$$
\min_{P,\mathcal{G}}
L_{\mathrm{BA}}
$$

BA 分为两个阶段：

### 前一半迭代

固定相机位姿，只优化 Gaussian 地图：

$$
\mathcal{G}
$$

### 后一半迭代

联合优化：

$$
P,
\quad
\mathcal{G}
$$

这样可以先让地图趋于稳定，再调整历史关键帧位姿，减小不准确地图对 pose 的干扰。

---

# 五、GS-SLAM 特色 Differentiable Pose Estimation

Tracking 时 Gaussian 地图固定，相机位姿 $P$ 会影响 Gaussian 的二维投影。

完整依赖关系为：

$$
P
\rightarrow
\left(
m_i,
\Sigma_i',
c_i
\right)
\rightarrow
\alpha_i
\rightarrow
\hat{C}
\rightarrow
L_c
$$

理论上的位姿梯度为：

$$
\frac{\partial L_c}{\partial P}
=
\frac{\partial L_c}{\partial C}
\left(
\frac{\partial C}{\partial c_i}
\frac{\partial c_i}{\partial P}
+
\frac{\partial C}{\partial \alpha_i}
\frac{\partial \alpha_i}{\partial P}
\right)
$$

其中：

$$
\frac{\partial \alpha_i}{\partial P}
=
\frac{\partial \alpha_i}{\partial \Sigma_i'}
\frac{\partial \Sigma_i'}{\partial P}
+
\frac{\partial \alpha_i}{\partial m_i}
\frac{\partial m_i}{\partial P}
$$

GS-SLAM 在 Tracking 中进行了两项简化。

### 1. 忽略颜色对位姿的梯度

虽然地图使用一阶球谐函数，但 Tracking 只关注 view-independent color，因此：

$$
\frac{\partial c_i}{\partial P}
=
0
$$

### 2. 忽略协方差对位姿的梯度

为提高效率，论文进一步近似：

$$
\frac{\partial \Sigma_i'}{\partial P}
\approx
0
$$

因此实际主要保留：

$$
\boxed{
\frac{\partial L_c}{\partial P}
\approx
\frac{\partial L_c}{\partial C}
\frac{\partial C}{\partial \alpha_i}
\frac{\partial \alpha_i}{\partial m_i}
\frac{\partial m_i}{\partial P}
}
$$


---

# 六、与原始 3D Gaussian Splatting 的联系

GS-SLAM 保留了原始 3DGS 的核心表示和渲染机制：

- 各向异性 Gaussian
- 尺度和旋转参数
- 球谐颜色
- 可微 Gaussian Rasterization
- Alpha Blending
- Clone、Split 和 Pruning

两者区别如下：

| 对比维度 | 原始 3DGS | GS-SLAM |
|---|---|---|
| 主要任务 | 离线新视角合成 | 在线 RGB-D SLAM |
| 相机位姿 | 由 SfM 预先获得 | 在线估计 |
| 初始化方式 | SfM 稀疏点云 | 第一帧深度反投影 |
| Gaussian 形状 | 各向异性椭球 | 各向异性椭球 |
| 外观表示 | 球谐函数 | 一阶球谐函数 |
| 渲染输出 | RGB | RGB、Depth、Opacity |
| 地图增长 | Clone、Split | RGB-D Adding、Floater Suppression、Clone、Split |
| 优化变量 | Gaussian 参数 | Gaussian 参数和相机位姿 |
| 运行模式 | 离线全局优化 | 在线 Tracking、Mapping 和 BA |

GS-SLAM 对原始 3DGS 的主要改造是：

$$
\boxed{
\text{在线位姿估计}
+
\text{RGB-D 地图扩张}
+
\text{错误 Gaussian 抑制}
+
\text{关键帧 Bundle Adjustment}
}
$$

---

# 七、与 SplaTAM 的联系与区别

GS-SLAM 与 SplaTAM 的宏观流程非常接近：

$$
\boxed{
\text{Tracking}
\rightarrow
\text{Gaussian Densification}
\rightarrow
\text{Map Update}
}
$$

两者都采用：

- RGB-D 输入
- 显式 Gaussian 地图
- 可微渲染直接法 Tracking
- 深度反投影初始化新 Gaussian
- 关键帧地图优化

它们的差异主要体现在各模块的具体实现方式。

| 对比部分 | SplaTAM | GS-SLAM |
|---|---|---|
| Gaussian 形状 | 各向同性球形 | 各向异性椭球 |
| 颜色表示 | 固定 RGB | 一阶球谐函数 |
| Tracking Loss | RGB 与 Depth | 主文采用 RGB Loss |
| 有效区域筛选 | Silhouette 像素 Mask | Gaussian 覆盖和深度一致性筛选 |
| Tracking 方式 | 直接迭代优化 | Coarse-to-Fine |
| 地图扩张 | Silhouette 和深度误差 | 累计 Opacity 和深度误差 |
| 错误 Gaussian 处理 | Mapping 中进行 Culling | 显式抑制 Floater |
| Map Update | 固定 Pose 优化地图 | 固定 Pose Mapping 和 Joint BA |
| 设计重点 | 简化表示和统一流程 | 保留 3DGS 表达能力并增强鲁棒性 |


## SplaTAM Tracking

SplaTAM 使用 RGB 和 Depth Loss，并通过 silhouette 限制有效区域：

$$
L_t
=
\sum_p
\mathbf{1}
\left[
S(p) > 0.99
\right]
\left[
L_1
\left(
D(p)
\right)
+
0.5
L_1
\left(
C(p)
\right)
\right]
$$

其核心是：

$$
\text{利用像素级 Silhouette Mask 选择已建图区域}
$$

## GS-SLAM Tracking

GS-SLAM 主文中的 Tracking Loss 为：

$$
L_{\mathrm{track}}
=
\sum_m
\left|
C_m
-
\hat{C}_m
\right|
$$

然后通过：

$$
P_c
\rightarrow
\left|
D_i-d_i
\right|
\leq
\varepsilon
\rightarrow
\mathcal{G}_{\mathrm{selected}}
$$

筛选可靠 Gaussian。

因此，两者可以概括为：

$$
\boxed{
\begin{aligned}
\text{SplaTAM：}
&\quad
\text{像素级 Silhouette-Guided Tracking}
\\
\text{GS-SLAM：}
&\quad
\text{Gaussian 级 Depth-Filtered Coarse-to-Fine Tracking}
\end{aligned}
}
$$

两篇论文属于高度相似的 Gaussian RGB-D SLAM 范式，区别主要不是整体流程，而是：

---

# 八、局限性

## 1. 高度依赖深度质量

深度图被用于：

- 第一帧初始化
- 新 Gaussian 添加
- Reliable Gaussian 筛选
- Floater 检测
- Mapping
- Bundle Adjustment

因此深度噪声会直接影响地图和位姿精度。

## 2. 地图内存较大

GS-SLAM 保留了：

- 各向异性协方差
- Gaussian 旋转
- 一阶球谐系数

因此单个 Gaussian 参数量较大，场景规模增大时内存占用明显上升。

## 3. Tracking 仍然属于局部优化

当出现以下情况时，系统可能不稳定：

- 相邻帧运动过大
- 当前帧和历史地图重叠过小
- Reliable Gaussian 数量不足
- 场景纹理较弱
- 深度图噪声较大

## 4. 大尺度场景扩展能力有限

Gaussian 数量会随新区域持续增加，需要进一步研究：

- Gaussian 压缩
- 参数量化
- 地图分块
- 层次化管理
- 长期地图维护

---

# 九、总结

GS-SLAM 可以概括为：

$$
\boxed{
\begin{aligned}
\text{Tracking：}
&\quad
\text{低分辨率粗定位}
\rightarrow
\text{深度筛选可靠 Gaussian}
\rightarrow
\text{全分辨率精定位}
\\
\text{Mapping：}
&\quad
\text{根据 Opacity 和 Depth 添加 Gaussian}
\rightarrow
\text{抑制 Floater}
\rightarrow
\text{RGB-D 优化地图}
\\
\text{Backend：}
&\quad
\text{联合优化关键帧位姿和 Gaussian 地图}
\end{aligned}
}
$$

从系统结构看，GS-SLAM 本质上是：

$$
\boxed{
\text{Gaussian Tracking Frontend}
+
\text{Adaptive Gaussian Mapping}
+
\text{Keyframe Bundle Adjustment}
}
$$

它与 SplaTAM 的整体 SLAM 骨架非常接近。两者的核心区别主要体现在：

- Gaussian 地图表示方式
- Tracking 的可靠区域选择方式
- 地图扩张与错误 Gaussian 处理方式
- 是否显式联合优化关键帧位姿和 Gaussian 地图
