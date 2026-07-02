## 第三章

## 软检测器

当前硬盘驱动器的信号处理系统开始采用迭代解码系统进行数据解码。迭代解码系统中的关键组件是软检测器（soft detector）和软解码器（soft decoder），它们在彼此之间交换软信息（soft information），以帮助系统性能在每次迭代中逐步提升。如第二章所述，BCJR算法[18]是一种最大后验（MAP: maximum a posteriori）算法，对于估计马尔可夫过程的状态或输出是最优的。因此，在迭代解码系统[3]最初被提出时，就采用了BCJR算法来构建软检测器和软解码器。

尽管BCJR算法中状态度量的计算具有递归性质，使得数据解码较为简单，然而BCJR算法在许多实际应用的信号处理芯片中并不常用，因为它计算资源消耗高（例如加法和乘法的运算次数），需要使用非线性函数进行计算（例如指数函数），并且对系统中的噪声方差敏感[23, 24]。因此，研究人员开发了在对数域中工作的类MAP算法（MAP-like algorithm），这些算法能够解决数值计算问题，并且复杂度远低于BCJR算法。

本章将介绍这些类MAP算法的工作原理，包括Max-Log-MAP[23, 24, 38, 39]、Log-MAP[23, 24]和SOVA（软输出维特比算法）[19, 42]，它们的性能接近或等同于BCJR算法，同时还将展示所有算法的性能并比较其复杂度。

![](images/chapter_3/16478bf0024cb8345da28a410d528f6c5a435a2e49eb076e050e604a727526b2.jpg)  
图3.1 MAP、Log-MAP、Max-Log-MAP和SOVA的关系

## 3.1 引言

维特比检测器[10, 13]是一种最大似然（ML: maximum-likelihood）检测器，其输出是对所需检测数据序列的估计，或者说ML检测器能使数据序列的误差最小化。然而，它不能保证数据序列中每个数据比特是最佳的。维特比检测器不能用于迭代解码系统，因为该系统需要在SISO（软输入软输出）检测器和SISO解码器之间交换软信息（或数据比特的可信度）。

BCJR算法是一种MAP算法，在早期被用于迭代解码系统。然而，BCJR算法在许多实际应用的信号处理芯片中存在局限。因此，研究人员开发了Max-Log-MAP和SOVA算法，其性能接近BCJR算法。随后又开发了Log-MAP算法，其性能等同于BCJR算法但复杂度低得多，因此可以在信号处理芯片中实际使用。图3.1展示了MAP算法和类MAP算法的关系。

## 3.2 Max-Log-MAP算法

Max-Log-MAP算法[23, 24, 38, 39]是从BCJR算法发展而来的，它利用最大值函数（maximum function）和对数函数（logarithm function），主要目的是使其能够在实际应用中实现（即在信号处理芯片中使用），同时保持接近BCJR算法的性能。通常Max-Log-MAP算法被认为是次优算法，其输出的软信息质量劣于BCJR算法输出的软信息。

根据第2.2节中BCJR算法的信道模型和方程，使Max-Log-MAP算法便于实际使用的形式将利用对数恒等式 $$x _ { i } = e ^ { \ln ( x _ { i } ) }$$ 和对数近似公式[24]：

$$
\ln \left( e ^ { x _ { 1 } } + e ^ { x _ { 2 } } + . . . + e ^ { x _ { n } } ight) pprox \operatorname* { m a x } _ { i \in \{ 1 , . . . , n \} } ( x _ { i } )	ag{3.1}
$$

其中 $$x _ { i }$$ 是实数，$$n$$ 是正整数。因此，数据比特 $$a _ { k }$$ 的LR值在方程(2.24)中可重新整理为：

$$
\lambda _ { p } \left( a _ { k } ight) = \ln \left( \sum _ { \left( u , q ight) \in S _ { 1 } } lpha _ { k } \left( u ight) \gamma _ { k } \left( u , q ight) eta _ { k + 1 } \left( q ight) ight) - \ln \left( \sum _ { \left( u , q ight) \in S _ { - 1 } } lpha _ { k } \left( u ight) \gamma _ { k } \left( u , q ight) eta _ { k + 1 } \left( q ight) ight)	ag{3.2}
$$

考虑方程(3.2)右侧第一项：

