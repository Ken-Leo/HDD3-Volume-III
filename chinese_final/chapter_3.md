## 第三章

## 软检测器

当前硬盘驱动器的信号处理系统开始采用迭代解码系统进行数据解码。迭代解码系统中的关键组件是软检测器（soft detector）和软解码器（soft decoder），它们在彼此之间交换软信息（soft information），以帮助系统性能在每次迭代中逐步提升。如第二章所述，BCJR算法[18]是一种最大后验（MAP: maximum a posteriori）算法，对于估计马尔可夫过程的状态或输出是最优的。因此，在迭代解码系统[3]最初被提出时，就采用了BCJR算法来构建软检测器和软解码器。

尽管BCJR算法中状态度量的计算具有递归性质，使得数据解码较为简单，然而BCJR算法在许多实际应用的信号处理芯片中并不常用，因为它计算资源消耗高（例如加法和乘法的运算次数），需要使用非线性函数进行计算（例如指数函数），并且对系统中的噪声方差敏感[23, 24]。因此，研究人员开发了在对数域中工作的类MAP算法（MAP-like algorithm），这些算法能够解决数值计算问题，并且复杂度远低于BCJR算法。

本章将介绍这些类MAP算法的工作原理，包括Max-Log-MAP[23, 24, 38, 39]、Log-MAP[23, 24]和SOVA（软输出维特比算法）[19, 42]，它们的性能接近或等同于BCJR算法，同时还将展示所有算法的性能并比较其复杂度。

![](../images/chapter_3/fig_3_1.jpg)  
图3.1 MAP、Log-MAP、Max-Log-MAP和SOVA的关系

## 3.1 引言

维特比检测器[10, 13]是一种最大似然（ML: maximum-likelihood）检测器，其输出是对所需检测数据序列的估计，或者说ML检测器能使数据序列的误差最小化。然而，它不能保证数据序列中每个数据比特是最佳的。维特比检测器不能用于迭代解码系统，因为该系统需要在SISO（软输入软输出）检测器和SISO解码器之间交换软信息（或数据比特的可信度）。

BCJR算法是一种MAP算法，在早期被用于迭代解码系统。然而，BCJR算法在许多实际应用的信号处理芯片中存在局限。因此，研究人员开发了Max-Log-MAP和SOVA算法，其性能接近BCJR算法。随后又开发了Log-MAP算法，其性能等同于BCJR算法但复杂度低得多，因此可以在信号处理芯片中实际使用。图3.1展示了MAP算法和类MAP算法的关系。

## 3.2 Max-Log-MAP算法

Max-Log-MAP算法[23, 24, 38, 39]是从BCJR算法发展而来的，它利用最大值函数（maximum function）和对数函数（logarithm function），主要目的是使其能够在实际应用中实现（即在信号处理芯片中使用），同时保持接近BCJR算法的性能。通常Max-Log-MAP算法被认为是次优算法，其输出的软信息质量劣于BCJR算法输出的软信息。

根据第2.2节中BCJR算法的信道模型和方程，使Max-Log-MAP算法便于实际使用的形式将利用对数恒等式 $$x _ { i } = e ^ { \ln ( x _ { i } ) }$$ 和对数近似公式[24]：

$$
\ln \left( e ^ { x _ { 1 } } + e ^ { x _ { 2 } } + . . . + e ^ { x _ { n } } 
ight) pprox \operatorname* { m a x } _ { i \in \{ 1 , . . . , n \} } ( x _ { i } )	ag{3.1}
$$

其中 $$x _ { i }$$ 是实数，$$n$$ 是正整数。因此，数据比特 $$a _ { k }$$ 的LR值在方程(2.24)中可重新整理为：

$$
\lambda _ { p } \left( a _ { k } 
ight) = \ln \left( \sum _ { \left( u , q 
ight) \in S _ { 1 } } lpha _ { k } \left( u 
ight) \gamma _ { k } \left( u , q 
ight) eta _ { k + 1 } \left( q 
ight) 
ight) - \ln \left( \sum _ { \left( u , q 
ight) \in S _ { - 1 } } lpha _ { k } \left( u 
ight) \gamma _ { k } \left( u , q 
ight) eta _ { k + 1 } \left( q 
ight) 
ight)	ag{3.2}
$$

考虑方程(3.2)右侧第一项：

$$
egin{array} { r l } { \displaystyle \operatorname { l n i m } \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } lpha _ { k } \left( u 
ight) \cap _ { \mathbb { H } } \left( u , q 
ight) eta _ { k + 1 } \left( q 
ight) 
ight) = \ln \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } e ^ { \ln ( lpha _ { k } \left( u 
ight) \cdot \hat { \gamma } _ { \mathbb { H } } \left( u , q 
ight) eta _ { k + 1 } \left( q 
ight) ) } 
ight) } & { } \ { = \ln \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } e ^ { \ln ( lpha _ { \mathbb { H } } \left( u 
ight) ) + \ln \left( \gamma _ { \mathbb { H } } \left( u , q 
ight) 
ight) + \ln \left( eta _ { k + 1 } \left( q 
ight) 
ight) } 
ight) } & { } \ { = \ln \left( \displaystyle \sum _ { ( u , q ] \in S _ { 1 } } e ^ { ar { lpha } _ { k } \left( u 
ight) + ar { \gamma } _ { \mathbb { H } } \left( u , q 
ight) + ar { \gamma } _ { \mathbb { H } + 1 } \left( q 
ight) } 
ight) } & { } \end{array}	ag{3.3}
$$

其中：

$$
	ilde { \gamma } _ { k } \left( u , q 
ight) = \ln \left( \gamma _ { k } \left( u , q 
ight) 
ight)	ag{3.4}
$$

$$
	ilde { lpha } _ { k } \left( u 
ight) = \ln \left( lpha _ { k } \left( u 
ight) 
ight)	ag{3.5}
$$

$$
\widetilde { eta } _ { k + 1 } \left( q 
ight) = \ln \left( eta _ { k + 1 } \left( q 
ight) 
ight)	ag{3.6}
$$

