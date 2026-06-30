# 第四章 LDPC 码

低密度奇偶校验 (LDPC: low-density parity-check) 码，简称"LDPC 码" [17]，被公认为是目前最优秀的纠错码 (ECC) [2, 5]，因为其性能比其他 ECC 码更接近香农极限 (Shannon limit) [25]。目前，LDPC 码已被广泛应用于多种实际系统，包括硬盘驱动器。

由于 LDPC 码是线性分组码 (linear block code) 的一种，本章将首先介绍线性分组码的基础知识，然后重点讲解 LDPC 码的工作原理，使读者理解 LDPC 编解码的步骤，并展示当前硬盘驱动器信号处理系统中使用的 Turbo 均衡器（即迭代解码）的性能，该方案由软检测器和 LDPC 解码器协同工作。

# 4.1 引言

本节将介绍线性分组码的工作原理，并解释线性分组码的编解码过程，为后续研究 LDPC 码奠定基础。

## 4.1.1 线性分组码

$(N, K)$ 线性分组码是一种信道码，它将 $K$ 位信息位 (message bit) 转换为 $N$ 位的码字 (codeword)。设 $\mathbf{m} = [m_1, m_2, \ldots, m_K]$ 是被编码的信息位向量，生成的码字为 $\mathbf{c} = [c_1, c_2, \ldots, c_N]$，如图 4.1 所示。增加的 $N-K$ 位称为"校验位 (parity bit)"，以向量形式表示为 $\mathbf{p} = [p_1, p_2, \ldots, p_{N-K}]$，帮助接收端检测错误。如果校验位足够多，还可以纠正数据错误。

$$
\begin{array}{c} \text{码字} \\ \left[ c_1, c_2, c_3, \dots, c_N \right] = \boxed{ \begin{array}{c c} \text{信息位} & \text{校验位} \\ \left[ m_1, m_2, m_3, \dots, m_K \right] & \left[ p_1, p_2, \dots, p_{N-K} \right] \end{array} } \\ \xleftarrow{} K \text{位} \xrightarrow{} N-K \text{位} \xrightarrow{} \end{array}
$$

图 4.1 $(N, K)$ 线性分组码的结构

![](images/chapter_4/3e9a9bd5249923ddfea04710590385de7751938de6cd5cd715224ab7a31a4c07.jpg)

线性分组码逐块进行编解码，数据块大小取决于具体应用。信息位数与码字位数的比值称为"码率 (code rate)" $R$，定义为：

$$
R = \frac{K}{N} \tag{4.1}
$$

其中 $0 < R \leq 1$。硬盘驱动器要求码率接近 1，以减少用于存储校验位的介质空间损耗 [43]。

## 4.1.2 生成矩阵

考虑 $1 \times K$ 的信息位 $\mathbf{m} = [m_1, m_2, \ldots, m_K]$。$(N, K)$ 线性分组码通过将信息位 $\mathbf{m}$ 与大小为 $K \times N$ 的生成矩阵 $\mathbf{G}$（元素为 0 或 1）相乘来生成 [2]：

$$
\mathbf{G}_{K \times N} = \left[ \mathbf{I}_{K \times K} \mid \mathbf{P}_{K \times (N-K)} \right] = \left[ \begin{array}{cccccccc} 1 & 0 & \dots & 0 & p_{1,1} & p_{1,2} & \dots & p_{1,(N-K)} \\ 0 & 1 & \dots & 0 & p_{2,1} & p_{2,2} & \dots & p_{2,(N-K)} \\ \vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & 1 & p_{K,1} & p_{K,2} & \dots & p_{K,(N-K)} \end{array} \right] \tag{4.2}
$$

其中 $\mathbf{I}$ 是 $K \times K$ 的单位矩阵，$\mathbf{P}$ 是 $K \times (N-K)$ 的校验矩阵，对应码字中的校验位。得到的码字 $\mathbf{c} = [c_1, c_2, \ldots, c_N]$ 大小为 $1 \times N$，即：

$$
\mathbf{c} = \mathbf{m} \mathbf{G} = \left[ \begin{array}{cccccccc} m_1 & m_2 & \dots & m_K & p_1 & p_2 & \dots & p_{N-K} \end{array} \right] \tag{4.3}
$$

公式 (4.3) 表明信息位 $\mathbf{m}$ 出现在码字 $\mathbf{c}$ 中，这类码称为"系统码 (systematic code)" [2]。

