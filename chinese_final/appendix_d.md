# 附录 D

# PR2信道的软估计

本附录将展示根据方程(5.23)推导PR2信道软估计的方法。考虑图D.1中的PR2信道模型，当输入数据序列 $a _ { k } \in \{ \pm 1 \}$ 发送至PR2信道时，即 $H \left( D \right) = \sum { { { h } _ { k } } } { { \cal { D } } ^ { k } } = 1 + 2 D + { { \cal { D } } ^ { 2 } }$，其中 $D$ 为单位延迟算子，由此得到数据序列 $r _ { k } = a _ { k } * h _ { k } \in \{ 0 , \pm 2 , \pm 4 \}$。

在接收端，Turbo均衡器为数据序列 $\{ a _ { k } \}$ 生成软信息或LLR值 $\{ \lambda _ { k } \}$，用于均衡器SOVA与LDPC译码器之间的信息交换。考虑无记忆系统，"软切片器(soft slicer)"使用LLR序列 $\{ \lambda _ { k } \}$ 计算软判决值 $\tilde { r } _ { k } = E \left[ r _ { k } \mid \left\{ \lambda _ { k } \right\} \right]$。由于PR2信道的输出数据为 {0, ±2, ±4}，因此软估计 $\tilde { r } _ { k }$ 可由下式求得：

$$
\begin{array} { r l } & { \tilde { r } _ { k } = \sum _ { i } m _ { i } \operatorname* { P r } \bigl [ r _ { k } = m _ { i } | \big \{ \lambda _ { k } \big \} \bigr ] } \\ & { \quad = ( - 4 ) \operatorname* { P r } \bigl [ r _ { k } = - 4 | \big \{ \lambda _ { k } \big \} \bigr ] + \bigl ( - 2 \bigr ) \operatorname* { P r } \bigl [ r _ { k } = - 2 | \big \{ \lambda _ { k } \big \} \bigr ] } \\ & { \qquad + \bigl ( 2 \bigr ) \operatorname* { P r } \bigl [ r _ { k } = 2 | \big \{ \lambda _ { k } \big \} \bigr ] + \bigl ( 4 \bigr ) \operatorname* { P r } \bigl [ r _ { k } = 4 | \big \{ \lambda _ { k } \big \} \bigr ] } \end{array}\tag{ง.1}
$$

其中 $m _ { i } \in \{ 0 , \pm 2 , \pm 4 \}$。定义

![](../images/appendix/bf117d47254d7d5a32ffaa39d912e4baf0501f9437081a1accc22c1bb2277add.jpg)  
图D.1 PR2信道

$$
\lambda _ { k } = \log \left( \frac { \operatorname* { P r } \left[ a _ { k } = 1 \mid \left\{ \lambda _ { k } \right\} \right] } { \operatorname* { P r } \left[ a _ { k } = - 1 \mid \left\{ \lambda _ { k } \right\} \right] } \right)
$$

可得

$$
\operatorname* { P r } \Bigl [ a _ { k } = 1 | \bigl \{ \lambda _ { k } \bigr \} \Bigr ] = \frac { e ^ { \lambda _ { k } / 2 } } { e ^ { \lambda _ { k } / 2 } + e ^ { - \lambda _ { k } / 2 } } \qquad \mathfrak { U A } _ { \circ } ^ { \circ } , \quad \operatorname* { P r } \Bigl [ a _ { k } = - 1 | \bigl \{ \lambda _ { k } \bigr \} \Bigr ] = \frac { e ^ { - \lambda _ { k } / 2 } } { e ^ { \lambda _ { k } / 2 } + e ^ { - \lambda _ { k } / 2 } }
$$

由图D.1可知，信道输出 $r _ { k } = - 4$ 当且仅当输入数据为 $\{ a _ { k } , \ a _ { k - 1 } , \ a _ { k - 2 } \} = \{ - 1 , - 1 , - 1 \}$，因此可得

