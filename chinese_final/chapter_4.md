## 第四章

## LDPC码

低密度奇偶校验码（LDPC: low-density parity-check）[17]被公认为当前最优秀的纠错码（ECC）[2, 5]，其性能比其他ECC码更接近香农极限[25]。目前，LDPC码已应用于多种领域，包括硬盘驱动器。

由于LDPC码是一种线性分组码，本章将从线性分组码的基础开始介绍，然后重点讲解LDPC码的工作原理，使读者理解LDPC码的编码和解码步骤，同时展示当前硬盘驱动器信号处理系统中使用的Turbo均衡器（或迭代解码）的性能——这是软检测器和LDPC解码器协同工作的结果。

## 4.1 引言

本节将介绍线性分组码的工作原理，并解释线性分组码的编码和解码方法，作为后续学习LDPC码的基础。

### 4.1.1 线性分组码

(N, K)线性分组码是一种将K比特信息比特转换为N比特码字的信道码。设 $\mathbf{m} = [m_1, m_2, ..., m_K]$ 是被编码的信息比特向量，得到码字 $\mathbf{c} = [c_1, c_2, ..., c_N]$，如图4.1所示。增加的 $N-K$ 个额外比特称为"奇偶校验比特"，用向量 $\mathbf{p} = [p_1, p_2, ..., p_{N-K}]$ 表示，它们帮助接收端检测错误。如果奇偶校验比特数量足够多，还可以纠正数据错误。

线性分组码逐块进行编码和解码，数据块的大小取决于各应用的特点。信息比特数与码字比特数的比率称为"码率" $R$，定义如下：

$$
R = { \frac { K } { N } }\tag{4.1}
$$

其中 $0 < R \leq 1$ 始终成立。对于硬盘驱动器，需要码率接近1的码，以减少存储介质中用于存储奇偶校验比特的面积损失[43]。

### 4.1.2 生成矩阵

考虑信息比特 $\mathbf{m} = [m_1, m_2, ..., m_K]$，大小为 $1 \times K$（水平方向）。(N, K)线性分组码是通过将信息比特m乘以一个大小为 $K \times N$ 的生成矩阵G（元素为0或1）生成的[2]：

$$
\mathbf{G}_{K \times N} = \left[ \mathbf{I}_{K \times K} \mid \mathbf{P}_{K \times (N-K)} \right] = \left[ { \begin{array} { c c c c c c c c c } { 1 } & { 0 } & { \cdots } & { 0 } & { p_{1,1} } & { p_{1,2} } & { \cdots } & { p_{1,(N-K)} } \\ { 0 } & { 1 } & { \cdots } & { 0 } & { p_{2,1} } & { p_{2,2} } & { \cdots } & { p_{2,(N-K)} } \\ { \vdots } & { \vdots } & { \ddots } & { \vdots } & { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { 0 } & { 0 } & { \cdots } & { 1 } & { p_{K,1} } & { p_{K,2} } & { \cdots } & { p_{K,(N-K)} } \end{array} } \right]\tag{4.2}
$$

其中I是大小为 $K \times K$ 的单位矩阵，P是大小为 $K \times (N-K)$ 的奇偶校验矩阵，对应于码字中的奇偶校验比特。编码结果得到大小为 $1 \times N$ 的码字 $\mathbf{c} = [c_1, c_2, ..., c_N]$，即：


$$
\mathbf{c} = \mathbf{mG} = \left[ m_1 \ m_2 \ \dots \ m_K \ p_1 \ p_2 \ \dots \ p_{N-K} \right]\tag{4.3}
$$

方程(4.3)表明信息比特m出现在码字c中，这种码称为"系统码"[2]。

**例4.1** 对数据 $\mathbf{m} = [101]$ 和 $\mathbf{m} = [110]$ 进行编码，设生成矩阵G为：

$$
\mathbf{G} = { \left[ \begin{array} { l l l l l l } { 1 } & { 0 } & { 0 } & { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 1 } \\ { 0 } & { 0 } & { 1 } & { 1 } & { 0 } & { 1 } \end{array} \right] }\tag{4.4}
$$

解：该生成矩阵G一次对3比特数据进行编码，即 $\mathbf{m} = [m_1 \ m_2 \ m_3]$。因此，使用矩阵G编码得到的码字为：

$$
\begin{array} { c } { \mathbf{c = mG =} \left[ m_1 \ m_2 \ m_3 \right] \left[ \begin{array} { l l l l l l } { 1 } & { 0 } & { 0 } & { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 1 } \\ { 0 } & { 0 } & { 1 } & { 1 } & { 0 } & { 1 } \end{array} \right] } \\ { \mathbf = } \left[ m_1 \ m_2 \ m_3 \ m_1 \oplus m_3 \ m_1 \oplus m_2 \ m_2 \oplus m_3 \right] \end{array}
$$

其中 $\oplus$ 是模2加法运算符（即XOR）。因此，若 $\mathbf{m} = [101]$，则 $\mathbf{c} = [1 \ 0 \ 1 \ 0 \ 1 \ 1]$；若 $\mathbf{m} = [110]$，则 $\mathbf{c} = [1 \ 1 \ 0 \ 1 \ 0 \ 1]$。

### 4.1.3 奇偶校验矩阵

(N, K)线性分组码还可以由大小为 $(N-K) \times N$ 的奇偶校验矩阵H定义，其满足如下关系：

$$
\mathbf{HG}^\mathrm{T} = \mathbf{0}\tag{4.5}
$$

因此，对于任意码字：

$$
\mathbf{Hc}^\mathrm{T} = \mathbf{HG}^\mathrm{T} \mathbf{m}^\mathrm{T} = \mathbf{0}\tag{4.6}
$$

始终成立。此外，矩阵H的每一行都是一个奇偶校验方程，用于确定码字中数据比特 $c_i \ (i=1,2,...,N)$ 的关系。当生成矩阵G采用(4.2)的系统形式时，奇偶校验矩阵为：

$$
{\mathbf{H}}_{(N-K) \times N} = \Bigl[ {\mathbf{P}}^\mathrm{T} \mid {\mathbf{I}}_{(N-K) \times (N-K)} \Bigr]\tag{4.7}
$$

其中 $(\cdot)^\mathrm{T}$ 表示矩阵转置。例如，方程(4.4)中的生成矩阵G可转换为矩阵H：

$$
\mathbf{H} = { \left[ \begin{array} { l l l l l l l } { 1 } & { 0 } & { 1 } & { 1 } & { 0 } & { 0 } \\ { 1 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } & { 0 } & { 0 } & { 1 } \end{array} \right] }\tag{4.8}
$$

### 4.1.4 码的最小距离

线性分组码的性能度量使用码字的汉明重量，定义为：

$$
w_H(\mathbf{c}) = \text{码字}\mathbf{c}\text{中非零元素的个数}\tag{4.9}
$$

例如，若 $\mathbf{c} = [1 \ 0 \ 0 \ 1 \ 0 \ 0]$，则 $w_H([1 \ 0 \ 0 \ 1 \ 0 \ 0]) = 2$。$\mathbf{c}_1$ 和 $\mathbf{c}_2$ 之间的汉明距离定义为：

$$
d_H(\mathbf{c}_1, \mathbf{c}_2) = w_H(\mathbf{c}_1 - \mathbf{c}_2) = \sum_{i=0}^{N-1} (c_{1,i} \neq c_{2,i})\tag{4.10}
$$


例如，若 $\mathbf{c}_1 = [1 \ 1 \ 0 \ 0 \ 1 \ 1]$ 且 $\mathbf{c}_2 = [0 \ 0 \ 0 \ 1 \ 1 \ 1]$，则汉明距离 $d_H(\mathbf{c}_1, \mathbf{c}_2) = 3$。

若码字c共有 $2^K$ 个，码字之间的最小汉明距离称为码的最小距离 $d_{\min}$，定义为：

$$
d_{\min} = \min_{i \neq j} \{ d_H(\mathbf{c}_i, \mathbf{c}_j) \}\tag{4.11}
$$

其中 $\{i, j\} = 0, 1, ..., 2^K - 1$。已知最小距离 $d_{\min}$ 后，可以知道该线性分组码能够纠正的误码数量t为：

$$
t = \frac{|d_{\min} - 1|}{2}\tag{4.12}
$$

能够检测的误码数量e为：

$$
e = d_{\min} - 1\tag{4.13}
$$

此外，码的最小距离 $d_{\min}$ 还可以直接从生成矩阵G和奇偶校验矩阵H求得：

- 码的最小距离等于矩阵G各行元素中最小的汉明重量
- 等于矩阵H中模2相加结果为零的最小列数

### 4.1.5 线性分组码的解码

实际中用于解码线性分组码的方法是"综合征解码"[2]。综合征向量s定义为：

$$
\mathbf{s} = \mathbf{Hr}^\mathrm{T}\tag{4.14}
$$

其中 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e} = [r_0, r_1, ..., r_{N-1}]$ 是待解码数据向量，c是码字向量，$\mathbf{e} = [e_0, e_1, ..., e_{N-1}]$ 是错误向量，$e_i \in \{0, 1\}$，$e_i = 1$ 表示码字第i位有错误。将 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e}$ 代入方程(4.14)可得：

$$
{ \begin{array} { l } { \mathbf{s} = \mathbf{H(c \oplus e)}^\mathrm{T} = \mathbf{Hc}^\mathrm{T} \oplus \mathbf{He}^\mathrm{T} } \\ { \mathbf{\simeq} } \\ { \mathbf{= He}^\mathrm{T} } \end{array} }\tag{4.15}
$$

无错误时（即 $\mathbf{r} = \mathbf{c}$），综合征值始终为零。

一般来说，线性分组码的解码依赖于查找表[2]，该表根据方程(4.15)显示综合征值与错误向量e之间的关系。因此，当接收端需要解码数据序列r时，根据方程(4.14)计算综合征值，然后从查找表中找到与综合征值对应的错误向量e，再根据以下公式解码数据序列r：

$$
\hat{\mathbf{c}} = \mathbf{r} \oplus \mathbf{e}\tag{4.16}
$$

这种解码方法可以自动纠正数据序列r中发生的错误。然而，综合征解码适用于码字长度短且每个码字错误数量少的系统。

由于硬盘驱动器的信号处理系统一次编码和解码一个扇区的数据（即4096比特），若信息比特长度K = 4096比特，则可能的码字总数高达 $2^{4096}$ 种。若为所有可能的综合征值构建查找表，该表将非常庞大（无法实际使用）。因此，综合征解码无法实际应用于硬盘驱动器。

## 4.2 LDPC码基础

