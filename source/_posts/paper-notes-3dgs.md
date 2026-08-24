---
title: "【Paper Notes】- 3D Gaussian Splatting"
date: 2026-07-19 17:34:20
tags:
  - "3DV"
  - "CV"
---
# 3D Gaussian Splatting（3DGS） Paper Notes

3DGS 使用一组**显式、可优化的三维高斯原语**表示场景，并通过可微投影与 tile-based rasterization 将其快速渲染为图像。

整体流程为：

$$\text{SfM 稀疏点云}\rightarrow\text{3D Gaussian 初始化}\rightarrow\text{投影与光栅化}\rightarrow\text{计算图像损失}\rightarrow\text{反向传播优化}\rightarrow\text{自适应增密与剪枝}$$

{% asset_img 3dgs-all.png 3dgs-workflow %}

---
## 1. 3D Gaussian 场景表示

### 1.1 Gaussian Primitives

每个三维高斯可以表示为：

$$G_{i} = \left( \mathbf{\mu}_{i},\mathbf{s}_{i},\mathbf{q}_{i},\alpha_{i},\mathbf{k}_{i} \right)$$

其中：

- $\mathbf{\mu}_{i} \in \mathbb{R}^{3}$ ：高斯中心位置；
- $\mathbf{s}_{i} \in \mathbb{R}^{3}$ ：三个主轴方向的尺度；
- $\mathbf{q}_{i} \in \mathbb{R}^{4}$ ：表示旋转的四元数；
- $\alpha_{i} \in \lbrack 0,1\rbrack$ ：高斯的不透明度；
- $\mathbf{k}_{i}$ ：球谐系数，用于表示方向相关颜色。

高斯在空间位置 $\mathbf{x}$ 处的影响为：

$$G_{i}(\mathbf{x}) = \exp\left( - \frac{1}{2}(\mathbf{x} - \mathbf{\mu}_{i})^{T}\mathbf{\Sigma}_{i}^{- 1}(\mathbf{x} - \mathbf{\mu}_{i}) \right)$$

这里使用的是**不归一化高斯核**，因此：

$$G_{i}(\mathbf{\mu}_{i}) = 1$$

高斯尺度增大时，中心值不会自动降低，只会扩大影响范围。高斯的形状、颜色和不透明度是相互独立的可学习参数。

### 1.2 协方差矩阵与高斯形状

协方差矩阵决定高斯椭球的大小、长宽比例和朝向：

$$\mathbf{\Sigma} = \mathbf{R}\mathbf{S}\mathbf{S}^{T}\mathbf{R}^{T}$$

其中：

$$\mathbf{S} = {diag}(s_{x},s_{y},s_{z})$$

因此：

$$\mathbf{S}\mathbf{S}^{T} = {diag}(s_{x}^{2},s_{y}^{2},s_{z}^{2})$$

- $\mathbf{S}$ 控制椭球三个主轴的长度；
- $\mathbf{R}$ 控制椭球在世界坐标系中的朝向；
- $\mathbf{R}$ 由归一化四元数 $\mathbf{q}$ 转换得到。

只要：

$$s_{x} > 0,\quad s_{y} > 0,\quad s_{z} > 0$$

则 $\mathbf{\Sigma}$ 为正定矩阵，可以安全求逆。

从特征值分解角度看：

$$\mathbf{\Sigma} = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{T}$$

其中 $\mathbf{R}$ 对应特征向量方向， $s_{x}^{2},s_{y}^{2},s_{z}^{2}$ 对应特征值。

### 1.3 球谐函数表示方向相关颜色

同一个高斯从不同方向观察时可能具有不同颜色，例如高光和反射。3DGS 使用球谐函数表示：

$$\mathbf{c}_{i}(\mathbf{d}) = \sum\limits_{l = 0}^{L}\sum\limits_{m = - l}^{l}\mathbf{k}_{i,l,m}Y_{l}^{m}(\mathbf{d})$$

其中：

- $\mathbf{d}$ ：相机与高斯之间的单位观察方向；
- $l$ ：球谐阶数；
- $m$ ：同一阶中的基函数编号；
- $Y_{l}^{m}$ ：固定的球谐基函数；
- $\mathbf{k}_{i,l,m} \in \mathbb{R}^{3}$ ：可学习的 RGB 系数。