$$
\mathrm { P r } \Big [ r _ { k } = - 4 \mid \big \{ \lambda _ { k } \big \} \Big ] = \mathrm { P r } \Big [ a _ { k } = - 1 \mid \big \{ \lambda _ { k } \big \} \Big ] \times \mathrm { P r } \Big [ a _ { k - 1 } = - 1 \mid \big \{ \lambda _ { k } \big \} \Big ] \times \mathrm { P r } \Big [ a _ { k - 2 } = - 1 \mid \big \{ \lambda _ { k } \big \} \Big ]
$$

$$
= \left( \frac { e ^ { - \lambda _ { k } / 2 } } { e ^ { \lambda _ { k } / 2 } + e ^ { - \lambda _ { k } / 2 } } \right) \left( \frac { e ^ { - \lambda _ { k - 1 } / 2 } } { e ^ { \lambda _ { k - 1 } / 2 } + e ^ { - \lambda _ { k - 1 } / 2 } } \right) \left( \frac { e ^ { - \lambda _ { k - 2 } / 2 } } { e ^ { \lambda _ { k - 2 } / 2 } + e ^ { - \lambda _ { k - 2 } / 2 } } \right)\tag{ง.2}
$$

信道输出 $r _ { k } = 4$ 当且仅当输入数据为 $\left\{ a _ { k } , \ a _ { k - 1 } , \ a _ { k - 2 } \right\} =$ {1, 1, 1}，因此可得

$$
\operatorname* { P r } \Big [ r _ { k } = 4 \mid \Big \{ \lambda _ { k } \Big \} \Big ] = \operatorname* { P r } \Big [ a _ { k } = 1 | \Big \{ \lambda _ { k } \Big \} \Big ] \times \operatorname* { P r } \Big [ a _ { k - 1 } = 1 | \Big \{ \lambda _ { k } \Big \} \Big ] \times \operatorname* { P r } \Big [ a _ { k - 2 } = 1 | \Big \{ \lambda _ { k } \Big \} \Big ]
$$

$$
= \left( { \frac { e ^ { \lambda _ { k } / 2 } } { e ^ { \lambda _ { k } / 2 } + e ^ { - \lambda _ { k } / 2 } } } \right) \left( { \frac { e ^ { \lambda _ { k - 1 } / 2 } } { e ^ { \lambda _ { k - 1 } / 2 } + e ^ { - \lambda _ { k - 1 } / 2 } } } \right) \left( { \frac { e ^ { \lambda _ { k - 2 } / 2 } } { e ^ { \lambda _ { k - 2 } / 2 } + e ^ { - \lambda _ { k - 2 } / 2 } } } \right)\tag{ง.3}
$$

类似地，信道输出 $r _ { k } = - 2$ 当且仅当输入数据为 $\{ a _ { k } ,$ $a _ { k - 1 } , \ a _ { k - 2 } \} = \{ - 1 , - 1 , 1 \}$ 或 {1, −1, −1}，因此可得

$$
\mathrm { P r } \Big [ r _ { k } = - 2 \mid \big \{ \lambda _ { k } \big \} \Big ] = \mathrm { P r } \Big [ a _ { k } = - 1 \mid \big \{ \lambda _ { k } \big \} \Big ] \times \mathrm { P r } \Big [ a _ { k - 1 } = - 1 \mid \big \{ \lambda _ { k } \big \} \Big ] \times \mathrm { P r } \Big [ a _ { k - 2 } = 1 | \big \{ \lambda _ { k } \big \} \Big ]
$$

---

