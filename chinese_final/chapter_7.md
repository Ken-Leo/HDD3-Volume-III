# 第7章 二维均衡与检测

## 7.1 一维目标和一维均衡器

考虑用于一维目标和一维均衡器设计的离散时间BPMR信道模型，如图7.1所示。设$\{a_{-1,k}, a_{0,k}, a_{1,k}\} \in \{\pm 1\}$分别为上磁道、中间磁道和下磁道的输入数据序列，这些序列被送入信道H，得到读回信号$r_k$：

$$
r_k = \sum_{m=-1}^{1} \sum_{n=-1}^{1} h_{m,n} a_{-m,k-n} + n_k\tag{7.1}
$$

其中$h_{m,n}$是矩阵H的系数（见式(6.18)），$n_k$是均值为零、方差为$\sigma^2$的加性高斯白噪声（AWGN），即$n_k \sim \mathcal{N}(0, \sigma^2)$。在接收端，读回信号$r_k$被送入一维均衡器$F(D)$，将读回信号整形为目标响应$G(D)$，然后将均衡器输出$\{z_k\}$送入通用维特比检测器，以估计中间磁道的数据序列$\{\hat{a}_{0,k}\}$。

假设ITI的影响被视为与噪声$n_k$类似的一种噪声，则本节的一维目标和一维均衡器设计与[10]第3章中描述的垂直记录系统中使用的目标和均衡器设计相同，总结如下。设均衡器有$N = 2K + 1$个抽头（K为正整数），其D域表达式为：

$$
F(D) = \sum_{k=-K}^{K} f_k D^k\tag{7.2}
$$

其中$D$是时延算子（时延为$T_x$）。类似地，$L = 3$个抽头的目标$G(D)$的D域表达式为：

$$
G(D) = \sum_{k=0}^{2} g_k D^k\tag{7.3}
$$

其中$f_k$和$g_k$分别是均衡器和目标的第k阶系数。

MMSE目标设计方法的目标是同时计算$F(D)$和$G(D)$的系数，使均衡器输出$z_k$与目标输出$d_k$之间的MSE最小。换句话说，选择系数$f_k$和$g_k$使下式最小：

$$
E[w_k^2] = E[\{(r_k * f_k) - (a_{0,k} * g_k)\}^2]\tag{7.4}
$$

其中$w_k = z_k - d_k$是目标设计误差，$*$是卷积算子，$E[\cdot]$是期望算子。

设$\mathbf{g} = [g_0\; g_1\; g_2]^\mathrm{T}$是目标$G(D)$的列向量，$\mathbf{f} = [f_{-K} \ldots f_0 \ldots f_K]^\mathrm{T}$是均衡器$F(D)$的列向量，$\mathbf{r}_k = [r_{k+K} \ldots r_k \ldots r_{k-K}]^\mathrm{T}$是读回信号的列向量，$\mathbf{a}_k = [a_{0,k}\; a_{0,k-1}\; a_{0,k-2}]^\mathrm{T}$是中间磁道输入数据$\{a_{0,k}\}$的列向量，$[\cdot]^\mathrm{T}$表示矩阵转置。因此，方程(7.4)可以写为矩阵形式：

$$
E[w^2] = E[(\mathbf{f}^\mathrm{T}\mathbf{r}_k - \mathbf{g}^\mathrm{T}\mathbf{a}_k)(\mathbf{f}^\mathrm{T}\mathbf{r}_k - \mathbf{g}^\mathrm{T}\mathbf{a}_k)^\mathrm{T}] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{A}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g}\tag{7.5}
$$

其中$\mathbf{R} = E[\mathbf{r}_k\mathbf{r}_k^\mathrm{T}]$是$\{r_k\}$的$N \times N$自相关矩阵，$\mathbf{A} = E[\mathbf{a}_k\mathbf{a}_k^\mathrm{T}]$是$\{a_{0,k}\}$的$L \times L$自相关矩阵，$\mathbf{P} = E[\mathbf{r}_k\mathbf{a}_k^\mathrm{T}]$是$\{r_k\}$和$\{a_{0,k}\}$之间的$N \times L$互相关矩阵，$N = 2K + 1$是均衡器抽头数，$L = 3$是目标抽头数。这三个矩阵的第$(i,j)$个元素（第$i$行第$j$列）为：

$$
\mathbf{R}(i,j) = E\left[\sum_{k=0}^{S-1} r_{k+K-i} r_{k+K-j}\right], \quad 0 \leq i,j \leq 2K\tag{7.6}
$$

