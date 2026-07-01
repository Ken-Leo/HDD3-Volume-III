# 第四章  LDPC 码

低密度奇偶校验码 (LDPC: low-density parity-check)，简称"LDPC 码"[17]，被公认为是目前最好的纠错码 (ECC: error-correction code) [2, 5]，因为其性能比其他 ECC 码更接近香农极限 (Shannon limit) [25]。目前，LDPC 码已被应用于多种应用中，包括硬盘驱动器。

由于 LDPC 码属于线性分组码 (linear block code) 的一种，因此本章首先介绍线性分组码的基础知识，然后重点讲解 LDPC 码的工作原理，使读者理解 LDPC 码的编码和解码步骤，同时展示当前硬盘驱动器信号处理系统中使用的 Turbo 均衡器（即迭代解码）的性能，这是软检测器和 LDPC 解码器协同工作的结果。

# 4.1 引言

本节将介绍线性分组码的工作原理，并解释线性分组码的编码和解码，为后续学习 LDPC 码奠定基础。

# 4.1.1 线性分组码

(N, K) 线性分组码是一种将 K 位信息位 (message bit) 转换为 N 位码字 (codeword) 的信道码。设 $\mathbf{m} = [m_1, m_2, \dots, m_K]$ 是被编码的信息位向量，得到码字 $\mathbf{c} = [c_1, c_2, \dots, c_N]$，如图 4.1 所示。增加的 $N - K$ 位称为"校验位 (parity bit)"，用向量 $\mathbf{p} = [p_1, p_2, \dots, p_{N-K}]$ 表示。校验位帮助接收端能够检测错误，如果校验位数量足够多，还可以纠正数据的错误 (error correction)。

$$
\begin{array}{c} \text{codeword} \\ \left[ c_1, c_2, c_3, \dots, c_N \right] = \boxed{ \begin{array}{c c} \text{message bits} & \text{parity bits} \\ \left[ m_1, m_2, m_3, \dots, m_K \right] & \left[ p_1, p_2, \dots, p_{N-K} \right] \end{array} } \\ \xleftarrow {} K \text{ 位 } \xrightarrow {} N - K \text{ 位 } \xrightarrow {} \end{array}
$$

图 4.1 (N, K) 线性分组码的结构

线性分组码每次对一个数据块进行编码和解码。数据块的大小取决于各应用的特点。信息位数与码字位数的比率称为"码率 (code rate)" $R$，定义为

$$
R = \frac{K}{N} \tag{4.1}
$$

其中 $0 < R \leq 1$。对于硬盘驱动器，需要码率接近 1 的码，以减少存储介质中用于存储校验位的空间浪费 [43]。

# 4.1.2 生成矩阵

考虑大小为 $1 \times K$ 的信息位向量 $\mathbf{m} = [m_1, m_2, \dots, m_K]$。(N, K) 线性分组码是通过将信息位 $\mathbf{m}$ 乘以大小为 $K \times N$ 的生成矩阵 $\mathbf{G}$（元素为 0 或 1）来生成的，其形式为 [2]

$$
\mathbf{G}_{K \times N} = [\mathbf{I}_{K \times K} \mid \mathbf{P}_{K \times (N-K)}] = \begin{bmatrix} 1 & 0 & \dots & 0 & p_{1,1} & p_{1,2} & \dots & p_{1,(N-K)} \\ 0 & 1 & \dots & 0 & p_{2,1} & p_{2,2} & \dots & p_{2,(N-K)} \\ \vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & 1 & p_{K,1} & p_{K,2} & \dots & p_{K,(N-K)} \end{bmatrix} \tag{4.2}
$$

其中 $\mathbf{I}$ 是大小为 $K \times K$ 的单位矩阵，$\mathbf{P}$ 是大小为 $K \times (N-K)$ 的校验矩阵，对应于码字中的校验位。结果得到大小为 $1 \times N$ 的码字 $\mathbf{c} = [c_1, c_2, \dots, c_N]$，即

$$
\mathbf{c} = \mathbf{m} \mathbf{G} = \begin{bmatrix} m_1 & m_2 & \dots & m_K & p_1 & p_2 & \dots & p_{N-K} \end{bmatrix} \tag{4.3}
$$

方程 (4.3) 显示信息位 $\mathbf{m}$ 出现在码字 $\mathbf{c}$ 中，这种码称为"系统码 (systematic code)" [2]。

**示例 4.1** 当给出如下生成矩阵 $\mathbf{G}$ 时，请对数据 $\mathbf{m} = [101]$ 和 $\mathbf{m} = [110]$ 进行编码。

$$
\mathbf{G} = \begin{bmatrix} 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 1 & 0 & 0 & 1 & 1 \\ 0 & 0 & 1 & 1 & 0 & 1 \end{bmatrix} \tag{4.4}
$$

**解** 该生成矩阵 $\mathbf{G}$ 用于每次对 3 位数据位进行编码，即 $\mathbf{m} = [m_1 \, m_2 \, m_3]$。因此，用矩阵 $\mathbf{G}$ 编码得到的码字为

$$
\begin{aligned}
\mathbf{c} &= \mathbf{m} \mathbf{G} = \begin{bmatrix} m_1 & m_2 & m_3 \end{bmatrix} \begin{bmatrix} 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 1 & 0 & 0 & 1 & 1 \\ 0 & 0 & 1 & 1 & 0 & 1 \end{bmatrix} \\
&= \begin{bmatrix} m_1 & m_2 & m_3 & m_1 \oplus m_3 & m_1 \oplus m_2 & m_2 \oplus m_3 \end{bmatrix}
\end{aligned}
$$

其中 $\oplus$ 是模二加法算子 (modulo-2 addition) 或 XOR (exclusive OR)。因此，如果 $\mathbf{m} = [101]$，则 $\mathbf{c} = [101011]$；如果 $\mathbf{m} = [110]$，则 $\mathbf{c} = [110101]$。

# 4.1.3 校验矩阵

(N, K) 线性分组码也可以用大小为 $(N-K) \times N$ 的校验矩阵 (parity-check matrix) $\mathbf{H}$ 来定义，必须满足以下关系

$$
\mathbf{H} \mathbf{G}^\mathrm{T} = \mathbf{0} \tag{4.5}
$$

因此，对于任何码字，有

$$
\mathbf{H} \mathbf{c}^\mathrm{T} = \mathbf{H} \mathbf{G}^\mathrm{T} \mathbf{m}^\mathrm{T} = \mathbf{0} \tag{4.6}
$$

此外，$\mathbf{H}$ 矩阵的每一行就是一条校验方程 (parity-check equation)，它决定了码字中数据位 $c_i$ ($i = 1, 2, \dots, N$) 之间的关系。通常，如果生成矩阵 $\mathbf{G}$ 如方程 (4.2) 所示是系统形式的，则校验矩阵为

$$
\mathbf{H}_{(N-K) \times N} = [\mathbf{P}^\mathrm{T} \mid \mathbf{I}_{(N-K) \times (N-K)}] \tag{4.7}
$$

其中 $(\cdot)^\mathrm{T}$ 是矩阵转置 (transpose matrix) 符号。例如，方程 (4.4) 中的生成矩阵 $\mathbf{G}$ 可以转换为 $\mathbf{H}$ 矩阵

$$
\mathbf{H} = \begin{bmatrix} 1 & 0 & 1 & 1 & 0 & 0 \\ 1 & 1 & 0 & 0 & 1 & 0 \\ 0 & 1 & 1 & 0 & 0 & 1 \end{bmatrix} \tag{4.8}
$$

# 4.1.4 码的最小距离

线性分组码的性能通过码字的汉明重量 (Hamming weight) 来衡量，定义为

$$
w_H(\mathbf{c}) = \text{码字 } \mathbf{c} \text{ 中值为 1 的位数} \tag{4.9}
$$

例如，如果 $\mathbf{c} = 100100$，则 $w_H([100100]) = 2$。$\mathbf{c}_1$ 和 $\mathbf{c}_2$ 之间的汉明距离 (Hamming distance) 定义为

$$
d_H(\mathbf{c}_1, \mathbf{c}_2) = w_H(\mathbf{c}_1 - \mathbf{c}_2) = \sum_{i=0}^{N-1} (c_{1,i} \neq c_{2,i}) \tag{4.10}
$$

例如，如果 $\mathbf{c}_1 = 110011$ 且 $\mathbf{c}_2 = 000111$，则汉明距离 $d_H(\mathbf{c}_1, \mathbf{c}_2) = 3$。

设码 $\mathcal{C}$ 共有 $2^K$ 个码字，码字之间的最小汉明距离通常称为码的最小距离 (minimum distance) 或 $d_{\min}$，定义为

$$
d_{\min} = \min_{i \neq j} \{d_H(\mathbf{c}_i, \mathbf{c}_j)\} \tag{4.11}
$$

其中 $\{i, j\} = 0, 1, \dots, 2^K - 1$。因此，当知道最小距离 $d_{\min}$ 后，就可以知道该线性分组码纠正 $t$ 位错误的能力

$$
t = \left\lfloor \frac{d_{\min} - 1}{2} \right\rfloor \tag{4.12}
$$

