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

## 7.5 二维目标和二维均衡器

本节将介绍使用二维目标和二维均衡器来降低ISI和ITI影响的方法，其性能优于一维均衡器[108]。此外，该方法还可应用于其他二维数据存储系统，如全息数据存储系统[122]、二维光存储系统（TwoDOS: 2D optical storage system）[123]或多磁头读取的水平/垂直数据存储系统[124, 125]等。

![](images/chapter_7/daf939f8ca3e6d31545f4ac22f6bd4f467b7c5d9cca4c847e9a1676c3c3e6f07.jpg)

![](images/chapter_7/ab4b19b8de2eb980209bff419faea59795772fc143f498fd7e8dc0921cea576f.jpg)  
图7.3 用于二维目标和二维均衡器设计的信道模型[108]

图7.3展示了使用多磁头读取数据的BPMR信道模型，用于二维目标和二维均衡器的设计。由于岛（或比特）的位置已确定在记录介质中，因此读回信号由比特位置（而非时间索引）决定。设参数$j$和$k$分别表示岛在跨磁道和沿磁道方向的位置，其中$j = 0$对应中间磁道。从图7.3可知，输入数据序列$a_{j,k} \in \{\pm 1\}$被送入具有二维脉冲响应$H(m,n)$的BPMR信道，得到的读回信号$r_{j,k}$可写为：

$$
r_{j,k} = \sum_m \sum_n h_{m,n} a_{j-m,k-n} + n_{j,k}\tag{7.41}
$$

其中$h_{m,n}$是信道$H(m,n)$的系数，$n_{j,k}$是AWGN噪声。类似地，在接收端，读回信号$r_{j,k}$被送入二维均衡器$F(D_z, D_x)$：

$$
F(D_z, D_x) = \sum_{m=-M}^{M} \sum_{n=-K}^{K} f_{m,n} D_z^m D_x^n\tag{7.42}
$$

其中$f_{m,n}$是$F(D_z, D_x)$的系数，$\{M, K\}$是正整数，$D_z$和$D_x$分别是跨磁道和沿磁道方向单位延迟算子。

![](images/chapter_7/99ebe321182ab604d81fe6d8af2c5dcea6a1c9d2bbdc447438b61fc90b79aeb5.jpg)

将读回信号的特性整形为所需的二维目标$G(D_z, D_x)$：

$$
G(D_z, D_x) = \sum_{m=-L}^{L} \sum_{n=0}^{2L} g_{m,n} D_z^m D_x^n\tag{7.43}
$$

其中$g_{m,n}$是$G(D_z, D_x)$的系数，$L$是正整数。然后结果被送入维特比检测器以估计数据序列$a_{0,k}$（即$\hat{a}_{0,k}$）。

接收端的目的是仅检测中间磁道（即$j=0$）的数据序列。因此，在二维目标和二维均衡器的设计中，仅使用中间磁道的均衡器输出和中间磁道的目标输出，分别记为$z_{0,k}$和$d_{0,k}$。设式(7.42)中的$F(D_z, D_x)$具有$(2M+1) \times (2K+1)$的矩阵形式：

$$
\mathbf{F} = \left[ \begin{array}{ccccc} f_{-M,-K} & \cdots & f_{-M,0} & \cdots & f_{-M,K} \\ \vdots & \vdots & \vdots & \vdots & \vdots \\ f_{0,-K} & \cdots & f_{0,0} & \cdots & f_{0,K} \\ \vdots & \vdots & \vdots & \vdots & \vdots \\ f_{M,-K} & \cdots & f_{M,0} & \cdots & f_{M,K} \end{array} \right]\tag{7.44}
$$

设式(7.43)中的$G(D_z, D_x)$具有$(2L+1) \times (2L+1)$的矩阵形式：

$$
\mathbf{G} = \left[ \begin{array}{ccccc} g_{-L,0} & \cdots & g_{-L,L} & \cdots & g_{-L,2L} \\ \vdots & \vdots & \vdots & \vdots & \vdots \\ g_{0,0} & \cdots & g_{0,L} & \cdots & g_{0,2L} \\ \vdots & \vdots & \vdots & \vdots & \vdots \\ g_{L,0} & \cdots & g_{L,L} & \cdots & g_{L,2L} \end{array} \right]\tag{7.45}
$$

其中$2M+1$是磁头数，$N = 2K+1$是均衡器每行的抽头数，$2L+1$是目标每行的抽头数。因此，从图7.3的BPMR信道模型可知，中间磁道的均衡器输出为：

$$
z_k = z_{0,k} = \sum_{m=-M}^{M} \sum_{n=-K}^{K} f_{m,n} r_{-m,k-n} = \mathbf{f}^\mathrm{T} \mathbf{r}_k\tag{7.46}
$$

![](images/chapter_7/6fb0ea9a9670cbf475940c1a185fae2090d0b2a1f3dd8697b33faafbaa720afe.jpg)

这是数据$r_{j,k}$和$f_{m,n}$之间的二维卷积。其中$\mathbf{f} = [f_{-M,-K} \ f_{-M,-K+1} \ \dots \ f_{-M,K} \ f_{-M+1,-K} \ \dots \ f_0 \ \dots \ f_{M,K-1} \ f_{M,K}]^\mathrm{T}$是均衡器的列向量（即将矩阵F的每行元素排列成向量f），有$N(2M+1)$个元素；$\mathbf{r}_k = [r_{M,k+K} \ r_{M,k+K-1} \ \ldots \ r_{M,k-K} \ r_{M-1,k+K} \ \ldots \ r_{0,k} \ \ldots \ r_{-M,k-K+1} \ r_{-M,k-K}]^\mathrm{T}$是对应于向量f的读回信号列向量。类似地，中间磁道的目标输出为：