**例 4.1** 对数据 $\mathbf{m} = [101]$ 和 $\mathbf{m} = [110]$ 进行编码，设生成矩阵 $\mathbf{G}$ 为：

$$
\mathbf{G} = \left[ \begin{array}{cccccc} 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 1 & 0 & 0 & 1 & 1 \\ 0 & 0 & 1 & 1 & 0 & 1 \end{array} \right] \tag{4.4}
$$

**解**：生成矩阵 $\mathbf{G}$ 每次编码 3 位数据，即 $\mathbf{m} = [m_1 m_2 m_3]$。因此用矩阵 $\mathbf{G}$ 编码得到的码字为：

$$
\begin{array}{l} \mathbf{c} = \mathbf{m} \mathbf{G} = \left[ \begin{array}{ccc} m_1 & m_2 & m_3 \end{array} \right] \left[ \begin{array}{cccccc} 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 1 & 0 & 0 & 1 & 1 \\ 0 & 0 & 1 & 1 & 0 & 1 \end{array} \right] \\ = \left[ \begin{array}{cccccc} m_1 & m_2 & m_3 & m_1 \oplus m_3 & m_1 \oplus m_2 & m_2 \oplus m_3 \end{array} \right] \end{array}
$$

其中 $\oplus$ 是模 2 加法算子（即 XOR）。因此，若 $\mathbf{m} = [101]$，则 $\mathbf{c} = [101011]$；若 $\mathbf{m} = [110]$，则 $\mathbf{c} = [110101]$。

## 4.1.3 校验矩阵

$(N, K)$ 线性分组码也可以用大小为 $(N-K) \times N$ 的校验矩阵 (parity-check matrix) $\mathbf{H}$ 来定义，满足如下关系：

$$
\mathbf{H} \mathbf{G}^{\mathrm{T}} = \mathbf{0} \tag{4.5}
$$

因此，对于任何码字有：

$$
\mathbf{H} \mathbf{c}^{\mathrm{T}} = \mathbf{H} \mathbf{G}^{\mathrm{T}} \mathbf{m}^{\mathrm{T}} = \mathbf{0} \tag{4.6}
$$

此外，$\mathbf{H}$ 的每一行是一个校验方程 (parity-check equation)，定义了码字中数据位 $c_i$（$i = 1, 2, \ldots, N$）之间的关系。如果生成矩阵 $\mathbf{G}$ 是系统形式如公式 (4.2)，则校验矩阵为：

$$
\mathbf{H}_{(N-K) \times N} = \left[ \mathbf{P}^{\mathrm{T}} \mid \mathbf{I}_{(N-K) \times (N-K)} \right] \tag{4.7}
$$

其中 $(\cdot)^{\mathrm{T}}$ 表示矩阵转置。例如，公式 (4.4) 中的生成矩阵 $\mathbf{G}$ 可转换为 $\mathbf{H}$ 矩阵：

$$
\mathbf{H} = \left[ \begin{array}{cccccc} 1 & 0 & 1 & 1 & 0 & 0 \\ 1 & 1 & 0 & 0 & 1 & 0 \\ 0 & 1 & 1 & 0 & 0 & 1 \end{array} \right] \tag{4.8}
$$

## 4.1.4 码的最小距离

线性分组码的性能通过码字的汉明重量 (Hamming weight) 衡量，定义为：

$$
w_H(\mathbf{c}) = \text{码字 } \mathbf{c} \text{ 中值为 1 的比特数} \tag{4.9}
$$

例如，若 $\mathbf{c} = 100100$，则 $w_H([100100]) = 2$。$\mathbf{c}_1$ 和 $\mathbf{c}_2$ 之间的汉明距离 (Hamming distance) 定义为：

$$
d_H(\mathbf{c}_1, \mathbf{c}_2) = w_H(\mathbf{c}_1 - \mathbf{c}_2) = \sum_{i=0}^{N-1} (c_{1,i} \neq c_{2,i}) \tag{4.10}
$$

例如，若 $\mathbf{c}_1 = 110011$ 且 $\mathbf{c}_2 = 000111$，则汉明距离 $d_H(\mathbf{c}_1, \mathbf{c}_2) = 3$。

如果码 $\mathbf{c}$ 共有 $2^k$ 个码字，则码字间最小的汉明距离称为最小距离 (minimum distance) $d_{\min}$：