$$
egin{array} { r l } { \displaystyle \operatorname { l n i m } \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } lpha _ { k } \left( u ight) \cap _ { \mathbb { H } } \left( u , q ight) eta _ { k + 1 } \left( q ight) ight) = \ln \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } e ^ { \ln ( lpha _ { k } \left( u ight) \cdot \hat { \gamma } _ { \mathbb { H } } \left( u , q ight) eta _ { k + 1 } \left( q ight) ) } ight) } & { } \ { = \ln \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } e ^ { \ln ( lpha _ { \mathbb { H } } \left( u ight) ) + \ln \left( \gamma _ { \mathbb { H } } \left( u , q ight) ight) + \ln \left( eta _ { k + 1 } \left( q ight) ight) } ight) } & { } \ { = \ln \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } e ^ { ar { lpha } _ { k } \left( u ight) + ar { \gamma } _ { \mathbb { H } } \left( u , q ight) + ar { \gamma } _ { \mathbb { H } + 1 } \left( q ight) } ight) } & { } \end{array}	ag{3.3}
$$

其中：

$$
	ilde { \gamma } _ { k } \left( u , q ight) = \ln \left( \gamma _ { k } \left( u , q ight) ight)	ag{3.4}
$$

$$
	ilde { lpha } _ { k } \left( u ight) = \ln \left( lpha _ { k } \left( u ight) ight)	ag{3.5}
$$

$$
\widetilde { eta } _ { k + 1 } \left( q ight) = \ln \left( eta _ { k + 1 } \left( q ight) ight)	ag{3.6}
$$

根据方程(3.1)，可近似计算方程(3.3)为：

$$
\ln \left( \sum _ { ( u , q ) \in S _ { 1 } } lpha _ { k } \left( u ight) \gamma _ { k } \left( u , q ight) eta _ { k + 1 } \left( q ight) ight) pprox \operatorname* { m a x } _ { \left( u , q ight) \in S _ { 1 } } \left( 	ilde { lpha } _ { k } \left( u ight) + 	ilde { \gamma } _ { k } \left( u , q ight) + 	ilde { eta } _ { k + 1 } \left( q ight) ight)	ag{3.7}
$$

类似地，方程(3.2)右侧第二项为：

$$
\ln \left( \sum _ { \left( u , q ight) \in S _ { - 1 } } lpha _ { k } \left( u ight) \gamma _ { k } \left( u , q ight) eta _ { k + 1 } \left( q ight) ight) pprox \operatorname* { m a x } _ { \left( u , q ight) \in S _ { - 1 } } \left( 	ilde { lpha } _ { k } \left( u ight) + 	ilde { \gamma } _ { k } \left( u , q ight) + 	ilde { eta } _ { k + 1 } \left( q ight) ight)	ag{3.8}
$$

将方程(3.7)和(3.8)代入方程(3.2)，得到Max-Log-MAP算法的数据比特 $$a _ { k }$$ 的LLR值为：

$$
\lambda _ { p } \left( a _ { k } ight) pprox \operatorname* { m a x } _ { \left( u , q ight) \in S _ { 1 } } \left( 	ilde { lpha } _ { k } \left( u ight) + 	ilde { \gamma } _ { k } \left( u , q ight) + 	ilde { eta } _ { k + 1 } \left( q ight) ight) - \operatorname* { m a x } _ { \left( u , q ight) \in S _ { - 1 } } \left( 	ilde { lpha } _ { k } \left( u ight) + 	ilde { \gamma } _ { k } \left( u , q ight) + 	ilde { eta } _ { k + 1 } \left( q ight) ight)	ag{3.9}
$$

## 计算方程(3.4)中的 $$	ilde { \gamma } _ { k } \left( u , q ight)$$

对方程(2.29)两边取自然对数，得到新的分支度量：

$$
\widetilde { \gamma } _ { k } \left( u , q ight) = \ln \left( { rac { 1 } { \sqrt { 2 \pi \sigma ^ { 2 } } } } ight) - { rac { 1 } { 2 \sigma ^ { 2 } } } igl ert y _ { k } - \widehat { r } \left( u , q ight) igr ert ^ { 2 } + { rac { \hat { a } \left( u , q ight) \lambda _ { a } \left( a _ { k } ight) } { 2 } }	ag{3.10}
$$

## 计算方程(3.5)中的 \tilde { \alpha } _ { k } \left( u \right)

对方程(2.14)两边取对数，可得：

$$
\widetilde { \alpha } _ { k + 1 } \left( q \right) = \ln \left( \sum _ { u = 0 } ^ { Q - 1 } e ^ { \widetilde { \gamma } _ { k } \left( u , q \right) + \widetilde { \alpha } _ { k } \left( u \right) } \right)	ag{3.11}
$$

## 计算方程(3.5)中的 \tilde{\alpha}_k(u)