LDPC码是一种线性分组码，由奇偶校验矩阵H中"1"的数量相对于矩阵规模非常少的条件定义，以实现码的高最小距离。LDPC码由Gallager于1960年在麻省理工学院提出[17]。然而，初期LDPC码未受到足够关注，原因是计算能力的限制。随后，Tanner于1981年提出使用Tanner图[44]来表示编码中产生的关系，并利用该图帮助简化数据解码。1990年，MacKay和Neal[45]发现LDPC码的性能比Turbo码[3]更接近香农极限，使得LDPC码重新受到广泛关注。此次LDPC码将不再被遗忘，因为目前它已被应用于多种领域，包括硬盘驱动器。

LDPC码是由稀疏矩阵H[17]（大小为M×N）定义的奇偶校验码。码字c的长度为N比特，所有码字必须满足方程(4.6)中的M个奇偶校验方程。LDPC码主要分为两类：

- **规则LDPC码**：矩阵H中"1"的分布是固定的，如Gallager的LDPC码[17]。矩阵H的每一行有相同数量的"1"，每一列也有相同数量的"1"。
- **非规则LDPC码**[46]：矩阵H中"1"的分布不固定，通常性能优于规则LDPC码。

为便于解释LDPC码的工作原理，这里仅考虑矩阵H的所有行均线性无关的情况，这意味着用于编码的信息比特长度为 $K = N - M$ 比特[4, 17]。

### 4.2.1 规则LDPC码

规则(j, k)-LDPC码是指由大小为M×N的奇偶校验矩阵H定义的LDPC码，其中每列有j个"1"，每行有k个"1"，且 $j < k$ 以及 $\{j, k\} \ll N$。这意味着每个奇偶校验方程关联k个数据比特，每个数据比特始终关联j个奇偶校验方程。因此，矩阵H中"1"的总数为 $Mk = Nj$。假设矩阵H的所有行线性无关，则规则LDPC码的码率为：

$$
R = 1 - \frac{M}{N} = 1 - \frac{j}{k}\tag{4.17}
$$

其中由于 $R \leq 1$，故 $j < k$ 始终成立。


在选择规则(j, k)-LDPC码的参数(M, N, j, k)时，需满足关系 $Mk = Nj$。因此，必须选择使 $M = \frac{Nj}{k}$ 为整数的参数N、j和k。例如，规则(3,4)-LDPC码必须用于N=1000或1004的系统，但不能用于N=1002的系统。又如，规则(2,4)-LDPC码的奇偶校验矩阵H为：

