---
title: "【Paper Notes】- SplaTAM"
date: 2026-07-21 12:07:36
tags:
  - "3DV"
  - "CV"
  - "SLAM"
---
# SplaTAM：3D Gaussian based dense RGB-D SLAM

## 论文信息

- **论文题目**：SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM
- **任务类型**：Dense RGB-D SLAM
- **输入**：连续 RGB 图像与对应深度图
- **输出**：
  - 在线估计的**相机轨迹**；
  - 可渲染的 **3D Gaussian 场景地图**。
- **核心表示**：显式、体积化的 3D Gaussian primitives
- **核心思想**：

$$\text{3D Gaussian Splatting} + \text{Camera Tracking} + \text{Online Map Expansion}$$

原始 3DGS 假设相机位姿已由 COLMAP 给定，主要解决离线新视角合成；SplaTAM 则将 Gaussian 表示引入在线 RGB-D SLAM，同时估计相机位姿并持续扩展场景地图。

---
## 1. 研究问题

传统稠密 SLAM 主要采用两类地图表示。

### 1.1 explicit, non-volumetric model

代表方法包括point cloud, surfel, TSDF, mesh

优点是几何位置明确、地图容易局部修改；缺点是：

- tracking 常依赖稀疏三维特征或几何对应；
- 对低纹理和大幅运动较敏感；
- 新视角渲染容易产生空洞和不连续；
- 难以同时获得高质量几何和真实感外观。

### 1.2 implicit, volumetric model

代表方法是 NeRF 和神经隐式 SLAM：

$$F_{\theta}(\mathbf{x},\mathbf{d})\rightarrow(\sigma,\mathbf{c})$$

它们支持可微体渲染和稠密光度优化，但存在：

- 沿射线采样和网络查询计算量大；
- 在线渲染与优化速度慢；
- 场景存储在网络权重中，难以直接编辑；
- 地图空间边界不明确；
- 持续学习新区域时可能发生灾难性遗忘。

SplaTAM 希望获得一种兼具两类表示优势的地图：

$$\boxed{\text{Explicit} + \text{Volumetric} + \text{Differentiable} + \text{Fast Rendering}}$$

---
## 2. 核心贡献

### 2.1 使用 3D Gaussian 作为 SLAM 地图

每个 Gaussian 都具有明确的位置、空间范围、颜色和不透明度，既能直接增删，又能通过 splatting 实现连续、高质量渲染。此外，作者对 Gaussian primitive 进行各向同性的简化。

### 2.2 利用稠密 RGB-D 误差进行相机跟踪

SplaTAM 不依赖稀疏特征点，而是通过可微渲染比较整张 RGB-D 图像，在实时条件下优化相机位姿。

### 2.3 使用 silhouette 表示地图覆盖范围

渲染得到的 silhouette 表示当前 Gaussian map 在某个视角下的累计 opacity，可用于区分：

- 已经建图的像素；
- 尚未建图的新区域。

因此 silhouette 同时服务于：

- Tracking：只使用已有地图区域估计位姿；
- Densification：在未覆盖区域增加新 Gaussian。

### 2.4 结构化在线扩展地图

对于新观测区域，利用输入深度将像素反投影到三维空间，并直接添加新的 Gaussian，无需重新训练整个隐式网络。

---
## 3. 整体 Pipeline

对于第 $t + 1$ 帧 RGB-D 输入：

$$\left( I_{t + 1}^{GT},D_{t + 1}^{GT} \right)$$

系统维护当前 Gaussian map：

$$\mathcal{G}_{t} = \left\{ G_{i} \right\}_{i = 1}^{N_{t}}$$

整体流程为：

$$\boxed{\text{RGB-D Frame}\rightarrow\text{Camera Tracking}\rightarrow\text{Gaussian Densification}\rightarrow\text{Map Update}}$$

{% asset_img pipeline.png pipeline %}

具体过程：

1.  根据前一帧位姿初始化当前相机位姿；
2.  固定 Gaussian map，优化当前相机位姿；
3.  渲染 silhouette 和 depth，检测尚未建图或地图深度错误的区域；
4.  根据输入 RGB-D 为这些区域创建新 Gaussian；
5.  选择当前帧及具有视野重叠的历史关键帧；
6.  固定相机位姿，联合优化 Gaussian map 参数；
7.  处理下一帧。

变量关系为：

| 阶段          | 优化变量             | 固定变量                       |
|---------------|----------------------|--------------------------------|
| Tracking      | 相机位姿 $T_{t + 1}$ | Gaussian map $\mathcal{G}_{t}$ |
| Densification | 新增 Gaussian        | 当前位姿与已有地图             |
| Map Update    | Gaussian map 参数    | 已估计相机位姿                 |

