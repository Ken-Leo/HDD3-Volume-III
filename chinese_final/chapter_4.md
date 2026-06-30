# 第四章 LDPC 码

低密度奇偶校验 (LDPC: low-density parity-check) 码，简称"LDPC 码" [17]，被公认为是目前最优秀的纠错码 (ECC) [2, 5]，因其性能比其他 ECC 码更接近香农极限 (Shannon limit) [25]。目前，LDPC 码已被应用于多种实际系统，包括硬盘驱动器。

由于 LDPC 码是线性分组码 (linear block code) 的一种，本章将首先介绍线性分组码的基础知识，然后重点讲解 LDPC 码的工作原理，使读者理解 LDPC 编解码的步骤，并展示当前硬盘驱动器信号处理系统中使用的 Turbo 均衡器（即迭代解码）的性能，该方案由软检测器和 LDPC 解码器协同工作。

# 4.1 引言

本节将介绍线性分组码的工作原理，并解释线性分组码的编解码过程，为后续研究 LDPC 码奠定基础。

## 4.1.1 线性分组码

$(N, K)$ 线性分组码是一种信道码，它将 $K$ 位信息位 (message bit) 转换为 $N$ 位的码字 (codeword)。设 $\mathbf{m} = [m_1, m_2, \ldots, m_K]$ 是被编码的信息位向量，生成的码字为 $\mathbf{c} = [c_1, c_2, \ldots, c_N]$，如图 4.1 所示。增加的 $N-K$ 位称为"校验位 (parity bit)"，以向量形式表示为 $\mathbf{p} = [p_1, p_2, \ldots, p_{N-K}]$，帮助接收端检测错误。如果校验位足够多，还可以纠正数据错误。

$$
\begin{array}{c} \text{码字} \\ \left[ c_1, c_2, c_3, \dots, c_N \right] = \boxed{ \begin{array}{c c} \text{信息位} & \text{校验位} \\ \left[ m_1, m_2, m_3, \dots, m_K \right] & \left[ p_1, p_2, \dots, p_{N-K} \right] \end{array} } \\ \xleftarrow{} K \text{位} \xrightarrow{} N-K \text{位} \xrightarrow{} \end{array}
$$

图 4.1 $(N, K)$ 线性分组码的结构

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

其中 $\oplus$ 是模 2 加运算符，即 XOR（异或）。因此，若 $\mathbf{m} = [101]$，则 $\mathbf{c} = [101011]$；若 $\mathbf{m} = [110]$，则 $\mathbf{c} = [110101]$。

## 4.1.3 校验矩阵

$(N, K)$ 线性分组码也可以用大小为 $(N-K) \times N$ 的校验矩阵 (parity-check matrix) $\mathbf{H}$ 来定义，其满足如下关系：

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

线性分组码的性能通过码字的汉明重量 (Hamming weight) 来衡量，定义为：

$$
w_H(\mathbf{c}) = \text{码字 } \mathbf{c} \text{ 中值为 1 的比特数} \tag{4.9}
$$

例如，若 $\mathbf{c} = 100100$，则 $w_H([100100]) = 2$。$\mathbf{c}_1$ 和 $\mathbf{c}_2$ 之间的汉明距离 (Hamming distance) 定义为：

$$
d_H(\mathbf{c}_1, \mathbf{c}_2) = w_H(\mathbf{c}_1 - \mathbf{c}_2) = \sum_{i=0}^{N-1} (c_{1,i} \neq c_{2,i}) \tag{4.10}
$$

## 4.1.5 线性分组码的解码

实践中线性分组码的解码采用"伴随式解码 (syndrome decoding)" [2]。伴随式向量 $\mathbf{s}$ 定义为：

$$
\mathbf{s} = \mathbf{H} \mathbf{r}^{\mathrm{T}} \tag{4.14}
$$

其中 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e} = [r_0, r_1, \ldots, r_{N-1}]$ 是待解码的数据向量，$\mathbf{c}$ 是码字向量，$\mathbf{e} = [e_0, e_1, \ldots, e_{N-1}]$ 是错误向量，$e_i \in \{0, 1\}$ 且 $e_i = 1$ 表示码字的第 i 位有错误。将 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e}$ 代入公式 (4.14) 得：