对方程(2.14)两边取对数，可得：

$$
\widetilde{\alpha}_{k+1}(q) = \ln\left(\sum_{u=0}^{Q-1} e^{\widetilde{\gamma}_k(u,q) + \widetilde{\alpha}_k(u)}\right)\tag{3.11}
$$


## 计算方程(3.5)中的 $\tilde { \alpha } _ { k } \left( u \right)$

对方程(2.14)两边取对数，可得：

$$
\widetilde { \alpha } _ { k + 1 } \left( q \right) = \ln \left( \sum _ { u = 0 } ^ { Q - 1 } e ^ { \widetilde { \gamma } _ { k } \left( u , q \right) + \widetilde { \alpha } _ { k } \left( u \right) } \right)\tag{3.11}
$$

根据方程(3.1)，可近似计算方程(3.11)为：

$$
\tilde { \alpha } _ { k + 1 } \left( q \right) \approx \max _ { \forall u } \left( \tilde { \gamma } _ { k } \left( u , q \right) + \tilde { \alpha } _ { k } \left( u \right) \right)\tag{3.12}
$$

对于所有在网格图中使状态转移(u, q)为真的状态q。

## 计算方程(3.6)中的 $\widetilde { \beta } _ { k + 1 } \left( q \right)$

对方程(2.16)两边取对数，可得：

$$
\widetilde { \beta } _ { k } \left( u \right) = \ln \left( \sum _ { q = 0 } ^ { Q - 1 } e ^ { \widetilde { \beta } _ { k + 1 } \left( q \right) + \widetilde { \gamma } _ { k } \left( u , q \right) } \right)\tag{3.13}
$$

同样地，根据方程(3.1)，可近似计算方程(3.13)为：

$$
\tilde { \beta } _ { k } \left( u \right) \approx \max _ { \forall q } \left( \tilde { \beta } _ { k + 1 } \left( q \right) + \tilde { \gamma } _ { k } \left( u , q \right) \right)\tag{3.14}
$$

对于所有在网格图中使状态转移(u, q)为真的状态u。


## 3.2.1 Max-Log-MAP算法步骤总结

Max-Log-MAP算法的操作步骤与图2.12中的BCJR算法相同，唯一的区别在于Max-Log-MAP算法使用方程(3.9)计算数据比特 $a_k$ 的LLR值，其中参数 $\tilde{\gamma}_k(u,q)$、$\tilde{\alpha}_k(u)$ 和 $\tilde{\beta}_{k+1}(q)$ 分别由方程(3.10)、(3.12)和(3.14)求得。图3.2总结了Max-Log-MAP算法的操作步骤。

**注意：** 在实际应用中使用图3.2中的Max-Log-MAP算法时，无需对每个状态u和每个时刻k的状态度量 $\tilde{\alpha}_k(u)$ 和 $\tilde{\beta}_k(u)$ 进行归一化处理，这与BCJR算法中所做的不同，因为Max-Log-MAP算法不会遇到数值下溢问题。

**Max-Log-MAP算法步骤**

1. 初始化状态度量 $\left[ \tilde{\alpha}_0(0), \tilde{\alpha}_0(1), ..., \tilde{\alpha}_0(Q-1) \right] = \left[ 0, -\infty, ..., -\infty \right]$
2. 前向递归 (forward recursion)
   - 对于 $k = 0, 1, ..., L + \nu - 1$
   - 对于 $q = 0, 1, ..., Q - 1$
     - 根据方程(3.10)计算 $\tilde{\gamma}_k(u,q)$，对于所有使(u,q)为真的u
     - 根据方程(3.12)计算 $\tilde{\alpha}_{k+1}(q)$
3. 初始化状态度量 $\left[ \tilde{\beta}_{L+\nu}(0), \tilde{\beta}_{L+\nu}(1), ..., \tilde{\beta}_{L+\nu}(Q-1) \right] = \left[ 0, -\infty, ..., -\infty \right]$
4. 后向递归 (backward recursion)
   - 对于 $k = L + \nu - 1, L + \nu - 2, ..., 0$
   - 对于 $u = 0, 1, ..., Q - 1$
     - 根据方程(3.10)计算 $\tilde{\gamma}_k(u,q)$，对于所有使(u,q)为真的q
     - 根据方程(3.14)计算 $\tilde{\beta}_k(u)$
   - 根据方程(3.9)计算 $\lambda_p(a_k)$
   - 根据方程(2.25)判决 $a_k$

