# 第四章 LDPC 码

## 4.1 引言

LDPC (Low-Density Parity-Check) 码 [17] 是一类具有稀疏校验矩阵的线性分组码，由 Gallager 于 1963 年提出。由于其接近香农极限的性能和高效的迭代解码算法，LDPC 码已成为现代通信系统中的重要纠错码。

### 4.1.1 线性分组码

线性分组码 (linear block code) $(n, k)$ 将 $k$ 位信息映射为 $n$ 位码字，其中 $n - k$ 位为校验位。码率 $R = k/n$。

### 4.1.2 生成矩阵

生成矩阵 $G$ 大小为 $k \times n$，将信息向量 $\mathbf{u}$ 映射为码字 $\mathbf{v} = \mathbf{u}G$。系统形式的生成矩阵为 $G = [I_k | P]$，其中 $P$ 是 $k \times (n-k)$ 的校验部分。

### 4.1.3 校验矩阵

校验矩阵 $H$ 大小为 $(n-k) \times n$，满足 $H\mathbf{v}^T = \mathbf{0}$ 对所有码字 $\mathbf{v}$ 成立。系统形式下 $H = [-P^T | I_{n-k}]$。对于 LDPC 码，$H$ 是稀疏矩阵（大多数元素为 0）。

### 4.1.4 最小距离

码的最小距离 $d_{\min}$ 是任意两个不同码字间的最小汉明距离，决定了码的纠错能力：最多可纠正 $\lfloor (d_{\min} - 1)/2 \rfloor$ 个错误。

### 4.1.5 线性分组码的解码

接收向量 $\mathbf{r}$ 解码为最可能码字。硬判决解码选择与 $\mathbf{r}$ 汉明距离最近的码字；软判决解码利用接收信号的概率信息。

## 4.2 LDPC 码基础

LDPC 码由稀疏校验矩阵 $H$ 定义。Tanner 图是 $H$ 的二部图表示，包含变量节点（对应码字位）和校验节点（对应校验方程）。

### 4.2.1 正则 LDPC 码

正则 LDPC 码的 $H$ 矩阵每列有 $w_c$ 个 1，每行有 $w_r$ 个 1。列重和行重恒定。

### 4.2.2 非正则 LDPC 码

非正则 LDPC 码的列重和行重可变，通常性能优于正则码。度分布多项式 $\lambda(x)$ 和 $\rho(x)$ 描述变量节点和校验节点的度分布。

### 4.2.3 双曲正切规则

迭代解码中校验节点的更新可用双曲正切函数表示：

$$
\tanh\left(\frac{\lambda_{c\to v}}{2}\right) = \prod_{v' \in N(c)\setminus\{v\}} \tanh\left(\frac{\lambda_{v'\to c}}{2}\right) \tag{4.x}
$$

## 4.3 LDPC 编码

给定校验矩阵 $H$，可通过高斯消元求生成矩阵 $G$。系统编码：$\mathbf{v} = \mathbf{u}G$。

## 4.4 LDPC 解码

LDPC 解码通常使用置信传播 (BP) 算法，即消息传递算法。

### 4.4.1 LDPC 解码基础

BP 算法在 Tanner 图上沿边传递对数似然比 (LLR) 消息。变量节点和校验节点交替更新消息。

### 4.4.2 LDPC 码的环

Tanner 图中的环影响 BP 算法的收敛性。短环（尤其是 4 环）会降低解码性能，设计 $H$ 矩阵时应避免。

### 4.4.3 数据位 LLR 的计算

信道 LLR：$\lambda_i = \ln(p(y_i|x_i=1)/p(y_i|x_i=-1))$。对 AWGN 信道，$\lambda_i = 2y_i/\sigma^2$。

### 4.4.4 消息传递算法

消息传递算法 (MP: Message Passing)：

## 消息传递算法 (MP)

1. 初始化：每个变量节点 $v_i$ 的初始消息为信道 LLR $\lambda_i$
2. 校验节点更新（变量→校验）：$\lambda_{c\to v} = 2\tanh^{-1}\left(\prod_{v' \neq v} \tanh(\lambda_{v'\to c}/2)\right)$
3. 变量节点更新（校验→变量）：$\lambda_{v\to c} = \lambda_v + \sum_{c' \neq c} \lambda_{c'\to v}$
4. 硬判决：$\hat{x}_i = \text{sign}(\lambda_v)$
5. 若 $H\hat{\mathbf{x}}^T = \mathbf{0}$ 或达最大迭代次数，停止；否则返回步骤 2

## 4.5 校验矩阵的构造

### 4.5.1 正则 LDPC 码

随机构造：随机生成列重 $w_c$、行重 $w_r$ 的稀疏矩阵，确保无短环。

### 4.5.2 阵列 LDPC 码

基于有限域构造的结构化 LDPC 码，具有准循环结构，便于硬件实现。

### 4.5.3 改进的阵列 LDPC 码

在阵列码基础上优化列重分布和环长分布，提高性能。

### 4.5.4 说明

实际系统常采用 QC-LDPC (准循环 LDPC) 码，兼顾性能和实现复杂度。5G NR 和 DVB-S2 等标准均采用 QC-LDPC。