$$
\mathbf{A}(i,j) = E\left[\sum_{k=0}^{S-1} a_{0,k-i} a_{0,k-j}\right], \quad 0 \leq i,j \leq L-1\tag{7.7}
$$

$$
\mathbf{P}(i,j) = E\left[\sum_{k=0}^{S-1} r_{k+K-i} a_{0,k-j}\right], \quad 0 \leq i \leq 2K, \; 0 \leq j \leq L-1\tag{7.8}
$$

其中$S$是输入数据序列$\{a_{0,k}\}$的长度（或比特数）。

为使$E[w^2]$相对于$\mathbf{f}$和$\mathbf{g}$最小化，必须在最小化过程中施加约束条件，以避免得到$\mathbf{f} = \mathbf{g} = \mathbf{0}$的解。因此，这里采用莫尼克约束[10, 14]进行目标设计，规定目标中间抽头的系数等于一（即$g_1 = 1$）[108]。设列向量$\mathbf{I} = [0\; 1\; 0]^\mathrm{T}$，则莫尼克约束可写为矩阵形式$\mathbf{I}^\mathrm{T}\mathbf{g} = 1$。因此，使用莫尼克约束的目标设计过程使方程(7.5)中的MSE最小化的同时始终保持$\mathbf{I}^\mathrm{T}\mathbf{g} = 1$。也就是说，该过程使下式最小：

$$
E[w^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{A}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g} - 2\lambda(\mathbf{I}^\mathrm{T}\mathbf{g} - 1)\tag{7.9}
$$

其中$\lambda$是标量拉格朗日乘子。对方程(7.9)分别对$\mathbf{f}$、$\mathbf{g}$和$\lambda$求导并令结果为零，可得：

$$
\lambda = \frac{1}{\mathbf{I}^\mathrm{T}(\mathbf{A} - \mathbf{P}^\mathrm{T}\mathbf{R}^{-1}\mathbf{P})^{-1}\mathbf{I}}\tag{7.10}
$$

$$
\mathbf{g} = \lambda(\mathbf{A} - \mathbf{P}^\mathrm{T}\mathbf{R}^{-1}\mathbf{P})^{-1}\mathbf{I}\tag{7.11}
$$

$$
\mathbf{f} = \mathbf{R}^{-1}\mathbf{P}\mathbf{g}\tag{7.12}
$$

其中$\lambda$就是此约束条件下目标设计得到的MMSE值。

注意，方程(7.10)-(7.12)与[10]第3.2.1节中描述的垂直磁记录系统中使用的目标和均衡器设计方程(3.19)-(3.21)相同。

## 7.2 零角二维目标和一维均衡器

一般来说，§7.1中描述的一维目标适用于ITI影响较小的BPMR系统（例如数据容量 < 2 Tb/in²）。但当BPMR系统受到中等程度的ITI影响（例如数据容量在2至2.5 Tb/in²之间）时，应改用二维目标。本节将介绍[109]中提出的零角二维目标和一维均衡器的设计方法，分两种情况讨论。

### 7.2.1 已知信道H

考虑图7.2中用于二维目标和一维均衡器设计的信道模型[109]。设$\{a_{-1,k}, a_{0,k}, a_{1,k}\} \in \{\pm 1\}$分别为上磁道、中间磁道和下磁道的输入数据序列，这些序列被送入由方程(6.18)定义的信道H：

$$
\mathbf{H} = \left[ \begin{array}{c} H_{-1}(D) \\ H_0(D) \\ H_1(D) \end{array} \right] = \left[ \begin{array}{lll} h_{-1,-1} & h_{-1,0} & h_{-1,1} \\ h_{0,-1} & h_{0,0} & h_{0,1} \\ h_{1,-1} & h_{1,0} & h_{1,1} \end{array} \right]\tag{7.13}
$$

其中$H_{-1}(D)$、$H_0(D)$和$H_1(D)$分别是上磁道、中间磁道和下磁道的信道响应。得到的读回信号$r_k$由方程(6.19)给出：

$$
r_k = (a_{0,k} * h_{0,k}) + (a_{-1,k} * h_{-1,k}) + (a_{1,k} * h_{1,k}) + n_k\tag{7.14}
$$

