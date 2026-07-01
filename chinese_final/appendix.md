
# 附录 A

# 雅可比对数函数

本附录证明方程 (3.15) 中的雅可比对数函数：

$$
\ln(e^a + e^b) = \max(a, b) + \ln(1 + e^{-|a-b|}) \tag{n.1}
$$

其中 $a$ 和 $b$ 是任意常数。证明分两种情况：

1) 当 $a > b$ 时：

$$
\begin{aligned}
\ln(e^a + e^b) &= \ln\left(e^a\left\{1 + \frac{e^b}{e^a}\right\}\right) = \ln\left(e^a\left\{1 + e^{b-a}\right\}\right) \\
&= \ln(e^a) + \ln(1 + e^{-(a-b)}) \\
&= a + \ln(1 + e^{-(a-b)}) \tag{n.2}
\end{aligned}
$$

2) 当 $b > a$ 时：

$$
\begin{aligned}
\ln(e^a + e^b) &= \ln\left(e^b\left\{\frac{e^a}{e^b} + 1\right\}\right) = \ln\left(e^b\left\{1 + e^{a-b}\right\}\right) \\
&= \ln(e^b) + \ln(1 + e^{-(b-a)}) \\
&= b + \ln(1 + e^{-(b-a)}) \tag{n.3}
\end{aligned}
$$

综合两种情况得到：

$$
\ln(e^a + e^b) = \max(a, b) + \ln(1 + e^{-|a-b|}) \tag{n.4}
$$

这与方程 (3.15) 一致。

# 附录 B

# 双曲正切规则

本附录证明方程 (4.30) 中的双曲正切规则。设奇偶函数 $\Phi(\mathbf{c}) \in \{0,1\}$ 是 $n$ 位数据集 $\mathbf{c} = [c_1, c_2, \dots, c_n]$ 的奇偶值，其中 $c_i \in \{0,1\}$。奇偶函数 $\Phi(\mathbf{c})$ 可由下式求得：

$$
\Phi(\mathbf{c}) = \frac{1}{2}\left(1 - \prod_{i=1}^n (1 - 2c_i)\right) \tag{1.1}
$$

$\Phi(\mathbf{c})=0$ 当 $\mathbf{c}$ 中 1 的个数为偶数，$\Phi(\mathbf{c})=1$ 当 1 的个数为奇数。$\Phi(\mathbf{c})=1$ 的概率等于 $\Phi(\mathbf{c})$ 的期望值：

$$
\begin{aligned}
\Pr[\Phi(\mathbf{c}) = 1] &= E[\Phi(\mathbf{c})] \\
&= \frac{1}{2}\left(1 - \prod_{i=1}^n (1 - 2E[c_i])\right) \\
&= \frac{1}{2}\left(1 - \prod_{i=1}^n \left(\frac{1 - e^{\lambda_i}}{1 + e^{\lambda_i}}\right)\right) \\
&= \frac{1}{2}\left(1 - \prod_{i=1}^n \tanh\left(\frac{-\lambda_i}{2}\right)\right) \tag{y.2}
\end{aligned}
$$

由于 $\Pr[\Phi(\mathbf{c})=0] = 1 - \Pr[\Phi(\mathbf{c})=1]$，$\Phi(\mathbf{c})$ 的 LLR 为：

$$
\lambda_{\Phi(\mathbf{c})} = \log\left(\frac{\Pr[\Phi(\mathbf{c})=1]}{\Pr[\Phi(\mathbf{c})=0]}\right) = \log\left(\frac{1 - \prod_i \tanh(-\lambda_i/2)}{1 + \prod_i \tanh(-\lambda_i/2)}\right) \tag{y.3}
$$

利用 $\tanh(-\lambda/2) = (1-e^\lambda)/(1+e^\lambda)$ 和 $\Psi = \prod_{i=1}^n \tanh(-\lambda_i/2)$，得到：

