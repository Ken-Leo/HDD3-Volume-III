# 第三章 软检测器

现代硬盘信号处理系统已开始采用迭代解码系统进行数据解码。迭代解码系统的核心组件是软检测器 (soft detector) 和软解码器 (soft decoder)，它们通过相互交换软信息 (soft information) 来提高每一轮迭代的系统性能。正如第二章所述，BCJR 算法 [18] 是一种最大后验 (MAP: maximum a posteriori) 算法，在估计马尔可夫过程 (Markov process) 的状态或输出数据时是最优的 (optimal)。因此，在迭代解码系统被发明之初 [3]，BCJR 算法被用于构建软检测器和软解码器。

尽管 BCJR 算法中的状态度量 (state metric) 计算具有递归 (recursive) 特性，便于数据解码，但由于其计算资源消耗较高（例如大量的加法和乘法运算）、涉及非线性函数（如指数函数）计算，且对系统中的噪声方差较为敏感 [23, 24]，因此在许多实际的信号处理芯片应用中并不受欢迎。为此，研究人员开发了在对数域 (logarithm domain) 运行的类 MAP 算法 (MAP-like algorithm)，这些算法不仅能解决数值计算问题，而且复杂度远低于 BCJR 算法。

本章将详细阐述这些类 MAP 算法的工作原理，包括 Max-Log-MAP [23, 24, 38, 39]、Log-MAP [23, 24] 以及 SOVA (soft-output Viterbi algorithm) [19, 42]。这些算法的性能与 BCJR 算法接近或相当，本章还将展示它们的性能对比及复杂度分析。
计算方程 (3.4) 中的 $\tilde{\gamma}_k(u, q)$：

在方程 (2.29) 两边取自然对数，可得新的支路度量为：
$$ \tilde{\gamma}_k(u, q) = \ln \left( \frac{1}{\sqrt{2\pi\sigma^2}} \right) - \frac{1}{2\sigma^2} |y_k - \hat{r}(u, q)|^2 + \frac{\hat{a}(u, q) \lambda_a(a_k)}{2} \tag{3.10} $$

计算方程 (3.5) 中的 $\tilde{\alpha}_k(u)$：

在方程 (2.14) 两边取对数，得：
$$ \begin{array}{l} \tilde{\alpha}_{k+1}(q) = \ln(\alpha_{k+1}(q)) = \ln \left( \sum_{u=0}^{Q-1} \gamma_k(u, q) \alpha_k(u) \right) = \ln \left( \sum_{u=0}^{Q-1} e^{\ln(\gamma_k(u, q) \alpha_k(u))} \right) \\ = \ln \left( \sum_{u=0}^{Q-1} e^{\ln(\gamma_k(u, q)) + \ln(\alpha_k(u))} \right) \\ = \ln \left( \sum_{u=0}^{Q-1} e^{\tilde{\gamma}_k(u, q) + \tilde{\alpha}_k(u)} \right) \tag{3.11} \end{array} $$
根据方程 (3.1)，方程 (3.11) 可近似为：
$$ \tilde{\alpha}_{k+1}(q) \approx \max_{\forall u} \left( \tilde{\gamma}_k(u, q) + \tilde{\alpha}_k(u) \right) \tag{3.12} $$
其中 $q$ 为使状态图中的转移 $(u, q)$ 成立的所有状态。

计算方程 (3.6) 中的 $\tilde{\beta}_{k+1}(q)$：

在方程 (2.16) 两边取对数，得：
$$ \begin{array}{l} \tilde{\beta}_k(u) = \ln(\beta_k(u)) = \ln \left( \sum_{q=0}^{Q-1} \beta_{k+1}(q) \gamma_k(u, q) \right) = \ln \left( \sum_{q=0}^{Q-1} e^{\ln(\beta_{k+1}(q) \gamma_k(u, q))} \right) \\ = \ln \left( \sum_{q=0}^{Q-1} e^{\ln(\beta_{k+1}(q)) + \ln(\gamma_k(u, q))} \right) \\ = \ln \left( \sum_{q=0}^{Q-1} e^{\tilde{\beta}_{k+1}(q) + \tilde{\gamma}_k(u, q)} \right) \tag{3.13} \end{array} $$
同理，根据方程 (3.1)，方程 (3.13) 可近似为：
$$ \tilde{\beta}_k(u) \approx \max_{\forall q} \left( \tilde{\beta}_{k+1}(q) + \tilde{\gamma}_k(u, q) \right) \tag{3.14} $$
其中 $u$ 为使状态图中的转移 $(u, q)$ 成立的所有状态。

