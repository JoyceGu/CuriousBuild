---
title: "Kaplan-Meier和Piecewise Exponential 生存分析在用户留存分析中的应用"
date: 2025-01-25
tags: ["Learning", "Data Science"]
---


最近又在做客户留存的项目，因为老板建议用 Kaplan-Meier 生存分析， 所以仔细琢磨了一下这个方法。这篇文章不讨论具体公式，但是会讨论将其用于用户留存分析时候的一些注意点。

## Kaplan-Meier 生存分析

简单地说，Kaplan-Meier 生存分析是一种非参数统计方法，用于估计生存函数（即个体存活时间的分布），
特别适用于右删失数据（right-censored data），所谓右删失就是在研究期间，某些个体的最终状态尚
未发生或者无法观测，但我们至少知道他们活过了某个时间点。

## 用户留存分析

用户留存分析中，我们关心的是用户在某个时间点是否留存，以及留存的时间。Kaplan-Meier 生存分析
在这种情况下可以很好地描述用户留存的情况。

比如下面的Python代码，我们计算了用户留存率：

```python
import pandas as pd
from lifelines import KaplanMeierFitter

# 创建一个示例数据集
data = pd.DataFrame({   
    'user_id': [1, 2, 3, 4, 5],
    'join_date': pd.to_datetime(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05']),
    'churn_date': pd.to_datetime(['2020-01-03', '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07'])，
    'durations': [5, 6, 7, 8, 9],
    'event': [1, 0, 1, 0, 1] # 1 表示用户留存，0 表示用户流失
})

# 使用 KaplanMeierFitter 进行生存分析
kmf = KaplanMeierFitter()

## 注意这里使用durations 而非churn_date
kmf.fit(data['durations'], event_observed=data['event'])


# 计算留存率
survival_prob = kmf.survival_function_

# 打印结果
print(survival_prob)
```


## 局限性
然而我发现它也有一定的局限性，
1. 其中一个比较常见的局限是：比如在真实的生存分析中，我们知道个体一定是每天都存活着一直到死亡或者故障发生，但是在留存分析中，我们可能只关心用户在某一天是否留存，而不关心他之前或者之后的情况。在这种情况下，Kaplan-Meier 生存分析可能会低估用户的留存率。
2. 使用Kaplan-Meier 生存分析，我们无法得知用户在留存的这段时间内实际使用产品的天数，比如用户在第1天和第15天留存，但是其实只用了这两天，另一个用户则在前14天内每天都使用产品，但是第15天没有使用，所以第15天流失了，但是Kaplan-Meier 生存分析会认为他没有留存。


## Piecewise Survival Analysis
另一种方法是分段生存分析（Piecewise Survival Analysis），它将时间分成多个时间段，然后对每个时间段进行生存分析。我让chatgpt生成了一个dummy data，然后分别用两种方法作比较。从图中可以看到，分段生存分析（Piecewise Exponential）的曲线更加平滑，而 Kaplan-Meier 的曲线则更加波动。

![Comparison of Kaplan-Meier and Piecewise Survival Analysis](/images/KMandPW.png)
所用的代码如下：

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, PiecewiseExponentialFitter

# 生成更多数据点
np.random.seed(42)
n = 50  # 增加数据点数量
durations = np.random.exponential(scale=10, size=n).astype(int)  # 生成生存时间（以天为单位）
event = np.random.choice([1, 0], size=n, p=[0.7, 0.3])  # 70% 的人发生事件，30% 是删失

# 创建 DataFrame
data = pd.DataFrame({'durations': durations, 'event': event})

# 设定时间段（分段模型）：0-5 个月, 5-10 个月, 10+ 个月
breakpoints = [5, 10]

# --- 1. Kaplan-Meier Estimator ---
kmf = KaplanMeierFitter()
kmf.fit(data['durations'], event_observed=data['event'])

# --- 2. Piecewise Exponential Model ---
pef = PiecewiseExponentialFitter(breakpoints)
pef.fit(data['durations'], event_observed=data['event'])

# --- 绘制生存曲线对比 ---
plt.figure(figsize=(8, 6))

# Kaplan-Meier 曲线（阶梯状）
kmf.plot_survival_function(label="Kaplan-Meier", linestyle="--", color="blue")

# Piecewise Exponential Model 曲线（平滑）
pef.plot_survival_function(label="Piecewise Exponential", linestyle="-", color="red")

# 图表信息
plt.title("Comparison of Kaplan-Meier and Piecewise Survival Analysis")
plt.xlabel("Time (Days)")
plt.ylabel("Survival Probability")
plt.legend()
plt.grid()

# 显示图表
plt.show()
```

## 总结
- Kaplan-Meier 生存曲线（蓝色虚线 --）
    - 阶梯状曲线，生存率在每次事件（流失）发生时下降。
    - 曲线不是光滑的，因为它完全依赖于观测到的数据点。
    - 适用于非参数分析，不假设固定的风险率。
- Piecewise Exponential Model 生存曲线（红色实线 -）
    - 分段平滑曲线，在不同时间段（0-5天、5-10天、10+天）内，生存率以不同的指数速率下降。
    - 适用于风险率随时间变化的情况，假设每个时间段内风险率是恒定的。
    - 适合处理风险模式变化明显的数据，比如客户流失最开始很快，但后面趋于稳定。


## 其他
- 本文部分内容和代码由chatgpt生成。
- 关于Kaplan-Meier 生存分析的公式，可以参考 [生存分析简明教程](http://thisis.yorven.site/blog/index.php/2020/04/06/survival-analysis/) 这篇文章，欢迎有兴趣的人继续阅读。

