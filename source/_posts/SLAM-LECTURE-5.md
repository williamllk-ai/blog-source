---
title: "SLAM LECTURE 5: 相机与图像"
date: 2026-02-03 19:35:35
author: williamllk
tags: SLAM
---

## 5.1 相机模型

### 5.1.1 针孔相机模型

&ensp;&ensp;&ensp;&ensp;从相机坐标系下$[X, Y, Z]^\top$(Z为距离相机的深度)转到**像素坐标系**$[u, v]^\top$：

$$Z
\begin{pmatrix}
u \\
v \\
1
\end{pmatrix}=
\begin{pmatrix}
f_x & 0 & c_x \\
0 & f_y & c_y \\
0 & 0 & 1
\end{pmatrix}
\begin{pmatrix}
X \\
Y \\
Z
\end{pmatrix}\overset{\mathrm{def}}{\operatorname*{=}}\boldsymbol{KP}.$$

&ensp;&ensp;&ensp;&ensp;其中，中间量组成的矩阵称为**相机的内参（Camera Intrinsics）矩阵$K$**


&ensp;&ensp;&ensp;&ensp;要从世界坐标系($P_w$)转换到像素坐标系，中间需要经过从世界坐标系到相机坐标系的转换，因此存在**外参**：

$$Z\boldsymbol{P}_{uv}=Z
\begin{bmatrix}
u \\
 \\
v \\
 \\
1
\end{bmatrix}=\boldsymbol{K}\left(\boldsymbol{R}\boldsymbol{P}_\mathrm{w}+\boldsymbol{t}\right)=\boldsymbol{K}\boldsymbol{T}\boldsymbol{P}_\mathrm{w}.$$

&ensp;&ensp;&ensp;&ensp;其中，相机的位姿$\boldsymbol{R}$，$\boldsymbol{t}$称为**相机的外参数（Camera Extrinsics）**。相较于不变的内参，外参会随着相机运动发生改变。

&ensp;&ensp;&ensp;&ensp;从另一个角度来看待投影过程，可以讲投影理解成线**归一化**深度，得到点再相机**归一化平面**上的投影，从而可见点的深度在他投影过程中丢失了。

### 5.1.2 畸变模型

1. 径向畸变：类似极坐标中$\vec{e}_r$方向有畸变项，一般中心对称，常见的有桶形畸变和枕形畸变
2. 切向畸变：累次极坐标中$\vec{e}_\theta$方向有畸变项

### 5.1.3 双目相机模型