其中$h_{m,k}$是矩阵H的系数，$m \in \{-1,0,1\}$，$n_k \sim \mathcal{N}(0,\sigma^2)$是均值为零、方差为$\sigma^2$的AWGN噪声。在接收端，读回信号$r_k$被送入一维均衡器$F(D)$，将读回信号整形为目标响应$G_m(D)$，然后将均衡器输出$\{z_k\}$送入改进的维特比检测器[108]，以估计中间磁道的数据序列$\{\hat{a}_{0,k}\}$。

目标和均衡器的设计使用MMSE方法。设一维均衡器$F(D)$有$N = 2K + 1$个抽头（如式(7.2)），$3 \times 3$的二维目标为：

$$
\mathbf{G} = \left[ \begin{array}{c} G_{-1}(D) \\ G_0(D) \\ G_1(D) \end{array} \right] = \left[ \begin{array}{lll} g_{-1,0} & g_{-1,1} & g_{-1,2} \\ g_{0,0} & g_{0,1} & g_{0,2} \\ g_{1,0} & g_{1,1} & g_{1,2} \end{array} \right]\tag{7.15}
$$

其中$G_{-1}(D)$、$G_0(D)$和$G_1(D)$分别是上磁道、中间磁道和下磁道的目标响应。对于零角二维目标（zero-corner target），有$g_{-1,0} = g_{1,0} = g_{-1,2} = g_{1,2} = 0$。

设$\mathbf{f} = [f_{-K}, \ldots, f_0, \ldots, f_K]^\mathrm{T}$为均衡器系数向量，$\mathbf{a}_k$为三个磁道的输入数据序列的列向量（包含$6K+9$个元素），$\mathbf{n}_k = [n_{k+K} \ldots n_k \ldots n_{k-K}]^\mathrm{T}$为噪声列向量（$N=2K+1$个元素），$\tilde{\mathbf{H}}$为大小为$N \times (6K+9)$的信道矩阵。则均衡器输出可写为矩阵形式：

$$
z_k = \mathbf{f}^\mathrm{T}(\tilde{\mathbf{H}}\mathbf{a}_k + \mathbf{n}_k) = \mathbf{f}^\mathrm{T}\tilde{\mathbf{r}}_k\tag{7.17}
$$

其中$\tilde{\mathbf{r}}_k = \tilde{\mathbf{H}}\mathbf{a}_k + \mathbf{n}_k$。

此外，设$\mathbf{u}_k = [a_{0,k}\; a_{-1,k-1}\; a_{0,k-1}\; a_{1,k-1}\; a_{0,k-2}]^\mathrm{T}$为对应于零角目标系数的三个磁道输入数据序列的列向量（仅非零元素），$\mathbf{g} = [g_{0,0}\; g_{-1,1}\; g_{0,1}\; g_{1,1}\; g_{0,2}]^\mathrm{T}$。则目标G的输出为：

$$
d_k = \mathbf{g}^\mathrm{T}\mathbf{u}_k\tag{7.18}
$$

因此，均衡器输出$z_k$与目标输出$d_k$之间的差为：

$$
\mathbf{w}_k = \mathbf{z}_k - \mathbf{d}_k = \mathbf{f}^\mathrm{T}\tilde{\mathbf{r}}_k - \mathbf{g}^\mathrm{T}\mathbf{u}_k\tag{7.19}
$$

MMSE方法选择系数$f_k$和$g_k$使均方误差（MSE）最小：

$$
E[w^2] = E[(z_k - d_k)^2] = E[(\mathbf{f}^\mathrm{T}\tilde{\mathbf{r}}_k - \mathbf{g}^\mathrm{T}\mathbf{u}_k)(\mathbf{f}^\mathrm{T}\tilde{\mathbf{r}}_k - \mathbf{g}^\mathrm{T}\mathbf{u}_k)^\mathrm{T}] = \mathbf{f}^\mathrm{T}\tilde{\mathbf{R}}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\tilde{\mathbf{P}}\mathbf{g}\tag{7.20}
$$

其中$\tilde{\mathbf{R}} = E[\tilde{\mathbf{r}}_k\tilde{\mathbf{r}}_k^\mathrm{T}]$是$N \times N$自相关矩阵，$\mathbf{U} = E[\mathbf{u}_k\mathbf{u}_k^\mathrm{T}]$是$5 \times 5$自相关矩阵，$\tilde{\mathbf{P}} = E[\tilde{\mathbf{r}}_k\mathbf{u}_k^\mathrm{T}]$是$N \times 5$互相关矩阵。