根据方程(3.1)，可近似计算方程(3.3)为：

$$
\ln \left( \sum _ { ( u , q ) \in S _ { 1 } } lpha _ { k } \left( u 
ight) \gamma _ { k } \left( u , q 
ight) eta _ { k + 1 } \left( q 
ight) 
ight) pprox \operatorname* { m a x } _ { \left( u , q 
ight) \in S _ { 1 } } \left( 	ilde { lpha } _ { k } \left( u 
ight) + 	ilde { \gamma } _ { k } \left( u , q 
ight) + 	ilde { eta } _ { k + 1 } \left( q 
ight) 
ight)	ag{3.7}
$$

类似地，方程(3.2)右侧第二项为：

$$
\ln \left( \sum _ { \left( u , q 
ight) \in S _ { - 1 } } lpha _ { k } \left( u 
ight) \gamma _ { k } \left( u , q 
ight) eta _ { k + 1 } \left( q 
ight) 
ight) pprox \operatorname* { m a x } _ { \left( u , q 
ight) \in S _ { - 1 } } \left( 	ilde { lpha } _ { k } \left( u 
ight) + 	ilde { \gamma } _ { k } \left( u , q 
ight) + 	ilde { eta } _ { k + 1 } \left( q 
ight) 
ight)	ag{3.8}
$$

将方程(3.7)和(3.8)代入方程(3.2)，得到Max-Log-MAP算法的数据比特 $$a _ { k }$$ 的LLR值为：

$$
\lambda _ { p } \left( a _ { k } 
ight) pprox \operatorname* { m a x } _ { \left( u , q 
ight) \in S _ { 1 } } \left( 	ilde { lpha } _ { k } \left( u 
ight) + 	ilde { \gamma } _ { k } \left( u , q 
ight) + 	ilde { eta } _ { k + 1 } \left( q 
ight) 
ight) - \operatorname* { m a x } _ { \left( u , q 
ight) \in S _ { - 1 } } \left( 	ilde { lpha } _ { k } \left( u 
ight) + 	ilde { \gamma } _ { k } \left( u , q 
ight) + 	ilde { eta } _ { k + 1 } \left( q 
ight) 
ight)	ag{3.9}
$$

## 计算方程(3.4)中的 $$	ilde { \gamma } _ { k } \left( u , q 
ight)$$

对方程(2.29)两边取自然对数，得到新的分支度量：

$$
\widetilde { \gamma } _ { k } \left( u , q 
ight) = \ln \left( { rac { 1 } { \sqrt { 2 \pi \sigma ^ { 2 } } } } 
ight) - { rac { 1 } { 2 \sigma ^ { 2 } } } igl ert y _ { k } - \widehat { r } \left( u , q 
ight) igr ert ^ { 2 } + { rac { \hat { a } \left( u , q 
ight) \lambda _ { a } \left( a _ { k } 
ight) } { 2 } }	ag{3.10}
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


解码数据比特为：

$$
\{ \hat{a}_0, \hat{a}_1, \hat{a}_2, \hat{a}_3, \hat{a}_4 \} = \{ 1, -1, 1, 1, 1 \}
$$

与使用Log-MAP算法解码的数据比特 $\{ a_k \}$ 一致。

## 3.4 SOVA算法

软输出维特比算法（简称SOVA算法）[19]是一种能够输出数据比特LLR值的算法，与MAP（或BCJR）、Max-Log-MAP和Log-MAP算法类似。一般来说，SOVA算法的性能与Max-Log-MAP相当，但复杂度更低[39]，因此SOVA算法在许多实际应用中广受欢迎，包括采用迭代解码系统的新型硬盘驱动器。

**注意：** 读者应先理解维特比算法的工作原理（参见文献[10]第4章），再学习SOVA算法的原理，以便更容易理解SOVA算法。

SOVA算法的工作方式类似于维特比算法[13]，但有两个重要的区别：

1) SOVA算法使用修正的分支度量（modified branch metric），其中包含了数据比特输入的先验概率影响。
2) SOVA算法提供软输出，用于指示每个数据比特判决的可信度。

考虑图2.10中的信道模型，维特比算法在第k阶段从时间k的状态u到时间k+1的状态q的分支度量 $\rho_k(u,q)$ 为[10, 13]：

$$
{ \rho } _ { k } \left( u , q \right) = { \ln } \left( p \left( { y } _ { k } \mid { a } _ { k } \right) \right) = { \ln } \left( \frac { 1 } { \sqrt { 2 \pi { \sigma } ^ { 2 } } } \right) - \frac { 1 } { 2 { \sigma } ^ { 2 } } { \left| y _ { k } - \hat { r } \left( u , q \right) \right| } ^ { 2 }\tag{3.21}
$$

其中 $\hat{r}(u,q)$ 是与网格图中状态转移(u,q)对应的信道输出，$\sigma^2$ 是噪声 $n_k$ 的方差。

输入数据比特 $a_k$ 的先验概率可以按照方程(3.10)合并到分支度量中。因此，SOVA算法中使用的分支度量为：

$$
\widetilde { \gamma } _ { k } \left( u , q \right) = \ln \left( p \left( y _ { k } ; a _ { k } \right) \right) = \ln \left( \frac { 1 } { \sqrt { 2 \pi \sigma ^ { 2 } } } \right) - \frac { 1 } { 2 \sigma ^ { 2 } } \left| y _ { k } - \widehat { r } \left( u , q \right) \right| ^ { 2 } + \frac { \hat { a } \left( u , q \right) \lambda _ { a } \left( a _ { k } \right) } { 2 }\tag{3.22}
$$

其中 $p(y_k; a_k) = p(y_k | a_k) p(a_k)$，$\hat{a}(u,q)$ 是与状态转移(u,q)对应的信道输入数据，$\lambda_a(a_k)$ 是输入数据比特 $a_k$ 的先验概率值。

