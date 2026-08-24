---
title: SLAM LECTURE 2
date: 2026-01-25 20:04:39
author: williamllk
tags: SLAM
---

## 2.1 引子

1. 感知 -> 定位（状态）+ 建图（环境）
2. 相机分类：单目（Monocular）相机、双目（Stereo）相机、深度（RGB-D）相机
    1. 单目相机通过移动确认深度，但存在尺度不确定性
    2. 双目相机有已知Baseline，可测量深度，但计算量大
    3. 深度相机通过物理手段判断距离，但使用空间受限，主要用于室内
    4. 双目相机/深度相机由于都存在真实时间的参数（baseline/depth）可以解决尺度问题

## 2.2 经典视觉SLAM框架

1. 传感器（相机）信息读取
2. 前端视觉里程计（Visual Odometry, VO，又称为前端Front End）：相邻图像之间的相机运动
    - 可能产生的问题：累计漂移（Accumulating Drift）
3. 后端（非线性）优化（Optimization，又称为Back End）：处理噪声问题
    - 如何从带有噪声的数据中估计整个系统的状态
    - 这个状态估计的不确定性有多大（最大后验概率估计, Maximum-a-Posteriori, MAP）
4. 回环检测（Loop Closure Detection）：解决漂移问题
    - 计算图像相似性来判别是否回到原点
5. 建图（Mapping）
    - 度量地图（Metric Map）
        - 稀疏（Sparse）图：只保留地标（Landmark），可用于定位
        - 稠密（Dense）图：二维图由许多小格子（Grid）组成，三维图由许多小方块（Voxel）组成；每一块含有占据、空闲、未知三种状态，可用于A*等导航算法
    - 拓朴地图（Topological Map）：Graph，由节点和边组成，只考虑节点间连通性

## 2.3 SLAM问题的数学表述


位置用$\boldsymbol{x}$表示，各时刻的位置记作$\boldsymbol{x}_i$，路标点则用$\boldsymbol{y}_i$表示。

得到**运动方程**，

$$
\boldsymbol{x}_k = f(\boldsymbol{x}_{k-1}, \boldsymbol{u}_k, \boldsymbol{w}_k), \quad k = 1, 2, \dots, K
$$

其中，$\boldsymbol{u}_k$是运动传感器的读数或者输入，$\boldsymbol{w}_k$为该过程中加入的噪声。

以及**观测方程**，

$$
\boldsymbol{z}_{k, j} = h(\boldsymbol{y}_{j}, \boldsymbol{x}_k, \boldsymbol{v}_{k, j}), \quad (k, j) \in \mathcal{O}
$$

其中$\boldsymbol{z}_{k, j}$为在$\boldsymbol{x}_k$观测到路标点$\boldsymbol{y}_{j}$时产生的观测数据，$\boldsymbol{v}_{k, j}$是观测里的噪声，$\mathcal{O}$是一个记录着哪个时刻观察到了哪个路标的集合。

从而，我们把SLAM问题建模成了一个状态估计问题，根据运动和观测方程是否线性，噪声是否服从高斯分布进行分类，分为**线性/非线性**和**高斯/非高斯**系统。