**例3.1** 从例2.4出发，请展示如何使用Max-Log-MAP算法解码数据 $y_k$，设数据比特 $a_k$ 的先验信息为 $\lambda_a(a_k) = \{2, -2, 2, 0\}$。

解：从例2.4知需要检测的数据为：
$$y_k = \{y_0, y_1, y_2, y_3\} = \{0.9, -0.2, 0.3, 0.6\}$$

信道 $H(D) = 1 + 0.5D$ 的网格图如图2.13所示，有两个状态：(a)和(b)。

1. 初始化状态度量 $\tilde{\alpha}_0(a) = 0$ 和 $\tilde{\alpha}_0(b) = -\infty$

## 前向递归

**阶段0 (k=0):** 算法接收 $y_0 = 0.9$ 和 $\lambda_a(a_0) = 2$，根据方程(3.10)计算分支度量：

$$
\widetilde{\gamma}_0(a,a) = 0 - \frac{1}{2\sigma^2} |0.9 - (-1.5)|^2 + \frac{(-1)(2)}{2} \approx -19.0956
$$

**阶段1 (k=1):** 继续计算剩余分支度量和状态度量...


$$
\widetilde{\gamma}_0(b,a) = 0 - \pi |0.9 - (-0.5)|^2 + \frac{(-1)(2)}{2} \approx -7.1575
$$

$$
\widetilde{\gamma}_0(a,b) = 0 - \pi |0.9 - (0.5)|^2 + \frac{(+1)(2)}{2} \approx 0.4973
$$

$$
\widetilde{\gamma}_0(b,b) = 0 - \pi |0.9 - (1.5)|^2 + \frac{(+1)(2)}{2} \approx -0.1309
$$

由于 $\sigma^2 = 1/(2\pi)$，然后根据方程(3.12)更新状态度量：

$$
\begin{array} { r l } & { \tilde{\alpha}_1(a) = \max \{ \tilde{\alpha}_0(a) + \tilde{\gamma}_0(a,a), \ \tilde{\alpha}_0(b) + \tilde{\gamma}_0(b,a) \} } \\ & { \qquad = \max \{ 0 + (-19.0956), \ -\infty + (-7.1575) \} = -19.0956 } \end{array}
$$

$$
\begin{array} { c } { { \tilde{\alpha}_1(b) = \max \{ \tilde{\alpha}_0(a) + \tilde{\gamma}_0(a,b), \ \tilde{\alpha}_0(b) + \tilde{\gamma}_0(b,b) \} } } \\ { { = \max \{ 0 + (0.4973), \ -\infty + (-0.1309) \} = 0.4973 } } \end{array}
$$

**阶段1 (k=1):** 接收 $y_1 = -0.2$ 和 $\lambda_a(a_1) = -2$，计算所有分支度量：

$$
\widetilde{\gamma}_1(a,a) = 0 - \pi |-0.2 - (-1.5)|^2 + \frac{(-1)(-2)}{2} \approx -4.3093
$$

$$
\widetilde{\gamma}_1(b,a) = 0 - \pi |-0.2 - (-0.5)|^2 + \frac{(-1)(-2)}{2} \approx 0.7173
$$

$$
\widetilde{\gamma}_1(a,b) = 0 - \pi |-0.2 - (0.5)|^2 + \frac{(+1)(-2)}{2} \approx -2.5394
$$

$$
\widetilde{\gamma}_1(b,b) = 0 - \pi |-0.2 - (1.5)|^2 + \frac{(+1)(-2)}{2} \approx -10.0792
$$

更新状态度量 $\tilde{\alpha}_2(a)$ 和 $\tilde{\alpha}_2(b)$：

$$
\begin{array} { r l } & { \tilde{\alpha}_2(a) = \max \{ \tilde{\alpha}_1(a) + \tilde{\gamma}_1(a,a), \ \tilde{\alpha}_1(b) + \tilde{\gamma}_1(b,a) \} } \\ & { \qquad = \max \{ (-19.0956) + (-4.3093), \ (0.4973) + (0.7173) \} = 1.2146 } \end{array}
$$

$$
\begin{array} { r l } & { \tilde{\alpha}_2(b) = \max \{ \tilde{\alpha}_1(a) + \tilde{\gamma}_1(a,b), \ \tilde{\alpha}_1(b) + \tilde{\gamma}_1(b,b) \} } \\ & { \qquad = \max \{ (-19.0956) + (-2.5394), \ (0.4973) + (-10.0792) \} = -9.5819 } \end{array}
$$