$$
\begin{array}{l} \mathbf{s} = \mathbf{H} (\mathbf{c} \oplus \mathbf{e})^{\mathrm{T}} = \mathbf{H} \mathbf{c}^{\mathrm{T}} \oplus \mathbf{H} \mathbf{e}^{\mathrm{T}} \\ = \mathbf{H} \mathbf{e}^{\mathrm{T}} \tag{4.15} \end{array}
$$

即伴随式仅取决于错误向量 $\mathbf{e}$。因此无错误的数据序列（即 $\mathbf{r} = \mathbf{c}$）的伴随式始终为零。

通常线性分组码的解码使用查找表 (look-up table) [2]，该表显示伴随式与错误向量 $\mathbf{e}$ 之间的关系。当接收端需要解码数据序列 $\mathbf{r}$ 时，先按公式 (4.14) 计算伴随式，然后从查找表中找到对应的错误向量 $\mathbf{e}$，再通过下式解码：

$$
\hat{\mathbf{c}} = \mathbf{r} \oplus \mathbf{e} \tag{4.16}
$$

这种解码方法可以自动纠正数据序列 $\mathbf{r}$ 中的错误。然而，伴随式解码仅适用于码字长度短且每个码字中错误数量少的系统。

由于硬盘驱动器信号处理系统每次编解码一个扇区（即 4096 比特），如果信息位长度为 $K = 4096$ 比特，则可能的码字总数为 $2^{4096}$ 种，对应的伴随式查找表将极其庞大（无法实际使用）。因此伴随式解码无法实际应用于硬盘驱动器。

# 4.2 LDPC 码基础

LDPC 码是一种特殊的线性分组码，其校验矩阵中 1 的数量相对于矩阵规模非常少，以获得较大的最小距离 $d_{\min}$。LDPC 码由 Gallager [17] 于 1960 年在美国麻省理工学院 (MIT) 提出。然而，初期 LDPC 码并未受到足够重视，主要受限于计算能力。1981 年，Tanner [44] 提出了 Tanner 图来表示编码关系，有助于简化解码过程。1990 年，MacKay 和 Neal [45] 发现 LDPC 码的性能比 Turbo 码 [3] 更接近香农极限，从而使 LDPC 码重新受到广泛关注，并被应用于多种实际系统，包括硬盘驱动器。

LDPC 码是由大小为 $M \times N$ 的稀疏矩阵 $\mathbf{H}$ [17] 定义的奇偶校验码。码字 $\mathbf{c}$ 长度为 $N$ 位，所有码字必须满足 $M$ 个如公式 (4.6) 所示的奇偶校验方程。LDPC 码主要分为两类：

**正则 LDPC 码 (regular LDPC code)** — $\mathbf{H}$ 矩阵中 1 的分布是固定的，与 Gallager [17] 的 LDPC 码相同：每行有相同数量的 1，每列有相同数量的 1。

**非正则 LDPC 码 (irregular LDPC code)** [46] — $\mathbf{H}$ 矩阵中 1 的分布不固定，通常性能优于正则 LDPC 码。

为便于解释 LDPC 码的工作原理，以下仅考虑 $\mathbf{H}$ 矩阵中所有行线性无关的情况，此时信息位的长度为 $K = N - M$ 比特 [4, 17]。

## 4.2.1 正则 LDPC 码

正则 LDPC 码 $(j, k)$ 由大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 定义，每列有 $j$ 个 1，每行有 $k$ 个 1，其中 $j < k$ 且 $\{j, k\} \ll N$。这意味着每个校验方程关联 $k$ 个数据位，每个数据位关联 $j$ 个校验方程。因此 $\mathbf{H}$ 中共有 $Mk = Nj$ 个 1。假设 $\mathbf{H}$ 的所有行线性无关，则正则 LDPC 码的码率为：

$$
R = 1 - \frac{M}{N} = 1 - \frac{j}{k} \tag{4.17}
$$

其中 $j < k$ 以保证 $R \leq 1$。

选择正则 LDPC 码 $(j, k)$ 的参数 $(M, N, j, k)$ 时，需满足 $Mk = Nj$，因此必须选择使下式为整数的参数：

$$
M = \frac{Nj}{k} \tag{4.18}
$$

例如，正则 LDPC 码 $(3, 4)$ 只能用于 $N = 1000$ 或 $1004$ 的系统，而不能用于 $N = 1002$ 的系统。正则 LDPC 码 $(2, 4)$ 的校验矩阵 $\mathbf{H}$ 为：