$$
d_k = d_{0,k} = \sum_{m=-L}^{L} \sum_{n=0}^{2L} g_{m,n} a_{-m,k-n} = \mathbf{g}^\mathrm{T} \mathbf{a}_k\tag{7.47}
$$

其中$\mathbf{g} = [g_{-L,0} \ g_{-L,1} \ \dots \ g_{-L,2L} \ g_{-L+1,0} \ \dots \ g_{0,L} \ \dots \ g_{L,2L-1} \ g_{L,2L}]^\mathrm{T}$是目标的列向量（有$(2L+1)^2$个元素），$\mathbf{a}_k = [a_{L,k} \ a_{L,k-1} \ \ldots \ a_{L,k-2L} \ a_{L-1,k} \ \ldots \ a_{0,k-L} \ \ldots \ a_{-L,k-2L+1} \ a_{-L,k-2L}]^\mathrm{T}$是对应于向量g的输入数据序列列向量。因此，$z_k$与$d_k$之间的差为：

$$
\boldsymbol{w}_k = z_k - d_k = \mathbf{f}^\mathrm{T} \mathbf{r}_k - \mathbf{g}^\mathrm{T} \mathbf{a}_k\tag{7.48}
$$

均方误差（MSE）为：

$$
E[w^2] = E[(z_k - d_k)^2] = \mathbf{f}^\mathrm{T} \mathbf{R} \mathbf{f} + \mathbf{g}^\mathrm{T} \mathbf{A} \mathbf{g} - 2\mathbf{f}^\mathrm{T} \mathbf{P} \mathbf{g}\tag{7.49}
$$

其中$\mathbf{R} = E[\mathbf{r}_k \mathbf{r}_k^\mathrm{T}]$是$\mathbf{r}_k$的自相关矩阵，$\mathbf{P} = E[\mathbf{r}_k \mathbf{a}_k^\mathrm{T}]$是$\mathbf{r}_k$和$\mathbf{a}_k$的互相关矩阵，$\mathbf{A} = E[\mathbf{a}_k \mathbf{a}_k^\mathrm{T}]$是$\mathbf{a}_k$的自相关矩阵。

MMSE目标设计方法使用莫尼克约束$g_{0,0} = 1$（以避免得到$\mathbf{f} = \mathbf{g} = \mathbf{0}$的解）。此外，为避免使用复杂度极高的二维维特比检测器[108]，对g施加另一个约束：将所有相邻磁道的目标系数设为零（zero-ITI forcing constraint），以消除ITI的影响，从而可以使用通用（一维）维特比检测器。满足这两个约束条件的$3 \times 3$目标G（ISI和ITI长度均为3）示例如下：

![](images/chapter_7/5ebb8d67749e1f4fa4c5c0e59cf8a0ff67c6f7c7af09081f5d87702b5fd4bbec.jpg)

$$
\mathbf{G} = \left[ \begin{array}{ccc} 0 & 0 & 0 \\ g_{0,0} & 1 & g_{0,2} \\ 0 & 0 & 0 \end{array} \right]\tag{7.50}
$$

写为向量形式为：

$$
\mathbf{g} = [0 \ 0 \ 0 \ g_{0,0} \ 1 \ g_{0,2} \ 0 \ 0 \ 0]^\mathrm{T}\tag{7.51}
$$

因此，这两个约束条件可以写为：

$$
\mathbf{E}^\mathrm{T} \mathbf{g} = \mathbf{I}\tag{7.52}
$$

其中

$$
\mathbf{I} = [1 \ 0 \ 0 \ 0 \ 0 \ 0 \ 0]^\mathrm{T}\tag{7.53}
$$

和

$$
\mathbf{E}^\mathrm{T} = \left[ \begin{array}{ccccccccc} 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \end{array} \right]\tag{7.54}
$$

采用这两个约束条件的MMSE方法使式(7.49)中的MSE最小化，同时始终保持$\mathbf{E}^\mathrm{T} \mathbf{g} = \mathbf{I}$，即最小化：

$$
E[w^2] = \mathbf{f}^\mathrm{T} \mathbf{R} \mathbf{f} + \mathbf{g}^\mathrm{T} \mathbf{A} \mathbf{g} - 2\mathbf{f}^\mathrm{T} \mathbf{P} \mathbf{g} - 2\boldsymbol{\lambda}^\mathrm{T} (\mathbf{E}^\mathrm{T} \mathbf{g} - \mathbf{I})\tag{7.55}
$$

其中$\boldsymbol{\lambda}$是列向量，其元素为7个拉格朗日乘子（对应于矩阵$\mathbf{E}^\mathrm{T}$的行数）。对式(7.55)分别对$\mathbf{f}$、$\mathbf{g}$和$\boldsymbol{\lambda}$求导并令结果为零，可得：

![](images/chapter_7/0e56679269d57d1129eaf1c2e8ef1e5c7314499393a02e94f4f62afd811f545e.jpg)

![](images/chapter_7/9e70c6acd1c1602b73c31599ce11c7522a4e60e47ec73bc64f3dac8d450ed999.jpg)  
图7.4 等效信道模型