---
## 4. Method

### 4.1 Gaussian 地图表示与可微渲染

#### 4.1.1 Gaussian 参数

SplaTAM 对原始 3DGS 进行简化，每个 Gaussian 表示为：

$$G_{i} = \left( \mathbf{\mu}_{i},r_{i},\mathbf{c}_{i},o_{i} \right)$$

其中：

- $\mathbf{\mu}_{i} \in \mathbb{R}^{3}$ ：三维中心；
- $r_{i} \in \mathbb{R}^{+}$ ：球形 Gaussian 半径；
- $\mathbf{c}_{i} \in \mathbb{R}^{3}$ ：固定 RGB 颜色；
- $o_{i} \in \lbrack 0,1\rbrack$ ：opacity。

SplaTAM 使用**各向同性** Gaussian：

$$\mathbf{\Sigma}_{i} = r_{i}^{2}\mathbf{I}$$

因此三个方向尺度相同，不再需要旋转四元数。

同时去除原始 3DGS 的视角相关球谐颜色：

$$\mathbf{c}_{i}(\mathbf{d})\rightarrow\mathbf{c}_{i}$$

即**每个 Gaussian 只保存一个与观察方向无关的固定 RGB**。

---
#### 4.1.2 从 3D Gaussian 投影到 2D Gaussian

设相机外参 $E_{t}$ 将世界坐标转换到相机坐标。

高斯中心在相机坐标系中的位置为：

$$\mathbf{\mu}_{i}^{c} = E_{t}\begin{bmatrix}
\mathbf{\mu}_{i} \\
1
\end{bmatrix}$$

其深度为：

$$d_{i} = \left( \mathbf{\mu}_{i}^{c} \right)_{z}$$

通过相机内参 $K$ 投影得到二维中心：

$$\mathbf{\mu}_{i}^{2D} = \pi\left( K\mathbf{\mu}_{i}^{c} \right)$$

由于三维 Gaussian 是球形，其二维投影近似为圆形 Gaussian，投影半径为：

$$r_{i}^{2D} = \frac{fr_{i}}{d_{i}}$$

其中 $f$ 为焦距。

---
#### 4.1.3 单个 Gaussian 的像素贡献

对于像素 $\mathbf{p}$ ，第 $i$ 个 Gaussian 的局部贡献为：

$$f_{i}(\mathbf{p}) = o_{i}\exp\left( - \frac{\left\| \mathbf{p} - \mathbf{\mu}_{i}^{2D} \right\|^{2}}{2\left( r_{i}^{2D} \right)^{2}} \right)$$

其中：

- 距离投影中心越近，贡献越大；
- $o_{i}$ 决定最大不透明度；
- $r_{i}^{2D}$ 决定投影覆盖范围。

所有 Gaussian 按照深度从近到远排序。

---
#### 4.1.4 RGB 渲染

像素颜色为：

$$\hat{\mathbf{C}}(\mathbf{p}) = \sum\limits_{i = 1}^{N}\mathbf{c}_{i}f_{i}(\mathbf{p})\prod\limits_{j = 1}^{i - 1}\left( 1 - f_{j}(\mathbf{p}) \right)$$

定义透射率：

$$T_{i}(\mathbf{p}) = \prod\limits_{j = 1}^{i - 1}\left( 1 - f_{j}(\mathbf{p}) \right)$$

则：

$$\hat{\mathbf{C}}(\mathbf{p}) = \sum\limits_{i}T_{i}(\mathbf{p})f_{i}(\mathbf{p})\mathbf{c}_{i}$$

---
#### 4.1.5 Depth 渲染

将颜色 $\mathbf{c}_{i}$ 替换为 Gaussian 深度 $d_{i}$ ：

$$\hat{D}(\mathbf{p}) = \sum\limits_{i = 1}^{N}d_{i}f_{i}(\mathbf{p})\prod\limits_{j = 1}^{i - 1}\left( 1 - f_{j}(\mathbf{p}) \right)$$

该结果用于与输入深度图比较，为 Tracking 和 Mapping 提供几何约束。

---
#### 4.1.6 Silhouette 渲染

Silhouette 是累计 opacity：

$$\hat{S}(\mathbf{p}) = \sum\limits_{i = 1}^{N}f_{i}(\mathbf{p})\prod\limits_{j = 1}^{i - 1}\left( 1 - f_{j}(\mathbf{p}) \right)$$

它也可以理解为：

$$\hat{S}(\mathbf{p}) = 1 - \prod\limits_{i = 1}^{N}\left( 1 - f_{i}(\mathbf{p}) \right)$$