$$
\mathbf{H}_{5 \times 10} = \left[ \begin{array}{cccccccccc} 1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 0 & 1 \\ 0 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 1 \end{array} \right] \tag{4.19}
$$

其中 $M = 5$，$N = 10$，满足公式 (4.18)。该 LDPC 码编码 $10 - 5 = 5$ 位信息位，生成 10 位的码字。

公式 (4.19) 的校验矩阵 $\mathbf{H}$ 表示了校验方程与数据位之间的关系。$\mathbf{H}$ 的每一行称为"校验节点 (check node)"，每一列称为"比特节点 (bit node)"。因此各校验节点的校验方程为：

校验节点 1：$c_1 + c_2 + c_3 + c_4 = 0$ \hfill (4.20)\\
校验节点 2：$c_1 + c_5 + c_6 + c_7 = 0$ \hfill (4.21)\\
校验节点 3：$c_2 + c_5 + c_8 + c_9 = 0$ \hfill (4.22)\\
校验节点 4：$c_3 + c_6 + c_8 + c_{10} = 0$ \hfill (4.23)\\
校验节点 5：$c_4 + c_7 + c_9 + c_{10} = 0$ \hfill (4.24)

奇偶校验码可以用 Tanner 图 [44, 50] 来表示，它是 $M \times N$ 校验矩阵 $\mathbf{H}$ 的一种图形化表示。Tanner 图有 $N$ 个比特节点（每个比特对应一个节点）和 $M$ 个校验节点（每个校验方程对应一个节点）。本文使用圆圈 $\circ$ 表示比特节点，方块 $\square$ 表示校验节点。校验节点连接到与其校验方程相关的比特节点。换句话说，当 $h_{m,n} = 1$ 时，第 $m$ 个校验节点与第 $n$ 个比特节点之间存在边 (edge)。Tanner 图也称为"二部图 (bipartite graph)"，因为图中只有两种节点（比特节点和校验节点），且相同类型的节点之间没有边相连。图 4.2 展示了正则 LDPC 码 $(j, k) = (2, 4)$ 的 Tanner 图，其校验矩阵 $\mathbf{H}$ 如公式 (4.19) 所示。可以看出，每个比特节点有 2 条边（对应 $j = 2$），每个校验节点有 4 条边（对应 $k = 4$）。同时，该 Tanner 图也对应于公式 (4.20)-(4.24) 中的所有校验方程。

## 4.2.2 非正则 LDPC 码

非正则 LDPC 码由 Richardson [46] 于 2001 年提出。其 $M \times N$ 校验矩阵 $\mathbf{H}$ 中 1 的分布不固定，即每行和每列中 1 的数量不必相等。

在实际中，非正则 LDPC 码由度分布多项式 (degree distribution polynomial) 定义，该多项式描述了每个节点的边数。比特节点的度分布多项式为 $\rho(x) = \sum_i \rho_i x^i$，其中 $\rho_i$ 是度为 $i$ 的比特节点数量。类似地，校验节点的度分布多项式为 $\xi(x) = \sum_i \xi_i x^i$，其中 $\xi_i$ 是度为 $i$ 的校验节点数量。

LDPC 码作为校验节点和比特节点度分布函数的性能，可以通过密度演化理论 (density evolution) [48] 来预测，该理论跟踪在校验节点和比特节点之间传递的消息的概率密度。通常，如果系统工作在足够高的 SNR 下，密度的均值会随着 LDPC 解码器内部迭代次数的增加而趋于无穷大，这意味着解码器对正确解码有很高的置信度。相反，如果系统工作在低 SNR 下，密度均值会收敛到某个常数，这意味着 LDPC 解码器存在解码缺陷。因此，作为 LDPC 码性能分界线的 SNR 值称为"阈值 (threshold)"。非正则 LDPC 码的设计目标是使该阈值尽可能接近香农容量极限 (Shannon capacity) [25]（优于正则 LDPC 码）[49]。

**例 4.2** 考虑 $(7, 4)$ 汉明码，其生成矩阵为：

$$
\mathbf{G} = \left[ \begin{array}{ccccccc} 1 & 0 & 0 & 0 & 1 & 0 & 1 \\ 0 & 1 & 0 & 0 & 1 & 1 & 1 \\ 0 & 0 & 1 & 0 & 1 & 1 & 0 \\ 0 & 0 & 0 & 1 & 0 & 1 & 1 \end{array} \right] \tag{4.25}
$$