$$
\tanh\left(\frac{-\lambda_{\Phi(\mathbf{c})}}{2}\right) = \Psi = \prod_{i=1}^n \tanh\left(\frac{-\lambda_i}{2}\right) \tag{1.4}
$$

这与方程 (4.30) 一致。

# 附录 C

# 方程 (4.30) 和 (4.32) 的等价性

本附录证明方程 (4.30) 和 (4.32) 等价。考虑方程 (4.30) 的双曲正切规则：

$$
\tanh\left(\frac{-\lambda_{\Phi(\mathbf{c})}}{2}\right) = \prod_{i=1}^n \tanh\left(\frac{-\lambda_i}{2}\right) \tag{9.1}
$$

对于实数 $\lambda_i$，有 $-\lambda_i = \operatorname{sign}(-\lambda_i) \times |-\lambda_i|$。代入方程 (9.1) 得到两个方程：

$$
\operatorname{sign}(-\lambda_{\Phi(\mathfrak{c})}) = \prod_{i=1}^n \operatorname{sign}(-\lambda_i) \tag{9.3}
$$

$$
\tanh\left(\frac{|\lambda_{\Phi(\mathbf{c})}|}{2}\right) = \prod_{i=1}^n \tanh\left(\frac{|\lambda_i|}{2}\right) \tag{9.4}
$$

对方程 (9.4) 两边取 $-\log(\cdot)$：

$$
f(|\lambda_{\Phi(\mathfrak{c})}|) = \sum_{i=1}^n f(|\lambda_i|) \tag{9.5}
$$

结合方程 (9.3) 和 (9.5) 得到方程 (4.32)：

$$
\lambda_{\Phi(\mathbf{c})} = -\prod_{i=1}^n \operatorname{sign}(-\lambda_i) \times f\left(\sum_{i=1}^n f(|\lambda_i|)\right) \tag{9.7}
$$

# 附录 D

# PR2 信道的软估计值

本附录推导 PR2 信道的软估计值 $\tilde{r}_k$，如方程 (5.23) 所示。考虑图 D.1 中的 PR2 信道模型，输入数据 $a_k \in \{\pm1\}$ 通过 PR2 信道 $H(D) = 1 + 2D + D^2$，得到输出 $r_k = a_k * h_k \in \{0, \pm2, \pm4\}$。

Turbo 均衡器为数据序列 $\{a_k\}$ 生成软信息（LLR）$\{\lambda_k\}$。软切片器使用 $\{\lambda_k\}$ 计算软判决值 $\tilde{r}_k = E[r_k \mid \{\lambda_k\}]$：

$$
\tilde{r}_k = (-4)\Pr[r_k=-4] + (-2)\Pr[r_k=-2] + (2)\Pr[r_k=2] + (4)\Pr[r_k=4] \tag{3.1}
$$

$r_k = -4$ 当且仅当输入 $\{a_k, a_{k-1}, a_{k-2}\} = \{-1, -1, -1\}$。因此：

$$
\Pr[r_k=-4] = \Pr[a_k=-1] \cdot \Pr[a_{k-1}=-1] \cdot \Pr[a_{k-2}=-1]
$$

类似地计算 $r_k = -2, 2, 4$ 的概率。代入并化简后得到方程 (5.23)：

$$
\tilde{r}_k = \frac{C_1 + C_2 + C_3}{2 \cosh(\lambda_k/2) \cosh(\lambda_{k-1}/2) \cosh(\lambda_{k-2}/2)}
$$

其中 $C_1 = 2\sinh((\lambda_k + \lambda_{k-1} + \lambda_{k-2})/2)$，$C_2 = \sinh((\lambda_k + \lambda_{k-1} - \lambda_{k-2})/2)$，$C_3 = \sinh((-\lambda_k + \lambda_{k-1} + \lambda_{k-2})/2)$，$E[\cdot]$ 是期望算子。