以及检测 $e$ 位错误的能力

$$
e = d_{\min} - 1 \tag{4.13}
$$

此外，码的最小距离 $d_{\min}$ 也可以直接从生成矩阵 $\mathbf{G}$ 和校验矩阵 $\mathbf{H}$ 求得如下：
- 码的最小距离等于 $\mathbf{G}$ 矩阵行的最小汉明重量
- $\mathbf{H}$ 矩阵中模二相加结果为零的最小列数

# 4.1.5 线性分组码的解码

在实际应用中，线性分组码的解码方法是"伴随式解码 (syndrome decoding)" [2]。伴随式向量 $\mathbf{s}$ 定义为

$$
\mathbf{s} = \mathbf{H} \mathbf{r}^\mathrm{T} \tag{4.14}
$$

其中 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e} = [r_0, r_1, \dots, r_{N-1}]$ 是需要解码的数据向量，$\mathbf{c}$ 是码字向量，$\mathbf{e} = [e_0, e_1, \dots, e_{N-1}]$ 是错误向量，$e_i \in \{0, 1\}$，$e_i = 1$ 表示码字的第 $i$ 位有错误（$e_i = 0$ 表示码字的第 $i$ 位无错误）。将 $\mathbf{r} = \mathbf{c} \oplus \mathbf{e}$ 代入方程 (4.14) 得到

$$
\begin{aligned}
\mathbf{s} &= \mathbf{H} (\mathbf{c} \oplus \mathbf{e})^\mathrm{T} = \mathbf{H} \mathbf{c}^\mathrm{T} \oplus \mathbf{H} \mathbf{e}^\mathrm{T} \\
&= \mathbf{H} \mathbf{e}^\mathrm{T} \tag{4.15}
\end{aligned}
$$

即伴随式仅取决于错误向量 $\mathbf{e}$。因此，无错误的数据序列（即 $\mathbf{r} = \mathbf{c}$）的伴随式始终为零。

通常，线性分组码的解码依赖于查找表 (look-up table) [2]，该表显示了伴随式与方程 (4.15) 中错误向量 $\mathbf{e}$ 之间的对应关系。因此，当接收端需要解码数据序列 $\mathbf{r}$ 时，先根据方程 (4.14) 计算伴随式，然后从查找表中找到对应于该伴随式的错误向量 $\mathbf{e}$。得到所需的错误向量 $\mathbf{e}$ 后，即可根据下式解码数据序列 $\mathbf{r}$

$$
\hat{\mathbf{c}} = \mathbf{r} \oplus \mathbf{e} \tag{4.16}
$$

# 4.2 LDPC 码基础

LDPC 码是一种线性分组码，由校验矩阵 $\mathbf{H}$ 定义，该矩阵中的 1 的数量与矩阵大小相比非常少，以获得较大的码的最小距离 ($d_{\min}$)。LDPC 码由 Gallager [17] 于 1960 年在美国麻省理工学院 (MIT) 提出。然而，最初 LDPC 码并未受到应有的关注，原因是计算能力的限制。随后，在 1981 年，Tanner [44] 提出了 Tanner 图 (Tanner graph) 来表示数据编码中产生的关系，并可用来辅助简化数据解码。在 1990 年，Mackey 和 Neal [45] 发现 LDPC 码的性能比 Turbo 码 [3] 更接近香农极限，这使 LDPC 码重新受到广泛关注，并被应用于多种应用中，包括硬盘驱动器。

LDPC 码是一种由大小为 $M \times N$ 的稀疏矩阵 (sparse matrix) [17] $\mathbf{H}$ 定义的校验码。码字 $\mathbf{c}$ 的长度为 $N$ 位，所有码字必须满足方程 (4.6) 中的 $M$ 个校验方程。通常，LDPC 码分为两种主要类型：

- **正则 LDPC 码 (regular LDPC code)**：$\mathbf{H}$ 矩阵中 1 的分布是固定的，类似于 Gallager [17] 的 LDPC 码——即 $\mathbf{H}$ 矩阵的每行含有相同数量的 1，每列也含有相同数量的 1。
- **非正则 LDPC 码 (irregular LDPC code)** [46]：1 的分布不是固定的，通常性能优于正则 LDPC 码。

为便于解释 LDPC 码的工作原理，这里仅考虑 $\mathbf{H}$ 矩阵的所有行线性无关的情况，则用于编码的信息位长度为 $K = N - M$ 位 [4, 17]。

# 4.2.1 正则 LDPC 码

$(j, k)$ 正则 LDPC 码是指由大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 定义的 LDPC 码，每列有 $j$ 个 1，每行有 $k$ 个 1，其中 $j < k$ 且 $\{j, k\} \ll N$。这意味着每个校验方程涉及 $k$ 个数据位，每个数据位关联 $j$ 个校验方程。因此，$\mathbf{H}$ 矩阵共有 $Mk = Nj$ 个 1。如果假设 $\mathbf{H}$ 矩阵的所有行线性无关，则正则 LDPC 码的码率为

$$
R = 1 - \frac{M}{N} = 1 - \frac{j}{k} \tag{4.17}
$$

其中 $j < k$，因为 $R \leq 1$。

选择正则 LDPC $(j, k)$ 码的参数 $(M, N, j, k)$ 时，需要利用关系 $Mk = Nj$。因此，必须选择使

$$
M = \frac{Nj}{k} \tag{4.18}
$$

为整数的参数 $N$、$j$ 和 $k$。例如，$(3, 4)$ 正则 LDPC 码只能用于 $N = 1000$ 或 $1004$ 的系统，而不能用于 $N = 1002$ 的系统。又如，$(2, 4)$ 正则 LDPC 码的校验矩阵 $\mathbf{H}$ 为

$$
\mathbf{H}_{5 \times 10} = \begin{bmatrix} 1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 1 & 1 & 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 0 & 1 \\ 0 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 1 \end{bmatrix} \tag{4.19}
$$

可得 $M = 5$，$N = 10$，满足方程 (4.18)。因此，该 LDPC 码用于编码 $10 - 5 = 5$ 位信息位，得到 10 位的码字。

方程 (4.19) 中的校验矩阵 $\mathbf{H}$ 揭示了校验方程与数据位之间的关系。$\mathbf{H}$ 矩阵的每一行称为"校验节点 (check node)"，每一列称为"变量节点 (bit node)"。因此，每个校验节点的校验方程如下：

- 校验节点 1：$c_1 + c_2 + c_3 + c_4 = 0$ \hfill (4.20)
- 校验节点 2：$c_1 + c_5 + c_6 + c_7 = 0$ \hfill (4.21)
- 校验节点 3：$c_2 + c_5 + c_8 + c_9 = 0$ \hfill (4.22)
- 校验节点 4：$c_3 + c_6 + c_8 + c_{10} = 0$ \hfill (4.23)
- 校验节点 5：$c_4 + c_7 + c_9 + c_{10} = 0$ \hfill (4.24)

校验码可以用 Tanner 图 [44, 50] 来表示，即用大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 表示。Tanner 图有 $N$ 个变量节点（每个节点对应一位）和 $M$ 个校验节点（每个节点对应一个校验方程）。这里用圆圈 ○ 表示变量节点，用方块 □ 表示校验节点。当 $h_{m,n} = 1$ 时，第 $m$ 个校验节点与第 $n$ 个变量节点之间存在一条边 (edge)。Tanner 图也可称为"二分图 (bipartite graph)"，因为图中只有两类节点（变量节点和校验节点），且同类节点之间没有边相连。图 4.2 显示了 $(j, k) = (2, 4)$ 正则 LDPC 码的 Tanner 图，其校验矩阵 $\mathbf{H}$ 如方程 (4.19) 所示。每个变量节点有 2 条边（对应 $j = 2$），每个校验节点有 4 条边（对应 $k = 4$）。此外，Tanner 图与方程 (4.20)-(4.24) 中的所有校验方程一致。

![](images/chapter_4/3e9a9bd5249923ddfea04710590385de7751938de6cd5cd715224ab7a31a4c07.jpg)

图 4.2 正则 (2, 4) LDPC 码的 Tanner 图（$\mathbf{H}$ 矩阵如方程 (4.19) 所示）

# 4.2.2 非正则 LDPC 码

非正则 LDPC 码由 Richardson 于 2001 年 [46] 提出。其大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 中 1 的分布是不固定的，即每行和每列中 1 的数量不必相等。

在实际应用中，非正则 LDPC 码由度分布多项式 (degree distribution polynomial) 定义，该多项式说明了每个节点的边的数量。变量节点的度分布多项式为 $\rho(x) = \sum_i \rho_i x^i$，其中 $\rho_i$ 是度为 $i$ 的变量节点的数量。类似地，校验节点的度分布多项式为 $\xi(x) = \sum_i \xi_i x^i$，其中 $\xi_i$ 是度为 $i$ 的校验节点的数量。