$$
\begin{array} { r l } { \frac { \| \tilde { \rho } ( t ) - \| \tilde { \rho } ( t ) \| } { \sqrt { \pi ( t , D ) } } \Bigg | _ { t = - \infty } \Bigg | \frac { \| \tilde { \rho } ( t ) \| _ { t = \infty } \sqrt { \kappa ( t ) } } { \sqrt { \kappa ( t , D ) } } \Bigg | \frac { \tilde { \rho } ( t ) - \| \tilde { \rho } ( t ) \| _ { t = \infty } ^ { y } \sqrt { \kappa ( t ) } - \tilde { \gamma } _ { t } - \bigg | \tilde { \rho } ( t ) \| _ { t = \infty } ^ { \infty } \sqrt { \kappa ( t ) } - \tilde { \rho } ( t - t ) \sqrt { \kappa ( t ) } - \bigg | \frac { \tilde { \rho } ( t ) \tilde { \rho } ( t ) \tilde { \rho } ( t ) } { \sqrt { \kappa ( t ) - \kappa ( t ) } } \Bigg | } { \sqrt { \kappa ( t ) - \kappa ( t ) } } } & { \frac { \| \tilde { \rho } ( t ) - \| \tilde { \rho } ( t ) \| _ { t = \infty } ^ { \infty } \sqrt { \kappa ( t ) } - \sqrt { \kappa ( t ) } } { \sqrt { \kappa ( t ) - \kappa ( t ) } } } \\ & { + \mathbb { P r } \Big [ \tilde { \rho } _ { t } = 1 \| \{ \lambda _ { t } \} \Big ] \times \mathbb { P r } \Big [ \tilde { \rho } _ { t } \Big ( t _ { \infty } - 1 ) \Big | \{ \lambda _ { t } \Big \} \Big ] \times \mathbb { P r } \Big [ \tilde { \rho } _ { t } \Big ( t _ { \infty } - 1 ) \Big | \{ \lambda _ { t } \Big \} \Big ] } \\ &  = \Bigg [ \frac { \tilde { \rho } ( t ) - \tilde { \rho } ( t ) } { \sqrt { \kappa ^ { 2 } + \kappa ^ { 2 } + \lambda ^ { 2 } } } \Bigg ] \Bigg | \frac { \tilde { \rho } ( t ) - \tilde { \rho } ( t ) ^ { 2 } } { \sqrt { \kappa ^ { 2 } + \lambda ^ { 2 } } + \zeta ^ { 2 } } \Bigg | \frac  \| \tilde { \rho } ( t ) - \tilde { \rho } ( t ) \| _  t = \infty \end{array}
$$

最后，信道输出 $r _ { k } = 2$ 当且仅当输入数据为 $\{ a _ { k } , \ a _ { k - 1 } ,$ $a _ { k - 2 } \} = \{ - 1 , 1 , 1 \}$ 或 {1, 1, -1}，因此可得

$$
\begin{array} { r l } & { \operatorname* { P r } \Bigl [ r _ { k } = 2 \mid \left\{ \lambda _ { k } \right\} \Bigr ] = \operatorname* { P r } \Bigl [ a _ { k } = - 1 \mid \left\{ \lambda _ { k } \right\} \Bigr ] \times \operatorname* { P r } \Bigl [ a _ { k - 1 } = 1 \mid \left\{ \lambda _ { k } \right\} \Bigr ] \times \operatorname * { P r } \Bigl [ a _ { k - 2 } = 1 \mid \left\{ \lambda _ { k } \right\} \Bigr ] } \\ & { \qquad + \operatorname* { P r } \Bigl [ a _ { k } = 1 \mid \left\{ \lambda _ { k } \right\} \Bigr ] \times \operatorname* { P r } \Bigl [ a _ { k - 1 } = 1 \mid \left\{ \lambda _ { k } \right\} \Bigr ] \times \operatorname* { P r } \Bigl [ a _ { k - 2 } = - 1 \mid \left\{ \lambda _ { k } \right\} \Bigr ] } \\ & { = \Bigg ( \frac { e ^ { - \lambda _ { k } / 2 } } { e ^ { \lambda _ { k } / 2 } + e ^ { - \lambda _ { k } / 2 } } \Bigg ) \Bigg ( \frac { e ^ { \lambda _ { k } \nu / 2 } } { e ^ { \lambda _ { k } / 2 } + e ^ { - \lambda _ { k } / 2 } } \Bigg ) \Bigg ( \frac { e ^ { \lambda _ { k } z / 2 } } { e ^ { \lambda _ { k } z / 2 } + e ^ { - \lambda _ { k } - 2 / 2 } } \Bigg ) } \\ & { \qquad + \Bigg ( \frac { e ^ { \lambda _ { k } / 2 } } { e ^ { \lambda _ { k } z / 2 } + e ^ { - \lambda _ { k } z / 2 } } \Bigg ) \Bigg ( \frac { e ^ { \lambda _ { k } z / 2 } } { e ^ { \lambda _ { k } z / 2 } + e ^ { - \lambda _ { k } z / 2 } } \Bigg ) \Bigg ( \frac { e ^ { - \lambda _ { k } z / 2 } } { e ^ { \lambda _ { k } z / 2 } + e ^ { - \lambda _ { k } z / 2 } } \Bigg ) } \end{array}\tag{ง.5}
$$