**阶段2和3 (k={2,3}):** 接收数据 $\{ y_2, y_3 \} = \{ 0.3, 0.6 \}$ 和 $\{ \lambda_a(a_2), \lambda_a(a_3) \} = \{ 2, 0 \}$，按上述相同方法计算所有分支度量和状态度量 $\tilde{\alpha}_{k+1}(q)$，结果如图3.3所示。图中每条分支旁的值对应 $\tilde{\gamma}_k(u,q)$，各状态节点处的分数形式中的数字表示 $\tilde{\alpha}_k(u)$ 和 $\tilde{\beta}_k(u)$：

$$
\frac { \tilde { \alpha } _ { k } \left( u \right) } { \tilde { \beta } _ { k } \left( u \right) }
$$

对于 $k \in \{0,1,2,3\}$ 和 $u \in \{a,b\}$。前向递归结束时的结果为：

$$
\tilde{\alpha}_4(a) = -1.7124 \quad \tilde{\alpha}_4(b) = -0.4558
$$

5. 初始化后向状态度量 $\tilde{\beta}_4(u) = \tilde{\alpha}_4(u)$，对于 $u \in \{a,b\}$：

$$
\tilde{\beta}_4(a) = -1.7124 \quad \tilde{\beta}_4(b) = -0.4558
$$

## 后向递归

**阶段3 (k=3):** 接收 $y_3 = 0.6$ 和 $\lambda_a(a_3) = 0$，计算所有分支度量：

$$
\begin{array} { l } { \displaystyle \tilde{\gamma}_3(a,a) = 0 - \pi |0.6 - (-1.5)|^2 + \frac{(-1)(0)}{2} \approx -13.8544 } \\ { \displaystyle \tilde{\gamma}_3(b,a) = 0 - \pi |0.6 - (-0.5)|^2 + \frac{(-1)(0)}{2} \approx -3.8013 } \\ { \displaystyle \tilde{\gamma}_3(a,b) = 0 - \pi |0.6 - (0.5)|^2 + \frac{(+1)(0)}{2} \approx -0.0314 } \\ { \displaystyle \tilde{\gamma}_3(b,b) = 0 - \pi |0.6 - (1.5)|^2 + \frac{(+1)(0)}{2} \approx -2.5447 } \end{array}
$$

更新状态度量 $\tilde{\beta}_3(a)$ 和 $\tilde{\beta}_3(b)$：

$$
\begin{array} { r l } & { \tilde{\beta}_3(a) = \max \{ \tilde{\gamma}_3(a,a) + \tilde{\beta}_4(a), \ \tilde{\gamma}_3(a,b) + \tilde{\beta}_4(b) \} } \\ & { \qquad = \max \{ (-13.8544) + (-1.7124), \ (-0.0314) + (-0.4558) \} = -0.4872 } \end{array}
$$

$$
\begin{array} { r l } & { \tilde{\beta}_3(b) = \max \{ \tilde{\gamma}_3(b,a) + \tilde{\beta}_4(a), \ \tilde{\gamma}_3(b,b) + \tilde{\beta}_4(b) \} } \\ & { \qquad = \max \{ (-3.8013) + (-1.7124), \ (-2.5447) + (-0.4558) \} = -3.0005 } \end{array}
$$

然后根据方程(3.9)计算 $\lambda_p(a_3)$：

$$
\begin{array} { r l } & { \lambda_p(a_3) \approx \max \{ (\tilde{\alpha}_3(a) + \tilde{\gamma}_3(a,b) + \tilde{\beta}_4(b)), \ (\tilde{\alpha}_3(b) + \tilde{\gamma}_3(b,b) + \tilde{\beta}_4(b)) \} } \\ & { \qquad - \max \{ (\tilde{\alpha}_3(a) + \tilde{\gamma}_3(a,a) + \tilde{\beta}_4(a)), \ (\tilde{\alpha}_3(b) + \tilde{\gamma}_3(b,a) + \tilde{\beta}_4(a)) \} } \\ & { \qquad = \max \{ (-9.9642 - 0.0314 - 0.4558), \ (2.0889 - 2.5447 - 0.4558) \} } \\ & { \qquad - \max \{ (-9.9642 - 13.8544 - 1.7124), \ (2.0889 - 3.8013 - 1.7124) \} } \\ & { \qquad = (-0.9116) - (-3.4248) = 2.5132 } \end{array}
$$


由于 $\lambda_p(a_3) > 0$，Max-Log-MAP算法解码数据比特为 $\hat{a}_3 = +1$。

**阶段2 (k=2):** 接收 $y_2 = 0.3$ 和 $\lambda_a(a_2) = 2$，计算所有分支度量：