#### 3.2.1 Max-Log-MAP 算法工作流程总结

Max-Log-MAP 算法的工作步骤与图 2.12 中的 BCJR 算法基本相同，唯一的区别是 Max-Log-MAP 采用方程 (3.9) 来计算数据位 $a_k$ 的 LLR 值，而参数 $\tilde{\gamma}_k(u, q)$、$\tilde{\alpha}_k(u)$ 和 $\tilde{\beta}_{k+1}(q)$ 则分别通过方程 (3.10)、(3.12) 和 (3.14) 计算得到。图 3.2 总结了 Max-Log-MAP 算法的工作流程。

*注：在实际实现图 3.2 中的 Max-Log-MAP 算法时，不需要像 BCJR 算法那样对所有状态 $u$ 和所有时刻 $k$ 的状态度量 $\tilde{\alpha}_k(u)$ 和 $\tilde{\beta}_k(u)$ 进行归一化 (normalization)，因为 Max-Log-MAP 算法不会出现数值下溢 (numerical underflow) 问题。*
**Max-Log-MAP 算法步骤**

1. 设定状态度量的初始值 $[\tilde{\alpha}_0(0), \tilde{\alpha}_0(1), \dots, \tilde{\alpha}_0(Q-1)] = [0, -\infty, \dots, -\infty]$。
2. 前向递归 (forward recursion)：
   - 对于 $k = 0, 1, \dots, L + \nu - 1$：
     - 对于 $q = 0, 1, \dots, Q - 1$：
       - 根据方程 (3.10) 计算所有满足转移条件 $(u, q)$ 的 $\tilde{\gamma}_k(u, q)$。
       - 根据方程 (3.12) 计算 $\tilde{\alpha}_{k+1}(q)$。
3. 设定状态度量的初始值 $[\tilde{\beta}_{L+\nu}(0), \tilde{\beta}_{L+\nu}(1), \dots, \tilde{\beta}_{L+\nu}(Q-1)] = [0, -\infty, \dots, -\infty]$。
4. 后向递归 (backward recursion)：
   - 对于 $k = L + \nu - 1, L + \nu - 2, \dots, 0$：
     - 对于 $u = 0, 1, \dots, Q - 1$：
       - 根据方程 (3.10) 计算所有满足转移条件 $(u, q)$ 的 $\tilde{\gamma}_k(u, q)$。
       - 根据方程 (3.14) 计算 $\tilde{\beta}_k(u)$。
     - 根据方程 (3.9) 计算 $\lambda_p(a_k)$。
     - 根据方程 (2.25) 判定数据位 $\hat{a}_k$。
**示例 3.1** 参考示例 2.4，演示使用 Max-Log-MAP 算法对数据 $y_k$ 进行解码的步骤。设定数据位 $a_k$ 的先验信息为 $\lambda_a(a_k) = \{2, -2, 2, 0\}$。

**解**：根据示例 2.4，需要使用 Max-Log-MAP 算法检测的数据为：
$$ y_k = \{y_0, y_1, y_2, y_3\} = \{0.9, -0.2, 0.3, 0.6\} $$
信道 $H(D) = 1 + 0.5D$ 的状态图如图 2.13 所示，包含两个状态：状态 (a) 和状态 (b)。Max-Log-MAP 算法的解码步骤如下：

1. 设定状态度量的初始值 $\tilde{\alpha}_0(a) = 0$ 且 $\tilde{\alpha}_0(b) = -\infty$。

**前向递归**