求校验矩阵 $\mathbf{H}$ 并绘制其 Tanner 图。

**解**：由于矩阵 $\mathbf{G}$ 的结构符合公式 (4.2)，因此可根据公式 (4.7) 求得矩阵 $\mathbf{H}$：

$$
\mathbf{H} = \left[ \begin{array}{ccccccc} 1 & 1 & 1 & 0 & 1 & 0 & 0 \\ 0 & 1 & 1 & 1 & 0 & 1 & 0 \\ 1 & 1 & 0 & 1 & 0 & 0 & 1 \end{array} \right] \tag{4.26}
$$

其 Tanner 图如图 4.3 所示。从公式 (4.26) 的 $\mathbf{H}$ 矩阵可以看出，$(7, 4)$ 汉明码可作为非正则 LDPC 码使用。

## 4.2.3 双曲正切规则

## 4.2.3 双曲正切规则

设 $\mathbf{c} = [c_1, c_2, \ldots, c_n]$ 是 $n$ 位数据位向量，$c_i \in \{0, 1\}$。定义奇偶函数 $\Phi(\mathbf{c}) \in \{0, 1\}$ 如下：

$$
\Phi(\mathbf{c}) = c_1 \oplus c_2 \oplus \ldots \oplus c_n \tag{4.27}
$$

其中 $\oplus$ 是模 2 加法算子。$\Phi(\mathbf{c}) = 0$（偶校验）当向量 $\mathbf{c}$ 中 1 的个数为偶数；$\Phi(\mathbf{c}) = 1$（奇校验）当 1 的个数为奇数。奇偶函数 $\Phi(\mathbf{c})$ 的先验 LLR 定义为：

$$
\lambda_{\Phi(\mathbf{c})} = \log\left(\frac{\operatorname{Pr}[\Phi(\mathbf{c}) = 1]}{\operatorname{Pr}[\Phi(\mathbf{c}) = 0]}\right) \tag{4.28}
$$

且有：