$$
\widetilde{\gamma}_2(a,a) = 0 - \pi |0.3 - (-1.5)|^2 + \frac{(-1)(2)}{2} \approx -11.1788
$$

$$
\widetilde{\gamma}_2(b,a) = 0 - \pi |0.3 - (-0.5)|^2 + \frac{(-1)(2)}{2} \approx -3.0106
$$

$$
\widetilde{\gamma}_2(a,b) = 0 - \pi |0.3 - (0.5)|^2 + \frac{(+1)(2)}{2} \approx 0.8743
$$

$$
\widetilde{\gamma}_2(b,b) = 0 - \pi |0.3 - (1.5)|^2 + \frac{(+1)(2)}{2} \approx -3.5239
$$

更新状态度量 $\tilde{\beta}_2(a)$ 和 $\tilde{\beta}_2(b)$：

$$
\begin{array} { r l } & { \tilde{\beta}_2(a) = \max \{ \tilde{\gamma}_2(a,a) + \tilde{\beta}_3(a), \ \tilde{\gamma}_2(a,b) + \tilde{\beta}_3(b) \} } \\ & { \qquad = \max \{ (-11.1788) + (-0.4872), \ (0.8743) + (-3.0005) \} = -2.1262 } \end{array}
$$

$$
\begin{array} { r l } & { \tilde{\beta}_2(b) = \max \{ \tilde{\gamma}_2(b,a) + \tilde{\beta}_3(a), \ \tilde{\gamma}_2(b,b) + \tilde{\beta}_3(b) \} } \\ & { \qquad = \max \{ (-3.0106) + (-0.4872), \ (-3.5239) + (-3.0005) \} = -3.4978 } \end{array}
$$

根据方程(3.9)计算 $\lambda_p(a_2)$：

$$
\begin{array} { r l } & { \lambda_p(a_2) \approx \max \{ (\tilde{\alpha}_2(a) + \tilde{\gamma}_2(a,b) + \tilde{\beta}_3(b)), \ (\tilde{\alpha}_2(b) + \tilde{\gamma}_2(b,b) + \tilde{\beta}_3(b)) \} } \\ & { \qquad - \max \{ (\tilde{\alpha}_2(a) + \tilde{\gamma}_2(a,a) + \tilde{\beta}_3(a)), \ (\tilde{\alpha}_2(b) + \tilde{\gamma}_2(b,a) + \tilde{\beta}_3(a)) \} } \\ & { = \max \{ (1.2146 + 0.8743 - 3.0005), \ (-9.5819 - 3.5239 - 3.0005) \} } \\ & { \qquad - \max \{ (1.2146 - 11.1788 - 0.4872), \ (-9.5819 - 3.0106 - 0.4872) \} } \\ & { = (-0.9116) - (-10.451) = 9.5394 } \end{array}
$$

由于 $\lambda_p(a_2) > 0$，Max-Log-MAP算法解码数据比特为 $\hat{a}_2 = +1$。

**阶段1和0 (k={1,0}):** 接收数据 $\{ y_1, y_0 \} = \{ -0.2, 0.9 \}$ 和 $\{ \lambda_a(a_0), \lambda_a(a_1) \} = \{ 2, -2 \}$，按相同方法计算所有分支度量并更新状态度量 $\tilde{\beta}_k(u)$，结果如图3.3所示。后向递归结束时得到：

$$
\lambda_p(a_0) = 24.221 \quad \lambda_p(a_1) = -12.168
$$

即Max-Log-MAP算法解码数据比特 $a_0$ 和 $a_1$ 为 $\hat{a}_0 = +1$ 和 $\hat{a}_1 = -1$。

9. 算法结束时，Max-Log-MAP算法输出的数据比特 $a_k$ 的MAP-LLR值为 $\{ \lambda_p(a_0), \lambda_p(a_1), \lambda_p(a_2), \lambda_p(a_3) \} \approx \{ 24.22, -12.17, 9.54, 2.51 \}$，解码数据比特为 $\{ \hat{a}_0, \hat{a}_1, \hat{a}_2, \hat{a}_3 \} = \{ 1, -1, 1, 1 \}$（最后一个比特在系统中并非真实存在，而是卷积运算产生的结果），这与发射端发送的数据比特 $\{ a_k \}$ 一致，表明使用Max-Log-MAP算法进行数据解码未发生错误。

**例3.2** 从例2.5出发，请使用Max-Log-MAP算法解码数据 $y_k$，设数据比特 $a_k$ 的先验信息为 $\lambda_a(a_k) = \{ 1, -1, 2, 1, -1 \}$。