$$
\mathbf{H}_{5 \times 10} = { \left[ \begin{array} { l l l l l l l l l l l } { 1 } & { 1 } & { 1 } & { 1 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { 1 } & { 0 } & { 0 } & { 0 } & { 1 } & { 1 } & { 1 } & { 0 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } & { 1 } & { 0 } & { 1 } \\ { 0 } & { 0 } & { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } & { 1 } & { 0 } & { 1 } \end{array} \right] }\tag{4.19}
$$

此时M=5, N=10，满足方程(4.18)。因此，该LDPC码用于编码5比特信息比特（10-5=5），得到10比特的码字。

方程(4.19)中的奇偶校验矩阵H揭示了校验方程与数据比特之间的关系。矩阵H的每一行称为"校验节点"，每一列称为"比特节点"。因此，各校验节点的奇偶校验方程为：

**校验节点1：**

$$
c_1 + c_2 + c_3 + c_4 = 0\tag{4.20}
$$

**校验节点2：**

$$
c_1 + c_5 + c_6 + c_7 = 0\tag{4.21}
$$

**校验节点3：**

$$
c_2 + c_5 + c_8 + c_9 = 0\tag{4.22}
$$

**校验节点4：**

$$
c_3 + c_6 + c_8 + c_{10} = 0\tag{4.23}
$$

**校验节点5：**

$$
c_4 + c_7 + c_9 + c_{10} = 0\tag{4.24}
$$

奇偶校验码可以用Tanner图[44, 50]来表示，这是大小为M×N的奇偶校验矩阵H的图形化表示。Tanner图有N个比特节点（每个比特一个节点）和M个校验节点（每个校验方程一个节点）。这里使用圆形○表示比特节点，使用方形□表示校验节点。当校验节点m与比特节点n之间存在连接边时，对应 $h_{m,n} = 1$。Tanner图也被称为"二分图"，因为图中只有两种节点（比特节点和校验节点），且同类型节点之间没有连接。图4.2显示了规则(2,4)-LDPC码（矩阵H如方程4.19所示）的Tanner图。可以看出，每个比特节点有2条边（对应j=2），每个校验节点有4条边（对应k=4）。该Tanner图也与方程(4.20)-(4.24)中的所有奇偶校验方程一致。

### 4.2.2 非规则LDPC码

非规则LDPC码由Richardson于2001年提出[46]。大小为M×N的奇偶校验矩阵H中"1"的分布不固定，即每行和每列中"1"的数量不一定相同。

在实际应用中，非规则LDPC码由度数分布多项式定义，用于描述各节点的边数。比特节点的度数分布多项式为 $\rho(x) = \sum_i \rho_i x^i$，其中 $\rho_i$ 是度数为i的比特节点数量。类似地，校验节点的度数分布多项式为 $\xi(x) = \sum_i \xi_i x^i$，其中 $\xi_i$ 是度数为i的校验节点数量。

此外，LDPC码的性能作为校验节点和比特节点度数分布的函数，可以通过密度演化理论[48]预测，该理论跟踪校验节点和比特节点之间传递的消息的概率密度。通常，如果系统工作在足够高的SNR下，随着LDPC解码器内解码次数的增加，概率密度的均值趋近于无穷大，这意味着解码器有很高的置信度能正确解码数据。相反，如果系统工作在低SNR下，概率密度的均值会收敛到某个常数，这意味着LDPC解码器存在解码缺陷。因此，作为LDPC码性能（好与坏）分界线的SNR值称为"门限"。非规则LDPC码旨在使该门限尽可能接近香农容量极限[25]（比规则LDPC码更接近）[49]。

图4.3 (7,4)汉明码的Tanner图（例4.2）

**例4.2** 考虑(7,4)汉明码，其生成矩阵为：

$$
\mathbf{G} = { \left[ \begin{array} { l l l l l l l } { 1 } & { 0 } & { 0 } & { 0 } & { 1 } & { 0 } & { 1 } \\ { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 1 } & { 1 } \\ { 0 } & { 0 } & { 1 } & { 0 } & { 1 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 1 } & { 0 } & { 1 } & { 1 } \end{array} \right] }\tag{4.25}
$$

求奇偶校验矩阵H并绘制对应的Tanner图。

解：由于矩阵G具有方程(4.2)的结构，可根据方程(4.7)求得矩阵H：

$$
\mathbf{H} = { \left[ \begin{array} { l l l l l l l } { 1 } & { 1 } & { 1 } & { 0 } & { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 1 } & { 1 } & { 0 } & { 1 } & { 0 } \\ { 1 } & { 1 } & { 0 } & { 1 } & { 0 } & { 0 } & { 1 } \end{array} \right] }\tag{4.26}
$$

其Tanner图如图4.3所示。从方程(4.26)中的矩阵H可以看出，(7,4)汉明码可用作非规则LDPC码。

### 4.2.3 双曲正切规则

设 $\mathbf{c} = [c_1, c_2, ..., c_n]$ 是n比特数据向量，$c_i \in \{0, 1\}$，定义奇偶函数 $\Phi(\mathbf{c}) \in \{0, 1\}$ 为：

$$
\Phi(\mathbf{c}) = c_1 \oplus c_2 \oplus ... \oplus c_n\tag{4.27}
$$

其中 $\oplus$ 是模2加法运算符。当向量c中"1"的个数为偶数时，$\Phi(\mathbf{c}) = 0$（偶校验）；当"1"的个数为奇数时，$\Phi(\mathbf{c}) = 1$（奇校验）。此外，奇偶函数 $\Phi(\mathbf{c})$ 的先验LLR值定义为：

$$
\lambda_{\Phi(\mathbf{c})} = \log\left(\frac{\mathrm{Pr}[\Phi(\mathbf{c}) = 1]}{\mathrm{Pr}[\Phi(\mathbf{c}) = 0]}\right)\tag{4.28}
$$

由此可得：

$$
\Phi(\mathbf{c}) = \left\{ \begin{array} { l l } { 1, } & { \mathrm{if} \ \lambda_{\Phi(\mathbf{c})} \geq 0 } \\ { 0, } & { \mathrm{if} \ \lambda_{\Phi(\mathbf{c})} < 0 } \end{array} \right.\tag{4.29}
$$

因此，假设所有数据比特相互独立，则 $\lambda_{\Phi(\mathbf{c})}$ 服从双曲正切规则（tanh rule）[51, 52]：


$$
\tanh\left(\frac{-\lambda_{\Phi(\mathbf{c})}}{2}\right) = \prod_{i=1}^{n} \tanh\left(\frac{-\lambda_i}{2}\right)\tag{4.30}
$$

（参见附录B的推导），其中 $\lambda_i = \log(\mathrm{Pr}[c_i=1] / \mathrm{Pr}[c_i=0])$。对方程(4.30)求解可得：

$$
\lambda_{\Phi(\mathbf{c})} = -2\tanh^{-1}\left\{ \prod_{i=1}^{n} \tanh\left(\frac{-\lambda_i}{2}\right) \right\}\tag{4.31}
$$

或者表示为另一种形式：

$$
\lambda_{\Phi(\mathbf{c})} = -\prod_{i=1}^{n} \mathrm{sign}(-\lambda_i) \times f\left( \sum_{i=1}^{n} f(|\lambda_i|) \right)\tag{4.32}
$$

（参见附录C的推导），其中：

$$
f(x) = \log\left(\frac{e^x+1}{e^x-1}\right) = -\log\left(\tanh\left(\frac{x}{2}\right)\right)\tag{4.33}
$$

在实际应用中，方程(4.32)比方程(4.30)或(4.31)更常用于硬件实现，因为它只使用数据的求和而非乘积。然而，方程(4.30)常用于分析LDPC解码器的性能。此外，方程(4.33)中的函数 $f(x)$ 具有如下有趣性质：$f(x)$ 是正函数，在 $x > 0$ 时单调递减，其中 $f(0) = \infty$ 且 $f(\infty) = 0$，如图4.4所示。此外，$f(x)$ 具有自逆性，即 $f(f(x)) = x$ 对所有 $x > 0$ 成立。

设 $\hat{\mathbf{c}} = [\hat{c}_1, ..., \hat{c}_n]$ 是c的最大似然估计，其中 $\hat{c}_i = 1$（若 $\lambda_i \geq 0$），$\hat{c}_i = 0$（若 $\lambda_i < 0$）。因此，$\lambda_{\Phi(\mathbf{c})}$ 的符号（指示奇偶函数 $\Phi(\mathbf{c})$ 的最大似然值）由 $\Phi(\hat{\mathbf{c}})$ 决定：

$$
\mathrm{sign}(\lambda_{\Phi(\mathbf{c})}) = -\prod_{i=1}^{n} \mathrm{sign}(-\lambda_i) = -(-1)^{\Phi(\hat{\mathbf{c}})} = (-1)^{\Phi(\hat{\mathbf{c}})+1}\tag{4.34}
$$

这表明当 $\lambda_i \geq 0$ 的个数为偶数时，$\Phi(\mathbf{c})$ 为偶校验；当 $\lambda_i \geq 0$ 的个数为奇数时，$\Phi(\mathbf{c})$ 为奇校验。此外，$\lambda_{\Phi(\mathbf{c})}$ 的大小用于度量计算出的校验值 $\Phi(\mathbf{c})$ 的可信度：

$$
|\lambda_{\Phi(\mathbf{c})}| = f\left( \sum_i f(|\lambda_i|) \right)\tag{4.35}
$$

假设c中第k个数据比特 $c_k$ 为1和0的概率相等，则 $\lambda_k = 0$。此时，求和 $\sum_i f(|\lambda_i|)$ 中的第k项为无穷大，导致方程(4.35)中的总和也为无穷大。由于 $f(\infty) = 0$，因此只要有任何数据比特的 $\lambda_i = 0$，方程(4.32)中的 $\lambda_{\Phi(\mathbf{c})}$ 必为零。这是因为只要有一个数据比特为1和0的概率相等，整个数据向量c的校验值也为1和0的概率相等（与其它比特无关）。因此，如果有某个数据比特的可信度低于其他比特，方程(4.35)中的总和将主要取决于 $f(|\lambda_{\min}|)$，其中 $|\lambda_{\min}| = \min_i\{|\lambda_i|\}$，从而使方程(4.35)简化为：

$$
|\lambda_{\Phi(\mathbf{c})}| = f\left( \sum_i f(|\lambda_i|) \right) \approx f(f(|\lambda_{\min}|)) = |\lambda_{\min}|\tag{4.36}
$$

将方程(4.36)代入方程(4.32)，可得：

$$
\lambda_{\Phi(\mathbf{c})} = (-1)^{\Phi(\hat{\mathbf{c}})+1} |\lambda_{\min}|\tag{4.37}
$$

总之，计算 $\lambda_{\Phi(\mathbf{c})}$ 可以使用方程(4.31)或(4.32)。然而，若需要降低解码算法的复杂度，则可使用方程(4.37)作为近似。

## 4.3 LDPC编码

考虑系统码[2]，将K比特数据 $\mathbf{m} = [m_1, m_2, ..., m_K]$ 编码为N比特码字 $\mathbf{c} = [c_1, c_2, ..., c_N]$，其结构如方程(4.3)所示：

$$
\mathbf{c} = [\mathbf{m} \mid \mathbf{p}] = \left[ m_1 \ m_2 \ \dots \ m_K \ p_1 \ p_2 \ \dots \ p_{N-K} \right]\tag{4.38}
$$

其中 $\mathbf{p} = [p_1, p_2, ..., p_{N-K}]$ 是 $N-K$ 个奇偶校验比特。因此，使用系统码编码时需要计算奇偶校验比特p，然后将其与数据m拼接，得到所需的码字c。

一般来说，LDPC码由大小为M×N的奇偶校验矩阵H定义。因此，本节将展示如何从矩阵H计算奇偶校验比特p。获得所需矩阵H后，利用方程(4.6)的关系计算p：

$$
\mathbf{Hc}^\mathrm{T} = \mathbf{0}_{M \times 1}\tag{4.39}
$$

其中 $\mathbf{0}_{M \times 1}$ 是大小为M×1的零向量。将矩阵H整理为：

$$
\mathbf{H} = \left[ \mathbf{H}_1 \mid \mathbf{H}_2 \right]\tag{4.40}
$$

其中 $\mathbf{H}_1$ 大小为M×K，$\mathbf{H}_2$ 大小为 $M \times (N-K)$。将方程(4.38)和(4.40)代入方程(4.39)：

$$
\left[ \mathbf{H}_1 \ \mathbf{H}_2 \right] { \left[ \begin{array} { l } { \mathbf{m}^\mathrm{T} } \\ { \mathbf{p}^\mathrm{T} } \end{array} \right] } = \mathbf{0}
$$

$$
\mathbf{H}_1 \mathbf{m}^\mathrm{T} + \mathbf{H}_2 \mathbf{p}^\mathrm{T} = \mathbf{0}
$$

$$
\mathbf{p}^\mathrm{T} = (\mathbf{H}_2)^{-1} \mathbf{H}_1 \mathbf{m}^\mathrm{T}\tag{4.41}
$$

由于 $\mathbf{H}_2$ 是方阵（因为 M = N-K），因此可以求逆。

**例4.3** 从例4.1出发，使用与生成矩阵G对应的奇偶校验矩阵H，对数据 $\mathbf{m}=[101]$ 和 $\mathbf{m}=[110]$ 进行编码。

解：利用方程(4.7)，可以从矩阵G得到矩阵H：


$$
\mathbf{H} = \left[ \mathbf{H}_1 \ \mathbf{H}_2 \right] = \left[ { 1 } \begin{array} { l l l } { 1 } & { 0 } & { 1 } \\ { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } \end{array} \right] \left[ \begin{array} { l l l } { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 1 } \end{array} \right]
$$

因此，对于 $\mathbf{m}=[101]$，根据方程(4.41)计算奇偶校验比特：

$$
\mathbf{p}^\mathrm{T} = { \left[ \begin{array} { l l l } { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 1 } \end{array} \right] }^{-1} { \left[ \begin{array} { l l l } { 1 } & { 0 } & { 1 } \\ { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } \end{array} \right] } { \left[ \begin{array} { l } { 1 } \\ { 0 } \\ { 1 } \end{array} \right] } = { \left[ \begin{array} { l } { 0 } \\ { 1 } \\ { 1 } \end{array} \right] }
$$

因此 $\mathbf{c} = [\mathbf{m} \mid \mathbf{p}] = [1 \ 0 \ 1 \ 0 \ 1 \ 1]$，与例4.1的结果一致。同样，对于 $\mathbf{m}=[110]$：

$$
\mathbf{p}^\mathrm{T} = { \left[ \begin{array} { l l l } { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 1 } \end{array} \right] }^{-1} { \left[ \begin{array} { l l l } { 1 } & { 0 } & { 1 } \\ { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } \end{array} \right] } { \left[ \begin{array} { l } { 1 } \\ { 1 } \\ { 0 } \end{array} \right] } = { \left[ \begin{array} { l } { 1 } \\ { 0 } \\ { 1 } \end{array} \right] }
$$

因此 $\mathbf{c} = [\mathbf{m} \mid \mathbf{p}] = [1 \ 1 \ 0 \ 1 \ 0 \ 1]$，也与例4.1的结果一致。

例4.3表明，对于系统码形式的LDPC编码，可以通过方程(4.41)计算奇偶校验比特p，然后代入方程(4.38)得到所需的码字c。方程(4.39)可用于验证所得码字的正确性。

## 4.4 LDPC解码

LDPC编码使得每个数据比特之间根据奇偶校验矩阵H的结构存在关联性。因此，LDPC解码也利用这些关联性来帮助解码数据。通常，LDPC码使用消息传递算法（MPA: message passing algorithm）进行解码，这里简称为"MP算法"[4, 17]。该算法从矩阵H建立奇偶校验方程开始，然后将其表示为Tanner图，再按照MP算法的步骤进行数据比特解码。

### 4.4.1 LDPC解码基础

考虑图4.5中的信道模型。输入数据序列 $m_n \in \{0, 1\}$ 共K比特，经规则(j, k)-LDPC码编码后得到N比特码字 $c_n \in \{0, 1\}$，然后送入映射器转换为数据序列 $s_n \in \{\pm 1\}$。因此，接收端接收到的信号为：

$$
r_n = s_n + w_n\tag{4.42}
$$

其中 $s_n = 2c_n - 1$ 是信道输出数据，$w_n$ 是均值为零、方差为 $\sigma^2$ 的加性高斯白噪声（AWGN），记为 $w_n \sim \mathcal{N}(0, \sigma^2)$。然后，LDPC解码器必须解码数据 $r_n$，以获得使误差最小的输入数据 $m_n$ 的估计值 $\hat{m}_n$。

这里仅考虑使用系统码形式的LDPC码，此时码字结构如方程(4.3)所示，即对于 $1 \leq i \leq K$ 有 $m_i = c_i$。设 $\mathbf{m} = [m_1, m_2, ..., m_K]$ 是输入数据序列，$\mathbf{c} = [c_1, c_2, ..., c_N]$ 是码字，$\mathbf{r} = [r_1, r_2, ..., r_N]$ 是接收端接收到的数据向量。因此，最大后验（MAP）接收端选择使每个时刻n的后验概率 $\mathrm{Pr}[c_n = c \mid \mathbf{r}]$ 最大的 $c$ 值。即MAP接收端计算后验LLR值 $\lambda_n$：

$$
\lambda_n = \log\left(\frac{\mathrm{Pr}[c_n=1 \mid \mathbf{r}]}{\mathrm{Pr}[c_n=0 \mid \mathbf{r}]}\right) = \log\left(\frac{\mathrm{Pr}[c_n=1 \mid r_n; \mathbf{r}_{i \neq n}]}{\mathrm{Pr}[c_n=0 \mid r_n; \mathbf{r}_{i \neq n}]}\right)\tag{4.43}
$$

并做出判决：当 $\lambda_n \geq 0$ 时 $\hat{c}_n = 1$，当 $\lambda_n < 0$ 时 $\hat{c}_n = 0$。其中参数 $\mathbf{r}_{i \neq n}$ 是接收端接收到的除 $i=n$ 以外的所有数据序列向量。利用贝叶斯规则，方程(4.43)的分子可整理为：

$$
\begin{array} { r l } & { \mathrm{Pr}[c_n=1 | r_n; \mathbf{r}_{i \neq n}] = \frac{p(r_n; c_n=1; \mathbf{r}_{i \neq n})}{p(r_n; \mathbf{r}_{i \neq n})} } \\ & { \qquad = \frac{p(r_n | c_n=1; \mathbf{r}_{i \neq n}) p(c_n=1; \mathbf{r}_{i \neq n})}{p(r_n | \mathbf{r}_{i \neq n}) p(\mathbf{r}_{i \neq n})} } \\ & { \qquad = \frac{p(r_n | c_n=1) \mathrm{Pr}[c_n=1 | \mathbf{r}_{i \neq n}]}{p(r_n | \mathbf{r}_{i \neq n})} } \end{array}\tag{4.44}
$$

其中 $p(r_n | c_n=c)$ 是已知数据比特 $c_n=c \in \{0,1\}$ 时 $r_n$ 的条件概率密度函数。方程(4.44)基于以下事实：若给定 $c_n$，则 $r_n$ 独立于 $\mathbf{r}_{i \neq n}$。类似地，方程(4.43)的分母可整理为：

$$
\mathrm{Pr}[c_n=0 | r_n; \mathbf{r}_{i \neq n}] = \frac{p(r_n | c_n=0) \mathrm{Pr}[c_n=0 | \mathbf{r}_{i \neq n}]}{p(r_n | \mathbf{r}_{i \neq n})}\tag{4.45}
$$

将方程(4.44)和(4.45)代入方程(4.43)可得：

$$
\begin{array} { r l } { \lambda_n = \log\left(\frac{p(r_n|c_n=1) \mathrm{Pr}[c_n=1|\mathbf{r}_{i \neq n}]}{p(r_n|c_n=0) \mathrm{Pr}[c_n=0|\mathbf{r}_{i \neq n}]}\right) } \\ { \quad = \log\left(\frac{p(r_n|c_n=1)}{p(r_n|c_n=0)}\right) + \log\left(\frac{\mathrm{Pr}[c_n=1|\mathbf{r}_{i \neq n}]}{\mathrm{Pr}[c_n=0|\mathbf{r}_{i \neq n}]}\right) } \end{array}\tag{4.46}
$$

$$
= \frac{2}{\sigma^2} r_n + \log\left(\frac{\mathrm{Pr}[c_n=1|\mathbf{r}_{i \neq n}]}{\mathrm{Pr}[c_n=0|\mathbf{r}_{i \neq n}]}\right)\tag{4.47}
$$

其中：

$$
p(r_n | c_n) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(\frac{-(r_n - 2c_n + 1)^2}{2\sigma^2}\right)\tag{4.48}
$$

是高斯随机变量的概率分布。方程(4.47)表明，右侧第一项是"内在信息"，来自接收端接收到的第n个数据（即 $r_n$）；右侧第二项是第n个数据比特 $c_n$ 的"外在信息"，来自接收端接收到的除第n个以外的所有数据。此外，可以看出内在信息与接收到的第n个数据 $r_n$ 成正比，比例常数 $2/\sigma^2$ 称为信道可信度[51]。

**例4.4** 考虑图4.6中的二进制对称信道（BSC），证明其后验LLR值符合方程(4.47)的形式，只是信道可信度为 $\log((1-\alpha)/\alpha)$ 而非 $2/\sigma^2$，其中 $\alpha$ 是交叉概率。

解：从图4.6的信道得到：$p(r_n=0|c_n=0)=1-\alpha$，$p(r_n=0|c_n=1)=\alpha$，$p(r_n=1|c_n=0)=\alpha$，$p(r_n=1|c_n=1)=1-\alpha$。因此：

$$
\begin{array} { c l } { { \displaystyle p(r_n|c_n=1) = } \sum_{i=\{0,1\}} (i) p(r_n=i|c_n=1) } \\ { { = (0)p(r_n=0|c_n=1) + (1)p(r_n=1|c_n=1) = 1-\alpha } } \end{array}
$$

$$
\begin{array} { l } { { p(r_n|c_n=0) = \sum_{i=\{0,1\}} (i) p(r_n=i|c_n=0) } } \\ { { \ = (0)p(r_n=0|c_n=0) + (1)p(r_n=1|c_n=0) = \alpha } } \end{array}
$$

因此，BSC信道的后验LLR值 $\lambda_n$ 符合方程(4.46)，其中内在信息 $\lambda_n^{\mathrm{int}}$ 为：

$$
\lambda_n^{\mathrm{int}} = \log\left(\frac{p(r_n|c_n=1)}{p(r_n|c_n=0)}\right) = \log\left(\frac{1-\alpha}{\alpha}\right)
$$

方程(4.43)可以整理为更便于使用的形式。考虑规则(j, k)-LDPC码的Tanner图，对于第n个比特节点，如图4.7所示。第n个比特节点连接到j个校验节点（编号1到j），每个校验节点又连接到其他k-1个比特节点。设 $\mathbf{c}(i) = [c_{i,2}, c_{i,3}, ..., c_{i,k}]$ 是连接到第i个校验节点的所有k-1个比特节点（除第n个比特节点外）的集合，其中 $i = \{1,2,...,j\}$。因此，图4.7说明 $c_n$ 的值取决于 $\mathbf{c}(1), \mathbf{c}(2), ..., \mathbf{c}(j)$ 的校验值，即 $\Phi(\mathbf{c}(i))$。


$$
c_n = \left\{ \begin{array} { l l } { 1, } & { \mathrm{if} \ \Phi(\mathbf{c}(1)) = \Phi(\mathbf{c}(2)) = \ldots = \Phi(\mathbf{c}(j)) = 1 } \\ { 0, } & { \mathrm{if} \ \Phi(\mathbf{c}(1)) = \Phi(\mathbf{c}(2)) = \ldots = \Phi(\mathbf{c}(j)) = 0 } \end{array} \right.\tag{4.49}
$$

这是为了使所有j个奇偶校验方程满足 $\mathbf{Hc}^\mathrm{T} = \mathbf{0}$ 的关系。为便于后续解释LDPC解码算法，将图4.7中的Tanner图重新整理为图4.8的形式。

### 4.4.2 LDPC码的环

环（cycle）是指图中起点和终点为同一比特节点的路径。环的长度等于构成该环的所有边的总数。由于Tanner图是二分图，最小环长度为4，如图4.8中的虚线所示。然而，若图中没有虚线，则该图没有环，称为"树图"。无环图的性质如下：

1) 移除任何边都会产生两个分离的子图。
2) 从一个比特节点到另一个比特节点只有唯一路径。
3) 连接到比特节点 $c_n$ 的每个比特节点必须经过与 $c_n$ 相连的唯一边。
4) 若比特节点 $c_j$ 和 $c_k$ 通过不同边连接到比特节点 $c_n$，则在忽略第n个数据比特时，$c_j$ 和 $c_k$ 条件独立：