第 $l$ 阶包含：

$$2l + 1$$

个基函数。使用到最高 $L$ 阶时，基函数总数为：

$$(L + 1)^{2}$$

原始 3DGS 使用三阶球谐函数：

$$L = 3,\qquad(3 + 1)^{2} = 16$$

因此每个高斯共有：

$$16 \times 3 = 48$$

个 RGB 球谐系数，其中 3 个为零阶基础颜色，其余 45 个描述方向相关颜色变化。

---
## 2. 从 3D 高斯投影到 2D 高斯

### 2.1 非线性变换

渲染时，需要将世界坐标系中的三维高斯投影到当前相机的二维图像平面。

高斯中心先变换到相机坐标系：

$$\mathbf{\mu}_{c} = \mathbf{W}\mathbf{\mu}_{w} + \mathbf{t}$$

再通过透视投影得到二维中心：

$$\mathbf{\mu}_{2D} = \pi(\mathbf{\mu}_{c})$$

三维协方差投影为二维协方差：

$$\mathbf{\Sigma}_{2D} = \mathbf{J}\mathbf{W}\mathbf{\Sigma}_{3D}\mathbf{W}^{T}\mathbf{J}^{T}$$

其中：

- $\mathbf{W}$ ：世界坐标系到相机坐标系的旋转；
- $\mathbf{J}$ ：透视投影函数在高斯中心处的雅可比矩阵。

透视投影是非线性变换，因此使用一阶泰勒展开进行局部线性近似：

$$f(\mathbf{x}) \approx f(\mathbf{\mu}) + \mathbf{J}(\mathbf{x} - \mathbf{\mu})$$

最终，一个三维椭球被近似投影成图像平面上的二维椭圆 splat。

### 2.2 高斯颜色 Splatting 渲染

对于图像像素 $\mathbf{p}$ ，第 $i$ 个二维高斯的权重为：

$$g_{i}(\mathbf{p}) = \exp\left( - \frac{1}{2}(\mathbf{p} - \mathbf{\mu}_{i,2D})^{T}\mathbf{\Sigma}_{i,2D}^{- 1}(\mathbf{p} - \mathbf{\mu}_{i,2D}) \right)$$

该高斯在当前像素上的实际不透明度为：

$${\overset{\sim}{\alpha}}_{i}(\mathbf{p}) = \alpha_{i}g_{i}(\mathbf{p})$$

将覆盖当前像素的高斯按照深度从近到远排序，像素颜色通过前向 $\alpha$ -blending 计算：

$$\mathbf{C}(\mathbf{p}) = \sum\limits_{i \in \mathcal{N}}\mathbf{c}_{i}(\mathbf{d}){\overset{\sim}{\alpha}}_{i}(\mathbf{p})\prod\limits_{j = 1}^{i - 1}\left( 1 - {\overset{\sim}{\alpha}}_{j}(\mathbf{p}) \right)$$

定义前方透射率：

$$T_{i}(\mathbf{p}) = \prod\limits_{j = 1}^{i - 1}\left( 1 - {\overset{\sim}{\alpha}}_{j}(\mathbf{p}) \right)$$

则渲染公式可简写为：

$$\mathbf{C}(\mathbf{p}) = \sum\limits_{i}T_{i}(\mathbf{p}){\overset{\sim}{\alpha}}_{i}(\mathbf{p})\mathbf{c}_{i}(\mathbf{d})$$

其中：

- $T_{i}$ ：光线穿过前方高斯后剩余的透射率；
- ${\overset{\sim}{\alpha}}_{i}$ ：当前高斯在该像素上的不透明度；
- $\mathbf{c}_{i}$ ：由球谐函数计算出的当前视角 RGB 颜色。

### 2.3 Tile Rasterizer

为了实现高速渲染，3DGS 将图像划分为多个 $16 \times 16$ 的 tile：