SOVA算法在网格图中搜索具有最大度量的路径。在时间k+1处状态q的路径度量等于方程(3.22)中分支度量之和：

$$
\Phi _ { k + 1 } \left( q \right) = \sum _ { i = 0 } ^ { k } \tilde { \gamma } _ { i }\tag{3.23}
$$

其中 $\tilde{\gamma}_i$ 是与到达时间k+1处状态q的"幸存路径（survivor path）"对应的时间i处的分支度量。因此，SOVA算法的工作方式与维特比算法类似，根据具有最大路径度量的路径（称为"ML路径"或最大似然路径）来选择输入数据序列（输入数据序列的估计 $\hat{a}_k$），唯一的区别是SOVA算法使用方程(3.22)中的分支度量。此外，SOVA算法还输出每个数据比特的LLR值，用于指示数据比特的取值及其可信度。

### 3.4.1 数据比特LLR的计算

SOVA算法可以按如下方式计算每个数据比特的LLR值。考虑图3.7中第k阶段的网格图。时间k+1处状态q的路径度量 $\Phi_{k+1}(q)$ 可由下式求得：

$$
\Phi _ { k + 1 } \left( q \right) = \ln \left( p \left( \mathbf { y } _ { 0 } ^ { k } ; \mathbf { a } _ { 0 } ^ { k } \right) \right)\tag{3.24}
$$

其中 $\mathbf{y}_0^k = [y_0, y_1, ..., y_k]$ 是从时间0到时间k的待解码数据序列，$\mathbf{a}_0^k = [a_0, a_1, ..., a_k]$ 是与 $\mathbf{y}_0^k$ 对应的输入数据序列。方程(3.24)可重新整理为：

$$
p \left( \mathbf { y } _ { 0 } ^ { k } : \mathbf { a } _ { 0 } ^ { k } \right) = e ^ { \Phi _ { k + 1 } ( q ) }\tag{3.25}
$$

SOVA算法输出的数据比特判决可信度（对于二进制码）可以按如下方式获得。从图3.7可以看出，有两条状态转移路径到达时间k+1处的状态q，即(u,q)和(s,q)，其路径度量分别为 $\Phi_{k+1}^{(1)}(q)$ 和 $\Phi_{k+1}^{(2)}(q)$。假设 $\Phi_{k+1}^{(1)}(q) > \Phi_{k+1}^{(2)}(q)$，则路径(1)是到达状态q的最佳状态转移路径。因此，SOVA算法选择路径(1)作为到达状态q的幸存路径的一部分，即 $\mathbf{S}_{k+1}(q)$。

定义路径度量差为：

$$
\Delta _ { k + 1 } \left( q \right) = \Phi _ { k + 1 } ^ { \left( 1 \right) } \left( q \right) - \Phi _ { k + 1 } ^ { \left( 2 \right) } \left( q \right)\tag{3.26}
$$

其中 $\Delta_{k+1}(q) \geq 0$ 始终成立。因此，正确判决的概率可由下式求得[19, 40]：

$$
\mathrm { P r } \big [ \mathrm { c o r r e c t ~ d e c i s i o n ~ a t } \Psi _ { k + 1 } = q \big ] = \frac { e ^ { \Phi _ { k + 1 } ^ { ( 1 ) } \left( q \right) } } { e ^ { \Phi _ { k + 1 } ^ { ( 1 ) } \left( q \right) } + e ^ { \Phi _ { k + 1 } ^ { ( 2 ) } \left( q \right) } } = \frac { e ^ { \Delta _ { k + 1 } \left( q \right) } } { 1 + e ^ { \Delta _ { k + 1 } \left( q \right) } }\tag{3.27}
$$

其中 $\mathrm{Pr}[x]$ 是x的概率，正确判决的LLR值为：

$$
\mathrm { L L R } = \ln \left( \frac { \mathrm { P r } \big [ \mathrm { c o r r e c t ~ d e c i s i o n ~ a t } \Psi _ { k + 1 } = q \big ] } { 1 - \mathrm { P r } \big [ \mathrm { c o r r e c t ~ d e c i s i o n ~ a t } \Psi _ { k + 1 } = q \big ] } \right) = \Delta _ { k + 1 } ( q )\tag{3.28}
$$

这意味着维特比算法中合并路径的路径度量差等于正确判决概率的LLR值。


与方程(3.28)类似，比特误差的LLR值等于 $\Delta_k^d$。因此，综合两种情况可以看出，第d条路径（被丢弃路径）中时间 $k-\delta$ 处的数据比特误差的LLR值为：

$$
\lambda(\hat{e}_{k-\delta}^d) = \ln\left(\frac{p(\hat{e}_{k-\delta}^d = 1)}{p(\hat{e}_{k-\delta}^d = -1)}\right) = \begin{cases} \infty, & \text{if } \hat{a}_{k-\delta} = \hat{a}_{k-\delta}^d \\ \Delta_k^d, & \text{if } \hat{a}_{k-\delta} \neq \hat{a}_{k-\delta}^d \end{cases}\tag{3.31}
$$

在实际应用中，每条被丢弃路径都为数据比特 $\hat{a}_{k-\delta}$ 被正确解码的可信度提供证据。因此，所有可能的被丢弃路径对 $\hat{a}_{k-\delta}$ 的总误差可由下式求得：

$$
\hat{e}_{k-\delta} = \sum_{d=0}^{\delta} \oplus \hat{e}_{k-\delta}^d = \hat{e}_{k-\delta}^0 \oplus \hat{e}_{k-\delta}^1 \oplus \ldots \oplus \hat{e}_{k-\delta}^\delta\tag{3.32}
$$

因此，数据比特 $\hat{a}_{k-\delta}$ 的LLR值可写为[40]：

$$
\lambda(\hat{a}_{k-\delta}) = \hat{a}_{k-\delta} \lambda(\hat{e}_{k-\delta}) = \hat{a}_{k-\delta} \lambda\left(\sum_{d=0}^{\delta} \oplus \hat{e}_{k-\delta}^d\right)\tag{3.33}
$$

