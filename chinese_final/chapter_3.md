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
