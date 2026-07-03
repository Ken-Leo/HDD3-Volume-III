## 附录 C

## 方程(4.30)与(4.32)的等价性

本附录将证明方程(4.30)和(4.32)是等价的。考虑方程(4.30)中的双曲正切规则（tanh rule），即

$$
\operatorname { t a n h } \left( \frac { - \lambda _ { \Phi ( \mathbf { c } ) } } { 2 } \right) = \prod _ { i = 1 } ^ { n } \operatorname { t a n h } \left( \frac { - \lambda _ { i } } { 2 } \right)\tag{ค.1}
$$

对于实数的 $\lambda _ { i }$，有以下关系

$$
- \lambda _ { i } = \mathrm { s i g n } \left( - \lambda _ { i } \right) \times \left| - \lambda _ { i } \right|\tag{ค.2}
$$

其中 $| x |$ 表示 $x$ 的绝对值，sign $( x ) = + 1$ 当 $x \geq 0$，sign $\left( x \right) = - 1$ 当 $x < 0$。将式(ค.2)代入式(ค.1)可得两个方程

$$
\operatorname { s i g n } \left( - \lambda _ { \Phi ( \mathbf { c } ) } \right) = \prod _ { i = 1 } ^ { n } \operatorname { s i g n } \left( - \lambda _ { i } \right)\tag{ค.3}
$$

$$
\operatorname { t a n h } \left( \frac { \left| \lambda _ { \Phi ( \mathbf { c } ) } \right| } { 2 } \right) = \prod _ { i = 1 } ^ { n } \operatorname { t a n h } \left( \frac { \left| \lambda _ { i } \right| } { 2 } \right)\tag{ค.4}
$$

对式(ค.4)两边取 -log() 函数，可得

$$
f \left( \left| \lambda _ { \Phi \left( \mathbf { c } \right) } \right| \right) = \sum _ { i = 1 } ^ { n } f \left( \left| \lambda _ { i } \right| \right)\tag{ค.5}
$$

![](images/appendix/2cc42992ffbbabb2419e0d71e6fa11d21563b9c74a7200dece7801798caeb6f2.jpg)

其中 $f \bigl ( x \bigr ) = - \log \bigl ( \operatorname { t a n h } \left( x / 2 \right) \bigr )$ 如方程(4.33)所示，它具有一个重要性质：对于 $x > 0$，有 $f ( f ( x ) ) = x$。因此对式(ค.5)两边应用 $f ()$ 函数，可得

$$
\Big | \lambda _ { \Phi ( \mathbf { c } ) } \Big | = f \Bigg | \sum _ { i = 1 } ^ { n } f \big ( | \lambda _ { i } | \big ) \Bigg |\tag{ค.6}
$$

将式(ค.3)和式(ค.6)合并，得到

$$
\lambda _ { \Phi ( \mathbf { c } ) } = - \prod _ { i = 1 } ^ { n } \mathrm { s i g n } \left( - \lambda _ { i } \right) \times f \left( \sum _ { i = 1 } ^ { n } f \left( \left| \lambda _ { i } \right| \right) \right)\tag{ค.7}
$$

这正是方程(4.32)，证毕。

![](images/appendix/f77c0b70d0144d494d0186aba5f321eb933d5b55ba91b17da82d0d2e143063e7.jpg)
