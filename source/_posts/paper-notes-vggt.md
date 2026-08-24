---
title: 【Paper Notes】- VGGT
date: 2026-08-24 14:46:57
tags: [3DV, CV]
---

# VGGT: Visual Geometry Grounded Transformer

## 论文信息

- **标题**：VGGT: Visual Geometry Grounded Transformer
- **会议**：CVPR 2025 Best Paper
- **任务定位**：统一的 feed-forward 3D vision foundation model
- **输入**：任意数量的同一场景图像
- **输出**：Camera parameters、Depth maps、3D point maps、2D point tracks

---

## 1. 研究问题

传统多视图几何通常依赖显式流水线：

```text
Feature Extraction
→ Matching
→ SfM
→ Camera Pose
→ Triangulation
→ MVS / Depth
→ Point Cloud
```

VGGT 希望直接学习：

$$
\{I_i\}_{i=1}^{N}
\longrightarrow
\{C_i,D_i,P_i,\text{Tracks}\}_{i=1}^{N}
$$

即输入一组图像，通过一次 feed-forward inference，同时预测相机、深度、3D 点和对应关系。

---

## 2. 核心贡献

1. **统一多种 3D 几何任务**：Camera、Depth、Point Map、Point Tracking。
2. **Alternating Attention**：Frame Attention 做单帧内部建模，Global Attention 做跨视图联合建模。
3. **统一的 geometry-aware representation**：同一组 Transformer tokens 服务于多个几何 head。
4. **Feed-forward 3D reconstruction**：不依赖传统 SfM / BA 才能产生初始几何结果，并可作为下游 3D 任务 backbone。

---

## 3. Overall Pipeline

![pipeline](vggt-pipeline.png)

```text
Input Images
    │
    ▼
DINOv2 Image Encoder
    │
    ▼
Image Patch Tokens t_i^I
    │
    ├── Camera Token t_i^G
    ├── Register Tokens t_i^R
    │
    ▼
Alternating-Attention Transformer
    │
    ├───────────────┬──────────────────┐
    │               │                  │
    ▼               ▼                  ▼
Camera Head       DPT Heads        Tracking DPT
    │               │                  │
    ▼          ┌────┴────┐             ▼
Camera         Depth     Point      Tracking Feature
Parameters      Map      Map           T_i
                  │        │             │
                  ▼        ▼             ▼
             Confidence Confidence   Tracker
                                      │
                                      ▼
                                  2D Tracks
```

---

## 4. Method

### 4.1 Image Tokens

每张输入图像经过 DINOv2：

$$
I_i \rightarrow t_i^I
$$

其中：

$$
t_i^I\in\mathbb R^{P\times C}
$$

对于 \(518\times518\) 图像、patch size \(14\)：

$$
P=37\times37=1369
$$

VGGT 额外插入 camera token 和 register tokens，单帧 token sequence：

$$
[t_i^G,\;t_i^R,\;t_i^I]
$$

### 4.2 Alternating Attention

VGGT 主体交替执行两种 attention。

#### Frame Attention

$$
[B,S,P,C]
\rightarrow
[B\cdot S,P,C]
$$

只允许同一张图内部的 camera/register/image tokens 交互。

#### Global Attention

$$
[B,S,P,C]
\rightarrow
[B,S\cdot P,C]
$$

使不同图像的 tokens 直接交换信息。

```text
Frame Attention
      ↓
Global Attention
      ↓
Frame Attention
      ↓
Global Attention
      ↓
...
```

可以概括为：

$$
\boxed{
\text{local image reasoning}
+
\text{multi-view global reasoning}
}
$$

当前实现还会将同层的 frame/global feature 在 channel 维拼接：

$$
F_l=[F_l^{frame};F_l^{global}]
$$

所以 backbone 内部 channel 为 1024，而 downstream head 输入为 2048。

### 4.3 Camera Prediction

Camera Head 使用最终 feature 中的 camera token：

$$
\hat t_i^G
$$

得到每帧的 camera representation，并进一步做 camera-only self-attention 和 iterative refinement。

Camera encoding 为 9D：

$$
c_i=
[T_x,T_y,T_z,\;q_1,q_2,q_3,q_4,\;\text{FoV}_h,\text{FoV}_w]
$$

其中：

- \(T\)：translation
- \(q\)：rotation quaternion
- FoV：视场角

由 FoV 恢复 focal length：

$$
f_y=\frac{H/2}{\tan(\text{FoV}_h/2)}
$$

$$
f_x=\frac{W/2}{\tan(\text{FoV}_w/2)}
$$

迭代更新：

$$
c_i^{(k)}
=
c_i^{(k-1)}+\Delta c_i^{(k)}
$$


### 4.4 Dense Prediction：DPT

Transformer 输出仍是 patch-level token：

$$
\hat t_i^I\in\mathbb R^{P\times C}
$$

而 depth / point 是 pixel-level prediction，因此需要 DPT：

$$
\hat t_i^I
\rightarrow
F_i
$$

其中：

$$
F_i\in\mathbb R^{C''\times H\times W}
$$

DPT 取多个 Transformer 层，例如：

$$
L_4,\;L_{11},\;L_{17},\;L_{23}
$$

它们最初空间尺寸均为 \(37\times37\)，先 reshape：

$$
[P,C]
\rightarrow
[C,37,37]
$$

再人为构造 feature pyramid：

```text
Layer 4   : 37×37 → 148×148
Layer 11  : 37×37 →  74×74
Layer 17  : 37×37 →  37×37
Layer 23  : 37×37 →  19×19
```

对应：

- ConvTranspose ×4
- ConvTranspose ×2
- Identity
- Strided Conv ÷2

然后 coarse-to-fine fusion：

