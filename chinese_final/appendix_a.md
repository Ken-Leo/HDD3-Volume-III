# 附录 A

# 雅可比对数函数

本附录将推导方程(3.15)中的雅可比对数函数（Jacobian logarithm），即

$$
\ln \left( e ^ { a } + e ^ { b } \right) = \operatorname* { m a x } \left( a , b \right) + \ln \left( 1 + e ^ { - \left| a - b \right| } \right)\tag{ก.1}
$$

其中 a 和 b 为任意常数。推导分为两种情况：1) 当 $a > b$ 时，

$$
{ \begin{array} { r l } & { \ln \left( e ^ { a } + e ^ { b } \right) = \ln \left( e ^ { a } \left\{ 1 + { \frac { e ^ { b } } { e ^ { a } } } \right\} \right) = \ln \left( e ^ { a } \left\{ 1 + e ^ { b - a } \right\} \right) } \\ & { \qquad = \ln \left( e ^ { a } \right) + \ln \left( 1 + e ^ { - ( a - b ) } \right) } \\ & { \qquad = a + \ln \left( 1 + e ^ { - ( a - b ) } \right) } \end{array} }\tag{ก.2}
$$

2) 当 $b > a$ 时，

$$
{ \begin{array} { r l } & { \ln \left( e ^ { a } + e ^ { b } \right) = \ln \left( e ^ { b } \left\{ { \frac { e ^ { a } } { e ^ { b } } } + 1 \right\} \right) = \ln \left( e ^ { b } \left\{ 1 + e ^ { a - b } \right\} \right) } \\ & { \qquad = \ln \left( e ^ { b } \right) + \ln \left( 1 + e ^ { - ( b - a ) } \right) } \\ & { \qquad = b + \ln \left( 1 + e ^ { - ( b - a ) } \right) } \end{array} }\tag{ก.3}
$$



$$
\ln \left( e ^ { a } + e ^ { b } \right) = \operatorname* { m a x } \left( a , b \right) + \ln \left( 1 + e ^ { - \left| a - b \right| } \right)
$$

(ก.4)

这与方程(3.15)一致，证毕。