$$
\boldsymbol{\lambda} = (\mathbf{E}^\mathrm{T} (\mathbf{A} - \mathbf{P}^\mathrm{T} \mathbf{R}^{-1} \mathbf{P})^{-1} \mathbf{E})^{-1} \mathbf{I}\tag{7.56}
$$

$$
\mathbf{g} = (\mathbf{A} - \mathbf{P}^\mathrm{T} \mathbf{R}^{-1} \mathbf{P})^{-1} \mathbf{E} \lambda\tag{7.57}
$$

$$
\mathbf{f} = \mathbf{R}^{-1} \mathbf{P} \mathbf{g}\tag{7.58}
$$

## 7.6 BPMR系统中使用的维特比检测器

本节将总结BPMR系统中使用的通用（一维）维特比检测器和各种二维维特比检测器的原理，并展示不同维特比检测器的复杂度。

### 7.6.1 一维维特比检测器

[10]的第4章详细说明了一维目标使用的通用（一维）维特比检测器的原理。因此，这里将总结一维维特比检测器的原理，以便读者更容易理解二维维特比检测器的原理。

假设完全均衡（perfect equalization），图7.1的模型可简化为图7.4的等效信道模型，其中$w_k \sim \mathcal{N}(0, \sigma^2)$是AWGN噪声。实际上，维特比检测器的工作原理基于trellis图[13]。图7.5定义了trellis图中的符号：$\Psi_k = [a_k \ a_{k-1} \ \dots \ a_{k-\nu+1}]$是时刻k的状态(state)，$Q = |\mathcal{A}|^\nu$是可能的状态总数，$|\mathcal{A}|$是输入数据的所有可能值数目，$\nu$是信道（或目标）的记忆长度，$(u, q)$表示从状态u到状态q的转移。

![](images/chapter_7/ba1bfe3ce9db6ec255c24cda49fde236c564a968b69536d20fcd2bcb5248a2b8.jpg)  
图7.5 trellis图说明

![](images/chapter_7/b770ef2375c4faaf3472234739ecda24c7c6c223e652948de8c3ade51232dc0d.jpg)  
图7.6 PR4信道的trellis图，$H(D) = 1 - D^2$

图7.6展示了PR4信道（即$G(D) = 1 - D^2$）的trellis图示例，其中有$Q = 2^2 = 4$个状态，用(0)、(1)、(2)和(3)表示，输入数据$a_{0,k} \in \{\pm 1\}$。在维特比算法中，每个时刻需要计算的是：从状态u到状态q的转移在时刻k的分支度量（branch metric）$\lambda_k(u, q)$；状态q在时刻k+1的路径度量（path metric）$\Phi_{k+1}(q)$；以及状态q在时刻k+1的前驱（predecessor）$\pi_{k+1}(q)$，它保存导致最佳转移路径的起始状态。例如，考虑时刻$k+1$的状态(2)，有2条转移路径：(1,2)和(3,2)。维特比算法只选择到达状态(2)的最佳路径。假设(1,2)是最佳转移路径，则$\pi_{k+1}(2) = 1$。

![](images/chapter_7/de3044392eb21d99358c307b1b984fad84d8b10d62b267259752951e91740adf.jpg)

使数据序列误差概率最小的检测器是"最大似然序列检测器（MLSD）"[13]，可通过维特比算法实现，因此称为"维特比检测器"。从图7.4的模型可知，维特比检测器选择使条件概率最大的输入数据序列$a_{0,k}$：

$$
p(\mathbf{r} \mid \mathbf{a}) = \frac{1}{(\sqrt{2\pi\sigma^2})^{S+\nu}} \exp\left\{ -\frac{1}{2\sigma^2} \sum_{k=0}^{S+\nu} |r_k - d_k|^2 \right\}\tag{7.59}
$$

其中$S$是$a_{0,k}$的总比特数。对式(7.59)两边取自然对数：

$$
\ln\{p(\mathbf{r} \mid \mathbf{a})\} = \ln\left\{ \frac{1}{(\sqrt{2\pi\sigma^2})^{S+\nu}} \right\} - \frac{1}{2\sigma^2} \sum_{k=0}^{S+\nu-1} |r_k - d_k|^2\tag{7.60}
$$

注意到使式(7.60)最大等价于使式(7.60)右边的第二项最小，因为第一项相当于常数。因此，维特比检测器选择使度量最小的输入数据序列$a_{0,k}$：

$$
\sum_{k=0}^{S+\nu-1} |r_k - d_k|^2\tag{7.61}
$$

这可以通过在trellis图中搜索具有最小度量的路径来实现，其中路径度量等于分支度量的总和。从状态u到状态q转移的分支度量定义为：

$$
\lambda_k(u, q) = |r_k - \hat{d}_k(u, q)|^2\tag{7.62}
$$

其中$\hat{d}_k(u, q)$是对应于(u, q)的信道输出。路径度量可由下式得到：

$$
\Phi_{k+1}(q) = \sum_{i=0}^{k} \lambda_i\tag{7.63}
$$

![](images/chapter_7/f3a6e1a357b2628b90eccc4fdfa5276b705d116145cd1e7b6beec9a842642a54.jpg)