此外，LDPC 码作为校验节点和变量节点度分布函数的性能，可以通过密度演化理论 (density evolution) [48] 来预测，该理论追踪在校验节点和变量节点之间传递的消息的概率密度。通常，如果系统工作在足够高的 SNR 水平，随着 LDPC 解码器内部解码迭代次数的增加，密度的均值趋向于无穷大，这意味着解码器对正确解码数据具有很高的信心。相反，如果系统在低 SNR 水平下工作，密度的均值收敛到某个常数值，这意味着 LDPC 解码器在解码数据时存在缺陷。因此，作为 LDPC 码性能分界线（好与坏）的 SNR 值称为"阈值 (threshold)"。非正则 LDPC 码的设计目标就是使该阈值尽可能接近香农容量极限 (Shannon capacity) [25]（比正则 LDPC 码更接近）[49]。

![](images/chapter_4/d8f11573da6620c20ccb2545394dce26c80f1a108d959fdff6b95825026789d6.jpg)

# 4.2.3 双曲正切规则

设 $\mathbf{c} = [c_1, c_2, \dots, c_n]$ 是 $n$ 位数据位向量，其中 $c_i \in \{0, 1\}$。定义奇偶校验函数 (parity function) $\Phi(\mathbf{c}) \in \{0, 1\}$ 如下

$$
\Phi(\mathbf{c}) = c_1 \oplus c_2 \oplus \dots \oplus c_n \tag{4.27}
$$

其中 $\oplus$ 是模二加法算子。当向量 $\mathbf{c}$ 中 1 的总数为偶数时，$\Phi(\mathbf{c}) = 0$ 或偶校验 (even parity)；当向量 $\mathbf{c}$ 中 1 的总数为奇数时，$\Phi(\mathbf{c}) = 1$ 或奇校验 (odd parity)。此外，定义奇偶校验函数 $\Phi(\mathbf{c})$ 的先验 LLR (a priori LLR) 为

$$
\lambda_{\Phi(\mathbf{c})} = \log\left(\frac{\Pr[\Phi(\mathbf{c}) = 1]}{\Pr[\Phi(\mathbf{c}) = 0]}\right) \tag{4.28}
$$

可得

$$
\Phi(\mathbf{c}) = \begin{cases} 1, & \text{if } \lambda_{\Phi(\mathbf{c})} \geq 0 \\ 0, & \text{if } \lambda_{\Phi(\mathbf{c})} < 0 \end{cases} \tag{4.29}
$$

因此，假设所有数据位相互独立，则 $\lambda_{\Phi(\mathbf{c})}$ 满足双曲正切规则 (tanh rule) 如下 [51, 52]

$$
\tanh\left(\frac{-\lambda_{\Phi(\mathbf{c})}}{2}\right) = \prod_{i=1}^n \tanh\left(\frac{-\lambda_i}{2}\right) \tag{4.30}
$$

（见附录 B 的解释）其中 $\lambda_i = \log(\Pr[c_i = 1] / \Pr[c_i = 0])$。然后，解方程 (4.30) 得到

$$
\lambda_{\Phi(\mathbf{c})} = -2 \tanh^{-1}\left\{\prod_{i=1}^n \tanh\left(\frac{-\lambda_i}{2}\right)\right\} \tag{4.31}
$$

或者写成另一种形式

$$
\lambda_{\Phi(\mathbf{c})} = -\prod_{i=1}^n \operatorname{sign}(-\lambda_i) \times f\left(\sum_{i=1}^n f(|\lambda_i|)\right) \tag{4.32}
$$

（见附录 C 的解释）其中

$$
f(x) = \log\left(\frac{e^x + 1}{e^x - 1}\right) = -\log\left(\tanh\left(\frac{x}{2}\right)\right) \tag{4.33}
$$

![](images/chapter_4/b0c4c501d519010e814ef805f7df4301402a259756229b5be4821e5a53a5edbc.jpg)

# 4.3 LDPC 编码

考虑系统码 [2]，它对 $K$ 位信息位 $\mathbf{m} = [m_1, m_2, \dots, m_K]$ 进行编码，得到 $N$ 位的码字 $\mathbf{c} = [c_1, c_2, \dots, c_N]$，其结构如方程 (4.3) 所示

$$
\mathbf{c} = [\mathbf{m} \mid \mathbf{p}] = [m_1 \, m_2 \, \dots \, m_K \, p_1 \, p_2 \, \dots \, p_{N-K}] \tag{4.38}
$$

其中 $\mathbf{p} = [p_1, p_2, \dots, p_{N-K}]$ 是 $N-K$ 位的校验位。因此，使用系统码编码时需要做的就是求校验位 $\mathbf{p}$，然后将 $\mathbf{p}$ 与信息位 $\mathbf{m}$ 按方程 (4.38) 连接，即得到所需的码字 $\mathbf{c}$。

通常，LDPC 码由大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 定义。因此，本节将展示如何从矩阵 $\mathbf{H}$ 求校验位 $\mathbf{p}$。在得到所需的 $\mathbf{H}$ 矩阵后，利用方程 (4.6) 的关系求 $\mathbf{p}$，即

$$
\mathbf{H} \mathbf{c}^\mathrm{T} = \mathbf{0}_{M \times 1} \tag{4.39}
$$

其中 $\mathbf{0}_{M \times 1}$ 是大小为 $M \times 1$ 的零向量。将矩阵 $\mathbf{H}$ 整理为

$$
\mathbf{H} = [\mathbf{H}_1 \mid \mathbf{H}_2] \tag{4.40}
$$

其中 $\mathbf{H}_1$ 大小为 $M \times K$，$\mathbf{H}_2$ 大小为 $M \times (N-K)$。将方程 (4.38) 和 (4.40) 代入方程 (4.39) 得到

$$
[\mathbf{H}_1 \; \mathbf{H}_2] \begin{bmatrix} \mathbf{m}^\mathrm{T} \\ \mathbf{p}^\mathrm{T} \end{bmatrix} = \mathbf{0}
$$

$$
\mathbf{H}_1 \mathbf{m}^\mathrm{T} + \mathbf{H}_2 \mathbf{p}^\mathrm{T} = \mathbf{0}
$$

$$
\mathbf{p}^\mathrm{T} = (\mathbf{H}_2)^{-1} \mathbf{H}_1 \mathbf{m}^\mathrm{T} \tag{4.41}
$$

由于 $\mathbf{H}_2$ 是方阵（因为 $M = N-K$），因此可以求逆。

**示例 4.3** 从示例 4.1 出发，请使用校验矩阵 $\mathbf{H}$ 对数据 $\mathbf{m} = [101]$ 和 $\mathbf{m} = [110]$ 进行编码，该 $\mathbf{H}$ 矩阵对应于方程 (4.4) 中的生成矩阵 $\mathbf{G}$。

**解** 利用方程 (4.7)，可以从 $\mathbf{G}$ 矩阵求得 $\mathbf{H}$ 矩阵

$$
\mathbf{H} = [\mathbf{H}_1 \; \mathbf{H}_2] = \begin{bmatrix} 1 & 0 & 1 & 1 & 0 & 0 \\ 1 & 1 & 0 & 0 & 1 & 0 \\ 0 & 1 & 1 & 0 & 0 & 1 \end{bmatrix}
$$

因此，对于 $\mathbf{m} = [101]$，由方程 (4.41) 求得校验位

$$
\mathbf{p}^\mathrm{T} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}^{-1} \begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix} \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \\ 1 \end{bmatrix}
$$

因此，$\mathbf{c} = [\mathbf{m} \; \mathbf{p}] = [101011]$，这与示例 4.1 的结果一致。

类似地，对于 $\mathbf{m} = [110]$，校验位为

$$
\mathbf{p}^\mathrm{T} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}^{-1} \begin{bmatrix} 1 & 0 & 1 \\ 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix} \begin{bmatrix} 1 \\ 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 1 \end{bmatrix}
$$

因此，$\mathbf{c} = [\mathbf{m} \; \mathbf{p}] = [110101]$，这也与示例 4.1 的结果一致。

示例 4.3 表明，对于系统码形式的 LDPC 码的编码，可以通过方程 (4.41) 求校验位 $\mathbf{p}$，然后代入方程 (4.38) 即得到所需的码字 $\mathbf{c}$。方程 (4.39) 用于验证所得码字的正确性。

# 4.4 LDPC 解码

LDPC 编码使得每个数据位之间根据校验矩阵 $\mathbf{H}$ 的结构相互关联。因此，LDPC 解码利用这些关联来辅助数据解码。通常，LDPC 码通过消息传递算法 (MPA: message passing algorithm) 进行解码，这里简称为"MP 算法"[4, 17]。该算法首先从矩阵 $\mathbf{H}$ 构造校验方程，然后将其表示为 Tanner 图，再根据 MP 算法的步骤解码数据位。

# 4.4.1 LDPC 解码基础

考虑图 4.5 中的信道。$K$ 位输入数据序列 $m_n \in \{0, 1\}$ 用 $(j, k)$ 正则 LDPC 码编码，得到 $N$ 位的码字 $c_n \in \{0, 1\}$，然后送入映射器 (mapper) 转换为数据序列 $s_n \in \{\pm 1\}$。因此，接收端接收到的信号为

$$
r_n = s_n + w_n \tag{4.42}
$$