其中 $\hat{a}_{k-\delta} \in \{\pm 1\}$ 决定LLR的符号（即维特比算法解码的数据比特估计值），$\lambda(\hat{e}_{k-\delta}) \geq 0$ 决定 $\hat{a}_{k-\delta}$ 的可信度大小。也就是说，$\lambda(\hat{e}_{k-\delta})$ 越大，维特比算法解码出的数据比特 $\hat{a}_{k-\delta}$ 的正确性越高（反之亦然）。

定义对数似然比的代数运算[40]如下：

$$
\lambda(x_1) \boxplus \lambda(x_2) \triangleq \lambda(x_1 \oplus x_2)\tag{3.34}
$$

其中 $x_1$ 和 $x_2$ 是属于{-1, 1}的二进制随机变量，$\boxplus$ 是LLR代数运算符，其关系如下：

$$
\lambda(x) \boxplus \infty = \lambda(x) \quad \quad \lambda(x) \boxplus -\infty = -\lambda(x) \quad \quad \lambda(x) \boxplus 0 = 0
$$

其中 $\infty$ 表示非常高的可信度，$-\infty$ 表示完全不可信，0 表示可信度模糊。

利用方程(3.34)，方程(3.33)中数据比特 $\hat{a}_{k-\delta}$ 的LLR值可重新整理为：

$$
\begin{array} { r l } { \lambda(\hat{a}_{k-\delta}) = \hat{a}_{k-\delta} \lambda\left(\sum_{d=0}^{\delta} \oplus \hat{e}_{k-\delta}^d\right) = \hat{a}_{k-\delta} \sum_{d=0}^{\delta} \boxplus \lambda(\hat{e}_{k-\delta}^d) } \\ { = \hat{a}_{k-\delta} \{ \lambda(\hat{e}_{k-\delta}^0) \boxplus \lambda(\hat{e}_{k-\delta}^1) \boxplus \ldots \boxplus \lambda(\hat{e}_{k-\delta}^\delta) \} } \end{array}\tag{3.35}
$$

根据方程(3.31)和LLR代数运算的性质，如果方程(3.35)中只对 $\hat{a}_{k-\delta}^d \neq \hat{a}_{k-\delta}$ 的d进行求和，则可得到[40]：

$$
\lambda(\hat{a}_{k-\delta}) = \hat{a}_{k-\delta} \cdot \min_{d \in \{0,1,\ldots,\delta\}} \Delta_k^d\tag{3.36}
$$

同样地，利用LLR代数运算的性质[40]，方程(3.36)可近似为：

$$
\lambda(\hat{a}_{k-\delta}) \approx \hat{a}_{k-\delta} \cdot \min_{d \in \{0,1,\ldots,\delta\}} \Delta_k^d\tag{3.37}
$$

即数据比特 $\hat{a}_{k-\delta}$ 的可信度取决于幸存路径上路径度量差 $\Delta_k^d$ 的最小值。因此，方程(3.37)中 $\lambda(\hat{a}_{k-\delta})$ 的符号是数据比特 $\hat{a}_{k-\delta}$ 的估计值，其大小是解码数据比特的可信度。

### 3.4.2 对SOVA算法的观察

从方程(3.37)可以看出，数据比特的LLR值取决于方程(3.26)中所示的路径度量差，即 $\Delta_k(q) = \Phi_k^{(1)}(q) - \Phi_k^{(2)}(q)$，其中 $\Phi_k^{(i)}(q)$ 是方程(3.23)中分支度量的和（$i = \{1,2\}$），分支度量 $\tilde{\gamma}_k(u,q)$ 由方程(3.22)求得。

然而，为了降低计算路径度量差 $\Delta_k(q)$ 的复杂度，SOVA算法可以使用以下形式的分支度量，而不会影响SOVA算法的性能：

$$
\widetilde { \gamma } _ { k } \left( u , q \right) \approx - \frac { 1 } { 2 \sigma ^ { 2 } } \big | y _ { k } - \widehat { r } \left( u , q \right) \big | ^ { 2 } + \frac { \widehat { a } \left( u , q \right) \lambda _ { a } \left( a _ { k } \right) } { 2 }\tag{3.38}
$$

因为方程(3.26)中计算路径度量差时结果保持不变。

### 3.4.3 SOVA算法步骤总结

设 $\pi_{k+1}(q)$ 是时间k+1处状态q的前驱节点，用于存储使得到达时间k+1处状态q的最佳状态转移之前的状态（即时间k处的状态）。该状态转移被视为幸存路径 $\mathbf{S}_{k+1}(q)$ 的一部分。例如，考虑图3.7中的网格图。假设路径(1)是使 $\Phi_{k+1}(q)$ 最大的最佳路径，则可得到 $\pi_{k+1}(q) = u$，即状态u是使得到达时间k+1处状态q的最佳状态转移的先驱状态。因此，SOVA算法的工作原理可按图3.9中的步骤总结。

**例3.5** 从例2.4出发，请使用SOVA算法解码数据 $y_k$，设 $\lambda_a(a_k) = \{ -1, 2, 1, 2 \}$，解码深度 $\delta = 3$。

解：从例2.4可知，需要使用SOVA算法检测的数据为：

$$
y_k = \{ y_0, y_1, y_2, y_3 \} = \{ 0.9, -0.2, 0.3, 0.6 \}
$$

信道 $H(D) = 1 + 0.5D$ 的网格图如图2.13所示，有两个状态：状态(a)和状态(b)。因此，SOVA算法的数据解码步骤如下：

**SOVA算法**

**硬解码**（与维特比算法步骤相同）