```text
19×19
  ↓ upsample
37×37 + skip
  ↓
74×74 + skip
  ↓
148×148 + skip
  ↓
full-resolution dense feature
```

因此：

$$
\boxed{
\text{DPT}
\approx
\text{Transformer multi-layer features}
+
\text{CNN/FPN/U-Net-like dense decoder}
}
$$


### 4.5 Depth Map

Dense feature 经 prediction head 得到：

$$
D_i\in\mathbb R^{H\times W}
$$

每个像素输出一个 depth：

$$
D_i(u,v)=d
$$

同时预测逐像素 confidence / uncertainty：

$$
C_i^D\in\mathbb R_+^{H\times W}
$$


### 4.6 Point Map

Point map：

$$
P_i\in\mathbb R^{3\times H\times W}
$$

每个像素直接预测：

$$
P_i(u,v)=(X,Y,Z)
$$

Depth 只给每像素一个标量 \(d\)，Point Map 直接给出三维坐标。

理论上 depth 可以反投影：

$$
X_c=
D_i(u,v)
K^{-1}
\begin{bmatrix}
u\\v\\1
\end{bmatrix}
$$

VGGT 仍显式预测 point map，以提供直接的 3D geometry supervision。


### 4.7 Tracking Feature

Tracking 分支也使用 DPT-style decoder，但只输出 dense feature：

$$
T_i\in\mathbb R^{C\times H\times W}
$$

它不是坐标，而是每个像素的 tracking descriptor：

$$
T_i(:,u,v)\in\mathbb R^C
$$

当前代码中 Tracking Head 内部使用独立的 `feature_only=True` DPTHead。


### 4.8 Point Tracking

给定 query image \(q\) 中 query point：

$$
y_j=(x_j,y_j)
$$

先在 \(T_q\) 上做 bilinear sampling：

$$
f_j=T_q(y_j)
$$

若坐标不在整数网格上，则对周围四个 feature vector 做双线性插值：

$$
f(x,y)=
(1-\alpha)(1-\beta)f_{00}
+
\alpha(1-\beta)f_{10}
+
(1-\alpha)\beta f_{01}
+
\alpha\beta f_{11}
$$

得到 query feature：

$$
f_j\in\mathbb R^C
$$

再与其他图像 feature map 计算 correlation：

$$
\mathcal C_i(u,v)
=
f_j^T T_i(:,u,v)
$$

得到 correlation maps，再通过 self-attention / iterative update 预测：

$$
\hat y_i=(\hat x_i,\hat y_i)
$$

所有 \(\hat y_i\) 对应同一个 3D scene point。

Tracker 不要求 temporal ordering，因此既可用于视频，也可用于 unordered image collections。


### 4.9 Confidence / Aleatoric Uncertainty

Depth 和 Point 均预测逐像素 reliability：

$$
\Sigma_i^D,\qquad\Sigma_i^P
$$

基本思想：

$$
\mathcal L
\sim
\gamma e c-\alpha\log c
$$

其中：

- \(e\)：预测误差
- \(c\)：confidence

这样困难区域可以降低监督权重，但模型又不能简单把所有 confidence 设得很低。

---

## 5. Training

总体是 multi-task supervision：

$$
\mathcal L
=
\mathcal L_{camera}
+
\mathcal L_{depth}
+
\mathcal L_{point}
+
\lambda\mathcal L_{track}
$$

### Camera Loss

多轮 refinement 均参与监督：

$$
c^{(1)},c^{(2)},\dots,c^{(K)}
$$

主要监督：

$$
\mathcal L_T,\quad
\mathcal L_R,\quad
\mathcal L_{FoV}
$$

分别对应 Translation、Rotation、FoV。

### Dense Geometry Loss

Depth / Point 包括：

- Regression loss
- Confidence-weighted loss
- 可选 multi-scale gradient / normal consistency loss

---

## 6. 与传统多视图几何的区别

传统 SfM / SLAM 依赖显式几何：

$$
x_2^T E x_1=0
$$

$$
\min_{R,t,X}
\sum
\|\pi(RX+t)-x\|^2
$$

而 VGGT 将大量 geometry reasoning 学习进模型参数 \(\theta\)。

| Traditional Geometry | VGGT |
|---|---|
| Explicit matching | Learned tracking/correlation |
| Essential/PnP | Camera Head |
| Triangulation | Point-map prediction |
| MVS | Dense DPT prediction |
| BA | Feed-forward prediction，可选后处理优化 |
| Hand-designed geometry | Learned multi-view representation |

---

## 7. 论文核心理解

VGGT 的贡献并不是某一个特别新的数学模块。

它的组成大多来自已有方法：

- DINOv2
- Transformer
- Alternating Attention
- DPT
- Correlation-based Tracking
- Multi-task Learning

真正重要的是：

$$
\boxed{
\text{将 Camera + Depth + Point + Tracking
统一进一个大规模多视图 Transformer}
}
$$

并证明：

$$
\boxed{
\text{Transformer 可以通过大规模 3D supervision
学习很强的隐式多视图几何}
}
$$

因此 VGGT 更接近 **system-level / foundation-model-level innovation**，而不是以新公式为核心的 geometry paper。

---

## 8. Summary

$$
\boxed{
\text{VGGT}
=
\text{DINO image representation}
+
\text{alternating multi-view Transformer}
+
\text{camera/dense/tracking heads}
}
$$

核心数据流：

```text
Images
→ Patch Tokens
→ Frame / Global Attention
→ Geometry-aware Tokens
→ Camera + Depth + Point + Tracking
```

其核心意义是：

> **用统一的大规模 feed-forward Transformer 学习通用多视图几何表示，并直接输出多种 3D 几何结果。**