$$
\mathrm{Pr}[c_j; c_k \mid \mathbf{r}_{i \neq n}] = \mathrm{Pr}[c_j \mid \mathbf{r}_{i \neq n}] \times \mathrm{Pr}[c_k \mid \mathbf{r}_{i \neq n}]\tag{4.50}
$$

此外，LDPC码中的环也可以从大小为M×N的奇偶校验矩阵H来考察。即当矩阵H中"1"的位置构成以下闭环关系时，存在长度为4的环：

$$
[h_{i,j}, h_{i,b}, h_{a,b}, h_{a,j}]\tag{4.51}
$$

其中 $h_{r,c}$ 是矩阵H中第r行第c列的"1"的位置，$\{i,a\} \in \{1,2,...,M\}$，$\{j,b\} \in \{1,2,...,N\}$。换句话说，矩阵H中长度为4的环是指"1"的闭环使用了2行和2列。例如，考虑规则(2,4)-LDPC码的奇偶校验矩阵H：

$$
\mathbf{H}_{5 \times 10} = \left[ \begin{array} { l l l l l l l l l l } { 1 } & { 1 } & { 1 } & { 1 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 0 } & { 1 } & { 1 } & { 1 } & { 0 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } & { 1 } & { 1 } & { 0 } & { 0 } \\ { 0 } & { 0 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } & { 1 } & { 0 } & { 1 } \\ { 1 } & { 0 } & { 0 } & { 1 } & { 0 } & { 0 } & { 0 } & { 0 } & { 1 } & { 1 } \end{array} \right]\tag{4.52}
$$

可以看出，该矩阵H有两个长度为4的环：第一个环在位置 $[h_{1,1}, h_{1,4}, h_{5,4}, h_{5,1}]$ 处形成闭环；第二个环在位置 $[h_{2,5}, h_{2,7}, h_{3,7}, h_{3,5}]$ 处形成闭环。然而，方程(4.8)和(4.19)中的矩阵H没有环。

好的LDPC码必须没有长度为4的环，因为长度为4的环是矩阵H中最容易形成的环。此外，LDPC解码算法基于比特节点和校验节点之间传递消息的概率原理，每个事件的概率必须相互独立。因此，如果在矩阵H中存在环，传递消息的概率将不再是相互独立的，这将显著降低数据解码的性能（参见图4.18中的实验结果）。

### 4.4.3 数据比特LLR的计算

考虑规则(j, k)-LDPC码的大小为M×N的奇偶校验矩阵H，由此可知有j个奇偶校验方程的约束条件。从方程(4.49)可知，数据比特 $c_n$ 等于数据向量 $\mathbf{c}(i)$ 的校验值，即 $c_n = \Phi(\mathbf{c}(i))$，对于 $i = \{1,2,...,j\}$。因此，方程(4.43)可重写为：

$$
\lambda_n = \frac{2}{\sigma^2} r_n + \log\left(\frac{\mathrm{Pr}[\Phi(\mathbf{c}(i))=1 \ \mathrm{for} \ i=1,2,...,j \mid \mathbf{r}_{i \neq n}]}{\mathrm{Pr}[\Phi(\mathbf{c}(i))=0 \ \mathrm{for} \ i=1,2,...,j \mid \mathbf{r}_{i \neq n}]}\right)\tag{4.53}
$$

假设矩阵H没有环，则给定 $\mathbf{r}_{i \neq n}$（即接收端接收到的除第n个以外的所有数据）时，$\mathbf{c}(1), \mathbf{c}(2), ..., \mathbf{c}(j)$ 条件独立，且 $\mathbf{c}(i)$ 内部的成员也条件独立。因此，方程(4.53)可简化为：

$$
\lambda_n = \frac{2}{\sigma^2} r_n + \log\left(\frac{\prod_{i=1}^j \mathrm{Pr}[\Phi(\mathbf{c}(i))=1 \mid \mathbf{r}_{i \neq n}]}{\prod_{i=1}^j \mathrm{Pr}[\Phi(\mathbf{c}(i))=0 \mid \mathbf{r}_{i \neq n}]}\right)
$$