1.  剔除视锥外的高斯；
2.  将三维高斯投影为二维高斯；
3.  判断每个高斯覆盖哪些 tile；
4.  为每个“高斯-tile”组合创建记录；
5.  使用“tile ID + 深度”作为排序 key；
6.  在 GPU 上进行一次全局排序；
7.  每个 tile 内按照深度顺序进行 $\alpha$ -blending。

该过程避免了逐像素射线采样，也避免了在空空间中进行无效计算。

由于投影和光栅化过程可微，图像损失可以反向传播到：

$$\mathbf{\mu},\quad\mathbf{s},\quad\mathbf{q},\quad\alpha,\quad\mathbf{k}$$

从而同时优化高斯的几何和外观。

---
## 3. 图像重建损失

3DGS 使用逐像素 L1 损失和 D-SSIM 损失：

$$\mathcal{L} = (1 - \lambda)\mathcal{L}_{1} + \lambda\mathcal{L}_{D\text{-}SSIM}$$

其中：

$$\mathcal{L}_{D\text{-}SSIM} = 1 - {SSIM}$$

原始论文设置：

$$\lambda = 0.2$$

因此：

$$\mathcal{L} = 0.8\mathcal{L}_{1} + 0.2(1 - {SSIM})$$

- $\mathcal{L}_{1}$ ：约束渲染图像与真实图像的逐像素 RGB 差异；
- SSIM：比较局部亮度、对比度和结构；
- D-SSIM：增强边缘和纹理等结构信息的优化。

---
## 4. 自适应高斯密度控制

初始 SfM 点云非常稀疏，因此 3DGS 在训练过程中动态执行：

- Pruning：删除无效高斯；
- Densification：增加高斯；
- Optimization：继续优化现有高斯参数。

{% asset_img rectification.png auto-rectification %}
增密主要依据高斯中心在屏幕空间中的位置梯度：

$$\left\| \nabla_{\mathbf{\mu}_{2D}}\mathcal{L} \right\| > \tau_{grad}$$

较大的位置梯度说明当前区域没有被充分表示，优化器正尝试大幅移动高斯来降低误差。

### 4.1 Pruning

为了控制高斯数量并删除伪影，训练过程中会周期性删除无效高斯。

#### 4.1.1 不透明度过小

若：

$$\alpha_{i} < \varepsilon_{\alpha}$$

说明该高斯几乎不影响任何像素，可以直接删除。

#### 4.1.2 高斯异常过大

若高斯在以下任一空间中过大，也可能被删除：

- 世界空间尺度过大；
- 投影到屏幕后 footprint 过大。

屏幕 footprint 过大可能由两种原因造成：

1.  高斯自身 scale 太大；
2.  高斯距离相机过近，导致透视投影被过度放大。

### 4.2 Densification

#### 4.2.1 欠重建：Clone

当高斯尺度较小，但位置梯度较大时，说明当前区域缺少足够的高斯：

$$\text{高梯度} + \text{小尺度}\rightarrow\text{Clone}$$

复制原高斯，并沿位置梯度方向移动新高斯：

$$G_{i}\rightarrow G_{i} + G_{i}^{clone}$$

Clone 会增加高斯数量和总体覆盖范围，用于补充缺失的几何。

#### 4.2 过度重建：Split

当高斯尺度较大且位置梯度较大时，说明一个高斯覆盖了过于复杂的区域：

$$\text{高梯度} + \text{大尺度}\rightarrow\text{Split}$$

将一个大高斯替换为多个较小高斯：

$$G_{i}\rightarrow\left\{ G_{i}^{(1)},G_{i}^{(2)} \right\}$$

新高斯的位置从原高斯分布附近采样，同时减小尺度，使其能够分别拟合局部细节。

---
## 5. 完整优化流程

每次训练迭代主要执行：

1.  随机选择一个训练视角；
2.  将三维高斯投影到当前图像平面；
3.  使用 tile rasterizer 渲染图像；
4.  与真实图像计算 L1 和 D-SSIM 损失；
5.  反向传播梯度；
6.  使用 Adam 更新高斯参数；
7.  在指定迭代执行 clone、split 和 pruning。

可概括为：

$$\text{Render}\rightarrow\text{Compare}\rightarrow\text{Backpropagate}\rightarrow\text{Optimize}\rightarrow\text{Densify / Prune}$$