![](images/chapter_4/bcab1aeadbc7a472acf552a87d6d978783f9d0dad1cefa76c337d254041f6799.jpg)

# 4.4.2 LDPC 码的环

环 (cycle) 指图中起点和终点为同一变量节点的路径。环的长度 (cycle length) 等于形成该环的边的总数。由于 Tanner 图是二分图 (bipartite graph)，因此最小环长度为 4，如图 4.8 中虚线所示。然而，如果图中没有虚线，则该图无环 (cycle-free)，无环的图称为"树图 (tree diagram)"。此外，无环图具有以下有趣的性质：

1) 移除任何一条边都会形成两个分离的子图 (subgraph)
2) 从一个变量节点到另一个变量节点有且仅有一条唯一路径 (unique path)
3) 所有连接到变量节点 $c_n$ 的变量节点必须通过且仅通过一条与 $c_n$ 相连的边
4) 如果变量节点 $c_j$ 和 $c_k$ 通过不同的边连接到变量节点 $c_n$，则在不考虑第 $n$ 个数据位的情况下，变量节点 $c_j$ 和 $c_k$ 是条件独立的 (conditionally independent)，即

$$
\Pr[c_j; c_k \mid \mathbf{r}_{i \neq n}] = \Pr[c_j \mid \mathbf{r}_{i \neq n}] \times \Pr[c_k \mid \mathbf{r}_{i \neq n}] \tag{4.50}
$$

此外，LDPC 码中的环也可以从大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 来考虑。即矩阵 $\mathbf{H}$ 中存在长度为 4 的环，当且仅当 $\mathbf{H}$ 矩阵中 1 的位置具有以下闭环 (closed loop) 关系

$$
[h_{i,j}, h_{i,b}, h_{a,b}, h_{a,j}] \tag{4.51}
$$

其中 $h_{r,c}$ 是 $\mathbf{H}$ 矩阵中第 $r$ 行、第 $c$ 列中 1 的位置，$\{i, a\} \in \{1, 2, \dots, M\}$，$\{j, b\} \in \{1, 2, \dots, N\}$。或者说，$\mathbf{H}$ 矩阵中长度为 4 的环是 1 的闭环，涉及两行和两列。例如，考虑 $(2, 4)$ 正则 LDPC 码，其校验矩阵 $\mathbf{H}$ 为

# 4.4.3 数据位 LLR 的计算

考虑 $(j, k)$ 正则 LDPC 码的大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$，该矩阵表明有 $j$ 个校验方程约束。从方程 (4.49) 可知，数据位 $c_n$ 等于数据向量 $\mathbf{c}(i)$ 的奇偶校验值，即 $c_n = \Phi(\mathbf{c}(i))$，$i = \{1, 2, \dots, j\}$。因此，方程 (4.43) 可以重新写为

$$
\lambda_n = \frac{2}{\sigma^2} r_n + \log\left(\frac{\Pr[\Phi(\mathbf{c}(i)) = 1 \text{ for } i = 1, 2, \dots, j \mid \mathbf{r}_{i \neq n}]}{\Pr[\Phi(\mathbf{c}(i)) = 0 \text{ for } i = 1, 2, \dots, j \mid \mathbf{r}_{i \neq n}]}\right) \tag{4.53}
$$

假设矩阵 $\mathbf{H}$ 无环，则在给定 $\mathbf{r}_{i \neq n}$（即接收端接收到的除第 $n$ 个数据之外的所有数据）的条件下，$\mathbf{c}(1), \mathbf{c}(2), \dots, \mathbf{c}(j)$ 是条件独立的，且 $\mathbf{c}(i)$ 内部的元素也是条件独立的。因此，方程 (4.53) 可以简化为

$$
\begin{aligned}
\lambda_n &= \frac{2}{\sigma^2} r_n + \log\left(\frac{\prod_{i=1}^j \Pr[\Phi(\mathbf{c}(i)) = 1 \mid \mathbf{r}_{i \neq n}]}{\prod_{i=1}^j \Pr[\Phi(\mathbf{c}(i)) = 0 \mid \mathbf{r}_{i \neq n}]}\right) \\
&= \frac{2}{\sigma^2} r_n + \sum_{i=1}^j \log\left(\frac{\Pr[\Phi(\mathbf{c}(i)) = 1 \mid \mathbf{r}_{i \neq n}]}{\Pr[\Phi(\mathbf{c}(i)) = 0 \mid \mathbf{r}_{i \neq n}]}\right) \\
&= \frac{2}{\sigma^2} r_n + \sum_{i=1}^j \lambda_{\Phi(\mathbf{c}(i))} \tag{4.54}
\end{aligned}
$$

$\lambda_{\Phi(\mathbf{c}(i))}$ 是奇偶校验值 $\Phi(\mathbf{c}(i))$ 的 LLR。由于每个数据位是条件独立的，每个 $\lambda_{\Phi(\mathbf{c}(i))}$ 满足方程 (4.31) 的双曲正切规则。因此，设

$$
\lambda_{i,l} = \log\left(\frac{\Pr[c_{i,l} = 1 \mid \mathbf{r}_{i \neq n}]}{\Pr[c_{i,l} = 0 \mid \mathbf{r}_{i \neq n}]}\right) \tag{4.55}
$$

其中 $c_{i,l}$ 是向量 $\mathbf{c}(i)$ 中的第 $l$ 个元素，$l = \{2, 3, \dots, k\}$。将方程 (4.31) 代入方程 (4.54)，得到

$$
\lambda_n = \frac{2}{\sigma^2} r_n - 2 \sum_{i=1}^j \tanh^{-1}\left\{\prod_{l=2}^k \tanh\left(\frac{-\lambda_{i,l}}{2}\right)\right\} \tag{4.56}
$$

或者写成另一种形式（比较方程 (4.31) 和 (4.32)）

$$
\lambda_n = \frac{2}{\sigma^2} r_n - \sum_{i=1}^j \left\{\prod_{l=2}^k \operatorname{sign}(-\lambda_{i,l}) \times f\left(\sum_{l=2}^k f(|\lambda_{i,l}|)\right)\right\} \tag{4.57}
$$

其中 $f(x) = -\log(\tanh(x/2))$，如方程 (4.33) 所定义。此外，如果需要降低解码算法的复杂度，可以利用方程 (4.36) 来近似计算方程 (4.57)，得到

$$
\lambda_n \approx \frac{2}{\sigma^2} r_n - \sum_{i=1}^j \left\{\prod_{l=2}^k \operatorname{sign}(-\lambda_{i,l}) \times \min_{l = \{2, \dots, k\}} |\lambda_{i,l}|\right\} \tag{4.58}
$$

从图 4.8 可以解释方程 (4.54) 的意义如下：变量节点 $c_{i,l}$ 将消息 $\lambda_{i,l}$ 发送到第 $i$ 个校验节点，第 $i$ 个校验节点收集来自 $\mathbf{c}(i)$ 中其他变量节点（不包括变量节点 $c_n$）的 $k-1$ 条消息，计算第 $i$ 个校验节点奇偶校验值的后验 LLR $\lambda_{\Phi(\mathbf{c}(i))}$，然后将计算结果发送到第 $n$ 个变量节点。最后，第 $n$ 个变量节点根据方程 (4.54) 计算 $\lambda_n$，即 $(2/\sigma^2)r_n$ 与到达第 $n$ 个变量节点的所有消息之和。

图 4.9 显示了变量节点和校验节点的工作方式，其中 $f(x) = \tanh(-x/2)$。可以看出，变量节点的计算仅使用求和 (summation)，而校验节点的计算相对复杂，因为需要用到 $f(x)$ 函数。

# 4.4.4 消息传递算法

在同一校验方程中，$c_{i,l}$ 与 $c_n$ 通过同一个校验节点相关联。然而，当给定 $\{\mathbf{r}_{i \neq n}\}$ 时，$c_{i,l}$ 与 $c_n$ 相互独立。此外，如果剔除接收端接收到的第 $n$ 个数据 $r_n$，则通过变量节点 $c_n$ 的其他数据 $\{\mathbf{r}_{i \neq n}\}$ 也会被一并剔除。因此，剔除数据 $r_n$ 相当于切断所有连接到变量节点 $c_n$ 的边，从而形成 $j$ 个子图。由于所有子图互不相交，可以认为每个子图是独立的，只有数据 $c_{i,l}$ 被用于计算 $\lambda_{i,l}$。

消息传递算法（或称 MP 算法）是一种简单的数据解码技术，通过 Tanner 图中节点之间的路径传递消息。每个节点（变量节点和校验节点）作为独立的处理单元，接收通过所有边传入的消息，进行计算，然后将结果发送回这些边。此外，如果图中无环，MP 算法是一种递归算法，其输出收敛到真实的 A Posteriori LLR（如方程 (4.43) 所定义），只需 MP 算法内部经过有限次数的迭代。然而，大多数好的 LDPC 码在 Tanner 图中包含环。如果使用 MP 算法对这些码进行数据解码，得到的是次优的解码结果。总之，即使 LDPC 码存在环，使用 MP 算法进行数据解码仍然具有良好的性能且复杂度很低（与其他码相比）。