1. 初始化路径度量 $\Phi_0(u) = 0$，对于所有 $u \in \{ 0, 1, ..., Q-1 \}$
2. 对于 $k = 0, 1, ..., L+\nu-1+\delta$（其中 $\delta$ 是解码深度）
   设 $y_k = 0$ 用于 $k \geq L+\nu$
   对于 $q = 0, 1, ..., Q-1$
   根据方程(3.38)计算 $\tilde{\gamma}_k(u,q)$，对所有使(u,q)为真的u
   根据方程(3.23)计算最佳状态转移对应的 $\Phi_{k+1}(q)$
   计算并记录路径度量差 $\Delta_{k+1}(q)$ 根据方程(3.26)
   记录前驱节点 $\pi_{k+1}(q)$（用于查找第d条路径或被丢弃路径）
   记录幸存路径 $\mathbf{S}_{k+1}(q)$
3. 根据ML路径（具有最大 $\Phi_{L+\nu+\delta}$ 的幸存路径）解码输入数据序列 $\hat{\mathbf{a}}_0^{L-1}$

**软解码**（计算LLR）

4. 初始化LLR幅度 $|\lambda(\hat{a}_k)| = +\infty$，对于 $k = 0, 1, ..., L-1$
5. 对于 $k = \delta, \delta+1, ..., L-1+\delta$
   对于 $d = 0, 1, ..., \delta$
   比较ML路径解码的数据比特 $\hat{a}_{k-\delta}$ 与第d条路径解码的数据比特 $\hat{a}_{k-\delta}^d$
   若 $\hat{a}_{k-\delta}^d \neq \hat{a}_{k-\delta}$，按以下关系更新LLR幅度：
   $|\lambda(\hat{a}_{k-\delta})| = \min\{ |\lambda(\hat{a}_{k-\delta})|, \Delta_{k+1}^d \}$
   解码数据比特 $a_{k-\delta}$ 的MAP-LLR值：
   $\lambda_p(\hat{a}_{k-\delta}) = \hat{a}_{k-\delta} |\lambda(\hat{a}_{k-\delta})|$

图3.9 SOVA算法步骤[19, 40]


**阶段6 (k=6):** 计算 $\lambda_p(a_3)$。解码数据比特 $\hat{a}_3 = 1$。图3.10(f)显示第d条路径（被丢弃路径）及其数据比特 $\hat{a}_3^d$ 和路径度量差 $\Delta_7^d$。此时 $\{ \hat{a}_3^0, \hat{a}_3^1, \hat{a}_3^2 \} \neq \hat{a}_3$，数据比特 $a_3$ 的LLR幅度为：

$$
|\lambda(\hat{a}_3)| = \min\{ +\infty, \Delta_7^0, \Delta_7^1, \Delta_7^2 \} = 9.5398
$$

数据比特 $a_3$ 的LLR值为 $\lambda(\hat{a}_3) = \hat{a}_3 |\lambda(\hat{a}_3)| = (1)(9.5398) = 9.5398$

因此，SOVA算法输出的数据比特 $a_k$ 的MAP-LLR值为：

$$
\{ \lambda_p(a_0), \lambda_p(a_1), \lambda_p(a_2), \lambda_p(a_3) \} \approx \{ 4.2832, -4.2832, 4.2832, 9.5398 \}
$$

解码数据比特为：

$$
\{ \hat{a}_0, \hat{a}_1, \hat{a}_2, \hat{a}_3 \} = \{ 1, -1, 1, 1 \}
$$

与发射端发送的数据比特 $\{ a_k \}$ 一致（最后一个比特在系统中并非真实存在，而是输入数据与信道卷积的结果），表明使用SOVA算法进行数据解码未发生错误。

**例3.6** 从例2.5出发，请使用SOVA算法解码数据 $y_k$，设 $\lambda_a(a_k) = \{ -1, 1, 2, -1, 1 \}$，解码深度 $\delta = 3$。

解：从例2.5可知，需要使用SOVA算法检测的数据为：

$$
y_k = \{ y_0, y_1, y_2, y_3, y_4 \} = \{ 1.2, -0.7, -0.2, 0.5, -0.7 \}
$$

信道 $H(D) = 1 - D^2$ 的网格图如图2.15所示，共有四个状态：状态(a)、(b)、(c)和(d)。

按照例3.5中所述方法使用SOVA算法进行数据解码，可得到路径度量差 $\Delta_{k+1}(q)$ 和先驱状态 $\pi_{k+1}(q)$，结果如图3.11所示。根据图3.11中的数据，按方程(3.37)可计算数据比特 $a_k$ 的MAP-LLR值：

$$
\{ \lambda_p(a_0), \lambda_p(a_1), \lambda_p(a_2), \lambda_p(a_3), \lambda_p(a_4) \} \approx \{ 16.59, -17.85, 24.88, -12.57, 17.08 \}
$$

解码数据比特为：

$$
\{ \hat{a}_0, \hat{a}_1, \hat{a}_2, \hat{a}_3, \hat{a}_4 \} = \{ 1, -1, 1, -1, 1 \}
$$

与发射端发送的数据比特 $\{ a_k \}$ 一致，表明使用SOVA算法进行数据解码未发生错误。

## 3.5 双向SOVA算法

第3.4节中描述的SOVA算法步骤较为复杂，可能难以理解。本节将介绍另一种形式的SOVA算法工作原理，称为"双向SOVA算法（bi-directional SOVA）"[41, 42]，其输出的数据比特LLR值与SOVA算法接近，且更易于实际应用。

考虑图2.10中的信道模型。SOVA算法输出的数据比特 $a_k$ 的MAP-LLR值根据方程(2.23)为：

$$
\lambda _ { p } \left( a _ { k } \right) = \ln \left( { \frac { \operatorname { P r } \left[ a _ { k } = 1 \mid \mathbf { y } \right] } { \operatorname { P r } \left[ a _ { k } = - 1 \mid \mathbf { y } \right] } } \right)\tag{3.39}
$$

其中 $a_k \in \{-1, 1\}$ 是信道输入数据，$\mathbf{y} = [y_0, y_1, ..., y_{L+\nu-1}]$ 是待解码数据序列，$L$ 是输入数据序列长度，$\nu$ 是信道记忆长度。