$$
= \frac{2}{\sigma^2} r_n + \sum_{i=1}^j \log\left(\frac{\mathrm{Pr}[\Phi(\mathbf{c}(i))=1 \mid \mathbf{r}_{i \neq n}]}{\mathrm{Pr}[\Phi(\mathbf{c}(i))=0 \mid \mathbf{r}_{i \neq n}]}\right)
$$

$$
= \frac{2}{\sigma^2} r_n + \sum_{i=1}^j \lambda_{\Phi(\mathbf{c}(i))}\tag{4.54}
$$

其中 $\lambda_{\Phi(\mathbf{c}(i))}$ 是校验值 $\Phi(\mathbf{c}(i))$ 的LLR值。由于每个数据比特条件独立，每个 $\lambda_{\Phi(\mathbf{c}(i))}$ 遵循方程(4.31)的双曲正切规则。因此，设：

$$
\lambda_{i,l} = \log\left(\frac{\mathrm{Pr}[c_{i,l}=1 | \mathbf{r}_{i \neq n}]}{\mathrm{Pr}[c_{i,l}=0 | \mathbf{r}_{i \neq n}]}\right)\tag{4.55}
$$

其中 $c_{i,l}$ 是向量 $\mathbf{c}(i)$ 中的第l个成员，$l = \{2,3,...,k\}$。将方程(4.31)代入方程(4.54)可得：

$$
\lambda_n = \frac{2}{\sigma^2} r_n - 2 \sum_{i=1}^j \tanh^{-1}\left\{ \prod_{l=2}^k \tanh\left(\frac{-\lambda_{i,l}}{2}\right) \right\}\tag{4.56}
$$

或表示为另一种形式（比较方程(4.31)和(4.32)）：

$$
\lambda_n = \frac{2}{\sigma^2} r_n - \sum_{i=1}^j \left\{ \prod_{l=2}^k \mathrm{sign}(-\lambda_{i,l}) \times f\left( \sum_{l=2}^k f(|\lambda_{i,l}|) \right) \right\}\tag{4.57}
$$

其中 $f(x) = -\log(\tanh(x/2))$ 如方程(4.33)所定义。此外，为降低解码算法的复杂度，可利用方程(4.36)近似计算方程(4.57)：

$$
\lambda_n \approx \frac{2}{\sigma^2} r_n - \sum_{i=1}^j \left\{ \prod_{l=2}^k \mathrm{sign}(-\lambda_{i,l}) \times \min_{l=\{2,...,k\}} |\lambda_{i,l}| \right\}\tag{4.58}
$$

从图4.8可以解释方程(4.54)的含义如下：比特节点 $c_{i,l}$ 向第i个校验节点发送消息 $\lambda_{i,l}$，第i个校验节点收集来自 $\mathbf{c}(i)$ 中其他比特节点的k-1条消息（除比特节点 $c_n$ 外），计算第i个校验节点校验值 $\Phi(\mathbf{c}(i))$ 的MAP-LLR值 $\lambda_{\Phi(\mathbf{c}(i))}$，然后将计算结果发送到 $\lambda_n$，即 $(2/\sigma^2)r_n$ 与到达第n个比特节点的所有消息之和。此外，图4.9显示了当 $f(x) = \tanh(-x/2)$ 时比特节点和校验节点的工作方式。可以看出，比特节点的计算仅使用求和，而校验节点的计算则较为复杂，因为需要使用函数 $f(x)$。


**例4.5** 考虑图4.10中的Tanner图，有4个比特节点连接到一个校验节点（所有4个比特节点必须满足该校验节点的校验方程）。给定数据比特 $\{c_x, c_y, c_z\}$ 的后验概率和接收数据 $r_n = (2c_n-1) + w_n = 1.5$，其中 $w_n$ 是均值为零、方差 $\sigma^2 = 0.5$ 的AWGN噪声。利用方程(4.56)-(4.58)计算数据比特 $c_n$ 的后验LLR值。

解：在向比特节点 $c_n$ 传递消息时，校验节点收集来自比特节点 $\{x, y, z\}$ 的消息以计算外在信息，然后将结果发送给比特节点 $c_n$，以求得第n个数据比特的后验LLR值。题目已给出 $\mathrm{Pr}[c_l=1 | \mathbf{r}_{i \neq n}]$ 的值，因此可计算比特节点 $\{x, y, z\}$ 发送给 $c_n$ 的外在信息：

$$
\lambda_x = \log\left(\frac{0.91}{0.09}\right) \approx 2.3
$$

$$
\lambda_y = \log\left(\frac{0.99}{0.01}\right) \approx 4.6
$$

$$
\lambda_z = \log\left(\frac{0.001}{0.999}\right) \approx -6.9
$$

由于 $\mathrm{Pr}[c_l=0 | \mathbf{r}_{i \neq n}] = 1 - \mathrm{Pr}[c_l=1 | \mathbf{r}_{i \neq n}]$。将 $r_n=1.5$, $\sigma^2=0.5$, $\lambda_x, \lambda_y, \lambda_z$ 代入方程(4.56)：

$$
\lambda_n = \frac{2}{0.5}(1.5) - 2\tanh^{-1}\left\{ \tanh\left(\frac{-2.3}{2}\right) \times \tanh\left(\frac{-4.6}{2}\right) \times \tanh\left(\frac{6.9}{2}\right) \right\}
$$

$$
= 6 - 2\tanh^{-1}\{(-0.8178) \times (-0.9801) \times (0.9980)\}
$$

$$
= 6 - (2.197) = 3.803
$$

也可从方程(4.57)求得 $\lambda_n$：

$$
\lambda_n = 6 - \{(-1)(-1)(1) \times f(f(|2.3|) + f(|4.6|) + f(|-6.9|))\}
$$

$$
= 6 - f(0.2012 + 0.0201 + 0.0200) = 6 - (2.197) = 3.803
$$

结果与使用方程(4.56)一致。如需降低计算复杂度，可使用方程(4.58)：

$$
\lambda_n = 6 - \{(-1)(-1)(1) \times |2.3|\} = 6 - 2.3 = 3.7
$$

结果与方程(4.56)和(4.57)接近。

### 4.4.4 消息传递算法

图4.8表明比特节点 $c_{i,l}$ 依赖于 $c_n$，因为两者连接到同一个校验方程。然而，当给定条件 $\{\mathbf{r}_{i \neq n}\}$ 时，$c_{i,l}$ 独立于 $c_n$。此外，若剔除接收到的第n个数据 $r_n$，则通过比特节点 $c_n$ 的其他数据 $\{\mathbf{r}_{i \neq n}\}$ 也被剔除。因此，剔除 $r_n$ 相当于切断所有与比特节点 $c_n$ 相连的边，从而产生j个子图。由于这些子图彼此不重叠，可认为各子图相互独立，因此只有数据比特 $c_{i,l}$ 被用于计算 $\lambda_{i,l}$。

消息传递算法（MP算法）是一种简单的数据解码技术，通过Tanner图中从一个节点到另一个节点的路径传递消息。每个节点（比特节点和校验节点）充当相互独立的处理单元，接收所有传入边上的消息，进行计算，并将结果传回这些边。此外，如果图是无环的，MP算法是一种递归算法，在有限次迭代后将收敛到方程(4.43)定义的真实后验LLR值。然而，大部分好的码在其Tanner图中都有环，此时使用MP算法解码得到的是次优结果。总之，即使LDPC码存在环，使用MP算法解码仍然能够提供相当好的性能，且复杂度非常低（与其他码相比）。

使用MP算法的LDPC解码器（或MP解码器）用于具有大小为M×N的奇偶校验矩阵H的二进制码，其步骤可总结如下。设 $\mathcal{M}_n = \{m: h_{m,n}=1\}$ 是连接到第n个比特节点的所有校验节点的集合，$\mathcal{N}_m = \{n: h_{m,n}=1\}$ 是连接到第m个校验节点的所有比特节点的集合。对于规则(j, k)-LDPC码，$\mathcal{M}_n$ 有j个元素（对所有n），$\mathcal{N}_m$ 有k个元素（对所有m）。此外，设 $u_{m \to n}^{(l)}$ 是第l次迭代时从第m个校验节点发送到第n个比特节点的消息，$\lambda_n^{(l)}$ 是第l次迭代时第n个数据比特的后验LLR值。

**MP算法步骤（LDPC解码）**：

1. 设置奇偶校验矩阵H大小为M×N（即M个校验节点和N个比特节点）
2. 初始化：
   - $u_{m \to n}^{(0)} = 0$，对所有 $m \in \{1,2,...,M\}$ 和 $n \in \mathcal{N}_m$
   - $\lambda_n^{(0)} = (2/\sigma^2) r_n$，对所有 $n \in \{1,2,...,N\}$
3. 对于 $l = 1, 2, ..., l_{\max}$（$l_{\max}$ 为所需迭代次数）：
   - **校验节点更新**：对所有 $m \in \{1,2,...,M\}$ 和 $n \in \mathcal{N}_m$
     
     $$
     u_{m \to n}^{(l)} = -2\tanh^{-1}\left\{ \prod_{i \in \mathcal{N}_m \backslash \{n\}} \tanh\left(\frac{-(\lambda_i^{(l-1)} - u_{m \to i}^{(l-1)})}{2}\right) \right\}\tag{4.59}
     $$
   
   - **比特节点更新**：对所有 $n \in \{1,2,...,N\}$
     
     $$
     \lambda_n^{(l)} = \frac{2}{\sigma^2} r_n + \sum_{m \in \mathcal{M}_n} u_{m \to n}^{(l)}\tag{4.60}
     $$

4. 解码输入数据序列（仅适用于系统码）：

   $$
   \hat{m}_i = \left\{ \begin{array} { l l } { 1, } & { \mathrm{if} \ \lambda_i^{(l_{\max})} \ge 0 } \\ { 0, } & { \mathrm{if} \ \lambda_i^{(l_{\max})} < 0 } \end{array} \right.\tag{4.61}
   $$
   
   对于 $i \in \{1, 2, ..., N-M\}$，其中 $N-M = K$ 是输入数据比特数。

**例4.6** 考虑图4.5中的AWGN信道，输入数据比特 $m \in \{0,1\}$，使用的LDPC码的生成矩阵为 $\mathbf{G} = [1 \ 1 \ 1] = [1 \ | \ \mathbf{P}]$，其中 $\mathbf{P} = [1 \ 1]$。因此接收到的信号为：

$$
\begin{array} { c } { { \left[ r_1 \right] } } \\ { { \left[ r_2 \right] = s \left[ 1 \right] + \left[ w_2 \right] } } \\ { { \left. r_3 \right] } } \end{array}
$$

