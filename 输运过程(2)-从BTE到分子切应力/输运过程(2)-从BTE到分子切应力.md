# 输运过程(2)-从BTE到分子切应力

> Chen G. Nanoscale energy transport and conversion: a parallel treatment of electrons, molecules, phonons, and photons[M]. Oxford university press, 2005.

## 线性Boltzmann方程

在弛豫时间近似下，BTE的形式为：
$$
\frac{\partial f}{\partial t}+v \cdot \nabla_{r} f+\frac{\boldsymbol{F}}{m} \cdot \nabla_{v} f=-\frac{f-f_{0}}{\tau}
$$
引入偏差函数：
$$
g = f - f_0
$$
此时BTE可以改写为：
$$
\frac{\partial g}{\partial t}+\frac{\partial f_{0}}{\partial t}+v \cdot \nabla_{r} f_{0}+v \cdot \nabla_{r} g+\frac{\boldsymbol{F}}{m} \cdot \nabla_{v} f_{0}+\frac{\boldsymbol{F}}{m} \cdot \nabla_{v} g=-\frac{g}{\tau}
$$
考虑分布函数离平衡态偏差很小的情况，此时成立以下假设：

- 非稳态项可以忽略
- $g$的梯度远远小于$f_0$的梯度
- $g$远小于$f_0$

于是方程可以简化为：
$$
g=-\tau\left(v \cdot \nabla_{r} f_{0}+\frac{\boldsymbol{F}}{m} \cdot \nabla_{v} f_{0}\right)
$$
即：
$$
f=f_0-\tau\left(v \cdot \nabla_{r} f_{0}+\frac{\boldsymbol{F}}{m} \cdot \nabla_{v} f_{0}\right)
$$
在小扰动情况下，分布函数的解可以通过把$g$看成是$f$的一阶展开（$f_0$是$f$的零阶展开）并忽略高阶项得到，这个方程被称作线性Boltzmann方程，由分布函数可以计算各种感兴趣物理量的通量，进而计算等效输运系数。

## 牛顿剪切应力定律