双向SOVA算法利用网格图解码信道输入数据，根据具有最大路径度量的路径（ML路径）选择输入数据序列 $\mathbf{a} = [a_0, a_1, ..., a_{L-1}]$。到达时间k+1处状态q的路径度量由方程(3.24)求得：

$$
\Phi _ { k + 1 } \left( q \right) = \ln \left( p \left( \mathbf { y } _ { 0 } ^ { k } ; \mathbf { a } _ { 0 } ^ { k } \right) \right)\tag{3.40}
$$

即沿到达时间k+1处状态q的幸存路径的分支度量之和。分支度量由方程(3.38)求得：

$$
\widetilde { \gamma } _ { k } \left( u , q \right) = \ln \left( p \left( y _ { k } ; a _ { k } \right) \right) \approx - \frac { 1 } { 2 \sigma ^ { 2 } } { \left| y _ { k } - \widehat { r } \left( u , q \right) \right| } ^ { 2 } + \frac { \hat { a } \left( u , q \right) \lambda _ { a } \left( a _ { k } \right) } { 2 }\tag{3.41}
$$

根据贝叶斯规则：

$$
p \left( \mathbf { a } \mid \mathbf { y } \right) = { \frac { p \left( \mathbf { a } ; \mathbf { y } \right) } { p \left( \mathbf { y } \right) } } { = { \frac { p \left( \mathbf { y } \mid \mathbf { a } \right) p \left( \mathbf { a } \right) } { p \left( \mathbf { y } \right) } } }\tag{3.42}
$$

由于 $p(\mathbf{y})$ 是与维特比算法选择幸存路径无关的常数，因此利用方程(3.25)可得到ML路径的概率正比于：

$$
p \left( \mathbf { a } \mid \mathbf { y } \right) \sim \exp \left\{ \Phi _ { L + \nu } ^ { \mathrm { m a x } } \right\}\tag{3.43}
$$

其中 $\Phi_{L+\nu}^{\mathrm{max}}$ 是时间 $L+\nu$ 处ML路径的最大路径度量。即输入数据序列的估计 $\hat{\mathbf{a}} = [\hat{a}_0, \hat{a}_1, ..., \hat{a}_{L-1}]$ 根据ML路径解码。

定义 $\Phi_k^c$ 为数据比特 $a_k^c$ 与ML路径在时间k处的数据比特 $\hat{a}_k$ 相反的路径的最大路径度量。因此，如果ML路径在时间k处的数据比特为 $\hat{a}_k = 1$，则"互补比特"为 $a_k^c = -1$，可得：

$$
p \left( a _ { k } = 1 | \mathbf { y } \right) \sim \exp \left\{ \Phi _ { L + \nu } ^ { \mathrm { m a x } } \right\} \qquad \text{和} \qquad p \left( a _ { k } = -1 | \mathbf { y } \right) \sim \exp \left\{ \Phi _ { k + 1 } ^ { c } \right\}\tag{3.44}
$$

方程(3.44)中两个概率的比值，即数据比特 $a_k$ 的MAP-LLR值为：

$$
\ln \left\{ { \frac { p \left( a _ { k } = 1 | \mathbf { y } \right) } { p \left( a _ { k } = - 1 | \mathbf { y } \right) } } \right\} \sim \ln \left\{ { \frac { e ^ { \Phi _ { L + \nu } ^ { \operatorname { m a x } } } } { e ^ { \Phi _ { k + 1 } ^ { c } } } } \right\} = \Phi _ { L + \nu } ^ { \operatorname { m a x } } - \Phi _ { k + 1 } ^ { c }\tag{3.45}
$$

设 $\Phi_{k+1}^{(1)}$ 是所有 $a_k = 1$ 的路径中的最大路径度量，$\Phi_{k+1}^{(-1)}$ 是所有 $a_k = -1$ 的路径中的最大路径度量。考虑以下两种情况：

1) 如果ML路径解码的数据比特为 $\hat{a}_k = 1$，则互补比特为 $-1$，因此 $\Phi_{k+1}^{(1)} = \Phi_{L+\nu}^{\mathrm{max}}$ 且 $\Phi_{k+1}^{(-1)} = \Phi_{k+1}^c$，可得：

$$
\ln \left\{ \frac { p \left( a _ { k } = 1 | \mathbf { y } \right) } { p \left( a _ { k } = - 1 | \mathbf { y } \right) } \right\} \sim \ln \left( \frac { e ^ { \Phi _ { L + \nu } ^ { \mathrm { m a x } } } } { e ^ { \Phi _ { k + 1 } ^ { c } } } \right) = \Phi _ { L + \nu } ^ { \mathrm { m a x } } - \Phi _ { k + 1 } ^ { c } = \Phi _ { k + 1 } ^ { ( 1 ) } - \Phi _ { k + 1 } ^ { ( - 1 ) }\tag{3.46}
$$

2) 如果ML路径解码的数据比特为 $\hat{a}_k = -1$，则互补比特为1，因此 $\Phi_{k+1}^{(-1)} = \Phi_{L+\nu}^{\mathrm{max}}$ 且 $\Phi_{k+1}^{(1)} = \Phi_{k+1}^c$，可得：

$$
\ln \left\{ \frac { p \left( a _ { k } = 1 | \mathbf { y } \right) } { p \left( a _ { k } = - 1 | \mathbf { y } \right) } \right\} \sim \ln \left( \frac { e ^ { \Phi _ { k + 1 } ^ { c } } } { e ^ { \Phi _ { L + \nu } ^ { \mathrm { m a x } } } } \right) = \Phi _ { k + 1 } ^ { c } - \Phi _ { L + \nu } ^ { \mathrm { m a x } } = \Phi _ { k + 1 } ^ { ( 1 ) } - \Phi _ { k + 1 } ^ { ( - 1 ) }\tag{3.47}
$$

方程(3.46)和(3.47)表明，无论ML路径的数据比特估计值如何，数据比特 $a_k$ 的MAP-LLR值都等于：