$$
d_{\min} = \min_{i \neq j} \{ d_H(\mathbf{c}_i, \mathbf{c}_j) \} \tag{4.11}
$$

其中 $\{i, j\} = 0, 1, \ldots, 2^k - 1$。知道了 $d_{\min}$ 就可知道该线性分组码能纠正 $t$ 位错误：

$$
t = \frac{|d_{\min} - 1|}{2} \tag{4.12}
$$

能检测 $e$ 位错误：

$$
e = d_{\min} - 1 \tag{4.13}
$$

此外，$d_{\min}$ 可直接从 $\mathbf{G}$ 和 $\mathbf{H}$ 矩阵求得：
- $\mathbf{G}$ 的行向量的最小汉明重量
- $\mathbf{H}$ 中模 2 相加为零的最小列数

## 4.1.5 线性分组码的解码

实践中线性分组码的解码采用"伴随式解码 (syndrome decoding)" [2]。伴随式向量 $\mathbf{s}$ 定义为：

$$
\mathbf{s} = \mathbf{H} \mathbf{r}^{\mathrm{T}} \tag{4.14}
$$

其中 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e} = [r_0, r_1, \ldots, r_{N-1}]$ 是待解码的数据向量，$\mathbf{c}$ 是码字向量，$\mathbf{e} = [e_0, e_1, \ldots, e_{N-1}]$ 是错误向量，$e_i \in \{0, 1\}$ 且 $e_i = 1$ 表示码字的第 $i$ 位有错误。将 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e}$ 代入公式 (4.14) 得：

$$
\begin{array}{l} \mathbf{s} = \mathbf{H} (\mathbf{c} \oplus \mathbf{e})^{\mathrm{T}} = \mathbf{H} \mathbf{c}^{\mathrm{T}} \oplus \mathbf{H} \mathbf{e}^{\mathrm{T}} \\ = \mathbf{H} \mathbf{e}^{\mathrm{T}} \tag{4.15} \end{array}
$$

即伴随式仅取决于错误向量 $\mathbf{e}$。因此无错误的序列（即 $\mathbf{r} = \mathbf{c}$）的伴随式始终为零。

通常线性分组码的解码使用查找表 (look-up table) [2]，该表显示伴随式与错误向量 $\mathbf{e}$ 的关系。当接收端需要解码数据序列 $\mathbf{r}$ 时，先按公式 (4.14) 计算伴随式，再从表中找到对应的错误向量 $\mathbf{e}$，再通过下式解码：

$$
\hat{\mathbf{c}} = \mathbf{r} \oplus \mathbf{e} \tag{4.16}
$$

然而，伴随式解码仅适用于码字短且错误少的系统。对于硬盘驱动器（每扇区 4096 比特），可能的码字数为 $2^{4096}$，查找表极其庞大而无法实际使用。

# 4.2 LDPC 码基础

LDPC 码是一种由稀疏校验矩阵 $\mathbf{H}$ 定义的线性分组码，其中 1 的数量相对于矩阵规模非常少。LDPC 码由 Gallager [17] 于 1960 年在美国麻省理工学院 (MIT) 提出。1981 年，Tanner [44] 提出了 Tanner 图来表示编码关系。1990 年，MacKay 和 Neal [45] 发现 LDPC 码的性能比 Turbo 码 [3] 更接近香农极限，使 LDPC 码重新受到广泛关注。

LDPC 码是由大小为 $M \times N$ 的稀疏矩阵 $\mathbf{H}$ [17] 定义的奇偶校验码，码字 $\mathbf{c}$ 长度为 $N$ 位，所有码字必须满足 $M$ 个如公式 (4.6) 所示的校验方程。LDPC 码主要分为两类：

**正则 LDPC 码 (regular LDPC code)** — $\mathbf{H}$ 矩阵中 1 的分布是固定的：每行有相同数量的 1，每列有相同数量的 1。

**非正则 LDPC 码 (irregular LDPC code)** [46] — $\mathbf{H}$ 矩阵中 1 的分布不固定，通常性能优于正则 LDPC 码。

## 4.2.1 正则 LDPC 码

正则 LDPC 码 $(j, k)$ 由校验矩阵 $\mathbf{H}$（大小 $M \times N$）定义，每列有 $j$ 个 1，每行有 $k$ 个 1，$j < k$ 且 $\{j, k\} \ll N$。$\mathbf{H}$ 中共有 $Mk = Nj$ 个 1。假设 $\mathbf{H}$ 所有行线性无关，则码率为：

