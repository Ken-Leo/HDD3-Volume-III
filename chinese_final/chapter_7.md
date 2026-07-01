
# 第7章

# BPMR 系统的目标设计和均衡器

部分响应最大似然 (PRML) 技术 [10, 27] 是用于各种磁记录系统（如水平记录、垂直记录和 BPMR）数据检测的主要技术。其优点在于系统不会出现噪声放大问题，且系统复杂度不高。

PRML 检测器是均衡器和维特比检测器 [10, 13] 的联合工作。PRML 检测器的性能取决于系统中使用的目标和均衡器的适合程度。均衡器负责将信号整形成期望的目标形状，然后基于该目标构建的维特比检测器负责数据解码。此外，在 BPMR 系统中，良好的目标和均衡器设计还有助于降低 ISI 和 ITI 的影响。

由于 BPMR 信道受到 ITI 的影响，接收端应使用二维维特比检测器 [108, 109] 以获得最佳性能。然而，二维维特比检测器的复杂度非常高。因此，Nabavi [108] 和 Karakulak [109] 提出了各种目标和均衡器的设计方法，如一维目标加一维均衡器、二维目标加一维均衡器以及二维目标加二维均衡器等，以便能够使用通用的维特比检测器（即 [10] 第 4 章所述的一维维特比检测器）。因此，本章将介绍 BPMR 系统的各种目标和均衡器设计方法，并展示所有这些目标的性能。

# 7.1 一维目标和一维均衡器

考虑图 7.1 中用于设计一维目标和一维均衡器的离散时间 BPMR 信道模型。设 $\{a_{-1,k}, a_{0,k}, a_{1,k}\}$ 分别为上磁道、主磁道和下磁道的输入数据序列，通过信道 $\mathbf{H}$ 后得到回读信号 $r_k$：

$$
r_k = \sum_{m=-1}^{1} \sum_{n=-1}^{1} h_{m,n} a_{-m, k-n} + n_k \tag{7.1}
$$

其中 $h_{m,n}$ 是矩阵 $\mathbf{H}$ 的系数（见方程 (6.18)），$n_k \sim \mathcal{N}(0, \sigma^2)$ 是 AWGN 噪声。在接收端，回读信号 $r_k$ 通过一维均衡器 $F(D)$ 进行整形，使其特性符合目标 $G(D)$，然后将均衡器输出 $\{z_k\}$ 送入通用维特比检测器，以估计主磁道的数据序列 $\hat{a}_{0,k}$。

假设 ITI 的影响被视为一种与 $n_k$ 相似的噪声，则本节中一维目标和一维均衡器的设计与 [10] 第 3 章所述的垂直记录系统目标与均衡器设计相同。设均衡器长度为 $N = 2K + 1$（$K$ 为正整数），用 D 域表示为

$$
F(D) = \sum_{k=-K}^{K} f_k D^k \tag{7.2}
$$

其中 $D$ 是延迟 $T_x$ 的算子。类似地，目标长度为 $L = 3$，用 D 域表示为

$$
G(D) = \sum_{k=0}^{2} g_k D^k \tag{7.3}
$$

其中 $f_k$ 和 $g_k$ 分别是均衡器和目标的第 $k$ 个系数。

MMSE 目标设计的目标是同时求解 $F(D)$ 和 $G(D)$ 的系数，使均衡器输出 $z_k$ 与目标输出 $d_k$ 之间的 MSE 最小化。即选择 $f_k$ 和 $g_k$ 使下式最小化：

$$
E[w_k^2] = E[\{(r_k * f_k) - (a_{0,k} * g_k)\}^2] \tag{7.4}
$$

其中 $w_k = z_k - d_k$ 是目标设计误差，$*$ 是卷积算子。

设 $\mathbf{g} = [g_0 \; g_1 \; g_2]^\mathrm{T}$ 为目标 $G(D)$ 的列向量，$\mathbf{f} = [f_{-K} \dots f_0 \dots f_K]^\mathrm{T}$ 为均衡器 $F(D)$ 的列向量，$\mathbf{r}_k = [r_{k+K} \dots r_k \dots r_{k-K}]^\mathrm{T}$ 为回读信号的列向量，$\mathbf{a}_k = [a_{0,k} \; a_{0,k-1} \; a_{0,k-2}]^\mathrm{T}$ 为主磁道输入数据的列向量。则方程 (7.4) 可以用矩阵形式表示为