对于具有大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 的二进制 LDPC 码，使用 MP 算法的 LDPC 解码器（或称 MP 解码器）的工作流程可总结如下。设 $\mathcal{M}_n = \{m : h_{m,n} = 1\}$ 为所有连接到第 $n$ 个变量节点的校验节点的集合，$\mathcal{N}_m = \{n : h_{m,n} = 1\}$ 为所有连接到第 $m$ 个校验节点的变量节点的集合。对于 $(j, k)$ 正则 LDPC 码，$|\mathcal{M}_n| = j$ 对所有 $n$ 成立，$|\mathcal{N}_m| = k$ 对所有 $m$ 成立。设 $u_{m \to n}^{(l)}$ 为第 $l$ 次迭代时从第 $m$ 个校验节点发送到第 $n$ 个变量节点的消息，设 $\lambda_n^{(l)}$ 为第 $l$ 次迭代时第 $n$ 个数据位的后验 LLR。因此，MP 解码器的工作流程如图 4.11 所示。

**消息传递 (MP) 算法**

1. 设校验矩阵 $\mathbf{H}$ 大小为 $M \times N$（即 $M$ 个校验节点和 $N$ 个变量节点）

2. 初始化

$$
u_{m \to n}^{(0)} = 0 \quad \text{对所有 } m \in \{1, 2, \dots, M\} \text{ 和 } n \in \mathcal{N}_m
$$

$$
\lambda_n^{(0)} = (2 / \sigma^2) r_n \quad \text{对所有 } n \in \{1, 2, \dots, N\}
$$

3. 对于 $l = 1, 2, \dots, l_{\max}$（其中 $l_{\max}$ 为所需迭代次数）

**校验节点更新**

对 $m \in \{1, 2, \dots, M\}$ 和 $n \in \mathcal{N}_m$

$$
u_{m \to n}^{(l)} = -2 \tanh^{-1}\left\{\prod_{i \in \mathcal{N}_m \setminus \{n\}} \tanh\left(\frac{-\bigl(\lambda_i^{(l-1)} - u_{m \to i}^{(l-1)}\bigr)}{2}\right)\right\} \tag{4.59}
$$

（$m$ 循环结束）

**变量节点更新**

对 $n \in \{1, 2, \dots, N\}$

$$
\lambda_n^{(l)} = \frac{2}{\sigma^2} r_n + \sum_{m \in \mathcal{M}_n} u_{m \to n}^{(l)} \tag{4.60}
$$

（$n$ 循环结束）

（$l$ 循环结束）

4. 根据以下关系解码输入数据序列（仅适用于系统码）

$$
\hat{m}_i = \begin{cases} 1, & \text{if } \lambda_i^{(l_{\max})} \geq 0 \\ 0, & \text{if } \lambda_i^{(l_{\max})} < 0 \end{cases} \tag{4.61}
$$

对 $i \in \{1, 2, \dots, N - M\}$，其中 $N - M = K$ 是输入数据位的数量（见图 4.1）

![](images/chapter_4/67108415cb3d37f4f6fbf460de6499b7c7d2fb163b9f04dc9584493cdff84c71.jpg)
**图 4.11** LDPC 解码中 MP 算法的工作流程 [4, 17]

**示例 4.6** 考虑图 4.5 中的 AWGN 信道，输入数据位 $m \in \{0, 1\}$，使用的 LDPC 码的生成矩阵为 $\mathbf{G} = [1 \; 1 \; 1] = [1 \; | \; \mathbf{P}]$，其中 $\mathbf{P} = [1 \; 1]$ 是校验矩阵。

因此，接收端接收到的信号为

$$
\begin{bmatrix} r_1 \\ r_2 \\ r_3 \end{bmatrix} = s \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} + \begin{bmatrix} w_1 \\ w_2 \\ w_3 \end{bmatrix}
$$

其中 $s \in \{\pm 1\}$，$w_n \sim \mathcal{N}(0, \sigma^2)$ 是 AWGN 噪声。求后验 LLR $\boldsymbol{\lambda} = [\lambda_1, \lambda_2, \lambda_3]^\mathrm{T}$，其中 $\lambda_n = \log(\Pr[c_n = 1 | \mathbf{r}] / \Pr[c_n = 0 | \mathbf{r}])$，$n = \{1, 2, 3\}$。需要找到第 2 次迭代结束时的 $\lambda_n^{(2)}$。

**解** 由方程 (4.7)，给定 $\mathbf{G}$ 矩阵对应的校验矩阵 $\mathbf{H}$ 为

$$
\mathbf{H} = [\mathbf{P}^\mathrm{T} \; | \; \mathbf{I}] = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 0 & 1 \end{bmatrix}
$$

通过高斯消元法 (Gaussian elimination) [53]，可以将矩阵 $\mathbf{H}$ 重新整理为

$$
\mathbf{H} = \begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}
$$

其 Tanner 图如图 4.12 所示。$\lambda_n$ 由方程 (4.47) 给出

$$
\lambda_n = L_c r_n + \log\left(\frac{\Pr[c_n = 1 \mid \mathbf{r}_{i \neq n}]}{\Pr[c_n = 0 \mid \mathbf{r}_{i \neq n}]}\right) \tag{4.62}
$$

其中 $L_c = 2/\sigma^2$ 是信道可靠度。

![](images/chapter_4/af0d2ef29e4017834c2b8b15a3faecb0052eb4e40d4cc56ab32c0151c731b3a2.jpg)
**图 4.12** 示例 4.6 解码使用的 Tanner 图

后验 LLR $\boldsymbol{\lambda} = [\lambda_1, \lambda_2, \lambda_3]^\mathrm{T}$ 可以通过图 4.11 的 MP 算法求得。

初始化：

$$
\boldsymbol{\lambda}^{(0)} = \begin{bmatrix} \lambda_1^{(0)} \\ \lambda_2^{(0)} \\ \lambda_3^{(0)} \end{bmatrix} = L_c \begin{bmatrix} r_1 \\ r_2 \\ r_3 \end{bmatrix}
$$

**第 1 次迭代**

每个变量节点将消息 $\lambda_n^{(0)}$ 发送到校验节点，如图 4.13(a) 所示。然后，每个校验节点根据方程 (4.59) 计算接收到的消息，并将结果发送回变量节点，如图 4.13(b) 所示。之后，变量节点根据方程 (4.60) 计算所有接收到的消息，得到第 $n$ 个数据位的 $\lambda_n^{(1)}$：

$$
\boldsymbol{\lambda}^{(1)} = \begin{bmatrix} \lambda_1^{(1)} \\ \lambda_2^{(1)} \\ \lambda_3^{(1)} \end{bmatrix} = L_c \begin{bmatrix} r_1 + r_2 \\ r_1 + r_2 + r_3 \\ r_2 + r_3 \end{bmatrix}
$$

**第 2 次迭代**

类似地，每个变量节点将消息发送到校验节点，如图 4.14(a) 所示。然后，每个校验节点根据方程 (4.59) 计算接收到的消息，并将结果发送回变量节点，如图 4.14(b) 所示。之后，变量节点根据方程 (4.60) 计算所有接收到的消息，得到 $\lambda_n^{(2)}$：

$$
\boldsymbol{\lambda}^{(2)} = \begin{bmatrix} \lambda_1^{(2)} \\ \lambda_2^{(2)} \\ \lambda_3^{(2)} \end{bmatrix} = L_c \begin{bmatrix} r_1 + 2r_2 + r_3 \\ r_1 + 3r_2 + r_3 \\ r_1 + 2r_2 + 2r_3 \end{bmatrix}
$$

![](images/chapter_4/57754386ba31a564a521c025922474816edfccaff6886596988bceab52101249.jpg)
**图 4.13** 第 1 次迭代结束时的消息传递：(a) 从变量节点到校验节点 (b) 从校验节点到变量节点

![](images/chapter_4/1bb9c49b3304e6a444234ef255dbc8933ed16655fa6be19160d6bbfa8deeb84b.jpg)
**图 4.14** 第 2 次迭代结束时的消息传递：(a) 从变量节点到校验节点 (b) 从校验节点到变量节点

# 4.5 校验矩阵的构造

在实际应用中，LDPC 码的性能取决于校验矩阵 $\mathbf{H}$，该矩阵应尽可能具有随机性且无环。关于 LDPC 码的研究 [4, 5, 8, 17, 54, 55] 着重于 $\mathbf{H}$ 矩阵的构造。因此，本节将介绍 $\mathbf{H}$ 矩阵的基本构造方法，为今后 LDPC 码相关的研究工作奠定基础。

# 4.5.1 正则 LDPC 码

$(j, k)$ 正则 LDPC 码的大小为 $M \times N$ 的校验矩阵 $\mathbf{H}$ 可以由大小为 $L \times N$ 的校验矩阵 $\mathbf{H}_0$ 构造，其中 $L = N/k = M/j$：