$$
R = 1 - \frac{M}{N} = 1 - \frac{j}{k} \tag{4.17}
$$

参数需满足 $M = \frac{Nj}{k}$ 为整数。例如，正则 LDPC 码 $(3, 4)$ 要求 $N$ 为 4 的倍数。

正则 LDPC 码 $(2, 4)$ 的校验矩阵 $\mathbf{H}$ 示例（$M=5, N=10$）：

$$
\mathbf{H}_{5 \times 10} = \left[ \begin{array}{cccccccccc} 1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 0 & 1 \\ 0 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 1 \end{array} \right] \tag{4.19}
$$

该 LDPC 码编码 $K = N - M = 5$ 位信息位，生成 10 位的码字。

$\mathbf{H}$ 的每一行称为"校验节点 (check node)"，每一列称为"比特节点 (bit node)"。校验方程为：

校验节点 1：$c_1 + c_2 + c_3 + c_4 = 0$ \hfill (4.20)
校验节点 2：$c_1 + c_5 + c_6 + c_7 = 0$ \hfill (4.21)
校验节点 3：$c_2 + c_5 + c_8 + c_9 = 0$ \hfill (4.22)
校验节点 4：$c_3 + c_6 + c_8 + c_{10} = 0$ \hfill (4.23)
校验节点 5：$c_4 + c_7 + c_9 + c_{10} = 0$ \hfill (4.24)

奇偶校验码可以用 Tanner 图 [44, 50] 表示，它是校验矩阵的二部图表示。Tanner 图有 $N$ 个比特节点（圆圈 $\circ$）和 $M$ 个校验节点（方块 $\square$），当 $h_{m,n} = 1$ 时节点间有边连接。![](images/chapter_4/3e9a9bd5249923ddfea04710590385de7751938de6cd5cd715224ab7a31a4c07.jpg)

图 4.2 正则 LDPC 码 $(2, 4)$ 的 Tanner 图

## 4.2.2 非正则 LDPC 码

非正则 LDPC 码由 Richardson [46] 于 2001 年提出。其校验矩阵 $\mathbf{H}$ 中 1 的分布不固定，即每行和每列中 1 的数量不必相等。非正则 LDPC 码由度分布多项式 (degree distribution polynomial) 定义：比特节点度分布 $\rho(x) = \sum_i \rho_i x^i$，校验节点度分布 $\xi(x) = \sum_i \xi_i x^i$。

LDPC 码的性能可通过密度演化理论 (density evolution) [48] 预测，该理论跟踪节点间传递消息的概率密度。非正则 LDPC 码的设计目标是使性能阈值尽可能接近香农容量极限 [25]。

**例 4.2** 考虑 $(7, 4)$ 汉明码，生成矩阵为：

$$
\mathbf{G} = \left[ \begin{array}{ccccccc} 1 & 0 & 0 & 0 & 1 & 0 & 1 \\ 0 & 1 & 0 & 0 & 1 & 1 & 1 \\ 0 & 0 & 1 & 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 & 0 & 1 & 1 \end{array} \right] \tag{4.25}
$$

求校验矩阵并绘制 Tanner 图。

**解**：根据公式 (4.7)，校验矩阵为：

$$
\mathbf{H} = \left[ \begin{array}{ccccccc} 1 & 1 & 1 & 0 & 1 & 0 & 0 \\ 0 & 1 & 1 & 1 & 0 & 1 & 0 \\ 1 & 1 & 0 & 1 & 0 & 0 & 1 \end{array} \right] \tag{4.26}
$$

Tanner 图如图 4.3 所示。该 $(7, 4)$ 汉明码可作为非正则 LDPC 码使用。

## 4.2.3 双曲正切规则

设 $\mathbf{c} = [c_1, c_2, \ldots, c_n]$ 是 $n$ 位数据位向量，$c_i \in \{0, 1\}$。定义奇偶函数 $\Phi(\mathbf{c}) \in \{0, 1\}$：

$$
\Phi(\mathbf{c}) = c_1 \oplus c_2 \oplus \ldots \oplus c_n \tag{4.27}
$$

$\Phi(\mathbf{c}) = 0$（偶校验）当 1 的个数为偶数；$\Phi(\mathbf{c}) = 1$（奇校验）当 1 的个数为奇数。$\Phi(\mathbf{c})$ 的先验 LLR 定义为：