其含义为：

- $\hat{S}(\mathbf{p})$ 较大：该像素已经被 Gaussian map 覆盖；
- $\hat{S}(\mathbf{p})$ 较小：该像素对应未建图区域。

---
### 4.2 初始化与相机 Tracking

#### 4.2.1 第一帧初始化

第一帧没有已有地图，因此跳过 Tracking，并设相机位姿为单位矩阵：

$$T_{1} = \mathbf{I}_{4 \times 4}$$

这等价于将第一帧相机坐标系定义为世界坐标系。

由于初始 Gaussian map 为空：

$${\hat{S}}_{1}(\mathbf{p}) = 0$$

因此第一帧中所有具有有效深度的像素都用于创建 Gaussian。

对像素：

$$\mathbf{p} = (u,v)$$

其相机坐标系三维位置为：

$$\mathbf{x}_{c} = D^{GT}(\mathbf{p})K^{- 1}\begin{bmatrix}
u \\
v \\
1
\end{bmatrix}$$

由于第一帧位姿为单位矩阵：

$$\mathbf{\mu}_{new} = \mathbf{x}_{c}$$

新 Gaussian 参数初始化为：

$$\mathbf{c}_{new} = I^{GT}(\mathbf{p})$$

$$o_{new} = 0.5$$

为了使 Gaussian 投影到第一帧图像后具有约一个像素的半径，令：

$$1 = \frac{fr_{new}}{D^{GT}(\mathbf{p})}$$

得到：

$$\boxed{r_{new} = \frac{D^{GT}(\mathbf{p})}{f}}$$

因此第一帧在概念上接近“每个有效深度像素初始化一个 Gaussian”。

---
#### 4.2.2 Tracking 目标

对于第 $t + 1$ 帧，已有地图为 $\mathcal{G}_{t}$ ，需要估计相机位姿：

$$T_{t + 1}$$

Tracking 阶段固定 Gaussian 参数，仅优化相机位姿：

$$T_{t + 1}^{\ast} = \underset{T}{\arg\min}\;\mathcal{L}_{track}(T)$$

由当前位姿渲染：

$${\hat{I}}_{t + 1}(T),\qquad{\hat{D}}_{t + 1}(T),\qquad{\hat{S}}_{t + 1}(T)$$

定义可见区域掩膜：

$$M_{vis}(\mathbf{p}) = \mathbb{I}\left\lbrack {\hat{S}}_{t + 1}(\mathbf{p}) > \tau_{s} \right\rbrack$$

Tracking loss 可概括为：

$$\mathcal{L}_{track} = \sum\limits_{\mathbf{p}}M_{vis}(\mathbf{p})\left\lbrack \lambda_{c}\left\| I_{t + 1}^{GT}(\mathbf{p}) - {\hat{I}}_{t + 1}(\mathbf{p}) \right\|_{1} + \lambda_{d}\left| D_{t + 1}^{GT}(\mathbf{p}) - {\hat{D}}_{t + 1}(\mathbf{p}) \right| \right\rbrack$$

只在 silhouette 覆盖区域计算误差，是因为未建图区域无法由当前地图渲染出来。若将这些区域加入 loss，优化器可能把“地图中缺少新物体”错误解释为“相机位姿不正确”。

因此 Tracking 的原则是：

$$\boxed{\text{只利用已有地图区域定位当前相机}}$$

---
### 4.3 Gaussian Densification

Tracking 得到当前相机位姿后，需要检测当前帧中新出现、但地图尚未表示的区域。

SplaTAM 结合 silhouette 和 depth 进行判断。

#### 4.3.1 条件一：地图未覆盖

若：

$${\hat{S}}_{t + 1}(\mathbf{p}) < \tau_{s}$$

说明该像素附近没有足够的 Gaussian 覆盖，需要添加新的 Gaussian。

---
#### 4.3.2 条件二：观测到地图前方的新几何

即使 silhouette 较大，也可能出现已有 Gaussian 位于真实表面后方的情况。

若：

$$D_{t + 1}^{GT}(\mathbf{p}) < {\hat{D}}_{t + 1}(\mathbf{p})$$

说明真实观测表面比当前地图渲染表面更靠近相机。

同时要求深度误差足够大：

$$\left| D_{t + 1}^{GT}(\mathbf{p}) - {\hat{D}}_{t + 1}(\mathbf{p}) \right| > \tau_{D}$$

综合得到添加 Gaussian 的掩膜：