$$
\mathbf{H}_0 = \begin{bmatrix}
\underbrace{1 1 \dots 1}_{k} & \mathbf{0} & \mathbf{0} & \dots & \mathbf{0} \\
\mathbf{0} & \underbrace{1 1 \dots 1}_{k} & \mathbf{0} & \dots & \mathbf{0} \\
\vdots & \ddots & \ddots & \ddots & \vdots \\
\mathbf{0} & \dots & \mathbf{0} & \underbrace{1 1 \dots 1}_{k} & \mathbf{0} \\
\mathbf{0} & \dots & \mathbf{0} & \mathbf{0} & \underbrace{1 1 \dots 1}_{k}
\end{bmatrix}_{L \times N} \tag{4.65}
$$

其中 $\mathbf{0} = [0 0 \dots 0]$ 是大小为 $1 \times k$ 的零向量。方程 (4.65) 表明，第 $m$ 行在列位置 $(m-1)k + 1$ 到 $mk$ 处为 1，其余位置为 0。在实践中，矩阵 $\mathbf{H}_0$ 可用于 $(1, k)$ 正则 LDPC 码，其中每个校验方程涉及 $k$ 个数据位，每个数据位仅涉及一个校验方程。然而，使用 $\mathbf{H}_0$ 矩阵的 LDPC 码的性能较差，因为 $\mathbf{H}_0$ 矩阵存在线性相关，例如码字 0000...0 和 1100...0 都是有效码字。因此，该码的最小距离为 $d_{\min} = 2$。

一般来说，$(j, k)$ 正则 LDPC 码的大小为 $M \times N$ 的 $\mathbf{H}$ 矩阵可以通过将经过列置换的 $\mathbf{H}_0$ 矩阵按如下方式堆叠而成：

$$
\mathbf{H} = \begin{bmatrix}
\pi_1(\mathbf{H}_0) \\
\pi_2(\mathbf{H}_0) \\
\vdots \\
\pi_j(\mathbf{H}_0)
\end{bmatrix}_{M \times N} \tag{4.66}
$$

其中 $\pi_i(\mathbf{H}_0)$ 是矩阵 $\mathbf{H}_0$ 经过列置换后的矩阵，$i = \{1, 2, \dots, j\}$。然而，在实践中，$\mathbf{H}_0$ 矩阵也可以有其他形式，例如

$$
\mathbf{H}_0 = \begin{bmatrix} \mathbf{I} & \mathbf{I} & \mathbf{I} & \dots & \mathbf{I} \end{bmatrix}_{L \times N} \tag{4.67}
$$

其中 $\mathbf{I}$ 是大小为 $L \times L$ 的单位矩阵，$L = N/k$。

好的置换应使得 $\mathbf{H}$ 矩阵具有大于 2 的最小距离 $d_{\min} > 2$。一般来说，设计 $j$ 种置换（每种长度为 $N$）是一项具有挑战性的工作。然而，Gallager [17] 已证明，纯随机置换会产生最佳的 $\mathbf{H}$ 矩阵，从而使 LDPC 码获得最优性能。

**示例 4.8** 考虑以下 $(3, 4)$ 正则 LDPC 码，大小为 $15 \times 20$ [17]

$$
\mathbf{H} = \begin{bmatrix}
1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 1 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 1 & 1 \\
\hline
1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 \\
\hline
1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1
\end{bmatrix} \tag{4.68}
$$

其中两条水平线将 $\mathbf{H}_0$ 矩阵与另外两个由 $\mathbf{H}_0$ 矩阵置换得到的矩阵按方程 (4.66) 分开，置换分别为 $\pi_1 = \{1\;2\;3\;4\;5\;\dots\;20\}$，$\pi_2 = \{1\;5\;9\;13\;2\;6\;10\;17\;3\;7\;14\;18\;4\;11\;15\;19\;8\;12\;16\;20\}$，$\pi_3 = \{1\;6\;12\;17\;2\;7\;11\;18\;3\;8\;15\;19\;4\;9\;14\;20\;5\;10\;13\;16\}$。方程 (4.68) 中的 $\mathbf{H}$ 矩阵表明，每列有 $j = 3$ 个 1，每行有 $k = 4$ 个 1。此外，还可发现第 10 行是第 1 至第 9 行的模二和，第 15 行是第 1 至第 5 行和第 11 至第 14 行的模二和。这意味着第 10 行和第 15 行与其他行线性相关。因此，$\mathbf{H}$ 矩阵中只有 13 行是线性无关的，或者说 $\mathbf{H}$ 矩阵的秩为 13。该 LDPC 码每次编码 $K = 20 - 13 = 7$ 个数据位，码率为 $R = K/N = 0.35$。

在实践中，$\mathbf{H}$ 矩阵可以通过删除第 10 行和第 15 行进行化简，得到 $\tilde{\mathbf{H}}$。由于 $\mathbf{cH}^\mathrm{T} = \mathbf{0}$ 当且仅当 $\mathbf{c}\tilde{\mathbf{H}}^\mathrm{T} = \mathbf{0}$，因此删减后的矩阵仍然产生相同的码字。由于 $\tilde{\mathbf{H}}$ 矩阵中每行/列的 1 的个数并不相同，$\tilde{\mathbf{H}}$ 不再满足正则 LDPC 码的性质。然而，这里我们只关注满足正则 LDPC 码性质的 $\mathbf{H}$ 矩阵，即使各行并非线性无关。

# 4.5.2 阵列 LDPC 码

阵列 LDPC 码 (array LDPC code) 由 Fan [54] 于 2000 年提出。该校验矩阵 $\mathbf{H}$ 具有阵列结构，从而解决了 $\mathbf{H}$ 矩阵构造的复杂性问题。此外，阵列 LDPC 码的性能接近于具有随机 $\mathbf{H}$ 矩阵的 LDPC 码。

阵列 LDPC 码由三个参数定义：素数 $p$ 和整数 $\{j, k\} \leq p$。$\mathbf{H}$ 矩阵的大小为 $jp \times kp$，其结构如下：

$$
\mathbf{H}_{(jp \times kp)} = \begin{bmatrix}
\mathbf{I} & \mathbf{I} & \mathbf{I} & \dots & \mathbf{I} \\
\mathbf{I} & \boldsymbol{\alpha} & \boldsymbol{\alpha}^2 & \dots & \boldsymbol{\alpha}^{k-1} \\
\mathbf{I} & \boldsymbol{\alpha}^2 & \boldsymbol{\alpha}^4 & \dots & \boldsymbol{\alpha}^{2(k-1)} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
\mathbf{I} & \boldsymbol{\alpha}^{j-1} & \boldsymbol{\alpha}^{2(j-1)} & \dots & \boldsymbol{\alpha}^{(j-1)(k-1)}
\end{bmatrix} \tag{4.69}
$$

其中 $j$ 和 $k$ 分别是 $\mathbf{H}$ 矩阵每列和每行中 1 的个数，$\mathbf{I}$ 是大小为 $p \times p$ 的单位矩阵，$\boldsymbol{\alpha}$ 是大小为 $p \times p$ 的置换矩阵，表示 $\mathbf{I}$ 矩阵向左或向右循环移位若干次，即

$$
\boldsymbol{\alpha} = \begin{bmatrix}
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 & 0
\end{bmatrix} \quad \text{或} \quad \boldsymbol{\alpha} = \begin{bmatrix}
0 & 0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0
\end{bmatrix} \tag{4.70}
$$

$\boldsymbol{\alpha}$ 的指数表示 $\boldsymbol{\alpha}$ 矩阵的循环移位次数。方程 (4.69) 表明 $\mathbf{H}$ 矩阵中 1 的分布是恒定的，因此阵列 LDPC 码属于正则 LDPC 码。

例如，通过循环移位从单位矩阵构造大小为 $5 \times 5$ 的 $\boldsymbol{\alpha}$ 矩阵，具有以下重要性质：

$$
\mathbf{I} = \begin{bmatrix}
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1
\end{bmatrix}
\quad
\boldsymbol{\alpha} = \begin{bmatrix}
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 & 0
\end{bmatrix}
\quad
\boldsymbol{\alpha}^2 = \begin{bmatrix}
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0
\end{bmatrix}
$$

$$
\boldsymbol{\alpha}^3 = \begin{bmatrix}
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0
\end{bmatrix}
\quad
\boldsymbol{\alpha}^4 = \begin{bmatrix}
0 & 0 & 0 & 0 & 1 \\
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0
\end{bmatrix}
\quad
\boldsymbol{\alpha}^5 = \begin{bmatrix}
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 1
\end{bmatrix}
$$

$\boldsymbol{\alpha}$ 被称为置换矩阵的原因是，当 $\boldsymbol{\alpha}$ 与任何矩阵相乘时，结果是对原矩阵重新排列（交换各列位置）。此外，置换矩阵的逆矩阵 $\boldsymbol{\alpha}^{-1}$ 等于 $\boldsymbol{\alpha}^\mathrm{T}$，其中 $(\cdot)^\mathrm{T}$ 是转置运算符。