其中 $s \in \{\pm 1\}$，$w_n \sim \mathcal{N}(0, \sigma^2)$ 是AWGN噪声。求在2次迭代后的后验LLR值 $\boldsymbol{\lambda} = [\lambda_1, \lambda_2, \lambda_3]^\mathrm{T}$，其中 $\lambda_n = \log(\mathrm{Pr}[c_n=1|\mathbf{r}] / \mathrm{Pr}[c_n=0|\mathbf{r}])$。

解：根据方程(4.7)，生成矩阵G对应奇偶校验矩阵H为：

$$
\mathbf{H} = \left[ \mathbf{P}^\mathrm{T} \mid \mathbf{I} \right] = \left[ \begin{array} { l l l } { 1 } & { 1 } & { 0 } \\ { 1 } & { 0 } & { 1 } \end{array} \right]
$$

利用高斯消元法，可将矩阵H重新整理为：

$$
\mathbf{H} = { \left[ \begin{array} { l l l } { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } \end{array} \right] }
$$

对应的Tanner图如图4.12所示。$\lambda_n$ 由方程(4.47)求得：

$$
\lambda_n = L_c r_n + \log\left(\frac{\mathrm{Pr}[c_n=1|\mathbf{r}_{i \neq n}]}{\mathrm{Pr}[c_n=0|\mathbf{r}_{i \neq n}]}\right)\tag{4.62}
$$

其中 $L_c = 2/\sigma^2$ 是信道可信度。


**第1次迭代：**

每个比特节点将消息 $\lambda_n^{(0)}$ 发送到校验节点，如图4.13(a)所示。然后每个校验节点根据方程(4.59)计算接收到的消息，并将结果返回给比特节点，如图4.13(b)所示。之后，比特节点根据方程(4.60)计算所有接收到的消息，得到第1次迭代后各数据比特的 $\lambda_n^{(1)}$：

$$
\pmb{\lambda}^{(1)} = \left[ \lambda_1^{(1)}, \lambda_2^{(1)}, \lambda_3^{(1)} \right]^\mathrm{T} = L_c \left[ r_1, r_2, r_1 + r_2 \right]
$$

**第2次迭代：**

类似地，每个比特节点将消息发送到校验节点，如图4.14(a)所示。然后每个校验节点根据方程(4.59)计算结果并返回比特节点，如图4.14(b)所示。之后比特节点根据方程(4.60)计算，得到第2次迭代后各数据比特的 $\lambda_n^{(2)}$：

$$
\lambda^{(2)} = \left[ \lambda_1^{(2)}, \lambda_2^{(2)}, \lambda_3^{(2)} \right]^\mathrm{T} = L_c \left[ r_1 + r_3, r_2 + r_3, r_1 + r_2 + r_3 \right]\tag{4.63}
$$

这就是第2次迭代后数据比特 $\{c_1, c_2, c_3\}$ 的后验LLR值。此外，如果让MP算法继续运行，会发现 $\lambda^{(l)} = \lambda^{(2)}$ 对于 $l > 2$，即MP算法已达到稳态。

例4.6也可以用另一种方法求解。从方程(4.43)出发，数据比特 $c_n$ 的后验LLR值为（利用贝叶斯规则）：

$$
\lambda_n = \log\left(\frac{p(\mathbf{r}|c_n=1)\mathrm{Pr}[c_n=1]/p(\mathbf{r})}{p(\mathbf{r}|c_n=0)\mathrm{Pr}[c_n=0]/p(\mathbf{r})}\right)\tag{4.64}
$$

其中 $\mathbf{r} = [r_1, r_2, r_3]^\mathrm{T}$。假设 $\mathrm{Pr}[c_n=1] = \mathrm{Pr}[c_n=0] = 0.5$，则方程(4.64)可简化为：

$$
\lambda_n = \log\left(\frac{p(\mathbf{r}|c_n=1)}{p(\mathbf{r}|c_n=0)}\right) = \log\left(\frac{C\exp\left(-\frac{1}{2\sigma^2}|\mathbf{r} - [1,1,1]^\mathrm{T}|^2\right)}{C\exp\left(-\frac{1}{2\sigma^2}|\mathbf{r} + [1,1,1]^\mathrm{T}|^2\right)}\right)
$$

$$
= \frac{1}{2\sigma^2}\{2(r_1+r_2+r_3) + 2(r_1+r_2+r_3)\} = \frac{2}{\sigma^2}(r_1+r_2+r_3)
$$

与方程(4.63)的结果一致，其中 $C = 1/\sqrt{2\pi\sigma^2}$。因此可以得出结论，如果LDPC码没有环，MP算法将随着迭代次数的增加收敛到正确值。

**例4.7** 考虑图4.5中的AWGN信道，输入数据 $\mathbf{m}=[1 \ 0 \ 1]$，使用的LDPC码的生成矩阵G如方程(4.4)所示。系统噪声为 $\mathbf{w} = [-0.5, 0.8, -0.5, 0.5, 0.5, -0.5]$，方差 $\sigma^2 = 0.5$。求第3次迭代结束后6个数据比特的后验LLR值。

解：从例4.1可知，$\mathbf{m}=[101]$ 编码后得到 $\mathbf{c} = [1 \ 0 \ 1 \ 0 \ 1 \ 1]$。因此LDPC解码器接收到的信号为：

$$
\mathbf{r} = (2\mathbf{c} - 1) + \mathbf{w} = [r_1, r_2, r_3, r_4, r_5, r_6] = [0.5, -0.2, 0.5, -0.5, 1.5, 0.5]
$$

由于生成矩阵G采用系统码形式，可根据方程(4.7)求得奇偶校验矩阵H：

$$
\mathbf{H} = { \left[ \begin{array} { l l l l l l } { 1 } & { 0 } & { 1 } & { 1 } & { 0 } & { 0 } \\ { 1 } & { 1 } & { 0 } & { 0 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } & { 0 } & { 0 } & { 1 } \end{array} \right] }
$$

解码器使用该矩阵H解码数据序列r，按照Tanner图（如图4.15所示）进行软消息交换。每次迭代中，校验节点和比特节点分别根据方程(4.59)和(4.60)计算 $u_{m \to n}^{(l)}$ 和 $\lambda_n^{(l)}$。

**第1次迭代：**

校验节点向比特节点发送软消息 $u_{m \to n}^{(1)}$：

$$
[u_{1 \to 1}^{(1)}, u_{1 \to 3}^{(1)}, u_{1 \to 4}^{(1)}] = [1.3250, 1.3250, -1.3250]
$$

$$
[u_{2 \to 1}^{(1)}, u_{2 \to 2}^{(1)}, u_{2 \to 5}^{(1)}] = [0.7956, -1.9822, 0.5958]
$$

$$
[u_{3 \to 2}^{(1)}, u_{3 \to 3}^{(1)}, u_{3 \to 6}^{(1)}] = [-1.3250, 0.5958, 0.5958]
$$

比特节点计算LLR值 $\lambda_n^{(1)}$：

$$
[\lambda_1^{(1)}, \lambda_2^{(1)}, \lambda_3^{(1)}, \lambda_4^{(1)}, \lambda_5^{(1)}, \lambda_6^{(1)}] = [4.1206, -4.1072, 3.9208, -3.325, 6.5958, 2.5958]
$$

**第2次迭代：**

$$
[u_{1 \to 1}^{(2)}, u_{1 \to 3}^{(2)}, u_{1 \to 4}^{(2)}] = [1.5710, 1.6358, -2.0021]
$$

$$
[u_{2 \to 1}^{(2)}, u_{2 \to 2}^{(2)}, u_{2 \to 5}^{(2)}] = [2.1048, -3.2585, 1.8660]
$$

$$
[u_{3 \to 2}^{(2)}, u_{3 \to 3}^{(2)}, u_{3 \to 6}^{(2)}] = [-1.7692, 1.6317, 2.3263]
$$

$$
[\lambda_1^{(2)}, \lambda_2^{(2)}, \lambda_3^{(2)}, \lambda_4^{(2)}, \lambda_5^{(2)}, \lambda_6^{(2)}] = [5.6758, -5.8276, 5.2675, -4.0021, 7.866, 4.3263]
$$

**第3次迭代：**

$$
[u_{1 \to 1}^{(3)}, u_{1 \to 3}^{(3)}, u_{1 \to 4}^{(3)}] = [1.8249, 1.8872, -3.1478]
$$

$$
[u_{2 \to 1}^{(3)}, u_{2 \to 2}^{(3)}, u_{2 \to 5}^{(3)}] = [2.5375, -3.4867, 2.2586]
$$

$$
[u_{3 \to 2}^{(3)}, u_{3 \to 3}^{(3)}, u_{3 \to 6}^{(3)}] = [-1.8256, 1.8822, 3.1323]
$$


第3次迭代后，比特节点计算LLR值 $\lambda_n^{(3)}$：

$$
[\lambda_1^{(3)}, \lambda_2^{(3)}, \lambda_3^{(3)}, \lambda_4^{(3)}, \lambda_5^{(3)}, \lambda_6^{(3)}] = [6.3624, -6.1122, 5.7694, -5.1478, 8.2586, 5.1323]
$$

因此，在第3次迭代结束时，LDPC解码器根据方程(4.61)解码数据比特，得到：

$$
\hat{\mathbf{m}} = [\hat{m}_1 \ \hat{m}_2 \ \hat{m}_3] = [1 \ 0 \ 1]
$$

与输入数据比特 $\mathbf{m}=[101]$ 一致，表明系统未发生错误。此外可以观察到，在正常系统工作条件下（噪声不强），每次迭代中的LLR值 $\lambda_n^{(l)}$ 逐渐增大，这意味着解码数据比特的可信度越来越高。

## 4.5 奇偶校验矩阵的构造

在实际应用中，LDPC码的性能取决于奇偶校验矩阵H，该矩阵应尽可能随机且无环。关于LDPC码的各种研究[4, 5, 8, 17, 54, 55]主要集中在矩阵H的构造上。因此，本节将介绍矩阵H的简单构造方法，为有兴趣在将来进行LDPC码研究的读者提供基础。

### 4.5.1 规则LDPC码

规则(j, k)-LDPC码的奇偶校验矩阵H（大小为M×N）可由大小为L×N的矩阵 $\mathbf{H}_0$ 构造，其中 $L = N/k = M/j$：

