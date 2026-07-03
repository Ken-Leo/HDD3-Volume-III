## ภาคผนวก ค

## ความสมมูลของสมการ (4.30) และ (4.32)

ภาคผนวกนี้จะแสดงให้เห็นว่าสมการ (4.30) และ (4.32) มีค่าเท่ากัน ให้พิจารณากฎของไฮเพอร์ โบลิกแทนเจนต์ (tanh rule) ในสมการ (4.30) นั่นคือ

$$
\operatorname { t a n h } \left( \frac { - \lambda _ { \Phi ( \mathbf { c } ) } } { 2 } \right) = \prod _ { i = 1 } ^ { n } \operatorname { t a n h } \left( \frac { - \lambda _ { i } } { 2 } \right)\tag{ค.1}
$$

สำหรับ $\lambda _ { i }$ ที่เป็นเลขจำนวนจริง จะได้ความสัมพันธุ์ดังนี้

$$
- \lambda _ { i } = \mathrm { s i g n } \left( - \lambda _ { i } \right) \times \left| - \lambda _ { i } \right|\tag{ค.2}
$$

โดยที่ $| x |$ คือค่าสัมบูรณ์ของ $x ,$ และ sign $( x ) = + 1$ เมื่อ $x \geq 0$ และ sign $\left( x \right) = - 1$ เมื่อ $x < 0$ จากนันแทนค่าสมการ (ค.2) ลงในสมการ (ค.1) ก็จะได้ผลลัพธ์เป็น 2 สมการคือ

$$
\operatorname { s i g n } \left( - \lambda _ { \Phi ( \mathbf { c } ) } \right) = \prod _ { i = 1 } ^ { n } \operatorname { s i g n } \left( - \lambda _ { i } \right)\tag{ค.3}
$$

$$
\operatorname { t a n h } \left( \frac { \left| \lambda _ { \Phi ( \mathbf { c } ) } \right| } { 2 } \right) = \prod _ { i = 1 } ^ { n } \operatorname { t a n h } \left( \frac { \left| \lambda _ { i } \right| } { 2 } \right)\tag{ค.4}
$$

ใส่ฟังก์ชัน -1og() เข้าไปทั้งสองข้างของสมการ (ค.4) ก็จะได้

$$
f \left( \left| \lambda _ { \Phi \left( \mathbf { c } \right) } \right| \right) = \sum _ { i = 1 } ^ { n } f \left( \left| \lambda _ { i } \right| \right)\tag{ค.5}
$$

![](images/appendix/2cc42992ffbbabb2419e0d71e6fa11d21563b9c74a7200dece7801798caeb6f2.jpg)

โดยที่ $f \bigl ( x \bigr ) = - \log \bigl ( \operatorname { t a n h } \left( x / 2 \right) \bigr )$ ตามสมการ (4.33) ซึ่งมีคุณสมบัติที่สำคัญคือ $f ( f ( x ) ) = x$ สำหรับ $x > 0$ ดังนั้นถ้าใส่ฟังก์ชัน f () เข้าไปทั้งสองข้างของสมการ (ค.5) ก็จะได้

$$
\Big | \lambda _ { \Phi ( \mathbf { c } ) } \Big | = f \Bigg | \sum _ { i = 1 } ^ { n } f \big ( | \lambda _ { i } | \big ) \Bigg |\tag{ค.6}
$$

และเมื่อนำสมการ (ค.3) และ (ค.6) มารวมกัน ก็จะได้ผลลัพธ์เป็น

$$
\lambda _ { \Phi ( \mathbf { c } ) } = - \prod _ { i = 1 } ^ { n } \mathrm { s i g n } \left( - \lambda _ { i } \right) \times f \left( \sum _ { i = 1 } ^ { n } f \left( \left| \lambda _ { i } \right| \right) \right)\tag{ค.7}
$$

ซึ่งตรงกับสมการ (4.32) ตามที่ต้องการ

![](images/appendix/f77c0b70d0144d494d0186aba5f321eb933d5b55ba91b17da82d0d2e143063e7.jpg)