$$
\Phi(\mathbf{c}) = \left\{ \begin{array}{ll} 1, & \text{若 } \lambda_{\Phi(\mathbf{c})} \geq 0 \\ 0, & \text{若 } \lambda_{\Phi(\mathbf{c})} < 0 \end{array} \right. \tag{4.29}
$$

假设所有数据位相互独立，则 $\lambda_{\Phi(\mathbf{c})}$ 满足双曲正切规则 (tanh rule) [51, 52]：

$$
\tanh\left(\frac{-\lambda_{\Phi(\mathbf{c})}}{2}\right) = \prod_{i=1}^{n} \tanh\left(\frac{-\lambda_i}{2}\right) \tag{4.30}
$$

（参见附录 B 的说明），其中 $\lambda_i = \log(\operatorname{Pr}[c_i = 1] / \operatorname{Pr}[c_i = 0])$。求解公式 (4.30) 得：

$$
\lambda_{\Phi(\mathbf{c})} = -2 \tanh^{-1}\left\{ \prod_{i=1}^{n} \tanh\left(\frac{-\lambda_i}{2}\right) \right\} \tag{4.31}
$$

或表示为另一种形式：

$$
\lambda_{\Phi(\mathbf{c})} = -\prod_{i=1}^{n} \operatorname{sign}(-\lambda_i) \times f\left(\sum_{i=1}^{n} f(|\lambda_i|)\right) \tag{4.32}
$$

（参见附录 C 的说明），其中：

$$
f(x) = \log\left(\frac{e^x + 1}{e^x - 1}\right) = -\log\left(\tanh\left(\frac{x}{2}\right)\right) \tag{4.33}
$$

# 4.3 LDPC 编码

给定 LDPC 码的校验矩阵 $\mathbf{H}$，可通过高斯消元法将 $\mathbf{H}$ 转换为系统形式 $[\mathbf{P}^T | \mathbf{I}]$，从而得到生成矩阵 $\mathbf{G} = [\mathbf{I} | \mathbf{P}]$。编码过程为 $\mathbf{v} = \mathbf{u} \mathbf{G}$，其中 $\mathbf{u}$ 是信息向量，$\mathbf{v}$ 是码字。

# 4.4 LDPC 解码

LDPC 码通常使用置信传播 (BP: Belief Propagation) 算法进行解码，也称为消息传递算法 (Message Passing Algorithm)。该算法在 Tanner 图上沿边传递对数似然比 (LLR) 消息。

## 4.4.1 LDPC 解码基础

BP 算法中，比特节点和校验节点交替更新并沿边传递消息。

# 4.4 LDPC 解码

LDPC 编码使各数据位根据校验矩阵 $\mathbf{H}$ 的结构产生关联，因此 LDPC 解码利用这些关联来帮助解码数据。LDPC 码通常使用消息传递算法 (MPA: Message Passing Algorithm) 进行解码，简称"MP 算法" [4, 17]。该算法首先从校验矩阵 $\mathbf{H}$ 构建校验方程，然后绘制 Tanner 图，最后按照 MP 算法的步骤进行解码。

## 4.4.1 LDPC 解码基础

考虑图 4.5 所示的信道模型。$K$ 位输入数据序列 $m_n \in \{0, 1\}$ 经正则 LDPC 码 $(j, k)$ 编码，得到 $N$ 位码字 $c_n \in \{0, 1\}$，送入映射器转换为 $s_n \in \{\pm 1\}$。接收端接收到的信号为：

$$
r_n = s_n + w_n \tag{4.42}
$$

其中 $s_n = 2c_n - 1$，$w_n \sim \mathcal{N}(0, \sigma^2)$ 是 AWGN。LDPC 解码器对 $r_n$ 进行解码，输出估计值 $\hat{m}_n$，使错误最小化。

这里仅考虑系统 LDPC 码，码字结构如公式 (4.3)，即 $m_i = c_i$（$1 \leq i \leq K$）。MAP 接收机为每个时刻 $n$ 选择使 $\operatorname{Pr}[c_n = c \mid \mathbf{r}]$ 最大的 $c$ 值，即计算后验 LLR：

$$
\lambda_n = \log\left(\frac{\operatorname{Pr}[c_n = 1 \mid \mathbf{r}]}{\operatorname{Pr}[c_n = 0 \mid \mathbf{r}]}\right) = \log\left(\frac{\operatorname{Pr}[c_n = 1 \mid r_n; \mathbf{r}_{i \neq n}]}{\operatorname{Pr}[c_n = 0 \mid r_n; \mathbf{r}_{i \neq n}]}\right) \tag{4.43}
$$

判断规则：$\hat{c}_n = 1$ 当 $\lambda_n \geq 0$，$\hat{c}_n = 0$ 当 $\lambda_n < 0$。根据贝叶斯法则（详见原文推导），可得：

$$
\lambda_n = \frac{2}{\sigma^2} r_n + \log\left(\frac{\operatorname{Pr}[c_n = 1 \mid \mathbf{r}_{i \neq n}]}{\operatorname{Pr}[c_n = 0 \mid \mathbf{r}_{i \neq n}]}\right) \tag{4.47}
$$

其中第一项是"内禀信息 (intrinsic information)"，来自接收数据 $r_n$；第二项是"外部信息 (extrinsic information)"，来自除 $c_n$ 外的所有其他接收数据。内禀信息与 $r_n$ 成正比，常数 $2/\sigma^2$ 称为信道可靠性 (channel reliability) [51]。

**例 4.4** 考虑图 4.6 的二进制对称信道 (BSC)，证明其后验 LLR 满足公式 (4.47)，其中信道可靠性为 $\log((1-\alpha)/\alpha)$ 而非 $2/\sigma^2$，$\alpha$ 是交叉概率。

**解**：从图 4.6 的信道可得 $p(r_n = 0|c_n = 0) = 1 - \alpha$，$p(r_n = 0|c_n = 1) = \alpha$，$p(r_n = 1|c_n = 0) = \alpha$，$p(r_n = 1|c_n = 1) = 1 - \alpha$。因此 BSC 信道的后验 LLR $\lambda_n$ 的内禀信息为：

$$
\lambda_n^{\text{int}} = \log\left(\frac{p(r_n|c_n = 1)}{p(r_n|c_n = 0)}\right) = \log\left(\frac{1 - \alpha}{\alpha}\right)
$$

公式 (4.43) 可通过考虑正则 LDPC 码 $(j, k)$ 的 Tanner 图进一步简化。比特节点 $n$ 连接 $j$ 个校验节点（编号 1 到 $j$），每个校验节点又连接其他 $k-1$ 个比特节点。

## 4.4.2 LDPC 码的环

Tanner 图中的环 (cycle) 会影响 BP 算法的收敛性。长度为 4 的短环会降低解码性能，因为环上的消息会自我增强导致错误收敛。设计 $\mathbf{H}$ 矩阵时应避免短环，通常要求最小环长至少为 6。

## 4.4.3 数据位 LLR 的计算

根据公式 (4.47)，信道 LLR 由接收信号和信道可靠性决定。对于 AWGN 信道，$\lambda_n^{\text{ch}} = 2r_n/\sigma^2$。对于 BSC 信道，$\lambda_n^{\text{ch}} = \log((1-\alpha)/\alpha)$。

## 4.4.4 消息传递算法

消息传递算法 (MP: Message Passing) 是 LDPC 码的标准解码算法：

# 消息传递算法 (MP)

1. **初始化**：每个比特节点 $v_n$ 的初始消息为信道 LLR $\lambda_n^{\text{ch}}$
2. **校验节点更新**（比特→校验方向）：对每个校验节点 $c_m$，计算
   $$ \lambda_{c_m \to v_n} = 2\tanh^{-1}\left(\prod_{v_{n'} \in N(c_m)\setminus\{v_n\}} \tanh(\lambda_{v_{n'} \to c_m}/2)\right) $$