$$
\begin{aligned}
E[w^2] &= E\left[(\mathbf{f}^\mathrm{T} \mathbf{r}_k - \mathbf{g}^\mathrm{T} \mathbf{a}_k)(\mathbf{f}^\mathrm{T} \mathbf{r}_k - \mathbf{g}^\mathrm{T} \mathbf{a}_k)^\mathrm{T}\right] \\
&= \mathbf{f}^\mathrm{T} \mathbf{R} \mathbf{f} + \mathbf{g}^\mathrm{T} \mathbf{A} \mathbf{g} - 2 \mathbf{f}^\mathrm{T} \mathbf{P} \mathbf{g} \tag{7.5}
\end{aligned}
$$

其中 $\mathbf{R} = E[\mathbf{r}_k \mathbf{r}_k^\mathrm{T}]$ 是大小为 $N \times N$ 的 $\{r_k\}$ 自相关矩阵，$\mathbf{A} = E[\mathbf{a}_k \mathbf{a}_k^\mathrm{T}]$ 是大小为 $L \times L$ 的 $\{a_{0,k}\}$ 自相关矩阵，$\mathbf{P} = E[\mathbf{r}_k \mathbf{a}_k^\mathrm{T}]$ 是大小为 $N \times L$ 的 $\{r_k\}$ 与 $\{a_{0,k}\}$ 之间的互相关矩阵。这些矩阵的 $(i,j)$ 元素（第 $i$ 行、第 $j$ 列）为

$$
\mathbf{R}(i,j) = E\left[\sum_{k=0}^{S-1} r_{k+K-i} r_{k+K-j}\right], \quad 0 \leq i,j \leq 2K \tag{7.6}
$$

$$
\mathbf{A}(i,j) = E\left[\sum_{k=0}^{S-1} a_{0,k-i} a_{0,k-j}\right], \quad 0 \leq i,j \leq L-1 \tag{7.7}
$$

$$
\mathbf{P}(i,j) = E\left[\sum_{k=0}^{S-1} r_{k+K-i} a_{0,k-j}\right], \quad 0 \leq i \leq 2K, \; 0 \leq j \leq L-1 \tag{7.8}
$$

其中 $S$ 是输入数据序列 $\{a_{0,k}\}$ 的长度。

为最小化 $E[w^2]$ 于 $\mathbf{f}$ 和 $\mathbf{g}$，需要施加约束条件以避免得到 $\mathbf{f} = \mathbf{g} = \mathbf{0}$ 的平凡解。这里使用单项约束 (monic constraint) [10, 14]，即令目标中心抽头系数为 1（$g_1 = 1$）[108]。设列向量 $\mathbf{I} = [0 \; 1 \; 0]^\mathrm{T}$，则约束条件为 $\mathbf{I}^\mathrm{T} \mathbf{g} = 1$。引入拉格朗日乘子 $\lambda$ 后，目标函数为

$$
E[w^2] = \mathbf{f}^\mathrm{T} \mathbf{R} \mathbf{f} + \mathbf{g}^\mathrm{T} \mathbf{A} \mathbf{g} - 2 \mathbf{f}^\mathrm{T} \mathbf{P} \mathbf{g} - 2\lambda(\mathbf{I}^\mathrm{T} \mathbf{g} - 1) \tag{7.9}
$$

分别对 $\mathbf{f}$、$\mathbf{g}$ 和 $\lambda$ 求导并令导数为零，得到

$$
\lambda = \frac{1}{\mathbf{I}^\mathrm{T} (\mathbf{A} - \mathbf{P}^\mathrm{T} \mathbf{R}^{-1} \mathbf{P})^{-1} \mathbf{I}} \tag{7.10}
$$

$$
\mathbf{g} = \lambda (\mathbf{A} - \mathbf{P}^\mathrm{T} \mathbf{R}^{-1} \mathbf{P})^{-1} \mathbf{I} \tag{7.11}
$$

$$
\mathbf{f} = \mathbf{R}^{-1} \mathbf{P} \mathbf{g} \tag{7.12}
$$

其中 $\lambda$ 即为此约束条件下 MMSE 目标设计得到的 MMSE 值。

注：方程 (7.10)-(7.12) 与 [10] 第 3.2.1 节中垂直磁记录系统目标与均衡器设计的方程 (3.19)-(3.21) 相同。