$$
\lambda _ { p } \left( a _ { k } \right) = \ln \left\{ \frac { p \left( a _ { k } = 1 \mid \mathbf { y } \right) } { p \left( a _ { k } = - 1 \mid \mathbf { y } \right) } \right\} \sim \Phi _ { k + 1 } ^ { ( 1 ) } - \Phi _ { k + 1 } ^ { ( - 1 ) }\tag{3.48}
$$

即数据比特 $a_k$ 的LLR值等于所有 $a_k = 1$ 的路径中的最大路径度量与所有 $a_k = -1$ 的路径中的最大路径度量之差。LLR的大小 $|\lambda_p(a_k)|$ 表示解码数据比特的可信度，LLR的符号表示数据比特的估计值：

$$
\hat { a } _ { k } = \left\{ \begin{array} { l l } { - 1 , } & { \mathrm { i f } \ \lambda _ { p } \left( a _ { k } \right) \le 0 } \\ { 1 , } & { \mathrm { i f } \ \lambda _ { p } \left( a _ { k } \right) > 0 } \end{array} \right.\tag{3.49}
$$

### 3.5.1 数据比特LLR的计算

双向SOVA算法的工作原理分为两个步骤：

1) 按照维特比算法的步骤解码数据，以找到输入数据序列的估计 $[\hat{a}_0, \hat{a}_1, ..., \hat{a}_{L-1}]$，该估计对应于ML路径，即在时间 $L+\nu$ 处具有最大路径度量的路径 $\Phi_{L+\nu}^{\mathrm{max}}$。记录 $\Phi_{L+\nu}^{\mathrm{max}}$ 和每个时间k、每个状态u的路径度量 $\Phi_k(u)$。

2) 按照原始网格图进行反向解码（backward decoding），如图3.12所示，以计算分支度量 $\tilde{\gamma}_k^b(\Psi_k = u, \Psi_{k+1} = q)$（简写为 $\tilde{\gamma}_k^b(u,q)$）和路径度量 $\Phi_k^b(u)$，从时间 $k = L+\nu$ 到 $k = 0$。路径度量计算如下[41, 42]：

$$
\Phi _ { k } ^ { b } \left( u \right) = \max _ { \forall q } \left\{ \tilde { \gamma } _ { k } ^ { b } \left( u , q \right) + \Phi _ { k + 1 } ^ { b } \left( q \right) \right\}\tag{3.50}
$$

其中初始化所有状态q的分支度量 $\Phi_{L+\nu}^b(q) = 0$。然后记录每个时间和每个状态u,q的 $\tilde{\gamma}_k^b(u,q)$ 和 $\Phi_k^b(u)$，用于计算输入数据比特的LLR值。


图3.13 双向SOVA算法步骤[41, 42]

与发射端发送的数据比特 $\{ a_k \}$ 一致，表明使用双向SOVA算法进行数据解码未发生错误。

## 反向计算

3. 初始化反向路径度量 $\Phi_4^b(u) = 0$，对于所有状态 $u = \{ a, b \}$

4. 阶段3 (k=3)：计算分支度量 $\tilde{\gamma}_3^b(u,q)$ 并更新所有状态的反向路径度量 $\Phi_3^b(u)$，结果如图3.14所示。由于时间k=3处ML路径的数据比特为 $\hat{a}_3 = 1$，互补比特 $a_3^c = -1$ 的最大路径度量由方程(3.51)求得：

$$
\begin{array} { l } { { \Phi_4^c = \max_{ \forall (u,q), \hat{a}(u,q) \neq \hat{a}_3 } \{ (\Phi_3(a) + \tilde{\gamma}_3^b(a,a) + \Phi_4^b(a)), (\Phi_3(b) + \tilde{\gamma}_3^b(b,a) + \Phi_4^b(a)) \} } } \\ { { = \max_{ \forall (u,q), \hat{a}(u,q) \neq 1 } \{ (-8.7075 - 14.8544 + 0), (-1.9111 - 4.8013 + 0) \} } } \\ { { = -6.7124 } } \end{array}
$$

因此，数据比特 $a_3$ 的MAP-LLR值由方程(3.48)求得：

$$
\lambda_p(a_3) = \Phi_4^{(1)} - \Phi_4^{(-1)} = \Phi_4^{\max} - \Phi_4^c = (-3.4558) - (-6.7124) = 3.2566
$$

5. 阶段2 (k=2)：计算分支度量并更新反向路径度量。由于ML路径数据比特 $\hat{a}_2 = 1$，互补比特 $a_2^c = -1$ 的最大路径度量为：

$$
\begin{array} { l } { { \Phi_3^c = \max_{ \forall (u,q), \hat{a}(u,q) \neq 1 } \{ (\Phi_2(a) + \tilde{\gamma}_2^b(a,a) + \Phi_3^b(a)), (\Phi_2(b) + \tilde{\gamma}_2^b(b,a) + \Phi_3^b(a)) \} } } \\ { { = \max \{ (-2.2854 - 10.6788 + 0.9686), (-6.1969 - 2.5106 + 0.9686) \} } } \\ { { = -7.7389 } } \end{array}
$$

因此：

$$
\lambda_p(a_2) = \Phi_3^{(1)} - \Phi_3^{(-1)} = \Phi_4^{\max} - \Phi_3^c = (-3.4558) - (-7.7389) = 4.2832
$$

6. 阶段1和0 (k=1和0)：按相同方法计算，得到互补比特的最大路径度量：

$$
\Phi_2^c = -7.7389 \quad \Phi_1^c = -7.7389
$$

因此：

$$
\lambda_p(a_1) = \Phi_2^{(1)} - \Phi_2^{(-1)} = \Phi_2^c - \Phi_4^{\max} = (-7.7389) - (-3.4558) = -4.2832
$$

$$
\lambda_p(a_0) = \Phi_1^{(1)} - \Phi_1^{(-1)} = \Phi_4^{\max} - \Phi_1^c = (-3.4558) - (-7.7389) = 4.2832
$$

因此，双向SOVA算法输出的数据比特 $a_k$ 的MAP-LLR值为：