$$M_{add}(\mathbf{p}) = \mathbb{I}\left\lbrack \hat{S}(\mathbf{p}) < \tau_{s} \right\rbrack \vee \mathbb{I}\left\lbrack D^{GT}(\mathbf{p}) < \hat{D}(\mathbf{p}) \land \left| D^{GT}(\mathbf{p}) - \hat{D}(\mathbf{p}) \right| > \tau_{D} \right\rbrack$$

第一项检测完全未建图区域，第二项检测当前地图未正确表示的前景新表面。

---
#### 4.3.3 新 Gaussian 初始化

对于满足 $M_{add}(\mathbf{p}) = 1$ 的像素，先反投影到相机坐标：

$$\mathbf{x}_{c} = D_{t + 1}^{GT}(\mathbf{p})K^{- 1}\begin{bmatrix}
u \\
v \\
1
\end{bmatrix}$$

再通过当前相机位姿转换到世界坐标：

$$\mathbf{\mu}_{new} = T_{cw}^{t + 1}\begin{bmatrix}
\mathbf{x}_{c} \\
1
\end{bmatrix}$$

其中 $T_{cw}^{t + 1}$ 表示相机坐标到世界坐标的变换。

其余参数初始化为：

$$\mathbf{c}_{new} = I_{t + 1}^{GT}(\mathbf{p})$$

$$o_{new} = 0.5$$

$$r_{new} = \frac{D_{t + 1}^{GT}(\mathbf{p})}{f}$$

最后加入地图：

$$\mathcal{G}_{t + 1}\leftarrow\mathcal{G}_{t} \cup \left\{ G_{new} \right\}$$

Densification 的本质是：

$$\boxed{\text{Silhouette / Depth 检测新区域}\rightarrow\text{Depth 反投影}\rightarrow\text{添加 Gaussian}}$$

---
### 4.4 Map Update 与关键帧优化

Densification 只负责增加新的 Gaussian，新加入和已有 Gaussian 的参数仍然需要进一步优化。

#### 4.4.1 优化目标

给定已经估计的相机位姿：

$$T_{1},T_{2},\ldots,T_{t + 1}$$

固定这些位姿，优化 Gaussian map：

$$\mathcal{G}^{\ast} = \underset{\mathcal{G}}{\arg\min}\;\mathcal{L}_{map}$$

对于所选帧集合 $\mathcal{K}_{t + 1}$ ：

$$\mathcal{L}_{map} = \sum\limits_{k \in \mathcal{K}_{t + 1}}\sum\limits_{\mathbf{p}}\left\lbrack \lambda_{c}\left\| I_{k}^{GT}(\mathbf{p}) - {\hat{I}}_{k}(\mathbf{p}) \right\|_{1} + \lambda_{d}\left| D_{k}^{GT}(\mathbf{p}) - {\hat{D}}_{k}(\mathbf{p}) \right| \right\rbrack$$

通过可微渲染更新：

$$\mathbf{\mu}_{i},\qquad r_{i},\qquad\mathbf{c}_{i},\qquad o_{i}$$

分别修正：

- 三维几何位置；
- Gaussian 覆盖范围；
- RGB 外观；
- opacity 与遮挡关系。

---
#### 4.4.2 为什么需要多帧优化

单帧 RGB-D 只能从一个视角约束 Gaussian。

若同一 Gaussian 在多个关键帧中可见，多帧联合优化可以：

- 减少单帧深度噪声；
- 提高三维位置一致性；
- 避免只对当前视角过拟合；
- 提升新视角渲染质量。

---
#### 4.4.3 关键帧选择

理论上，可以使用从第 $1$ 帧到第 $t + 1$ 帧的所有图像：

$$\sum\limits_{k = 1}^{t + 1}\mathcal{L}_{k}$$

但计算量会随时间不断增加。

实际中只选择：

- 当前帧；
- 最近关键帧；
- 与当前帧具有较大视野重叠的历史关键帧。

选择依据是历史帧与当前帧可见 Gaussian 或视锥范围的重叠程度。

因此 Map Update 实际是一个局部滑动窗口优化：

$$\boxed{\text{当前帧} + \text{重叠关键帧}\rightarrow\text{联合优化 Gaussian Map}}$$

它与传统 SLAM 中的局部 Bundle Adjustment 类似，但优化变量由三维特征点变为 Gaussian 参数。

---
## 5. 与相关论文的联系与创新点

### 5.1 与原始 3DGS 的关系

SplaTAM 继承了原始 3DGS 的：

- 显式 Gaussian 场景表示；
- Gaussian 投影与 splatting；
- 前向 alpha blending；
- 可微渲染；
- 基于图像重建误差的参数优化。

但两者的任务与假设不同。