MMSE目标设计使用莫尼克约束，规定目标中心抽头的系数等于一（即$g_{0,1} = 1$）[109]。设列向量$\mathbf{I} = [0\; 0\; 1\; 0\; 0]^\mathrm{T}$，则莫尼克约束可写为$\mathbf{I}^\mathrm{T}\mathbf{g} = 1$。因此，使用莫尼克约束的MMSE目标设计过程使下式最小：

$$
E[w^2] = \mathbf{f}^\mathrm{T}\tilde{\mathbf{R}}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\tilde{\mathbf{P}}\mathbf{g} - 2\lambda(\mathbf{I}^\mathrm{T}\mathbf{g} - 1)\tag{7.21}
$$

其中$\lambda$是拉格朗日乘子。对方程(7.21)分别对$\mathbf{f}$、$\mathbf{g}$和$\lambda$求导并令结果为零，可得：

$$
\lambda = \frac{1}{\mathbf{I}^\mathrm{T}(\mathbf{U} - \tilde{\mathbf{P}}^\mathrm{T}\tilde{\mathbf{R}}^{-1}\tilde{\mathbf{P}})^{-1}\mathbf{I}}\tag{7.22}
$$

$$
\mathbf{g} = \lambda(\mathbf{U} - \tilde{\mathbf{P}}^\mathrm{T}\tilde{\mathbf{R}}^{-1}\tilde{\mathbf{P}})^{-1}\mathbf{I}\tag{7.23}
$$

$$
\mathbf{f} = \tilde{\mathbf{R}}^{-1}\tilde{\mathbf{P}}\mathbf{g}\tag{7.24}
$$

其中$\lambda$就是此莫尼克约束下目标设计得到的MMSE值。注意，方程(7.22)-(7.24)与方程(7.10)-(7.12)类似。

### 7.2.2 未知信道H

§7.2.1中描述的目标和均衡器设计方法需要已知信道H来计算$\tilde{\mathbf{r}}_k$。然而，实际工作系统无法预知信道H的值，但仍可获得读回信号$r_k$（见图7.2）。因此，本节将介绍通过读回信号$r_k$来设计零角二维目标和一维均衡器的方法，其性能与§7.2.1中的目标设计相近。

从图7.2的BPMR信道模型可知，均衡器输出为$z_k = r_k * f_k = \mathbf{f}^\mathrm{T}\mathbf{r}_k$，其中$\mathbf{f} = [f_{-K} \ldots f_0 \ldots f_K]^\mathrm{T}$是均衡器系数向量（$N=2K+1$个元素），$\mathbf{r}_k = [r_{k+K} \ldots r_k \ldots r_{k-K}]^\mathrm{T}$是读回信号列向量。类似地，设$\mathbf{g} = [g_{0,0}\; g_{-1,1}\; g_{0,1}\; g_{1,1}\; g_{0,2}]^\mathrm{T}$是零角目标系数向量，$\mathbf{u}_k = [a_{0,k}\; a_{-1,k-1}\; a_{0,k-1}\; a_{1,k-1}\; a_{0,k-2}]^\mathrm{T}$是对应于目标系数的三个磁道输入数据序列的列向量，则目标输出为$d_k = \mathbf{g}^\mathrm{T}\mathbf{u}_k$。因此，$z_k$与$d_k$之间的差为：

$$
w_k = z_k - d_k = \mathbf{f}^\mathrm{T}\mathbf{r}_k - \mathbf{g}^\mathrm{T}\mathbf{u}_k\tag{7.25}
$$

均方误差（MSE）为：

$$
E[w^2] = E[(z_k - d_k)^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g}\tag{7.26}
$$

其中$\mathbf{R} = E[\mathbf{r}_k\mathbf{r}_k^\mathrm{T}]$是$N \times N$自相关矩阵，$\mathbf{P} = E[\mathbf{r}_k\mathbf{u}_k^\mathrm{T}]$是$N \times 5$互相关矩阵，$\mathbf{U} = E[\mathbf{u}_k\mathbf{u}_k^\mathrm{T}]$是$5 \times 5$自相关矩阵。

使用莫尼克约束的MMSE目标和均衡器设计方法使方程(7.26)中的MSE最小化的同时始终保持$\mathbf{I}^\mathrm{T}\mathbf{g} = 1$，其中$\mathbf{I} = [0\; 0\; 1\; 0\; 0]^\mathrm{T}$（即$g_{0,1} = 1$）。也就是说，该目标设计方法使下式最小：

$$
E[w^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g} - 2\lambda(\mathbf{I}^\mathrm{T}\mathbf{g} - 1)\tag{7.27}
$$