2. 阶段 0（当 $k=0$ 时）：Max-Log-MAP 算法接收数据 $y_0 = 0.9$ 以及先验信息 $\lambda_a(a_0) = 2$，根据方程 (3.10) 计算图 2.13 中所有满足转移条件 $(u, q)$ 的支路度量 $\tilde{\gamma}_0(u, q)$，结果如下：
$$
\tilde {\gamma} _ {0} (a, a) = 0 - \pi | 0. 9 - (- 1. 5) | ^ {2} + \frac {(- 1) (2)}{2} \approx - 1 9. 0 9 5 6
$$
$$
\tilde {\gamma} _ {0} (b, a) = 0 - \pi \left| 0. 9 - (- 0. 5) \right| ^ {2} + \frac {(- 1) (2)}{2} \approx - 7. 1 5 7 5
$$
$$
\tilde {\gamma} _ {0} (a, b) = 0 - \pi | 0. 9 - (0. 5) | ^ {2} + \frac {(+ 1) (2)}{2} \approx 0. 4 9 7 3
$$
$$
\tilde {\gamma} _ {0} (b, b) = 0 - \pi | 0. 9 - (1. 5) | ^ {2} + \frac {(+ 1) (2)}{2} \approx - 0. 1 3 0 9
$$
已知 $\sigma^2 = 1/(2\pi)$，随后根据方程 (3.12) 调整状态度量：
$$
\begin{array}{l} \tilde {\alpha} _ {1} (a) = \max \left\{\tilde {\alpha} _ {0} (a) + \tilde {\gamma} _ {0} (a, a), \tilde {\alpha} _ {0} (b) + \tilde {\gamma} _ {0} (b, a) \right\} \\ = \max \left\{0 + (- 1 9. 0 9 5 6), - \infty + (- 7. 1 5 7 5) \right\} = - 1 9. 0 9 5 6 \\ \end{array}
$$
$$
\tilde {\alpha} _ {1} (b) = \max \left\{\tilde {\alpha} _ {0} (a) + \tilde {\gamma} _ {0} (a, b), \tilde {\alpha} _ {0} (b) + \tilde {\gamma} _ {0} (b, b) \right\}
$$
$$
= \max \left\{0 + (0. 4 9 7 3), - \infty + (- 0. 1 3 0 9) \right\} = 0. 4 9 7 3
$$

3. 阶段 1（当 $k=1$ 时）：Max-Log-MAP 算法接收数据 $y_1 = -0.2$ 以及先验信息 $\lambda_a(a_1) = -2$，计算所有支路度量如下：
$$
\tilde {\gamma} _ {1} (a, a) = 0 - \pi \left| - 0. 2 - (- 1. 5) \right| ^ {2} + \frac {(- 1) (- 2)}{2} \approx - 4. 3 0 9 3
$$
$$
\tilde {\gamma} _ {1} (b, a) = 0 - \pi \left| - 0. 2 - (- 0. 5) \right| ^ {2} + \frac {(- 1) (- 2)}{2} \approx 0. 7 1 7 3
$$
$$
\tilde {\gamma} _ {1} (a, b) = 0 - \pi \left| - 0. 2 - (0. 5) \right| ^ {2} + \frac {(+ 1) (- 2)}{2} \approx - 2. 5 3 9 4
$$
$$
\tilde {\gamma} _ {1} (b, b) = 0 - \pi | - 0. 2 - (1. 5) | ^ {2} + \frac {(+ 1) (- 2)}{2} \approx - 1 0. 0 7 9 2
$$
随后调整状态度量 $\tilde{\alpha}_2(a)$ 和 $\tilde{\alpha}_2(b)$：
$$
\begin{array}{l} \tilde {\alpha} _ {2} (a) = \max \left\{\tilde {\alpha} _ {1} (a) + \tilde {\gamma} _ {1} (a, a), \tilde {\alpha} _ {1} (b) + \tilde {\gamma} _ {1} (b, a) \right\} \\ = \max \left\{\left(- 1 9. 0 9 5 6\right) + (- 4. 3 0 9 3), (0. 4 9 7 3) + (0. 7 1 7 3) \right\} = 1. 2 1 4 6 \\ \end{array}
$$
$$
\begin{array}{l} \tilde {\alpha} _ {2} (b) = \max \left\{\tilde {\alpha} _ {1} (a) + \tilde {\gamma} _ {1} (a, b), \tilde {\alpha} _ {1} (b) + \tilde {\gamma} _ {1} (b, b) \right\} \\ = \max \left\{(- 1 9. 0 9 5 6) + (- 2. 5 3 9 4), (0. 4 9 7 3) + (- 1 0. 0 7 9 2) \right\} = - 9. 5 8 1 9 \\ \end{array}
$$