$$
\{ \lambda_p(a_0), \lambda_p(a_1), \lambda_p(a_2), \lambda_p(a_3) \} \approx \{ 4.2832, -4.2832, 4.2832, 3.2566 \}
$$

## 3.6 软检测器的复杂度

这里比较第2章和第3章中描述的所有软检测器的复杂度，考虑解码每比特数据所需的加法运算符和乘法运算符的数量，基于以下准则：

- 1个选择/比较/最大化/硬判决运算符的复杂度等同于1个加法运算符。
- 加法和减法具有相同复杂度，乘法和除法具有相同复杂度。
- 各种数学函数（如自然对数函数、指数函数、绝对值函数和方程(3.16)中的纠错函数）可通过查表获得，因此不计入检测器复杂度。

表3.1 每比特解码所需的软检测器复杂度（$Q = 2^\nu$为网格图状态数，$\nu$为网格图生成目标的记忆长度）

| 软检测器 | 加法运算（每比特） | 乘法运算（每比特） |
|---------|------------------|------------------|
| BCJR (或MAP) | $14Q - 3$ | $22Q + 1$ |
| Max-Log-MAP | $24Q$ | $12Q$ |
| Log-MAP | $32Q - 4$ | $12Q$ |
| SOVA [35] | $7Q + \frac{\delta^2 + 9\delta + 9}{2} + 1$ | $6Q + 1$ |
| 双向SOVA | $17Q + 1$ | $12Q$ |

在实际电路中，乘法运算的复杂度高于加法运算。因此，这里仅考虑乘法运算数量来比较不同软检测器的复杂度（每比特），如图3.16所示。可以看出，BCJR算法的复杂度最高，特别是当目标记忆长度较大时。Max-Log-MAP、Log-MAP和双向SOVA的复杂度相同，而SOVA的复杂度最低。这就是为什么SOVA算法在各种应用的迭代解码系统（包括硬盘驱动器）中比BCJR算法更广泛使用的原因。然而，从表3.1的整体来看，复杂度从高到低依次为：BCJR、Log-MAP、Max-Log-MAP、双向SOVA、SOVA。

## 3.7 本章小结

迭代解码系统的关键组件是软检测器和软解码器，它们在彼此之间交换软信息，以帮助系统在每次迭代中提高性能。BCJR算法是一种MAP算法，可用于构建软检测器和软解码器，并能保证解码出的每个数据比特是最优的（误差最小）。然而，BCJR算法的复杂度很高，因此不常用于各种应用的迭代解码系统。

因此，本章介绍了各种类MAP算法的概念和原理，包括Max-Log-MAP、Log-MAP、SOVA和双向SOVA，它们的性能与BCJR算法接近，但复杂度更低（见表3.1）。特别是SOVA算法，其复杂度最低，但在各种应用的迭代解码系统中使用时性能接近BCJR算法（参见第4.6.2节的示例）。因此，目前SOVA算法已广泛应用于各种应用的迭代解码系统，包括硬盘驱动器。

## 3.8 习题

1. 请解释BCJR、Max-Log-MAP、Log-MAP、SOVA和双向SOVA算法之间的区别。

2. 从图2.10的信道模型出发，设输入数据序列 $a_k = \{ 1, 1, -1 \}$，信道 $H(D) = 1 - D$，噪声 $n_k = \{ -0.2, -0.3, 0.2, 0.1 \}$，方差 $\sigma^2 = 1/(2\pi)$。请使用Max-Log-MAP算法解码数据 $y_k$，设先验信息为：
   2.1) $\lambda_a(a_k) = \{ 0, 0, 0, 0 \}$
   2.2) $\lambda_a(a_k) = \{ 4, 6, -2, 0 \}$
   2.3) $\lambda_a(a_k) = \{ -4, -6, 2, 0 \}$
   2.4) 比较并解释 2.1-2.3 中检测所得的译码结果。

3. 从习题2出发，使用BCJR算法解码数据 $y_k$。

4. 从习题2出发，使用Log-MAP算法解码数据 $y_k$。

5. 从习题2出发，使用SOVA算法解码数据 $y_k$，设解码深度为：
   5.1) $\delta = 1$

5.2) $\delta = 3$

5.3) 比较并解释 5.1 和 5.2 中检测所得的译码结果。

6. 从习题2出发，使用双向SOVA算法解码数据 $y_k$。

7. 比较并解释使用不同算法（BCJR、Max-Log-MAP、Log-MAP、SOVA 和双向SOVA）对习题2进行检测所得的结果，使用与习题2相同的先验信息。

8. 从图2.10的信道模型出发，设输入数据序列 $a_k = \{ 1, 1, -1 \}$，信道 $H(D) = 1 - 2D + D^2$，噪声 $n_k = \{ 0.1, -0.2, 0.2, 0.5, -0.2 \}$，方差 $\sigma^2 = 1/(2\pi)$。请使用Max-Log-MAP算法解码数据 $y_k$，设先验信息为：
   8.1) $\lambda_a(a_k) = \{ 0, 0, 0, 0, 0 \}$
   8.2) $\lambda_a(a_k) = \{ 2, 4, -4, 0, 0 \}$
   8.3) $\lambda_a(a_k) = \{ -2, -4, 4, 0, 0 \}$
   8.4) 比较并解释 8.1 至 8.3 中检测所得的译码结果。

9. 从习题8出发，使用BCJR算法解码数据 $y_k$。

10. 从习题8出发，使用Log-MAP算法解码数据 $y_k$。

11. 从习题8出发，使用SOVA算法解码数据 $y_k$，设解码深度为：
    11.1) $\delta = 1$
    11.2) $\delta = 3$
    11.3) 比较并解释 8.1 和 8.2 中检测所得的译码结果。

12. 从习题8出发，使用双向SOVA算法解码数据 $y_k$。

13. 比较并解释使用不同算法（BCJR、Max-Log-MAP、Log-MAP、SOVA 和双向SOVA）对习题8进行检测所得的结果，使用与习题8相同的先验信息。