其中$\lambda$是拉格朗日乘子。对方程(7.27)分别对$\mathbf{f}$、$\mathbf{g}$和$\lambda$求导并令结果为零，得到的解与方程(7.22)-(7.24)相同，只需将$\tilde{\mathbf{R}}$替换为$\mathbf{R}$，将$\tilde{\mathbf{P}}$替换为$\mathbf{P}$。

## 7.3 对称二维目标和一维均衡器

在理想情况下（BPMR系统没有介质噪声和磁道误配准等非线性问题），磁头获得的二维脉冲响应是对称的，如图6.13和6.23所示。也就是说，上磁道和下磁道的跨磁道脉冲相同。在实际应用中，当BPMR系统具有高数据容量或较大的ITI影响（例如数据容量$\geq 3$ Tb/in²）时，所采用的二维目标的上磁道和下磁道目标系数不应为零，以使频率响应尽可能接近信道H的响应。因此，本节将介绍适用于高容量且无TMR影响的BPMR系统的对称二维目标设计方法[120]。

对称二维目标定义为$G_{-1}(D) = G_1(D)$，其矩阵形式为：

$$
\mathbf{G} = \left[ \begin{array}{c} G_{-1}(D) \\ G_0(D) \\ G_1(D) \end{array} \right] = \left[ \begin{array}{ccc} g_{-1,0} & g_{-1,1} & g_{-1,2} \\ g_{0,0} & g_{0,1} & g_{0,2} \\ g_{-1,0} & g_{-1,1} & g_{-1,2} \end{array} \right]\tag{7.28}
$$

从图7.2的BPMR信道模型可知，均衡器输出为$z_k = r_k * f_k = \mathbf{f}^\mathrm{T}\mathbf{r}_k$，其中$\mathbf{f} = [f_{-K} \ldots f_0 \ldots f_K]^\mathrm{T}$（$N=2K+1$个元素），$\mathbf{r}_k = [r_{k+K} \ldots r_k \ldots r_{k-K}]^\mathrm{T}$。设$\mathbf{g} = [g_{-1,0}\; g_{0,0}\; g_{-1,1}\; g_{0,1}\; g_{-1,2}\; g_{0,2}]^\mathrm{T}$为对称目标的系数向量，$\mathbf{u}_k = [(a_{-1,k}+a_{1,k})\; a_{0,k}\; (a_{-1,k-1}+a_{1,k-1})\; a_{0,k-1}\; (a_{-1,k-2}+a_{1,k-2})\; a_{0,k-2}]^\mathrm{T}$为对应于系数向量的输入数据序列列向量，则目标输出为$d_k = \mathbf{g}^\mathrm{T}\mathbf{u}_k$。因此，$z_k$与$d_k$之间的差为：

$$
w_k = z_k - d_k = \mathbf{f}^\mathrm{T}\mathbf{r}_k - \mathbf{g}^\mathrm{T}\mathbf{u}_k\tag{7.29}
$$

均方误差（MSE）为：

$$
E[w^2] = E[(z_k - d_k)^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g}\tag{7.30}
$$

其中$\mathbf{R} = E[\mathbf{r}_k\mathbf{r}_k^\mathrm{T}]$是$N \times N$自相关矩阵，$\mathbf{P} = E[\mathbf{r}_k\mathbf{u}_k^\mathrm{T}]$是$N \times 6$互相关矩阵，$\mathbf{U} = E[\mathbf{u}_k\mathbf{u}_k^\mathrm{T}]$是$6 \times 6$自相关矩阵。

使用莫尼克约束的MMSE目标设计方法使方程(7.30)中的MSE最小化的同时始终保持$\mathbf{I}^\mathrm{T}\mathbf{g} = 1$，其中$\mathbf{I} = [0\; 0\; 0\; 1\; 0\; 0]^\mathrm{T}$（即$g_{0,1} = 1$）。也就是说，该目标设计方法使下式最小：

$$
E[w^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g} - 2\lambda(\mathbf{I}^\mathrm{T}\mathbf{g} - 1)\tag{7.31}
$$

其中$\lambda$是拉格朗日乘子。对方程(7.31)分别对$\mathbf{f}$、$\mathbf{g}$和$\lambda$求导并令结果为零，可得：

$$
\lambda = \frac{1}{\mathbf{I}^\mathrm{T}(\mathbf{U} - \mathbf{P}^\mathrm{T}\mathbf{R}^{-1}\mathbf{P})^{-1}\mathbf{I}}\tag{7.32}
$$

