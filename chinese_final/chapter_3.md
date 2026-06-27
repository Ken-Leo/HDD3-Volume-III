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