$$
\mathbf{H}_0 = \left[ \begin{array} { c c c c c c } { \underbrace{1\dots1}_{k} } & { \mathbf{0} } & { \mathbf{0} } & { \cdots } & { \mathbf{0} } \\ { \mathbf{0} } & { \underbrace{11\dots1}_{k} } & { \mathbf{0} } & { \cdots } & { \mathbf{0} } \\ { \vdots } & { \ddots } & { \ddots } & { \ddots } & { \vdots } \\ { \mathbf{0} } & { \dots } & { \mathbf{0} } & { \underbrace{11\dots1}_{k} } & { \mathbf{0} } \\ { \mathbf{0} } & { \dots } & { \mathbf{0} } & { \mathbf{0} } & { \underbrace{11\dots1}_{k} } \end{array} \right]_{L \times N}\tag{4.65}
$$

其中 $\mathbf{0} = [0\ 0\ ...\ 0]$ 是大小为1×k的零向量。方程(4.65)表明，第 $(m-1)k+1$ 到 $mk$ 行的列以外的其他位置元素为0。在实际应用中，矩阵 $\mathbf{H}_0$ 可用于规则(1, k)-LDPC码，每个校验方程关联k个数据比特，每个数据比特仅关联一个校验方程。然而，使用矩阵 $\mathbf{H}_0$ 的LDPC码性能不佳，因为矩阵 $\mathbf{H}_0$ 线性相关——例如码字0000...0和1100...0都被认为是有效码字。因此，该码的最小距离为 $d_{\min}=2$。

一般来说，规则(j, k)-LDPC码的大小为M×N的矩阵H可以通过将 $\mathbf{H}_0$ 进行列置换后叠放来构造：

$$
\mathbf{H} = { \left[ \begin{array} { l } { \pi_1(\mathbf{H}_0) } \\ { \pi_2(\mathbf{H}_0) } \\ { \vdots } \\ { \pi_j(\mathbf{H}_0) } \end{array} \right] }_{M \times N}\tag{4.66}
$$

其中 $\pi_i(\mathbf{H}_0)$ 是对矩阵 $\mathbf{H}_0$ 进行列置换后的矩阵，$i=\{1,2,...,j\}$。在实际应用中，$\mathbf{H}_0$ 也可以是其他形式，例如：

$$
\mathbf{H}_0 = \left[ \mathbf{I} \ \mathbf{I} \ \mathbf{I} \ \cdots \ \mathbf{I} \right]_{L \times N}\tag{4.67}
$$

其中 $\mathbf{I}$ 是大小为L×L的单位矩阵，$L = N/k$。

好的置换应使矩阵H的最小距离 $d_{\min} > 2$。设计j个置换（每个长度为N）是一个富有挑战性的问题。然而，Gallager[17]已经证明，纯随机置换可以得到最优的矩阵H，从而使LDPC码的性能最大化。

### 4.5.2 阵列LDPC码

阵列LDPC码（array LDPC code）由Fan于2000年提出[54]。其奇偶校验矩阵H具有阵列结构，因此解决了矩阵H构造的复杂性问题。此外，阵列LDPC码的性能接近具有随机矩阵H的LDPC码。

阵列LDPC码由三个参数定义：素数p和整数 $\{j,k\} \le p$。矩阵H的大小为 $jp \times kp$，其结构如下：

$$
\mathbf{H}_{(jp \times kp)} = \left[ \begin{array} { l l l l l } { \mathbf{I} } & { \mathbf{I} } & { \mathbf{I} } & { \mathbf{I} } & { \mathbf{I} } \\ { \mathbf{I} } & { \mathbf{a} } & { \mathbf{a}^2 } & { \cdots } & { \mathbf{a}^{k-1} } \\ { \mathbf{I} } & { \mathbf{a}^2 } & { \mathbf{a}^4 } & { \cdots } & { \mathbf{a}^{2(k-1)} } \\ { \vdots } & { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { \mathbf{I} } & { \mathbf{a}^{j-1} } & { \mathbf{a}^{2(j-1)} } & { \cdots } & { \mathbf{a}^{(j-1)(k-1)} } \end{array} \right]\tag{4.69}
$$

其中j和k分别是矩阵H每列和每行中"1"的数量；$\mathbf{I}$ 是大小为p×p的单位矩阵；$\mathbf{a}$ 是大小为p×p的置换矩阵，表示对单位矩阵$\mathbf{I}$向左或向右循环移位：

$$
\mathbf{a} = { \left[ \begin{array} { l l l l l } { 0 } & { 1 } & { 0 } & { 0 } & { 0 } \\ { 0 } & { 0 } & { 1 } & { 0 } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 0 } & { 0 } & { 1 } \\ { 1 } & { 0 } & { 0 } & { 0 } & { 0 } \end{array} \right] }\tag{4.70}
$$

a的指数表示循环移位的次数。方程(4.69)表明矩阵H中"1"的分布仍然是固定的，因此阵列LDPC码属于规则LDPC码。

使用参数(j, k, p)的阵列LDPC码，输入数据比特数为 $K = N-M = (k-j)p$，奇偶校验比特数为 $M = jp$，码字比特数为 $N = kp$，码率为 $1 - (jp-j+1)/p^2$。然而，由于方程(4.66)和(4.69)中的矩阵H不是如方程(4.7)所示的系统形式，因此编码时需要先通过高斯消元法将矩阵H转换为系统形式，再按照第4.3节描述的步骤进行编码。此外，Fan[54]已证明阵列码没有长度为4的环，并且可以使用图4.11中的MP算法进行解码（如第4.6.1节所述）。总之，Fan的研究解决了LDPC码在以下方面的不足：从{0,1}随机生成矩阵H、控制每行每列的"1"的数量以及避免长度为4的环。

### 4.5.3 改进型阵列LDPC码

Richardson的研究[46]指出，通过将奇偶校验矩阵H整理为三角形形式，可以提高编码性能并使编码复杂度呈线性。因此，Eleftheriou于2002年提出了一种新的LDPC码，称为"改进型阵列LDPC码（MAC: modified array code）"，采用循环移位方法。改进型阵列LDPC码与阵列LDPC码一样由参数(j, k, p)定义，矩阵H大小为 $jp \times kp$，其结构如下：

$$
\mathbf{H}_{(jp \times kp)} = { \left[ \begin{array} { l l l l l l l l } { \mathbf{I} } & { \mathbf{I} } & { \cdots } & { \mathbf{I} } & { \mathbf{I} } & { \mathbf{I} } & { \cdots } & { \mathbf{I} } \\ { \mathbf{0} } & { \mathbf{I} } & { \mathbf{a} } & { \cdots } & { \mathbf{a}^{j-2} } & { \mathbf{a}^{j-1} } & { \cdots } & { \mathbf{a}^{k-2} } \\ { \mathbf{0} } & { \mathbf{0} } & { \mathbf{I} } & { \cdots } & { \mathbf{a}^{2(j-3)} } & { \mathbf{a}^{2(j-2)} } & { \cdots } & { \mathbf{a}^{2(k-3)} } \\ { \vdots } & { \vdots } & { \vdots } & { \ddots } & { \vdots } & { \vdots } & { \ddots } & { \vdots } \\ { \mathbf{0} } & { \mathbf{0} } & { \mathbf{0} } & { \cdots } & { \mathbf{I} } & { \mathbf{a}^{(j-1)} } & { \cdots } & { \mathbf{a}^{(j-1)(k-j)} } \end{array} \right] }\tag{4.71}
$$

其中 $\mathbf{0}$ 是大小为p×p的零矩阵，$\mathbf{a}$ 是置换矩阵。可以观察到，矩阵H中的三角形形式导致"1"的分布从固定变为不固定，因此改进型阵列LDPC码属于非规则LDPC码。

对于具有参数(j, k, p)的改进型阵列LDPC码，输入数据比特数 $K = (k-j)p$，奇偶校验比特数 $M = jp$，码字比特数 $N = kp$，码率 $= (1 - j/k)$。此外，方程(4.71)中的矩阵H没有长度为4的环，可以使用MP算法进行解码（如第4.6.1节所述），并且其性能（低错误平台）与使用随机矩阵H的LDPC码相当。


改进型阵列LDPC码的编码比阵列LDPC码更简单，因为方程(4.71)中的矩阵H具有三角形结构。将码字重新整理为：

$$
\mathbf{c} = [\mathbf{p} \mid \mathbf{m}]\tag{4.72}
$$

其中p是大小为 $M = jp$ 比特的奇偶校验比特向量，m是大小为 $K = N-M = (k-j)p$ 比特的信息比特向量。将方程(4.72)中的c代入方程(4.6)：

$$
\mathbf{H}_{(M \times N)} \left[ \frac{\mathbf{p}}{\mathbf{m}} \right]^\mathrm{T} = \mathbf{0}^\mathrm{T}_{(M \times 1)}\tag{4.73}
$$

结果是编码复杂度大幅降低，因为计算奇偶校验比特p不再需要方程(4.41)中的矩阵求逆。

例如，设 $j=3, k=5, p=3$，置换矩阵为：

$$
\mathbf{a} = { \left[ \begin{array} { l l l } { 0 } & { 0 } & { 1 } \\ { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } \end{array} \right] } \quad \mathbf{a}^2 = { \left[ \begin{array} { l l l } { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 1 } \\ { 1 } & { 0 } & { 0 } \end{array} \right] } \quad \mathbf{a}^3 = { \left[ \begin{array} { l l l } { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } \\ { 0 } & { 0 } & { 1 } \end{array} \right] } \quad \mathbf{a}^4 = { \left[ \begin{array} { l l l } { 0 } & { 0 } & { 1 } \\ { 1 } & { 0 } & { 0 } \\ { 0 } & { 1 } & { 0 } \end{array} \right] }
$$

因此，大小为9×15的矩阵H的结构为方程(4.74)所示。码字为：

$$
\mathbf{c} = [\mathbf{p} \mid \mathbf{m}] = [p_1 \ p_2 \ p_3 \ ... \ p_9 \ m_1 \ m_2 \ m_3 \ ... \ m_6]\tag{4.75}
$$