3. **比特节点更新**（校验→比特方向）：对每个比特节点 $v_n$，计算
   $$ \lambda_{v_n \to c_m} = \lambda_n^{\text{ch}} + \sum_{c_{m'} \in N(v_n)\setminus\{c_m\}} \lambda_{c_{m'} \to v_n} $$
4. **硬判决**：计算总 LLR $\lambda_n^{\text{total}} = \lambda_n^{\text{ch}} + \sum_{c_m \in N(v_n)} \lambda_{c_m \to v_n}$，$\hat{c}_n = 1$ 若 $\lambda_n^{\text{total}} \geq 0$，否则 $\hat{c}_n = 0$
5. **校验**：若 $\mathbf{H} \hat{\mathbf{c}}^{\text{T}} = \mathbf{0}$ 或达到最大迭代次数，停止；否则返回步骤 2

## 4.5 校验矩阵的构造

### 4.5.1 正则 LDPC 码

随机构造法：随机生成具有固定列重 $j$ 和行重 $k$ 的 $M \times N$ 稀疏矩阵，通过消除 4 环优化性能。

### 4.5.2 阵列 LDPC 码

阵列 LDPC 码基于有限域构造，具有准循环结构，便于硬件实现。

### 4.5.3 改进的阵列 LDPC 码

在阵列码基础上优化列重分布和环长分布，进一步提高性能。

### 4.5.4 说明

实际系统中常采用 QC-LDPC (Quasi-Cyclic LDPC) 码，兼顾性能和实现复杂度。5G NR、DVB-S2、Wi-Fi (802.11n/ac/ax) 等标准均采用 QC-LDPC 码。

# 4.6 实验结果

## 4.6.1 AWGN 信道

在不同 $E_c/N_0$ 条件下测试 LDPC 码的 BER 性能。结果表明，非正则 LDPC 码的性能优于正则 LDPC 码，且随迭代次数增加性能提升。在足够高的 $E_c/N_0$ 下，LDPC 码的性能接近香农极限。

## 4.6.2 迭代信道

在迭代解码系统中，LDPC 码与软检测器协同工作，通过迭代交换软信息提升整体性能。对于硬盘驱动器信道模型，LDPC 码配合迭代检测可获得接近信道容量的性能。

# 4.7 本章小结

LDPC 码是一类具有稀疏校验矩阵的线性分组码，采用消息传递算法进行解码。正则和非正则 LDPC 码各有特点：正则码结构简单，非正则码性能更优。LDPC 码的性能接近香农极限，已广泛应用于现代通信和存储系统。

# 4.8 本章习题

1. 推导 LDPC 码校验节点更新的双曲正切规则公式。
2. 说明 Tanner 图中环对 BP 解码性能的影响。
3. 对比正则与非正则 LDPC 码的优缺点。
4. 推导公式 (4.47) 中 LLR 分解为内禀和外部信息的过程。
5. 设计一个 $(3, 6)$ 正则 LDPC 码的校验矩阵，$N=12$。