解：从例2.5可知，需要使用Max-Log-MAP算法检测的数据为：

$$
y_k = \{ y_0, y_1, y_2, y_3, y_4 \} = \{ 1.2, -0.7, -0.2, 0.5, -0.7 \}
$$

信道 $H(D) = 1 - D^2$ 的网格图如图2.15所示，共有四个状态：状态(a)、(b)、(c)和(d)。


从图3.4中的分支度量和状态度量，根据方程(3.9)可计算数据比特 $a_k$ 的MAP-LLR值：

$$
\{ \lambda_p(a_0), \lambda_p(a_1), \lambda_p(a_2), \lambda_p(a_3), \lambda_p(a_4) \} \approx \{ 7.28, -26.65, 7.28, -10.57, 5.54 \}
$$

解码数据比特为：

$$
\{ \hat{a}_0, \hat{a}_1, \hat{a}_2, \hat{a}_3, \hat{a}_4 \} = \{ 1, -1, 1, -1, 1 \}
$$

与发射端发送的数据比特 $\{ a_k \}$ 一致（最后两个比特在系统中并非真实存在，而是输入数据与信道卷积产生的结果），表明使用Max-Log-MAP算法进行数据解码未发生错误。

## 3.2.2 对Max-Log-MAP算法的观察

如上所述，Max-Log-MAP算法利用方程(3.1)中的最大值函数来近似BCJR算法的状态度量 $\alpha_k(u)$ 和 $\beta_{k+1}(q)$。因此，Max-Log-MAP算法不可避免地会面临近似误差，并且由于两个状态度量在每个时刻都是递归计算的，近似误差会沿整个数据序列 $y$ 传播。

一般来说，当Max-Log-MAP算法在高SNR下工作时，近似误差问题较小。然而，当在低SNR下工作时，Max-Log-MAP算法的性能较差（因为近似误差的幅度与系统中的噪声相当[24]，并且面临近似误差传播问题）。尽管Max-Log-MAP算法的复杂度低于BCJR算法，但其性能也明显劣于BCJR算法。因此，在选择使用哪种算法时，用户需要在复杂度和可接受的性能之间进行权衡。然而，第3.3节将介绍Log-MAP算法，该算法从Max-Log-MAP算法发展而来，性能等同于BCJR算法，但复杂度低得多。

## 3.3 Log-MAP算法

由于Max-Log-MAP算法使用方程(3.1)来近似BCJR算法的各种参数，因此面临近似误差问题，导致性能劣于BCJR算法。然而，方程(3.1)中的近似误差可以通过使用雅可比对数（Jacobian logarithm）[24, 38]来纠正（参见附录A的证明）：

$$
\begin{array} { r } { \ln \left( e ^ { x _ { 1 } } + e ^ { x _ { 2 } } \right) = \max \left( x _ { 1 } , x _ { 2 } \right) + \ln \left( 1 + e ^ { - \left| x _ { 1 } - x _ { 2 } \right| } \right) } \\ { = \max \left( x _ { 1 } , x _ { 2 } \right) + f _ { c } \left( \left| x _ { 1 } - x _ { 2 } \right| \right) } \end{array}\tag{3.15}
$$

其中 $f_c(|x_1 - x_2|) = \ln(1 + e^{-|x_1 - x_2|})$ 是纠错函数。此外，为便于解释Log-MAP算法的工作原理，定义新的最大值函数如下：

$$
\max^* \left( x _ { 1 } , x _ { 2 } \right) = \max \left( x _ { 1 } , x _ { 2 } \right) + f _ { c } \left( \left| x _ { 1 } - x _ { 2 } \right| \right)\tag{3.16}
$$

因此，方程(3.1)中的 $\ln(e^{x_1} + e^{x_2} + ... + e^{x_n})$ 可以通过以下方式精确计算。设已知值 $x$，且有 $x = \ln(e^{x_1} + e^{x_2} + ... + e^{x_{n-1}}) = \ln(\Delta)$，其中 $\Delta = e^{x_1} + e^{x_2} + ... + e^{x_{n-1}} = e^x$，则可得到：

