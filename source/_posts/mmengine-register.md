---
title: mmengine.registry 注册表
date: 2026-07-22 18:36:59
tags: misc
---
# mmengine.registry 注册表使用

## STEP 1: 创建注册表

```py
from mmengine.registry import Registry
OPENOCC_DATASET = Registry('openocc_dataset)
```

类似一个类的字典，key是类的名字字符串

## STEP 2: 注册自定义类

### 2.1 注册（未触发）

使用decorator，将自定义类加入到字典

```py
@OPENOCC_DATASET.register_module()
class Scannet_Scene_OpenOccupancy_Dataset(data.Dataset):
    def __init__(self, date_path, phase = 'train', ...):
        ...
```

### 2.1 import触发注册

```py
from .dataset_scannet_occ_openocc import Scannet_Scene_OpenOccupancy_Dataset # 触发注册
```

## STEP 3: 实例化

### 3.1 配置config字典

```py
train_dataset_config = dict(
    type = 'Scannet_Scene_OpenOccupancy_Dataset',
    data_path = data_path,
    num_frames = num_frames,
    phase = 'train',
    ...
)
```

此处只需字符串，不需要import

### 3.2 利用config字典实例化

```py
train_dataset = OPENOCC_DATASET.build(train_dataset_config)
```

效果即是根据type找到对应类，剩余参数作为该类构造函数的参数传入来创建实例

也可以用以下方式创建：
```py
from mmengine import build_from_cfg
train_dataset = build_from_cfg(train_dataset_config, OPENOCC_DATASET)
```

## Appendix

### 内置 MODELS

```py
from mmengine.registry import MODELS
```

这是mmengine注册表内置的一个注册表，提前内置了**深度学习**的一些通用底层框架，常见的有`ReLU`, `LeakyReLU`, `BN`, `LN`, `init_weights`等，当然也可以override方法。

示例：

```py
from mmengine import build_from_cfg
from mmengine.registry import MODELS

def build_model(model_config):
    model = build_from_cfg(model_config, MODELS)
    model.init_weights()
    return model
```