4. 阶段 2 和 3（当 $k \in \{2, 3\}$ 时）：Max-Log-MAP 算法接收数据 $\{y_2, y_3\} = \{0.3, 0.6\}$ 以及先验信息 $\{\lambda_a(a_2), \lambda_a(a_3)\} = \{2, 0\}$。采用与步骤 2 和 3 相同的方法计算支路度量并调整状态度量 $\tilde{\alpha}_{k+1}(q)$（其中 $q \in \{a, b\}$）。计算结果如图 3.3 所示，支路上的数值为对应的 $\tilde{\gamma}_k(u, q)$，状态节点上的数值表示状态度量 $\tilde{\alpha}_k(u)$ 与 $\tilde{\beta}_k(u)$ 的比值：
$$ \frac{\tilde{\alpha}_k(u)}{\tilde{\beta}_k(u)} $$
对于每个 $k \in \{0, 1, 2, 3\}$ 和 $u \in \{a, b\}$。前向递归结束时（归一化后）的结果为：
$$ \tilde{\alpha}_4(a) = -1.7124 \quad \text{且} \quad \tilde{\alpha}_4(b) = -0.4558 $$

5. 设定状态度量的初始值 $\tilde{\beta}_4(u) = \tilde{\alpha}_4(u)$（其中 $u \in \{a, b\}$），即：
$$ \tilde{\beta}_4(a) = -1.7124 \quad \text{且} \quad \tilde{\beta}_4(b) = -0.4558 $$

# 后向递归

6. 阶段 3（$k = 3$）：Max-Log-MAP 接收 $y_3 = 0.6$，$\lambda_a(a_3) = 0$，得 $\lambda_p(a_3) pprox 2.5132$，$\hat{a}_3 = +1$。

7. 阶段 2（$k = 2$）：接收 $y_2 = 0.3$，$\lambda_a(a_2) = 2$，得 $\lambda_p(a_2) pprox 9.5394$，$\hat{a}_2 = +1$。

8. 阶段 1 和 0：接收 $\{y_1, y_0\} = \{-0.2, 0.9\}$，$\{\lambda_a(a_0), \lambda_a(a_1)\} = \{2, -2\}$，得 $\lambda_p(a_0) = 24.221$，$\lambda_p(a_1) = -12.168$，$\hat{a}_0 = +1$，$\hat{a}_1 = -1$。

9. 最终结果：$\{\lambda_p(a_k)\} pprox \{24.22, -12.17, 9.54, 2.51\}$，$\{\hat{a}_k\} = \{1, -1, 1, 1\}$，与发送数据一致。

**例 3.2** 参考例 2.5，使用 Max-Log-MAP 解码 $y_k$，$\lambda_a(a_k) = \{1, -1, 2, 1, -1\}$。

**解**：$y_k = \{1.2, -0.7, -0.2, 0.5, -0.7\}$，信道 $H(D)=1-D^2$（四状态格图）。结果：$\{\lambda_p(a_k)\} pprox \{7.28, -26.65, 7.28, -10.57, 5.54\}$，$\{\hat{a}_k\} = \{1, -1, 1, -1, 1\}$，与发送数据一致。

# 3.2.2 Max-Log-MAP 算法的说明

Max-Log-MAP 使用公式 (3.1) 近似 BCJR 的状态度量，存在近似误差且沿序列传播。高 SNR 时误差小，低 SNR 时性能差 [24]。复杂度低于 BCJR 但性能也低。3.3 节的 Log-MAP 算法性能与 BCJR 相当，复杂度低得多。

# 3.3 Log-MAP 算法

Max-Log-MAP 的近似误差可通过雅可比对数 (Jacobian logarithm) [24, 38] 修正（证明见附录 A）：