设 $a = \lambda _ { k } / 2 , b = \lambda _ { k - 1 } / 2 ,$ 且 $c = \lambda _ { k - 2 } / 2$，将其代入方程(ง.2)-(ง.5)，再将方程(ง.2)-(ง.5)代入方程(ง.1)，利用 cosh $( x ) =$ $\left( e ^ { x } + e ^ { - x } \right) / 2$ 和 sinh $\displaystyle \left( x \right) = \left( e ^ { x } - e ^ { - x } \right) / 2$，可得

$$
\begin{array} { r l } & { \tilde { r } _ { k } = \left\{ \frac { \left( - 2 e ^ { - a } e ^ { - b } e ^ { - c } \right) + 2 e ^ { a } e ^ { b } e ^ { c } + \left( - e ^ { - a } e ^ { - b } e ^ { c } \right) + \left( - e ^ { a } e ^ { - b } e ^ { - c } \right) + e ^ { - a } e ^ { b } e ^ { c } + e ^ { a } e ^ { b } e ^ { - c } } { 4 \cosh \left( a \right) \cosh \left( b \right) \cosh \left( c \right) } \right\} } \\ & { \qquad = \left\{ \frac { - 2 e ^ { - \left( a + b + c \right) } + 2 e ^ { \left( a + b + c \right) } - e ^ { - \left( a + b - c \right) } - e ^ { - \left( c + a + b + c \right) } + e ^ { \left( c - a + b + c \right) } } { 4 \cosh \left( a \right) \cosh \left( b \right) \cosh \left( c \right) } \right\} } \\ & { \qquad = \left\{ \frac { 2 \sinh \left( a + b + c \right) + \sinh \left( a + b - c \right) + \sinh \left( - a + b + c \right) } { 2 \cosh \left( a \right) \cosh \left( b \right) \cosh \left( c \right) } \right\} } \end{array}\tag{ง.6}
$$

![](../images/appendix/4feeca1530c17304f1dd1cf5cfb7bee457d4ce4946d498eab225374b0cc3f264.jpg)

将 $a = \lambda _ { \scriptscriptstyle k } / 2 , b = \lambda _ { \scriptscriptstyle k - 1 } / 2 .$ 和 $c = \lambda _ { k - 2 } / 2$ 代入方程(ง.6)，可得最终结果

$$
\tilde { r } _ { k } = \frac { C _ { 1 } + C _ { 2 } + C _ { 3 } } { 2 \cosh \left( \lambda _ { k } \mathrm { ~ / ~ } 2 \right) \cosh \left( \lambda _ { k - 1 } \mathrm { ~ / ~ } 2 \right) \cosh \left( \lambda _ { k - 2 } \mathrm { ~ / ~ } 2 \right) }\tag{ง.7}
$$

其中常数 $C _ { 1 } = 2 \sinh \Bigl ( \bigl ( \lambda _ { k } + \lambda _ { k - 1 } + \lambda _ { k - 2 } \bigr ) / 2 \Bigr ) , ~ C _ { 2 } = \sinh \Bigl ( \bigl ( \lambda _ { k } + \lambda _ { k - 1 } - \lambda _ { k - 2 } \bigr ) / 2 \Bigr )$ 且 $C _ { 3 } = \sinh \left( \left( - \lambda _ { k } + \lambda _ { k - 1 } + \lambda _ { k - 2 } \right) / 2 \right)$，此即所求的方程(5.23)。