$$
\begin{array} { r l } & { \ln \left( e ^ { x _ { 1 } } + e ^ { x _ { 2 } } + \ldots + e ^ { x _ { n - 1 } } + e ^ { x _ { n } } \right) = \ln \left( \Delta + e ^ { x _ { n } } \right) = \ln \left( e ^ { \ln \left( \Delta \right) } + e ^ { x _ { n } } \right) } \\ & { \qquad = \max \left( \ln \left( \Delta \right) , x _ { n } \right) + f _ { c } \left( \left| \ln \left( \Delta \right) - x _ { n } \right| \right) } \\ & { \qquad = \max \left( x , x _ { n } \right) + f _ { c } \left( \left| x - x _ { n } \right| \right) } \\ & { \qquad = \max ^ { * } \left( x , x _ { n } \right) } \end{array}\tag{3.17}
$$

Log-MAP算法的工作方式与Max-Log-MAP算法相同，唯一的区别在于它利用方程(3.16)和(3.17)来代替方程(3.1)，以近似BCJR算法的各种参数。因此，从方程(3.9)出发，Log-MAP算法计算数据比特 $a_k$ 的LLR值如下：

$$
\lambda _ { k } = \max _ { ( u , q ) \in S _ { 1 } } ^ { * } \left( \hat { \alpha } _ { k } \left( u \right) + \tilde { \gamma } _ { k } \left( u , q \right) + \hat { \beta } _ { k + 1 } \left( q \right) \right) - \max _ { ( u , q ) \in S _ { - 1 } } ^ { * } \left( \hat { \alpha } _ { k } \left( u \right) + \tilde { \gamma } _ { k } \left( u , q \right) + \hat { \beta } _ { k + 1 } \left( q \right) \right)\tag{3.18}
$$

其中分支度量 $\tilde{\gamma}_k(u,q)$ 由方程(3.10)求得，且：

$$
\hat { \alpha } _ { k + 1 } \left( q \right) = \max _ { \forall u } ^ { * } \left( \tilde { \gamma } _ { k } \left( u , q \right) + \hat { \alpha } _ { k } \left( u \right) \right)\tag{3.19}
$$

$$
\hat { \beta } _ { k } \left( u \right) = \max _ { \forall q } ^ { * } \left( \hat { \beta } _ { k + 1 } \left( q \right) + \tilde { \gamma } _ { k } \left( u , q \right) \right)\tag{3.20}
$$

在实际应用中，Log-MAP算法的性能等同于BCJR算法，但计算资源消耗较少，且对噪声方差的敏感度也低于BCJR算法。然而，尽管Log-MAP算法的性能优于Max-Log-MAP算法，但其复杂度也更高。因此，在选择使用哪种算法时，用户需要在复杂度和可接受的性能之间进行权衡。

**例3.3** 从例3.1出发，请使用Log-MAP算法解码数据 $y_k$，设数据比特 $a_k$ 的先验信息为 $\lambda_a(a_k) = \{ 1, -4, 3, -2 \}$。

解：从例3.1可知，Log-MAP算法接收数据 $y_k = \{ 0.9, -0.2, 0.3, 0.6 \}$ 和 $\lambda_a(a_k) = \{ 1, -4, 3, -2 \}$ 用于数据解码。使用例3.1中所示的相同方法，Log-MAP算法的各种参数值如图3.5所示，其中每条分支旁的值对应 $\tilde{\gamma}_k(u,q)$，各状态节点处的分数形式中的数字表示 $\hat{\alpha}_k(u)$ 和 $\hat{\beta}_k(u)$：

$$
\frac { \hat { \alpha } _ { k } \left( u \right) } { \hat { \beta } _ { k } \left( u \right) }
$$

对于 $k \in \{ 0, 1, 2, 3 \}$ 和 $u \in \{ a, b \}$。

根据图3.5中的分支度量和状态度量，按方程(3.18)可计算数据比特 $a_k$ 的MAP-LLR值：

$$
\{ \lambda_p(a_0), \lambda_p(a_1), \lambda_p(a_2), \lambda_p(a_3) \} \approx \{ 23.60, -16.32, 12.22, -1.49 \}
$$

解码数据比特为：

$$
\{ \hat{a}_0, \hat{a}_1, \hat{a}_2, \hat{a}_3 \} = \{ 1, -1, 1, -1 \}
$$

**例3.4** 从例3.2出发，请使用Log-MAP算法解码数据 $y_k$，设数据比特 $a_k$ 的先验信息为 $\lambda_a(a_k) = \{ -1, 2, 1, 2, -2 \}$。

解：从例3.2可知，Log-MAP算法接收数据 $y_k = \{ 1.2, -0.7, -0.2, 0.5, -0.7 \}$ 和 $\lambda_a(a_k) = \{ -1, 2, 1, 2, -2 \}$ 用于数据解码。Log-MAP算法的各种参数值如图3.6所示。