(A-1) 初始化所有状态p的路径度量$\Phi_0(p) = 0$  
(A-2) For $k = 0, 1, ..., S+\nu-1$  
(A-3) For $q = 0, 1, ..., Q-1$  
(A-4) $\lambda_k(p, q) = |r_k - \hat{d}(p, q)|^2$ for $\forall p$  
(A-5) $\pi_{k+1}(q) = \arg\min_p \{\Phi_k(p) + \lambda_k(p, q)\}$  
(A-6) $\Phi_{k+1}(q) = \Phi_k(\pi_{k+1}(q)) + \lambda_k(\pi_{k+1}(q), q)$  
(A-7) $\mathbf{S}_{k+1}(q) = [\mathbf{S}_k(\pi_{k+1}(q)) \ | \ \pi_{k+1}(q)]$  
(A-8) End  
(A-9) End  
(A-10) 从具有最小$\Phi_{S+\nu}$的存活路径解码输入数据$\hat{a}_{0,k}$  
图7.7 一维维特比算法的步骤[10]

图7.7展示了一维维特比算法的步骤。例如，考虑图7.6中trellis图的第k阶段，有2条转移路径到达时刻$k+1$的状态(2)，即(1,2)和(3,2)。然后根据步骤(A-4)计算2条路径的分支度量$\lambda_k(1,2)$和$\lambda_k(3,2)$。根据步骤(A-5)选择对应于到达状态(2)的最佳转移路径的起始状态。假设(1,2)是最佳转移路径，则$\pi_{k+1}(2) = 1$。然后根据步骤(A-6)更新到达状态(2)的路径度量$\Phi_{k+1}(2)$，根据步骤(A-7)更新到达状态(2)的存活路径$\mathbf{S}_{k+1}(2)$。对接收到的整个数据序列$\{r_k\}$重复这些步骤。最后一步是选择具有最小路径度量$\Phi_{S+\nu}$的存活路径，判决出最大似然数据序列$\{a_{0,k}\}$。

由于维特比检测器需要处理整个序列后才能判决哪个输入序列最可能，因此在实际中，维特比检测器的复杂度取决于多个因素：输入数据可能值的数目$|\mathcal{A}|$、输入数据序列的长度S和目标记忆长度$\nu$。维特比算法的计算示例可参考[10]的第4章。

![](images/chapter_7/e50f1305a185691413efc1796a7d0f67fea5c2b68ceb7821b0a84e5cb6aca7ab.jpg)

### 7.6.2 二维维特比检测器

本节使用图7.2的信道模型说明二维维特比检测器的基本原理，其中目标的输入数据有3个磁道（上磁道、中间磁道和下磁道），二维维特比检测器仅解码中间磁道的输入数据。

一般来说，二维维特比检测器的工作步骤与§7.6.1所述的一维维特比检测器类似，只是二维维特比检测器使用的trellis图可能有更多的状态Q，每个状态转移有更多分支，以及每个状态出发的分支多于两条。因此，不同二维维特比检测器的复杂度取决于trellis图每阶段k的状态数和分支总数，具体说明如下。

#### 7.6.2.1 对称零角二维目标

一般来说，根据§7.2的零角二维目标设计，当系统没有磁道误配准（TMR）问题时，得到的目标G如式(7.15)所示，其系数满足$g_{-1,1} = g_{1,1}$和$g_{-1,0} = g_{1,0} = g_{-1,2} = g_{1,2} = 0$。因此，本节将说明由对称零角二维目标构建的维特比检测器的基本原理。设$3 \times 3$对称零角二维目标为：

$$
\mathbf{G} = \left[ \begin{array}{c} G_{-1}(D) \\ G_0(D) \\ G_1(D) \end{array} \right] = \left[ \begin{array}{ccc} 0 & c & 0 \\ u & p & w \\ 0 & c & 0 \end{array} \right]\tag{7.64}
$$

因此从图7.2可得目标输出为：

$$
d_k = c (a_{-1,k-1} + a_{1,k-1}) + u (a_{0,k}) + p (a_{0,k-1}) + w (a_{0,k-2})\tag{7.65}
$$

图7.8显示了由式(7.64)的二维目标G构建的trellis图一个分支中的转移细节，其中时刻k的每个状态由2个数据决定：中间磁道在时刻k-2和k-1的输入数据（即$a_{0,k-2}$和$a_{0,k-1}$）。

![](images/chapter_7/a86b331a8612390fb4e1ffabd8337ceda972cf895a6385746ba88651fc5cd433.jpg)  
图7.8 由对称零角二维目标构建的trellis图一个分支中的转移

因此，由对称零角二维目标构建的trellis图总共有$2 \times 2 = 4$个状态。每个分支由符号x/y表示，其中$x = [a_{-1,k-1} \ a_{0,k} \ a_{1,k-1}]$是时刻k的目标输入数据（包括上磁道在时刻k-1的输入、中间磁道在时刻k的输入和下磁道在时刻k-1的输入），$y = d_k$是对应于该分支转移的时刻k的目标输出。因此，时刻k的每个状态总共有$2 \times 2 \times 2 = 8$个分支，分为2组（每组4个分支），每组分支转移到时刻$k+1$的2个不同状态。

设$d_k^1$和$d_k^2$分别是与输出$\{a_{-1,k-1}=+1, a_{1,k-1}=-1\}$和$\{a_{-1,k-1}=-1, a_{1,k-1}=+1\}$对应的时刻k的目标输出。从式(7.65)可得$d_k^1 = d_k^2$，这意味着每组中有2个分支（4个分支中的2个）具有相同的目标输出。因此，可以将从时刻k状态到时刻k+1状态q的分支数减少到3个，每个分支的目标输出为：