$$
\lambda_{\Phi(\mathbf{c})} = \log\left(\frac{\operatorname{Pr}[\Phi(\mathbf{c}) = 1]}{\operatorname{Pr}[\Phi(\mathbf{c}) = 0]}\right) \tag{4.28}
$$

且有：

$$
\Phi(\mathbf{c}) = \left\{ \begin{array}{ll} 1, & \text{若 } \lambda_{\Phi(\mathbf{c})} \geq 0 \\ 0, & \text{若 } \lambda_{\Phi(\mathbf{c})} < 0 \end{array} \right. \tag{4.29}
$$

假设所有数据位独立，则 $\lambda_{\Phi(\mathbf{c})}$ 满足双曲正切规则 (tanh rule) [51, 52]：

$$
\tanh\left(\frac{-\lambda_{\Phi(\mathbf{c})}}{2}\right) = \prod_{i=1}^{n} \tanh\left(\frac{-\lambda_i}{2}\right) \tag{4.30}
$$

其中 $\lambda_i = \log(\operatorname{Pr}[c_i = 1] / \operatorname{Pr}[c_i = 0])$。求解得：

$$
\lambda_{\Phi(\mathbf{c})} = -2 \tanh^{-1}\left\{ \prod_{i=1}^{n} \tanh\left(\frac{-\lambda_i}{2}\right) \right\} \tag{4.31}
$$

或表示为另一种形式：

$$
\lambda_{\Phi(\mathbf{c})} = -\prod_{i=1}^{n} \operatorname{sign}(-\lambda_i) \times f\left(\sum_{i=1}^{n} f(|\lambda_i|)\right) \tag{4.32}
$$

其中：

$$
f(x) = \log\left(\frac{e^x + 1}{e^x - 1}\right) = -\log\left(\tanh\left(\frac{x}{2}\right)\right) \tag{4.33}
$$

图 4.4 显示 $f(x)$ 函数性质：$f(x)$ 正定且对 $x > 0$ 单调递减，$f(0) = \infty$，$f(\infty) = 0$，且 $f(f(x)) = x$。

符号关系：$\operatorname{sign}(\lambda_{\Phi(\mathbf{c})}) = (-1)^{\Phi(\hat{\mathbf{c}}) + 1}$，其中 $\hat{\mathbf{c}}$ 是 $\mathbf{c}$ 的最可能估计。$\lambda_{\Phi(\mathbf{c})}$ 的幅度衡量计算出的奇偶值的可靠性：

$$
|\lambda_{\Phi(\mathbf{c})}| = f\left(\sum_i f(|\lambda_i|)\right) \tag{4.35}
$$

当只有一个 $\lambda_i = 0$ 时，$\lambda_{\Phi(\mathbf{c})} = 0$（奇偶值完全不确定）。最小值近似：

$$
|\lambda_{\Phi(\mathbf{c})}| \approx |\lambda_{\min}| \tag{4.36}
$$

因此：

$$
\lambda_{\Phi(\mathbf{c})} = (-1)^{\Phi(\hat{\mathbf{c}}) + 1} |\lambda_{\min}| \tag{4.37}
$$

# 4.3 LDPC 编码

给定校验矩阵 $\mathbf{H}$，通过高斯消元转换为系统形式 $[\mathbf{P}^T | \mathbf{I}]$，得到生成矩阵 $\mathbf{G} = [\mathbf{I} | \mathbf{P}]$。编码：$\mathbf{v} = \mathbf{u} \mathbf{G}$，$\mathbf{u}$ 为信息向量，$\mathbf{v}$ 为码字。

# 4.4 LDPC 解码

LDPC 码通常使用消息传递算法 (MPA: Message Passing Algorithm) [4, 17] 解码，在 Tanner 图上沿边传递 LLR 消息。

## 4.4.1 LDPC 解码基础

考虑图 4.5 所示 AWGN 信道下的编解码系统。接收信号 $r_n = s_n + w_n$，其中 $s_n = 2c_n - 1$，$w_n \sim \mathcal{N}(0, \sigma^2)$。MAP 接收机计算后验 LLR：

$$
\lambda_n = \log\left(\frac{\operatorname{Pr}[c_n = 1 \mid \mathbf{r}]}{\operatorname{Pr}[c_n = 0 \mid \mathbf{r}]}\right) \tag{4.43}
$$

根据贝叶斯法则推导得（见源文公式 4.44-4.46）：

$$
\lambda_n = \frac{2}{\sigma^2} r_n + \log\left(\frac{\operatorname{Pr}[c_n = 1 \mid \mathbf{r}_{i \neq n}]}{\operatorname{Pr}[c_n = 0 \mid \mathbf{r}_{i \neq n}]}\right) \tag{4.47}
$$

其中 $2/\sigma^2$ 是信道可靠性 (channel reliability)，$\frac{2}{\sigma^2} r_n$ 是内禀信息，第二项是外部信息。

**例 4.4** BSC 信道的后验 LLR 为 $\lambda_n^{\text{int}} = \log((1-\alpha)/\alpha)$，$\alpha$ 为交叉概率。

由 Tanner 图结构，比特节点 $n$ 连接 $j$ 个校验节点。外部信息从其他比特节点经校验节点获得。

## 4.4.2 LDPC 码的环

Tanner 图中的环 (cycle) 影响 BP 算法收敛性。4 环会降低性能，设计 $\mathbf{H}$ 时应避免短环。

## 4.4.3 数据位 LLR 的计算

信道 LLR：$\lambda_n^{\text{ch}} = 2r_n/\sigma^2$（AWGN）或 $\lambda_n^{\text{ch}} = \log((1-\alpha)/\alpha)$（BSC）。

## 4.4.4 消息传递算法

消息传递算法 (MP: Message Passing)：

# 消息传递算法 (MP)

1. **初始化**：每个比特节点 $v_n$ 的初始消息为信道 LLR $\lambda_n^{\text{ch}}$
2. **校验节点更新**：对每个校验节点 $c_m$ 和相邻比特节点 $v_n$：
   $$ \lambda_{c_m \to v_n} = 2\tanh^{-1}\left(\prod_{v_{n'} \in N(c_m)\setminus\{v_n\}} \tanh(\lambda_{v_{n'} \to c_m}/2)\right) $$