| 对比项        | 原始 3DGS               | SplaTAM                          |
|---------------|-------------------------|----------------------------------|
| 任务          | 离线新视角合成          | 在线 RGB-D SLAM                  |
| 输入          | 多视角 RGB              | 连续 RGB-D                       |
| 相机位姿      | COLMAP 预先给定         | 在线估计                         |
| 初始地图      | SfM 稀疏点云            | 第一帧深度反投影                 |
| Gaussian 形状 | 各向异性椭球            | 各向同性球                       |
| 协方差        | $\Sigma = RSS^{T}R^{T}$ | $\Sigma = r^{2}I$                |
| 颜色          | 球谐方向相关颜色        | 固定 RGB                         |
| 地图增长      | Clone / Split           | Silhouette + Depth 添加 Gaussian |
| 优化目标      | Gaussian 参数           | 相机位姿与 Gaussian 地图交替优化 |

因此：

$$\boxed{\text{SplaTAM} = \text{简化版 3DGS 表示} + \text{在线 Tracking} + \text{在线 Mapping}}$$

---
### 5.2 与传统显式 SLAM 的关系

传统点云、surfel 或 TSDF SLAM：

- 地图容易直接更新；
- 几何位置明确；
- 但图像渲染质量和新视角合成能力有限；
- tracking 常依赖稀疏特征或几何配准。

SplaTAM 将显式地图原语换成具有连续空间范围的 Gaussian，因此同时获得：

- 显式空间位置；
- 可微稠密渲染；
- 稠密 RGB-D tracking；
- 更高质量的新视角合成。

---
### 5.3 与 NeRF-SLAM 的关系

NeRF-SLAM 同样可以利用 RGB-D 重建误差优化相机和地图，但其场景被编码在神经网络参数中：

$$F_{\theta}(\mathbf{x},\mathbf{d})\rightarrow(\sigma,\mathbf{c})$$

相比之下，SplaTAM：

- 不需要对每条射线进行大量采样；
- 不需要反复查询 MLP；
- 地图由局部 Gaussian primitives 构成；
- 可以直接添加新 Gaussian；
- 新区域扩展不会强制修改整个场景函数；
- 地图空间覆盖范围可由 silhouette 直接得到。

---
### 5.4 主要创新点

#### 创新一：Gaussian-based dense SLAM

首次系统性地将 3D Gaussian 作为在线稠密 RGB-D SLAM 的核心地图表示，同时支持定位、建图和新视角合成。

#### 创新二：Silhouette 驱动的地图感知

通过累计 opacity 构造 silhouette，使系统能够直接判断：

$$\text{Mapped Region}\quad\text{vs.}\quad\text{Unmapped Region}$$

并分别用于 Tracking 和 Densification。

#### 创新三：稠密、实时的相机位姿优化

利用快速 Gaussian rasterization，在实时条件下使用稠密 RGB 和 Depth loss，而不是只使用少量特征点或随机采样像素。

#### 创新四：结构化地图扩展

利用输入深度直接在新区域添加 Gaussian：

$$\text{New Pixel} + \text{Depth} + \text{Camera Pose}\rightarrow\text{New Gaussian}$$

地图扩展是局部、显式且可控的。

#### 创新五：面向在线 SLAM 的表示简化

将原始 3DGS 的：

- 各向异性椭球；
- 旋转参数；
- 高阶球谐颜色；

简化为：

- 球形 Gaussian；
- 单一半径；
- 固定 RGB。

通过牺牲部分视角相关外观表达能力，降低实时优化难度并提升 tracking 稳定性。

---
## 6. 总结

SplaTAM 将原始 3DGS 从：

$$\boxed{\text{已知相机位姿的离线场景优化}}$$

扩展为：

$$\boxed{\text{未知相机位姿的在线 RGB-D SLAM}}$$

其核心闭环为：

$$\boxed{\text{Track}\rightarrow\text{Densify}\rightarrow\text{Map}\rightarrow\text{Repeat}}$$

其中：

- Tracking 利用已有 Gaussian map 的 RGB、Depth 和 Silhouette 渲染结果估计相机位姿；
- Densification 利用 silhouette 与输入 depth 检测并补充新区域；
- Map Update 利用当前帧和重叠关键帧联合优化 Gaussian 参数。

SplaTAM 的关键价值不只是“用 Gaussian 替换传统地图”，而是利用 Gaussian 同时具有：

$$\boxed{\text{显式性} + \text{连续体积范围} + \text{快速可微渲染} + \text{局部可扩展性}}$$

从而RGB-D SLAM，统一相机跟踪、高质量建图和新视角合成。
