# ภาคผนวก ก

# ฟังก์ชันลอการิทึมจาโคเบียน

ญ ภาคผนวกนี้จะพิสูจน์ฟังก์ชันลอการิทึ่มจาโคเบียน (Jacobian logarithm) ในสมการ (3.15) นั้นคือ

$$
\ln \left( e ^ { a } + e ^ { b } \right) = \operatorname* { m a x } \left( a , b \right) + \ln \left( 1 + e ^ { - \left| a - b \right| } \right)\tag{ก.1}
$$

เมื่อ a และ b คือค่าคงตัวใดๆ โดยการพิสูจน์จะแบ่งออกเป็น 2 กรณี ดังนี้ 1)กรณีที่ $a > b$ จะได้ว่า

$$
{ \begin{array} { r l } & { \ln \left( e ^ { a } + e ^ { b } \right) = \ln \left( e ^ { a } \left\{ 1 + { \frac { e ^ { b } } { e ^ { a } } } \right\} \right) = \ln \left( e ^ { a } \left\{ 1 + e ^ { b - a } \right\} \right) } \\ & { \qquad = \ln \left( e ^ { a } \right) + \ln \left( 1 + e ^ { - ( a - b ) } \right) } \\ & { \qquad = a + \ln \left( 1 + e ^ { - ( a - b ) } \right) } \end{array} }\tag{ก.2}
$$

2)กรณีที่ $b > a$ จะได้ว่า

$$
{ \begin{array} { r l } & { \ln \left( e ^ { a } + e ^ { b } \right) = \ln \left( e ^ { b } \left\{ { \frac { e ^ { a } } { e ^ { b } } } + 1 \right\} \right) = \ln \left( e ^ { b } \left\{ 1 + e ^ { a - b } \right\} \right) } \\ & { \qquad = \ln \left( e ^ { b } \right) + \ln \left( 1 + e ^ { - ( b - a ) } \right) } \\ & { \qquad = b + \ln \left( 1 + e ^ { - ( b - a ) } \right) } \end{array} }\tag{ก.3}
$$

$$
\ln \left( e ^ { a } + e ^ { b } \right) = \operatorname* { m a x } \left( a , b \right) + \ln \left( 1 + e ^ { - \left| a - b \right| } \right)
$$

(ก.4)

ซึ่งตรงกับสมการ (3.15) ตามที่ต้องการ