对于参数为 $(j, k, p)$ 的阵列 LDPC 码，输入数据位数为 $K = N - M = (k - j)p$，校验位数为 $M = jp$，码字位数为 $N = kp$，码率为 $1 - (jp - j + 1)/p^2$。然而，由于方程 (4.66) 和 (4.69) 中的 $\mathbf{H}$ 矩阵并非如方程 (4.7) 所示的系统形式，数据的编码必须首先通过高斯消元法 [53] 将 $\mathbf{H}$ 矩阵转换为系统形式，然后使用第 4.3 节中描述的编码步骤。此外，Fan [54] 还证明了阵列码不存在长度为 4 的环，并且可以使用 MP 算法（图 4.11）像正则 LDPC 码一样进行数据解码，如第 4.6.1 节所述。总之，Fan 的研究解决了 LDPC 码在从 $\{0, 1\}$ 随机数据构造 $\mathbf{H}$ 矩阵、控制每行每列中 1 的数量以及避免长度为 4 的环等方面的缺点。

# 4.5.3 修改阵列 LDPC 码

Richardson 的研究 [46] 指出，通过将校验矩阵 $\mathbf{H}$ 排列成三角形形式，可以提高编码性能并使编码复杂度呈线性。因此，Eleftheriou [55] 于 2002 年提出了一种新的 LDPC 码，称为"修改阵列码 (MAC: modified array code)"，采用循环移位方法。修改阵列 LDPC 码的参数 $(j, k, p)$ 与阵列 LDPC 码相同，其中 $\mathbf{H}$ 矩阵的大小为 $jp \times kp$，其结构如下：

$$
\mathbf{H}_{(jp \times kp)} = \begin{bmatrix}
\mathbf{I} & \mathbf{I} & \dots & \mathbf{I} & \mathbf{I} & \mathbf{I} & \dots & \mathbf{I} \\
\mathbf{0} & \mathbf{I} & \boldsymbol{\alpha} & \dots & \boldsymbol{\alpha}^{j-2} & \boldsymbol{\alpha}^{j-1} & \dots & \boldsymbol{\alpha}^{k-2} \\
\mathbf{0} & \mathbf{0} & \mathbf{I} & \dots & \boldsymbol{\alpha}^{2(j-3)} & \boldsymbol{\alpha}^{2(j-2)} & \dots & \boldsymbol{\alpha}^{2(k-3)} \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \ddots & \vdots \\
\mathbf{0} & \mathbf{0} & \mathbf{0} & \dots & \mathbf{I} & \boldsymbol{\alpha}^{(j-1)} & \dots & \boldsymbol{\alpha}^{(j-1)(k-j)}
\end{bmatrix} \tag{4.71}
$$

其中 $\mathbf{0}$ 是大小为 $p \times p$ 的零矩阵，$\boldsymbol{\alpha}$ 是置换矩阵。可以观察到，$\mathbf{H}$ 矩阵中的三角形结构使得 1 的分布从恒定变为非恒定。因此，修改阵列 LDPC 码属于非正则 LDPC 码 (irregular LDPC code)。

对于参数为 $(j, k, p)$ 的修改阵列 LDPC 码，输入数据位数为 $K = (k - j)p$，校验位数为 $M = jp$，码字位数为 $N = kp$，码率为 $(1 - j/k)$。此外，方程 (4.71) 中的 $\mathbf{H}$ 矩阵不存在长度为 4 的环，可以使用 MP 算法进行数据解码，如第 4.6.1 节所述，并且具有与使用随机 $\mathbf{H}$ 矩阵的 LDPC 码相当的优异性能（误码平层低）。

修改阵列 LDPC 码的数据编码比阵列 LDPC 码更简单，因为方程 (4.71) 中的 $\mathbf{H}$ 矩阵是三角形结构。首先，将码字重新排列为

$$
\mathbf{c} = [\mathbf{p} \mid \mathbf{m}] \tag{4.72}
$$

其中 $\mathbf{p}$ 是长度为 $M = jp$ 的校验位向量，$\mathbf{m}$ 是长度为 $K = N - M = (k - j)p$ 的数据位向量。将方程 (4.72) 中的 $\mathbf{c}$ 代入方程 (4.6)，得到

$$
\mathbf{H}_{(M \times N)} \begin{bmatrix} \mathbf{p} \\ \mathbf{m} \end{bmatrix}^\mathrm{T} = \mathbf{0}_{(M \times 1)}^\mathrm{T} \tag{4.73}
$$

这一结果使得编码复杂度相比第 4.3 节中描述的编码步骤显著降低，因为计算校验位 $\mathbf{p}$ 时不需要像方程 (4.41) 中那样求逆矩阵。

例如，设 $j = 3, k = 5, p = 3$，置换矩阵为

$$
\boldsymbol{\alpha} = \begin{bmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0
\end{bmatrix}
\quad
\boldsymbol{\alpha}^2 = \begin{bmatrix}
0 & 1 & 0 \\
0 & 0 & 1 \\
1 & 0 & 0
\end{bmatrix}
\quad
\boldsymbol{\alpha}^3 = \begin{bmatrix}
1 & 0 & 0 \\
0 & 1 & 0 \\
0 & 0 & 1
\end{bmatrix}
\quad
\boldsymbol{\alpha}^4 = \begin{bmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0
\end{bmatrix}
$$

因此，大小为 $9 \times 15$ 的 $\mathbf{H}$ 矩阵为

$$
\mathbf{H} = \begin{bmatrix}
\mathbf{I} & \mathbf{I} & \mathbf{I} & \mathbf{I} & \mathbf{I} \\
\mathbf{0} & \mathbf{I} & \boldsymbol{\alpha} & \boldsymbol{\alpha}^2 & \boldsymbol{\alpha}^3 \\
\mathbf{0} & \mathbf{0} & \mathbf{I} & \boldsymbol{\alpha}^2 & \boldsymbol{\alpha}^4
\end{bmatrix} = \begin{bmatrix}
1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 \\
0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 1 & 0
\end{bmatrix} \tag{4.74}
$$

根据方程 (4.72)，码字为

$$
\mathbf{c} = [\mathbf{p} \mid \mathbf{m}] = [p_1 \; p_2 \; p_3 \; \dots \; p_9 \; m_1 \; m_2 \; m_3 \; \dots \; m_6] \tag{4.75}
$$

校验位 $\mathbf{p}$ 由方程 (4.73) 求得，即将 $\mathbf{H}$ 矩阵与码字 $\mathbf{c}$ 相乘，得到总共 $M = 9$ 个校验方程：

$$
p_1 + p_4 + p_7 + m_1 + m_4 = 0 \tag{4.76}
$$

$$
p_2 + p_5 + p_8 + m_2 + m_5 = 0 \tag{4.77}
$$

$$
p_3 + p_6 + p_9 + m_3 + m_6 = 0 \tag{4.78}
$$

$$
p_4 + p_9 + m_2 + m_4 = 0 \tag{4.79}
$$

$$
p_5 + p_7 + m_3 + m_5 = 0 \tag{4.80}
$$

$$
p_6 + p_8 + m_1 + m_6 = 0 \tag{4.81}
$$

$$
p_7 + m_2 + m_6 = 0 \tag{4.82}
$$

$$
p_8 + m_1 + m_4 = 0 \tag{4.83}
$$

$$
p_9 + m_3 + m_5 = 0 \tag{4.84}
$$

从方程 (4.82)-(4.84) 开始，可以直接求得 $p_7, p_8, p_9$，然后代入方程 (4.79)-(4.81) 求得 $p_4, p_5, p_6$，最后代入方程 (4.76)-(4.78) 求得 $p_1, p_2, p_3$。因此，使用修改阵列码的编码不需要方程 (4.41) 中的矩阵求逆操作。

# 4.5.4 备注

综上所述，LDPC 码是从过去到现在性能最好的纠错码 (ECC)，因为其性能比其他 ECC 码更接近香农极限 [4]。LDPC 码的性能取决于校验矩阵 $\mathbf{H}$ 的结构（应尽可能随机）和要编码的数据长度（即 $K$ 值）。也就是说，当 $K \to \infty$ [4, 17] 时，LDPC 码具有最高性能，这也导致 $\mathbf{H}$ 矩阵非常大。过去各种应用无法使用 LDPC 码的原因是，需要具有大内存的处理芯片来存储 $\mathbf{H}$ 矩阵，成本非常高。

然而，在 2000 年之后，Fan [54] 提出了阵列结构的 $\mathbf{H}$ 矩阵，这是一种结构化 $\mathbf{H}$ 矩阵，其性能接近于使用随机 $\mathbf{H}$ 矩阵的 LDPC 码，并解决了 $\mathbf{H}$ 矩阵构造的复杂性问题。此外，它可以实际应用于各种应用中，因为当今的处理芯片具有更大的内存容量，并且价格更具竞争力。

# 4.7 本章总结

LDPC 码（低密度奇偶校验码）是当前最好的纠错码 [2, 5, 8]，已被实际应用于多种应用中，包括硬盘驱动器。

由于 LDPC 码是线性分组码的一种类型，本章首先介绍了线性分组码的编码和解码步骤，以及生成矩阵和校验矩阵的含义。然后，介绍了 LDPC 码的基础知识，并详细说明了 LDPC 码的编码和解码过程。实验发现，LDPC 码的性能取决于所使用的校验矩阵。第 4.5 节展示了各种校验矩阵的构造示例。一个好的校验矩阵不应存在长度为 4 的环，并且矩阵中 1 的分布应尽可能随机，以使 LDPC 码获得最佳性能 [17]。此外，还展示了将 LDPC 码应用于 HDD 信道迭代解码系统的示例。实验结果表明，迭代解码可以提高系统性能，且系统性能随着迭代解码次数的增加而提高。

# 4.8 习题

1. 请解释内信息 (intrinsic information) 和外信息 (extrinsic information) 的含义。
2. 请解释第 4.1.5 节中校正子解码的原理，并举例说明计算过程。
3. 设 LDPC 码的生成矩阵 $\mathbf{G} = \begin{bmatrix} 1 & 0 & 1 & 1 & 0 \\ 0 & 1 & 1 & 0 & 1 \end{bmatrix}$，求校验矩阵 $\mathbf{H}$ 并绘制其 Tanner 图。
4. 使用与方程 (4.25) 中生成矩阵 $\mathbf{G}$ 对应的校验矩阵 $\mathbf{H}$，对数据 $\mathbf{m} = [1101]$ 和 $\mathbf{m} = [1011]$ 进行编码。
5. 使用方程 (4.74) 中的校验矩阵 $\mathbf{H}$，对数据 $\mathbf{m} = [101011]$ 和 $\mathbf{m} = [111010]$ 进行编码。
6. 考虑图 4.5 中的信道模型。设输入数据位 $m_n = \{1, 1, 0\}$，使用的 LDPC 码生成矩阵 $\mathbf{G}$ 如方程 (4.4) 所示，噪声 $w_n = \{0.2, 0.3, -0.1, -0.2, 0.5, -0.4\}$，方差 $\sigma^2 = 0.5$。求第 3 次迭代结束时的后验 LLR $\{\lambda_1, \lambda_2, \lambda_3, \lambda_4, \lambda_5, \lambda_6\}$。
7. 考虑图 4.19 中的信道模型。设输入数据序列 $m_n = \{1, 1\}$，使用的 LDPC 码生成矩阵 $\mathbf{G} = \begin{bmatrix} 1 & 0 & 1 & 1 & 0 \\ 0 & 1 & 1 & 0 & 1 \end{bmatrix}$，信道 $H(D) = 1 + D$，噪声 $w_n = \{0.3, -0.2, 0.1, 0.2, -0.4, -0.5\}$，方差 $\sigma^2 = 0.5$。使用 Turbo 均衡器解码数据序列 $r_n$，在第 3 次迭代结束时结束。其中 LDPC 解码器在 MP 算法内部进行 3 次迭代，SISO 均衡器由以下算法构造：
   7.1) BCJR 算法
   7.2) Max-Log-MAP 算法
   7.3) Log-MAP 算法
   7.4) SOVA 算法