$$
\mathbf{g} = \lambda(\mathbf{U} - \mathbf{P}^\mathrm{T}\mathbf{R}^{-1}\mathbf{P})^{-1}\mathbf{I}\tag{7.33}
$$

$$
\mathbf{f} = \mathbf{R}^{-1}\mathbf{P}\mathbf{g}\tag{7.34}
$$

其中方程(7.32)中的$\lambda$就是莫尼克约束下目标设计得到的MSE值。

## 7.4 非对称二维目标和一维均衡器

对称二维目标不适用于存在非线性问题（如磁道误配准）的BPMR系统，因为磁头获取的二维脉冲响应是非对称的。因此，本节将介绍非对称二维目标的设计方法[120, 121]。

类似地，从图7.2的BPMR信道模型可知，均衡器输出为$z_k = r_k * f_k = \mathbf{f}^\mathrm{T}\mathbf{r}_k$，其中$\mathbf{f} = [f_{-K} \ldots f_0 \ldots f_K]^\mathrm{T}$（$N=2K+1$个元素），$\mathbf{r}_k = [r_{k+K} \ldots r_k \ldots r_{k-K}]^\mathrm{T}$。考虑方程(7.15)中的$3 \times 3$二维目标，设$\mathbf{g} = [g_{-1,0}\; g_{0,0}\; g_{1,0}\; g_{-1,1}\; g_{0,1}\; g_{1,1}\; g_{-1,2}\; g_{0,2}\; g_{1,2}]^\mathrm{T}$为非对称目标的系数向量，$\mathbf{u}_k = [a_{-1,k}\; a_{0,k}\; a_{1,k}\; a_{-1,k-1}\; a_{0,k-1}\; a_{1,k-1}\; a_{-1,k-2}\; a_{0,k-2}\; a_{1,k-2}]^\mathrm{T}$为输入数据序列列向量，则目标输出为$d_k = \mathbf{g}^\mathrm{T}\mathbf{u}_k$。因此，$z_k$与$d_k$之间的差为：

$$
w_k = z_k - d_k = \mathbf{f}^\mathrm{T}\mathbf{r}_k - \mathbf{g}^\mathrm{T}\mathbf{u}_k\tag{7.35}
$$

均方误差（MSE）为：

$$
E[w^2] = E[(z_k - d_k)^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g}\tag{7.36}
$$

其中$\mathbf{R} = E[\mathbf{r}_k\mathbf{r}_k^\mathrm{T}]$是$N \times N$自相关矩阵，$\mathbf{P} = E[\mathbf{r}_k\mathbf{u}_k^\mathrm{T}]$是$N \times 9$互相关矩阵，$\mathbf{U} = E[\mathbf{u}_k\mathbf{u}_k^\mathrm{T}]$是$9 \times 9$自相关矩阵。

使用莫尼克约束的MMSE目标设计方法使方程(7.36)中的MSE最小化的同时始终保持$\mathbf{I}^\mathrm{T}\mathbf{g} = 1$，其中$\mathbf{I} = [0\; 0\; 0\; 0\; 0\; 1\; 0\; 0\; 0\; 0]^\mathrm{T}$（即$g_{0,1} = 1$）。该目标设计方法使下式最小：

$$
E[w^2] = \mathbf{f}^\mathrm{T}\mathbf{R}\mathbf{f} + \mathbf{g}^\mathrm{T}\mathbf{U}\mathbf{g} - 2\mathbf{f}^\mathrm{T}\mathbf{P}\mathbf{g} - 2\lambda(\mathbf{I}^\mathrm{T}\mathbf{g} - 1)\tag{7.37}
$$

其中$\lambda$是拉格朗日乘子。对方程(7.37)分别对$\mathbf{f}$、$\mathbf{g}$和$\lambda$求导并令结果为零，可得：

$$
\lambda = \frac{1}{\mathbf{I}^\mathrm{T}(\mathbf{U} - \mathbf{P}^\mathrm{T}\mathbf{R}^{-1}\mathbf{P})^{-1}\mathbf{I}}\tag{7.38}
$$

$$
\mathbf{g} = \lambda(\mathbf{U} - \mathbf{P}^\mathrm{T}\mathbf{R}^{-1}\mathbf{P})^{-1}\mathbf{I}\tag{7.39}
$$

$$
\mathbf{f} = \mathbf{R}^{-1}\mathbf{P}\mathbf{g}\tag{7.40}
$$