$$
\ln(e^{\delta_1} + e^{\delta_2}) = \max(\delta_1, \delta_2) + \ln(1 + e^{-|\delta_1 - \delta_2|}) 	ag{3.15}
$$

其中 $\ln(1 + e^{-|\delta_1 - \delta_2|})$ 是修正项。将式 (3.15) 代入式 (3.1) 即可消除近似误差，使 Log-MAP 性能与 BCJR 相同。多个变量时递归应用：以 $\ln(e^{\delta_1} + 
Log-MAP 的前向递归为：

$$
	ilde{lpha}_{k+1}(q) = \max_{orall u}^* \left( 	ilde{lpha}_k(u) + 	ilde{\gamma}_k(u,q) ight) 	ag{3.16}
$$

后向递归为：

$$
	ilde{eta}_k(u) = \max_{orall q}^* \left( 	ilde{eta}_{k+1}(q) + 	ilde{\gamma}_k(u,q) ight) 	ag{3.17}
$$

其中 $\max^*$ 表示带修正的最大值运算。实际实现时需查表计算修正项，复杂度略高于 Max-Log-MAP 但远低于 BCJR [24]。

# 3.4 SOVA 算法

SOVA (Soft-Output Viterbi Algorithm) [19] 在维特比算法基础上增加软输出能力，为每个解码位提供 LLR 值。

## 3.4.1 数据位 LLR 的计算

SOVA 的路径度量与传统维特比算法相同。在每阶段选择幸存路径后，比较幸存路径与被淘汰路径的度量差，该差值近似为数据位的 LLR。

# 3.4.1 数据位 LLR 的计算 (续)

SOVA 算法可按如下方式求每位 LLR。考虑图 3.7 中第 k 阶段的格图。状态 q 在时间 k+1 的路径度量 $\Phi_{k+1}(q)$ 由下式求得：

$$
\Phi_{k+1}(q) = \ln\left(p(\mathbf{y}_0^k; \mathbf{a}_0^k)\right) \tag{3.24}
$$

其中 $\mathbf{y}_0^k = [y_0, y_1, \ldots, y_k]$ 是待解码序列，$\mathbf{a}_0^k = [a_0, a_1, \ldots, a_k]$ 是对应的输入序列。路径度量差定义为：

$$
\Delta_{k+1}(q) = \Phi_{k+1}^{(1)}(q) - \Phi_{k+1}^{(2)}(q) \tag{3.26}
$$

其中 $\Phi_{k+1}^{(1)}(q)$ 和 $\Phi_{k+1}^{(2)}(q)$ 是到达状态 q 的两条路径度量，且 $\Phi_{k+1}^{(1)}(q) > \Phi_{k+1}^{(2)}(q)$。正确决策概率为：

$$
\operatorname{Pr}[\text{correct decision at } \psi_{k+1}=q] = \frac{e^{\Delta_{k+1}(q)}}{1 + e^{\Delta_{k+1}(q)}} \tag{3.27}
$$

正确决策的 LLR 等于路径度量差：

$$
\mathrm{LLR} = \Delta_{k+1}(q) \tag{3.28}
$$

即维特比算法中汇合路径的度量差等于正确决策概率的 LLR 值。

# 3.4.2 SOVA 算法的说明

SOVA 的硬判决部分与维特比算法完全相同，软信息通过路径度量差获得。相比 BCJR，SOVA 无需后向递归，复杂度低，但软输出精度不如 BCJR。

# 3.4.3 SOVA 算法步骤总结

SOVA 算法步骤见图 3.8，核心思路：
1. 硬解码：标准维特比前向搜索，每阶段选幸存路径
2. 软解码：对每位计算路径度量差作为 LLR

# SOVA 算法

## 硬解码（同维特比 [1]）

1. 初始化路径度量 $[\Phi_0(0), \ldots, \Phi_0(Q-1)] = [0, -\infty, \ldots, -\infty]$
2. 对 $k = 0, 1, \ldots, L+\nu-1$：
   - 对 $q = 0, 1, \ldots, Q-1$：
     - 计算分支度量 $\tilde{\gamma}_k(u,q)$
     - 计算 $\Phi_{k+1}(q) = \max_u(\Phi_k(u) + \tilde{\gamma}_k(u,q))$
     - 存储幸存路径
3. 回溯，输出硬判决 $\hat{a}_k$

## 软解码（LLR 计算）

4. 对每阶段 k，对汇合路径计算 $\Delta_{k+1}(q) = \Phi_{k+1}^{(1)}(q) - \Phi_{k+1}^{(2)}(q)$
5. 将 $\Delta$ 沿幸存路径回溯，对每位取最小值作为 LLR 估计

# 3.5 双向 SOVA 算法

双向 SOVA (Bi-Directional SOVA) 同时进行前向和后向搜索，利用两个方向的路径度量差提高 LLR 估计的可靠性。

## 3.5.1 数据位 LLR 的计算

前向搜索与标准 SOVA 相同，得前向幸存路径和路径度量差 $\Delta_{k+1}^f(q)$。后向搜索反向进行，得后向幸存路径和 $\Delta_k^b(u)$。综合双向信息，数据位 $a_k$ 的 LLR 为：

$$
\lambda_p(a_k) \approx \text{function of both } \Delta^f \text{ and } \Delta^b \tag{3.x}
$$

双向 SOVA 比标准 SOVA 提供更精确的软信息，接近 Log-MAP 性能，但需额外存储后向度量。

## 3.5.2 双向 SOVA 算法步骤总结

# 双向 SOVA 算法

## 硬解码（同维特比）
1. 前向初始化和递归（同 SOVA）
2. 后向初始化：$[\beta_{L+\nu}(0), \ldots] = [0, -\infty, \ldots]$
3. 后向递归：$k = L+\nu-1, \ldots, 0$，对每个 $u$ 计算
4. 结合前后向路径得最优解码路径

## 软解码（LLR 计算）
5. 前向 LLR：路径度量差 $\Delta_{k+1}^f(q)$
6. 后向 LLR：路径度量差 $\Delta_k^b(u)$
7. 综合双向信息得最终 LLR 估计

# 3.6 软检测器的复杂度

| 算法 | 前向递归 | 后向递归 | 软输出质量 | 相对复杂度 |
|------|---------|---------|-----------|-----------|
| BCJR | 是 | 是 | 最优 | 高 (基准) |
| Log-MAP | 是 | 是 | 与 BCJR 相同 | 中 (需查表) |
| Max-Log-MAP | 是 | 是 | 近似 | 中低 |
| SOVA | 是 | 否 | 近似 | 低 |
| 双向 SOVA | 是 | 是 | 较好 | 中 |

BCJR 复杂度最高但性能最优；SOVA 复杂度最低但软输出精度有限；Log-MAP 在复杂度和性能间取得最佳平衡。

# 3.7 本章小结

本章介绍了用于迭代解码系统的软检测算法。Max-Log-MAP 通过对数域 max 近似降低 BCJR 复杂度；Log-MAP 用雅可比对数修正近似误差，获得与 BCJR 相同的性能；SOVA 在维特比基础上提供软输出，无需后向递归；双向 SOVA 结合前后向信息提高精度。实际系统需在复杂度和性能间权衡。

# 3.8 本章习题

1. 推导 Max-Log-MAP 的前向递归公式 (3.12)。
2. 推导 Log-MAP 的雅可比对数公式 (3.15)。
3. 比较 BCJR、Max-Log-MAP 和 Log-MAP 在 AWGN 信道下的 BER 性能。
4. 解释 SOVA 路径度量差 $\Delta_{k+1}(q)$ 的物理意义。
5. 证明双向 SOVA 的 LLR 估计优于标准 SOVA。
6. 对例 3.1 中的系统使用 Log-MAP 算法重新解码，并与 Max-Log-MAP 结果比较。
7. 设计一个 $H(D) = 1 + D$ 的 2 状态信道，使用 SOVA 算法解码 $a_k = \{1, -1, 1\}$ 受 AWGN 干扰的信号。
8. 解释为什么 SOVA 不需要后向递归而 BCJR 需要。
9. 推导公式 (3.27) 中正确决策概率与 $\Delta$ 的关系。
10. 对比所有五种检测器（BCJR、Log-MAP、Max-Log-MAP、SOVA、双向 SOVA）的优缺点。