$$
d_k = \left\{ \begin{array}{ll} (g_{0,k} * a_{0,k}) + 2c, & \mathrm{if} \ a_{-1,k-1} = a_{1,k-1} = 1 \\ (g_{0,k} * a_{0,k}), & \mathrm{if} \ a_{-1,k-1} \neq a_{1,k-1} \\ (g_{0,k} * a_{0,k}) - 2c, & \mathrm{if} \ a_{-1,k-1} = a_{1,k-1} = -1 \end{array} \right.\tag{7.66}
$$

其中$*$是卷积算子，$g_{0,k}$是对应于中间磁道输入数据$a_{0,k}$的目标$G_0(D)$的系数。图7.9显示了由二维目标G构建的trellis图。

![](images/chapter_7/3a7835c39982f37e5683f6cdf14328c7d4098f2647621def8a2c2b28012c4e09.jpg)  
图7.9 由式(7.64)的二维目标G构建的trellis图

使用此trellis图解码数据的维特比检测器称为"改进的二维维特比检测器（modified 2D Viterbi detector）"[126]，它是所有二维维特比检测器中复杂度最低的。

#### 7.6.2.2 对称二维目标

这里，式(7.28)的$3 \times 3$对称二维目标是指上磁道和下磁道系数相等的二维目标G，即$g_{-1,0} = g_{1,0}$，$g_{-1,1} = g_{1,1}$，$g_{-1,2} = g_{1,2}$。为便于说明，设对称二维目标为：

$$
\mathbf{G} = \left[ \begin{array}{c} G_{-1}(D) \\ G_0(D) \\ G_1(D) \end{array} \right] = \left[ \begin{array}{ccc} b & c & d \\ u & p & w \\ b & c & d \end{array} \right]\tag{7.67}
$$

因此从图7.2可得目标输出为：

$$
d_k = b(a_{-1,k} + a_{1,k}) + c(a_{-1,k-1} + a_{1,k-1}) + d(a_{-1,k-2} + a_{1,k-2}) + u(a_{0,k}) + p(a_{0,k-1}) + w(a_{0,k-2})\tag{7.68}
$$

由于BPMR系统使用对称二维目标，因此可以将上磁道$a_{-1,k}$和下磁道$a_{1,k}$的输入数据合并，其值为：

![](images/chapter_7/06e7587628e3caf8b0c8968a145263fb41534194031fb95ff31626046fa6bd7e.jpg)

![](images/chapter_7/45aff2c1599a99678e03016723bf8d99e0fecea35f77f84d538737c8117eb894.jpg)  
图7.10 由对称二维目标构建的trellis图一个分支中的转移

$$
(a_{-1,k} + a_{1,k}) = \left\{ \begin{array}{ll} -2, & \mathrm{if} \ a_{-1,k} = -1 \ \mathrm{and} \ a_{1,k} = -1 \\ 0, & \mathrm{if} \ a_{-1,k} = -1 \ \mathrm{and} \ a_{1,k} = +1 \\ 0, & \mathrm{if} \ a_{-1,k} = +1 \ \mathrm{and} \ a_{1,k} = -1 \\ +2, & \mathrm{if} \ a_{-1,k} = +1 \ \mathrm{and} \ a_{1,k} = +1 \end{array} \right.\tag{7.69}
$$

将两个磁道的输入数据合并考虑有助于降低二维维特比检测器的复杂度。图7.10显示了由对称二维目标构建的trellis图一个分支中的转移细节，其中时刻k的每个状态由4个数据决定：时刻k-2的上下磁道输入数据和、时刻k-1的上下磁道输入数据和、中间磁道在时刻k-2的输入数据和中间磁道在时刻k-1的输入数据。因此，由对称二维目标构建的trellis图总共有$3 \times 3 \times 2 \times 2 = 36$个状态，每个状态在时刻k有$3 \times 2 = 6$个分支，分别转移到时刻k+1的6个不同状态。此外，每个分支由符号$x/y$表示，其中$x = [(a_{-1,k} + a_{1,k}) \ a_{0,k}]$是时刻k的目标输入数据，$y = d_k$是对应于该分支转移的时刻k的目标输出。

#### 7.6.2.3 非对称二维目标

这里，式(7.15)的$3 \times 3$非对称二维目标是指上磁道和下磁道系数不等的二维目标G，即$G_{-1}(D) \neq G_1(D)$。因此，BPMR系统的接收端必须使用复杂度最高的全复杂度二维维特比检测器（full-complexity 2D Viterbi detector）来解码数据。图7.11显示了由非对称二维目标构建的trellis图一个分支中的转移细节。这里假设二维目标G的记忆长度为$\nu = 2$，所有可能的输入模式数为$|\mathcal{A}| = 2 \times 2 \times 2 = 8$。因此，由非对称二维目标构建的trellis图共有$|\mathcal{A}|^\nu = 8^2 = 64$个状态，其中时刻k的每个状态由所有磁道在时刻k-2和k-1的输入数据决定。每个状态在时刻k有$2 \times 2 \times 2 = 8$个分支，分别转移到时刻k+1的8个不同状态。此外，每个分支由符号$x/y$表示，其中$x = [a_{-1,k} \ a_{0,k} \ a_{1,k}]$是时刻k的目标输入数据（来自上磁道、中间磁道和下磁道），$y = d_k$是对应于该分支转移的时刻k的目标输出。

![](images/chapter_7/00504c739880e173fe6952b151e40269c9577aa327712d431b52d225defaacc0.jpg)

![](images/chapter_7/1adf72a4f4cdd14405c4e2ec9f81c748a3bb86fda7a62a02d041b4f7a706f5f3.jpg)  
图7.11 由非对称二维目标构建的trellis图一个分支中的转移

## 7.7 实验结果

考虑图7.2的BPMR信道模型，定义信号功率与噪声功率之比为：

$$
\mathrm{SNR} = 10 \log_{10} \left( \frac{1}{\sigma^2} \right)\tag{7.70}
$$

单位为分贝（dB）。这里比较以下4种系统的性能：

系统1：使用一维目标（§7.1）和一维维特比检测器（§7.6.1），称为"1D target"。

![](images/chapter_7/6ef6b46791a5884178174ce441ad0bb91004b719a87cb51ef20dda521cdbbf76.jpg)

系统2：使用零角二维目标（§7.2）和改进的二维维特比检测器（§7.6.2.1），称为"Zero-corner 2D target"。

系统3：使用对称二维目标（§7.3）和二维维特比检测器（§7.6.2.2），称为"Symmetric 2D target"。

系统4：使用非对称二维目标（§7.4）和二维维特比检测器（§7.6.2.3），称为"Asymmetric 2D target"。

所有系统均使用11抽头的一维均衡器（增加均衡器抽头数不会显著提高系统性能[108]）。

考虑BPMR系统使用方形岛制作的记录介质，岛边长a = 11 nm，岛高δ = 10 nm，磁头飞行高度d = 10 nm，使用MR磁头，厚度t = 4 nm，宽度W = 15 nm，绝缘层与MR元件之间的间隙宽度g = 6 nm，对应的二维脉冲响应为$\mathrm{PW}_{50}^{\mathrm{along}} = 19.8$ nm和$\mathrm{PW}_{50}^{\mathrm{cross}} = 24.8$ nm[108]（各参数含义见图6.8）。这里使用式(6.14)的二维高斯脉冲信号，在给定$\mathrm{PW}_{50}^{\mathrm{along}}$和$\mathrm{PW}_{50}^{\mathrm{cross}}$的条件下，构建不同数据容量下的信道矩阵H。在容量为$2 \ \mathrm{Tb/in}^2$时，由式(6.13)可得$T_x = T_z \approx 18$ nm，且：

$$
\mathbf{H}_{2 \ \mathrm{Tb/in}^2} = \left[ \begin{array}{ccccc} 2.43\times10^{-5} & 0.023 & 0.232 & 0.023 & 2.43\times10^{-5} \\ 1\times10^{-4} & 0.101 & 1 & 0.101 & 1\times10^{-4} \\ 2.43\times10^{-5} & 0.023 & 0.232 & 0.023 & 2.43\times10^{-5} \end{array} \right]\tag{7.71}
$$

在容量为$2.5 \ \mathrm{Tb/in}^2$时，由式(6.13)可得$T_x = T_z \approx 16$ nm，且：

$$
\mathbf{H}_{2.5 \ \mathrm{Tb/in}^2} = \left[ \begin{array}{ccccc} 2.26\times10^{-4} & 0.052 & 0.315 & 0.052 & 2.26\times10^{-4} \\ 7.16\times10^{-4} & 0.164 & 1 & 0.164 & 7.16\times10^{-4} \\ 2.26\times10^{-4} & 0.052 & 0.315 & 0.052 & 2.26\times10^{-4} \end{array} \right]\tag{7.72}
$$

在容量为$3 \ \mathrm{Tb/in}^2$时，由式(6.13)可得$T_x = T_z \approx 14.5$ nm，且：

$$
\mathbf{H}_{3 \ \mathrm{Tb/in}^2} = \left[ \begin{array}{ccccc} 0.0010 & 0.088 & 0.388 & 0.088 & 0.0010 \\ 0.0026 & 0.226 & 1 & 0.226 & 0.0026 \\ 0.0010 & 0.088 & 0.388 & 0.088 & 0.0010 \end{array} \right]\tag{7.73}
$$

在容量为$3.5 \ \mathrm{Tb/in}^2$时，由式(6.13)可得$T_x = T_z \approx 13.6$ nm，且：

![](images/chapter_7/96811bff3abf16eaa69e1b02efd32e1dfa0992026f4757ae74a9a641328ab1ee.jpg)

![](images/chapter_7/b31e3565e409ab7bfd62b3497b3b9e432f03f9b15d5d058d8149b91e5fa1da7b.jpg)  
图7.12 使用不同目标的系统性能

$$
\mathbf{H}_{3.5 \ \mathrm{Tb/in}^2} = \left[ \begin{array}{ccccc} 0.0023 & 0.117 & 0.434 & 0.117 & 0.0023 \\ 0.0053 & 0.270 & 1 & 0.270 & 0.0053 \\ 0.0023 & 0.117 & 0.434 & 0.117 & 0.0023 \end{array} \right]\tag{7.74}
$$

图7.12比较了使用不同目标的系统性能。可以看出，在数据容量$\leq 2 \ \mathrm{Tb/in}^2$时，所有系统的性能相近（因为ITI的严重程度低于ISI）。因此，当BPMR系统数据容量不高（$\leq 2 \ \mathrm{Tb/in}^2$）时，应选择"1D target"，以便使用复杂度低且性能尚可的一维维特比检测器。然而，当数据容量增加（$> 2 \ \mathrm{Tb/in}^2$）时，"1D target"系统的性能开始劣于使用二维目标的系统（因为ITI变得更加严重）。因此，当BPMR系统具有高数据容量（$\geq 2.5 \ \mathrm{Tb/in}^2$）时，应选择二维目标，因为它在降低ITI影响方面优于一维目标。从图7.12还发现，使用"Symmetric 2D target"和"Asymmetric 2D target"的系统性能优于使用"Zero-corner 2D target"的系统，特别是在高数据容量（$\geq 3 \ \mathrm{Tb/in}^2$）时。这是因为当ITI非常严重时（从矩阵H第一行和第三行的系数可以看出），使用"Symmetric 2D target"或"Asymmetric 2D target"可以比使用"Zero-corner 2D target"更好地降低ITI影响。此外，在本实验中还发现使用"Symmetric 2D target"和"Asymmetric 2D target"的系统性能相同，因为信道响应（即矩阵H）是对称的，且系统没有磁道误配准影响，使得设计的对称和非对称二维目标系数非常接近，从而导致系统性能相同。

![](images/chapter_7/6e53f11c6a2a3f0352f6675f4f25e912f9aca8ef4a633fdd1b13c0d0e4363bf1.jpg)

![](images/chapter_7/07a4de6d07f1c21b2bd027d321240859beb8a1046b70dfb8637991b7ba81ee78.jpg)  
图7.13 用于二维目标和二维均衡器设计的BPMR信道模型（3磁头）[108]

### 7.7.1 二维均衡器的性能

图7.13展示了使用3个磁头读取数据的BPMR信道模型，用于§7.5所述的二维目标和二维均衡器设计（改编自图7.3），其中二维均衡器F和二维目标G分别如式(7.44)和(7.45)所示，$M = 1$，$L = 1$。由于$M = 1$的二维均衡器F使用3个相邻磁道的读回信号（即$r_{-1,k}$、$r_{0,k}$和$r_{1,k}$），因此生成这3个读回信号需要使用5个磁道的输入数据（即$a_{-2,k}$、$a_{-1,k}$、$a_{0,k}$、$a_{1,k}$和$a_{2,k}$），以使每个读回信号包含ITI的影响。

图7.14比较了使用一维均衡器的BPMR系统（使用"1D target"和"Zero-corner 2D target"）和使用3磁头二维均衡器的BPMR系统（这里称为"1D target with 2D-EQ"）的性能，其中使用的二维目标形式如式(7.50)（可视为一维目标，能使用一维维特比检测器）。从图可以看出，当系统使用相同类型的目标（这里是一维目标）时，使用二维均衡器的系统性能总是优于使用一维均衡器的系统，特别是在高数据容量时。这是因为二维均衡器在降低ITI影响方面优于一维均衡器。

![](images/chapter_7/1371692ea0ca05fad1852a31cb8c7dbca879c8f6468c02fe98c85e9c39e46886.jpg)

![](images/chapter_7/568e7235c89549e11449d56c48990d0d8ce298ccc3e07755530c61738170516a.jpg)  
图7.14 使用一维和二维均衡器的系统性能

尽管二维均衡器的性能优于一维均衡器，但使用二维均衡器需要系统配备3个磁头，这在实践中难以实现（特别是应用于当前使用的垂直记录系统时）。然而，如果要将二维均衡器用于单磁头BPMR系统，也可以通过使用缓冲器来存储3个读回信号（即系统读取3次数据），然后将这3个读回信号一起用二维均衡器处理。这是因为BPMR系统中的每个岛在记录介质中有确定的位置，因此3个读回信号的同步并不困难[108]。

### 7.7.2 介质噪声和磁道误配准的影响

本节将展示在有介质噪声和磁道误配准（TMR）影响的BPMR系统中，二维目标和一维均衡器的性能，如图7.15所示。使用式(6.15)的时域连续信道$P(z,x)$来包含介质噪声的影响，并使用式(6.21)来包含TMR的影响。这里，磁头获得的读回信号为：

![](images/chapter_7/adb80679ba10ff538a724ad8dfab4ceb4b51c84dbc6a9a1a630b9caf76e18d19.jpg)

![](images/chapter_7/016f5c9e35762ac86fb80c96e46984289d85f92f5dc4c191e4f9623172e19e8d.jpg)  
图7.15 包含介质噪声和磁道误配准影响的单磁头BPMR信道模型

$$
y(t) = \sum_{m=-1}^{1} \sum_{n=-1}^{1} a_{m,n} P(-mT_z - \Delta_T, t - nT_x) + n(t)\tag{7.75}
$$

其中$n(t)$是功率谱密度为$N_0/2$的双边AWGN噪声。读回信号$y(t)$在时刻$t = kT_x$采样，得到序列$r_k$。然后使用输入数据$\{a_{m,k}\}$和$\{r_k\}$来设计15抽头一维均衡器和各种$3 \times 3$二维目标。此外，使用的SNR由式(7.70)定义，其中$\sigma^2 = N_0/(2T)$。

图7.16展示了在3 Tb/in²容量下，不同介质噪声强度时使用不同目标的系统性能，其中y轴是使$\mathrm{BER} = 10^{-4}$所需的SNR。从图可以看出，"1D target"系统的性能最差，而"Asymmetric 2D target"系统的性能最好，特别是在介质噪声非常强时。同样，图7.17展示了在3 Tb/in²容量下，不同TMR强度时使用不同目标的系统性能，发现"Asymmetric 2D target"系统的性能优于其他目标。此外，当TMR非常严重时，信道变得不对称，因此对称目标的性能比零角目标更差。

### 7.7.3 迭代BPMR系统的性能

如§4.6.2所述，使用迭代解码技术（软检测器和LDPC解码器协同工作）[3, 21]的系统可以显著提高性能，相比不使用迭代解码技术的系统。

![](images/chapter_7/5bcbd478309388acab1f55d939837ba8f8a45bd65c9885279658f2b19fd31391.jpg)  
图7.16 具有介质噪声影响的系统性能（使用不同目标）

![](images/chapter_7/1ebfae1f5c40e7adfd12cfb664b5d5e23cf3d901696998aab2c9f5b081095173.jpg)  
图7.17 具有磁道误配准影响的系统性能（使用不同目标）

因此，本节将展示使用迭代解码技术的BPMR系统的性能。

![](images/chapter_7/a514428afb227a660481d141417d95b941f29282ea75c35c83ff396cb423738a.jpg)  
图7.18 (a)编码器 (b)解码器，添加到图7.2的BPMR系统中

由于迭代解码技术必须用于编码系统，因此可以通过添加图7.18所示的编码器和解码器，将图7.2中的未编码BPMR系统变为编码系统。即在发送端，每个磁道的消息比特$\{u_{m,k}\}$（$m \in \{0, \pm 1\}$，每磁道3640比特）使用码率为8/9的规则(3,27)LDPC码[17]进行编码，得到每磁道4095比特的数据序列$\{a_{m,k}\}$，如图7.18(a)所示，其中校验矩阵每列有3个1，每行有27个1。然后数据序列$\{a_{m,k}\}$根据图7.2送入信道H。在接收端，图7.2中均衡器的输出$z_k$被送入图7.18(b)所示的Turbo均衡器[21]，这是二维SOVA检测器（2D-SOVA detector）[120]和LDPC解码器之间的迭代工作。LDPC解码基于消息传递算法（Message-Passing）[17]，进行3次内部迭代，得到中间磁道消息比特的估计值$\hat{u}_{0,k}$。

二维SOVA检测器是双向SOVA（bi-directional SOVA）[42]，如§3.5所述。只是2D-SOVA检测器使用的trellis图具有更多的状态Q、从每个状态出发的分支多于两条、或每个状态转移有多条分支（与二维维特比检测器的trellis图相同），这取决于系统中使用的二维目标类型。然而，如果BPMR系统使用一维目标（1D target），则Turbo均衡器使用SOVA检测器[19, 42]（普通或双向均可，如§3.4和§3.5所述），而不是2D-SOVA检测器。

![](images/chapter_7/1b71f6c328679fd383cfd1e029f5edf9433ab710c0642d3f4d5c0d3d8719d570.jpg)

![](images/chapter_7/9a41d2ab803c08fe43aff734e12bc6fca7200a9aeadb278351c42f46da6251ac.jpg)  
图7.19 第5次迭代时使用不同目标的迭代BPMR系统性能

以下实验比较了使用3种目标（1D target、Zero-corner 2D target和Symmetric 2D target）的迭代BPMR系统的性能。使用的均衡器有15个抽头，SNR定义为：

$$
\mathrm{SNR} = 10 \log_{10} \left( \frac{1}{R\sigma^2} \right)\tag{7.76}
$$

单位为分贝（dB），其中$\sigma^2 = N_0/(2T)$，$R = 8/9$是LDPC码率。图7.19比较了第5次迭代时使用不同目标的迭代BPMR系统的性能。可以发现，使用"Symmetric 2D target"的系统性能优于使用"Zero-corner 2D target"和"1D target"的系统，特别是在高数据容量时。

## 7.8 本章总结

在实际中，PRML检测器仍可用于BPMR系统的数据检测，就像目前常用的记录系统一样。然而，PRML检测器的性能取决于系统中目标和均衡器的适当选择。因此，本章介绍了针对不同情况的各种一维和二维目标以及一维和二维均衡器的设计方法，因为良好的目标和均衡器可以有效降低BPMR系统中ISI和ITI的影响。

从实验结果发现，"1D target"适用于低数据容量（≤ 2.5 Tb/in²）的系统，"Zero-corner 2D target"适用于中等数据容量（2.5–3 Tb/in²）的系统，而"Symmetric 2D target"和"Asymmetric 2D target"适用于高数据容量（≥ 3 Tb/in²）的系统。此外还发现，"Symmetric 2D target"不适用于有磁道误配准影响的系统，二维均衡器的性能优于一维均衡器，但需要系统配备3个磁头，这在实际中仍然难以实现。

## 7.9 习题

1. 编写SCILAB程序设计：
   1.1) 一维目标和一维均衡器
   1.2) 零角二维目标和一维均衡器
   1.3) 对称二维目标和一维均衡器
   1.4) 非对称二维目标和一维均衡器
   1.5) 二维目标和二维均衡器

2. 比较一维均衡器和二维均衡器之间的差异。

3. 画出输入数据为{-1, 1}的详细trellis图（显示所有状态、分支和分支数据）：
   3.1) 式(7.64)定义的对称零角二维目标
   3.2) 式(7.67)定义的对称二维目标
   3.3) 式(7.15)定义的非对称二维目标

4. 详细说明2D-SOVA检测器的工作原理，并给出计算示例：
   4.1) 对称零角二维目标
   4.2) 对称二维目标