3. **比特节点更新**：对每个比特节点 $v_n$ 和相邻校验节点 $c_m$：
   $$ \lambda_{v_n \to c_m} = \lambda_n^{\text{ch}} + \sum_{c_{m'} \in N(v_n)\setminus\{c_m\}} \lambda_{c_{m'} \to v_n} $$
4. **硬判决**：总 LLR $\lambda_n^{\text{total}} = \lambda_n^{\text{ch}} + \sum_{c_m \in N(v_n)} \lambda_{c_m \to v_n}$，$\hat{c}_n = 1$ 若 $\lambda_n^{\text{total}} \geq 0$
5. **校验**：若 $\mathbf{H} \hat{\mathbf{c}}^{\text{T}} = \mathbf{0}$ 或达最大迭代次数，停止；否则返回步骤 2

# 4.5 校验矩阵的构造

## 4.5.1 正则 LDPC 码

随机构造：生成固定列重 $j$、行重 $k$ 的 $M \times N$ 稀疏矩阵，避免 4 环。

## 4.5.2 阵列 LDPC 码

基于有限域构造，具有准循环结构，便于硬件实现。

## 4.5.3 改进的阵列 LDPC 码

优化列重和环长分布，进一步提高性能。

## 4.5.4 说明

实际系统多采用 QC-LDPC 码（5G NR、DVB-S2、802.11n/ac/ax 等标准均采用）。

# 4.6 实验结果

## 4.6.1 AWGN 信道

测试不同 $E_c/N_0$ 下 LDPC 码的 BER 性能。非正则 LDPC 码优于正则码，性能随迭代次数增加而提升。

## 4.6.2 迭代信道

LDPC 码与软检测器协同工作，通过迭代交换软信息提升系统整体性能。

# 4.7 本章小结

LDPC 码是稀疏校验矩阵定义的线性分组码，使用消息传递算法解码。性能接近香农极限，广泛应用于通信和存储系统。

# 4.8 本章习题

1. 推导 LDPC 码校验节点更新的双曲正切规则。
2. 说明 Tanner 图中环对 BP 算法的影响。
3. 对比正则与非正则 LDPC 码。
4. 推导 LLR 分解为内禀和外部信息的过程。
5. 设计一个 $(3,6)$ 正则 LDPC 码校验矩阵，$N=12$。