# 4.6 实验结果

本节将测试 LDPC 码在 AWGN 信道和使用迭代解码技术的 HDD 信道中的性能，以展示 LDPC 码的能力。

# 4.6.1 AWGN 信道

考虑图 4.5 中的 AWGN 信道。使用的 LDPC 码是修改阵列码 (MAC)，其校验矩阵 $\mathbf{H}$ 大小为 $9 \times 15$，如方程 (4.74) 所示。该 LDPC 码每次编码 6 个输入数据位，产生 15 位的码字（校验位为 9 位）。信噪比 (SNR) 定义为

$$
\mathrm{SNR} = 10 \log_{10}\left(\frac{E_b}{N_0}\right) \tag{4.85}
$$

其中 $E_b = 1$ 是每个输入数据位的能量，$N_0/2$ 是噪声 $w_n \sim \mathcal{N}(0, \sigma^2)$ 的双边功率谱密度，$\sigma^2 = N_0/(2T)$，$T$ 是输入数据位 $m_n$ 的周期。每个 SNR 下的误码率 (BER) 通过向系统发送多个输入数据块（每块 6 位）计算，直到解码器检测到的总错误位数不少于 1000 位。

![](images/chapter_5/253f8a2c165f9b9392f4c515d86605e3c401c0950a753a01ece989da1d488ede.jpg)

![](images/chapter_5/d24f4b7fe8839f639326c1a6a67f06cef5f2580d51e0a877cc5e480acc729dbf.jpg)
**图 4.16** 图 4.5 中系统在不同 LDPC 解码迭代次数下的性能

图 4.16 显示了 LDPC 解码器在不同迭代次数下的系统性能。标记为"Threshold detector"的曲线表示将图 4.5 中的 LDPC 解码器替换为具有以下判决规则的阈值检测器时的性能：

$$
\hat{m}_n = \begin{cases} 1, & \text{if } r_n \geq 0 \\ 0, & \text{if } r_n < 0 \end{cases} \tag{4.86}
$$

对于 $n = \{1, 2, \dots, 6\}$。从图中可以看出，LDPC 解码器的性能远优于阈值检测器，特别是当 LDPC 解码器内部的迭代次数增加时。然而，当迭代次数增加到一定程度时，LDPC 解码器的性能开始趋于饱和（这里可以看到第 3 次和第 5 次迭代的性能接近）。这一结论可以通过绘制不同 SNR 下各次迭代的 BER 曲线来确认，如图 4.17 所示。可以看出，在第 4 次迭代之后，LDPC 解码器的性能开始趋于稳定，这种现象称为误码平层 (error floor)。

![](images/chapter_5/4b524c4cc67af623815d00cc1d68a0b0a753b31e35d40d9e4985a71076405a8c.jpg)
**图 4.17** LDPC 解码器在各次迭代下的性能

接下来将比较使用有环和无环校验矩阵 $\mathbf{H}$ 的 LDPC 码的性能。这里将对方程 (4.74) 中的 $\mathbf{H}$ 矩阵进行修改，引入 2 个环，得到

$$
\tilde{\mathbf{H}} = \begin{bmatrix}
1 & 0 & 0 & 1 & 0 & 0 & \tilde{1} & 0 & 0 & \tilde{1} & 0 & 0 & 1 & 0 & 0 \\
0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & \hat{1} & 0 & 0 & \hat{1} & 0 \\
0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 & 0 & 0 & 1 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & \tilde{1} & 0 & 0 & \tilde{1} & 0 & 1 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & \hat{1} & 0 & 0 & \hat{1} & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 & 0
\end{bmatrix} \tag{4.87}
$$

其中 $\tilde{1}$ 和 $\hat{1}$ 表示引入环的位置。图 4.18 比较了使用有环和无环 $\mathbf{H}$ 矩阵的 LDPC 码的性能，其中实线表示无环 $\mathbf{H}$ 矩阵，虚线表示有环 $\mathbf{H}$ 矩阵。可以清楚地看出，使用无环 $\mathbf{H}$ 矩阵的 LDPC 码在所有迭代次数下的性能都优于使用有环 $\mathbf{H}$ 矩阵的 LDPC 码。因此，好的 LDPC 码不应使用含有环的 $\mathbf{H}$ 矩阵 [4, 5]。

![](images/chapter_5/9f302fd7305ce6265d290e5f51482f0c6cd6762e3e60a49e1a816f9250d32cb8.jpg)
**图 4.18** 使用有环和无环 $\mathbf{H}$ 矩阵的 LDPC 码性能比较

# 4.6.2 迭代解码信道

考虑图 4.19 中 HDD 信道的迭代解码模型，其中 LDPC 码用作外码。在该模型中，解码过程在内解码器（SISO 均衡器）和外解码器（LDPC 解码器）之间交替进行。LDPC 解码器内部使用 MP 算法，而 SISO 均衡器可以使用 BCJR、Max-Log-MAP、Log-MAP 或 SOVA 算法。

![](images/chapter_4/8171bf7b9cb1e4458c6a4d0e82b41d40e862877f9bb05f3957edc251c01fbd.jpg)
**图 4.19** 带 LDPC 码的 HDD 信道迭代解码模型

图 4.20 显示了使用不同 SISO 均衡器的迭代解码系统在 3 次外迭代下的性能，其中 LDPC 解码器内部使用修正阵列码 (MAC) 在 MP 算法中进行 3 次内迭代。可以看出，使用 BCJR 算法的系统提供了最佳性能，其次是 Log-MAP、Max-Log-MAP 和 SOVA 算法。然而，所有迭代解码系统的性能都远优于阈值检测器系统。

图 4.21 显示了使用 BCJR 算法且在不同外迭代次数下的性能。可以看出，系统性能随着外迭代次数的增加而提高。然而，当外迭代次数达到一定值时，性能改善趋于饱和。

![](images/chapter_4/3dab336dd33544ec6bdb3ac5f9910b8e4ddf276cba3b871a4e9eed1e6343eef.jpg)
**图 4.20** 使用不同 SISO 均衡器的迭代解码系统性能

![](images/chapter_4/fee2d9f54d1f1a8c2e84b5a7017da94a3a4f64d38e5b1977d8a5b9ca1761c0b.jpg)
**图 4.21** 使用 BCJR 算法在不同外迭代次数下的系统性能

实验结果表明，LDPC 码能够显著提高 HDD 信道迭代解码系统的性能，且系统性能随着迭代次数的增加而提高，直到达到饱和点。