奇偶校验比特p通过方程(4.73求得，即矩阵H与码字c相乘后得到M=9个校验方程：

$$
p_1 + p_4 + p_7 + m_1 + m_4 = 0\tag{4.76}
$$
$$
p_2 + p_5 + p_8 + m_2 + m_5 = 0\tag{4.77}
$$
$$
p_3 + p_6 + p_9 + m_3 + m_6 = 0\tag{4.78}
$$
$$
p_4 + p_9 + m_2 + m_4 = 0\tag{4.79}
$$
$$
p_5 + p_7 + m_3 + m_5 = 0\tag{4.80}
$$
$$
p_6 + p_8 + m_1 + m_6 = 0\tag{4.81}
$$
$$
p_7 + m_2 + m_6 = 0\tag{4.82}
$$
$$
p_8 + m_3 + m_4 = 0\tag{4.83}
$$
$$
p_9 + m_1 + m_5 = 0\tag{4.84}
$$

因此，给定信息比特m后，可以通过这些方程（模2加法）求解p。从最后一个方程(4.84)开始求 $p_9$，然后解方程(4.83)求 $p_8$，依此类推直到方程(4.76)，即可得到所有奇偶校验比特p。

**例4.9** 使用方程(4.74)中的奇偶校验矩阵H，对数据 $\mathbf{m}=[110011]$ 和 $\mathbf{m}=[011010]$ 进行编码。

解：该矩阵H一次对6比特信息进行编码，得到9个奇偶校验比特，由方程(4.76)-(4.84)求得：
- 若 $\mathbf{m}=[110011]$，则奇偶校验比特 $\mathbf{p}=[011110000]$，码字 $\mathbf{c}=[\mathbf{p} \mid \mathbf{m}]$
- 若 $\mathbf{m}=[011010]$，则奇偶校验比特 $\mathbf{p}=[101011111]$，码字 $\mathbf{c}=[\mathbf{p} \mid \mathbf{m}]$

### 4.5.4 总结

综上所述，LDPC码是迄今为止性能最优的纠错码（ECC），其性能比其他ECC码更接近香农极限[4]。LDPC码的性能取决于奇偶校验矩阵H的结构（应尽可能随机）和待编码数据长度K。即当 $K \to \infty$ 时LDPC码性能达到最优[4, 17]，这也导致矩阵H规模非常大。过去各种应用无法使用LDPC码的原因是处理芯片需要大容量存储器来存储矩阵H，成本极高。

然而，2000年Fan[54]提出了一种阵列结构的矩阵H构造方法，这是一种结构化矩阵H，性能接近使用随机矩阵H的LDPC码，同时解决了矩阵H构造的复杂性问题，可以实际应用于各种场合——处理芯片只需存储矩阵H的结构特征和置换矩阵a，无需存储整个矩阵H，从而大大降低了所需内存。因此，2000年以后的LDPC码研究主要集中在结构化矩阵H的开发上，目标是使矩阵H尽可能随机化，同时简化编/解码步骤。例如，第4.5.3节介绍了Eleftheriou[55]于2002年提出的改进型阵列LDPC码（MAC）。

过去硬盘驱动器未能使用LDPC码的原因是，其信号处理系统每次读写一个扇区（4096比特或4KB），导致矩阵H规模极大（码率高于0.9时），读通道芯片成本极高，与系统性能提升相比不具成本效益。然而，随着2000年以来结构化矩阵H技术的发展，现代新型硬盘驱动器已能在读通道芯片中实际使用LDPC码。LDPC码用于迭代解码，由SOVA检测器和LDPC解码器协同工作。

## 4.6 实验结果

本节将测试LDPC码在AWGN信道和采用迭代解码技术的硬盘驱动器信道中的性能，以展示LDPC码的能力。

### 4.6.1 AWGN信道

考虑图4.5中的AWGN信道。使用的LDPC码是改进型阵列LDPC码（MAC），奇偶校验矩阵H大小为9×15（方程4.74），即该LDPC码一次编码6比特信息，输出15比特码字（9个奇偶校验比特）。信噪比定义为：

$$
\mathrm{SNR} = 10 \log_{10} \left( \frac{E_b}{N_0} \right)\tag{4.85}
$$

其中 $E_b=1$ 是每比特信息能量，$N_0/2$ 是噪声的双边功率谱密度，$w_n \sim \mathcal{N}(0,\sigma^2)$，$\sigma^2 = N_0/(2T)$，T是信息比特 $m_n$ 的周期。每个SNR的误码率通过将多个数据块（每块6比特）送入系统，直到解码器检测到的总错误不少于1000比特来获得。

图4.16显示了LDPC解码器在不同迭代次数下的系统性能。"Threshold detector"曲线是指将图4.5中的解码器从LDPC解码器替换为具有以下判决规则的阈值检测器：

$$
\hat{m}_n = \left\{ \begin{array} { l l } { 1, } & { \mathrm{if} \ r_n \geq 0 } \\ { 0, } & { \mathrm{if} \ r_n < 0 } \end{array} \right.\tag{4.86}
$$

对于 $n = \{1,2,...,6\}$。从图中可以看出，LDPC解码器的性能远优于阈值检测器，特别是当LDPC解码器内的迭代次数增加时。然而，当迭代次数增加到一定程度后，LDPC解码器的性能开始趋于稳定（这里可以看到第3次和第5次迭代的性能接近）。图4.17通过绘制不同SNR下每次迭代的BER曲线证实了这一结论——第4次迭代后LDPC解码器的性能开始稳定，这种现象称为错误平层。

接下来比较使用有环和无环奇偶校验矩阵H的LDPC码性能。修改方程(4.74)中的矩阵H，使其包含两个长度为4的环，得到矩阵 $\tilde{\mathbf{H}}$。图4.18比较了使用有环和无环矩阵H的LDPC码性能——实线为无环矩阵H，虚线为有环矩阵H。可以清楚地看到，在所有迭代次数下，使用无环矩阵H的LDPC码性能均优于使用有环矩阵H的LDPC码。因此，好的LDPC码不应使用有环的矩阵H[4, 5]。

### 4.6.2 迭代信道

本节展示第2.4节中描述的Turbo均衡器（迭代解码技术）的性能，该技术由软检测器和LDPC解码器协同工作，如图4.19所示。使用的LDPC码是改进型阵列LDPC码（MAC），其奇偶校验矩阵H如方程(4.71)所示，参数 $j=4, k=40, p=103$。即该LDPC码一次编码 $(40-3)\times 103 = 3708$ 比特信息，输出 $40\times 103 = 4120$ 比特的码字（奇偶校验比特数为 $4120-3708=412$ 比特），码率 $R = K/N = 0.9$。

从图4.19，信息 $m_n \in \{0,1\}$ 共3708比特，经LDPC编码器和映射器后得到数据序列 $s_n \in \{\pm 1\}$ 共4120比特。然后 $s_n$ 通过具有传递函数 $H(D) = 1 + 2D + D^2$ 的信道，得到读回信号：

$$
r_n = s_n * h_n + w_n\tag{4.88}
$$

其中 $h_n$ 是信道的第n个系数，$*$ 是卷积运算符，$w_n$ 是均值为零、方差为 $N_0/(2T)$ 的AWGN噪声。然后对数据序列 $r_n$ 进行迭代解码，在"SISO均衡器"（即第3章描述的各种软检测器）和LDPC解码器（内部MP算法迭代3次）之间交换软信息。编码系统的SNR定义为：

$$
\frac{E_c}{N_0} = 10 \log_{10} \left( \frac{\sum_i |h_i|^2}{N_0 R} \right)\tag{4.89}
$$

其中 $E_c = 1$ 是每编码比特的能量。每个SNR的BER通过将多个数据块（每块3708比特）送入系统，直到LDPC解码器在第5次迭代后检测到的总错误不少于1000比特来获得。

图4.20和图4.21以BER和扇区错误率（SER）的形式比较了BCJR和SOVA检测器与LDPC解码器协同工作的性能。"0.5 iteration"表示系统在软检测器首次输出时的性能（在将结果发送到LDPC解码器之前）。可以看出，随着迭代解码次数的增加，系统性能不断提高。使用BCJR检测器的系统性能优于使用SOVA检测器的系统，因为BCJR算法输出的LLR质量优于SOVA算法（如第3章所述）。

"0.5 iteration"曲线也可用于表示未编码系统的性能，这表明编码系统的性能始终优于未编码系统。因此可以得出结论，迭代解码系统可以进一步提高系统性能。

图4.22比较了BCJR和SOVA检测器在不同迭代次数下的性能，表明在所有迭代次数中，使用BCJR检测器的系统性能均优于使用SOVA检测器的系统。类似地，随着迭代解码次数的增加，系统性能始终提高。

## 4.7 本章小结

LDPC码是当前最优秀的纠错码[2, 5, 8]，已实际应用于各种领域，包括硬盘驱动器。

由于LDPC码是一种线性分组码，本章首先介绍了线性分组码的编码和解码步骤，包括生成矩阵和奇偶校验矩阵的含义。然后阐述了LDPC码的基础知识，并详细展示了LDPC码的编码和解码方法。实验结果表明，LDPC码的性能取决于所使用的奇偶校验矩阵。第4.5节展示了各种奇偶校验矩阵的构造示例——好的奇偶校验矩阵应无长度为4的环，且其中的"1"应尽可能随机分布，以实现LDPC码的最高性能[17]。此外，还展示了将LDPC码用于硬盘驱动器信道迭代解码系统的示例。实验结果表明，迭代解码可进一步提高系统性能，且性能随迭代解码次数的增加而提高。

## 4.8 习题

1. 请解释内在信息和外在信息的含义。
2. 请解释第4.1.5节中综合征解码的原理，并举例计算。
3. 设LDPC码的生成矩阵 $\mathbf{G} = \left[ \begin{array} { l l l l l } { 1 } & { 0 } & { 1 } & { 1 } & { 0 } \\ { 0 } & { 1 } & { 1 } & { 0 } & { 1 } \end{array} \right]$，求奇偶校验矩阵H并绘制Tanner图。
4. 使用与方程(4.25)中生成矩阵G对应的奇偶校验矩阵H，对数据 $\mathbf{m}=[1101]$ 和 $\mathbf{m}=[1011]$ 进行编码。
5. 使用方程(4.74)中的奇偶校验矩阵H，对数据 $\mathbf{m}=[101011]$ 和 $\mathbf{m}=[111010]$ 进行编码。
6. 从图4.5的信道模型出发，设输入数据比特 $m_n = \{1,1,0\}$，使用的LDPC码生成矩阵G如方程(4.4)所示，噪声 $w_n = \{0.2, 0.3, -0.1, -0.2, 0.5, -0.4\}$，方差 $\sigma^2 = 0.5$。求第3次迭代结束后的后验LLR值。
7. 从图4.19的信道模型出发，设输入数据序列 $m_n = \{1,1\}$，使用的LDPC码生成矩阵G如方程(4.4)所示，信道 $H(D) = 1 + D$，噪声 $w_n = \{0.3, -0.2, 0.1, 0.2, -0.4, -0.5\}$，方差 $\sigma^2 = 0.5$。使用Turbo均衡器解码数据序列 $r_n$，第3次迭代结束，LDPC解码器内部MP算法迭代3次，使用的SISO均衡器为：
   7.1) BCJR算法
   7.2) Max-Log-MAP算法
   7.3) Log-MAP算法
   7.4) SOVA算法
