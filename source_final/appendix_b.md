# ภาคผนวกข

# กฎของไฮเพอร์โบลิกแทนเจนต์

ภาคผนวกนี้จะพิสูจน์กฎของไฮเพอร์โบลิกแทนเจนต์ (tanh rนle) ในสมการ (4.30) ดังนี้ ถ้าให้ ฟังก์ชันพาริตี $\Phi ( \mathbf { c } ) \in \{ 0 , 1 \}$ คือค่าพาริตีของเซตข้อมูล $\mathbf { c } = [ c _ { 1 } , \ c _ { 2 } , \ . . . , \ c _ { n } ]$ จำนวน n บิต เมื่อ $c _ { i } \in \{ 0 , 1 \}$ ดังนั้นฟังก์ชันพาริตี 4(c) สามารถหาได้จาก

$$
\Phi \left( \mathbf { c } \right) = \frac { 1 } { 2 } \Bigg ( 1 - \prod _ { i = 1 } ^ { n } \left( 1 - 2 c _ { i } \right) \Bigg )\tag{ข.1}
$$

เนืองจาก $\Phi ( \mathbf { c } ) = 0$ โดยที่ c มีเลขหนึ่งรวมกันเป็นจำนวนคู่และ $\Phi ( \mathbf { c } ) = 1$ เมื่อ c มีเลขหนึ่ง รวมกันเป็นจำนวนดี นอกจากนีความน่าจะเป็น (probability) $\stackrel { \mathrm { d } } { \bar { \eta } } \Phi ( \mathbf { c } ) = 1$ มีค่าเท่ากับค่าคาดหมาย (expected value) ของ $\Phi ( \mathbf { c } )$ นั่นคือ

$$
\begin{array} { r l } { \operatorname { p } _ { t } [ \Phi ( \mathbf { x } ) - 1 ] = E \left\{ \Phi ( \mathbf { x } ) \right\} } \\ { \ } & { = ( 1 ) \operatorname { P r } _ { [ \tilde { \mathbf { e } } ] } ( \mathbf { x } ) = 1 ] + ( 0 ) \operatorname { P r } _ { [ \tilde { \mathbf { e } } ] } ( \mathbf { \Phi } \mathbf { e } ) = 0 ] } \\ { \ } & { = \frac { 1 } { 2 } \Bigg ( 1 - E \left[ \underset { \mathrm { i } \sim 1 } { \overset { \times } { \prod } } \left( 1 - 2 \epsilon _ { s } \right) \right] } \\ { \ } &  = \frac { 1 } { 2 } \Bigg ( 1 - \underset { \mathrm { i } \sim 1 } { \overset { \times } { \prod } } \left( 1 - 2 E \left[ \epsilon _ { s } \right] \right) \Bigg ) \quad \ ( \underset { \mathrm { i } \sim 1 } { \overset { \cdot } { \prod } } \mathrm { a r s i m m a n ~ m a x i n ~ f i a \bar { \mathbf { k } } \bar { \mathbf { q } } \cdot \mathbf { n } \bar { \mathbf { q } } \bar { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } ) } \\ { \ } &  = \frac { 1 } { 2 } \Bigg ( 1 - \underset { \mathrm { i } \sim 1 } { \overset { \cdot } { \prod } } \left( 1 - \frac { 2 E ^ { d } } { 1 + \epsilon ^ { k } } \right) \Bigg ) \quad \ ( \underset { \mathrm { i } \sim 1 } { \overset { \cdot } { \prod } } \mathrm { a r s i m m a \bar { \mathbf { n } } } ) \mathrm  a r s i n ~ f i a \bar { \mathbf { k } } \bar { \mathbf { q } } \cdot \mathbf { n } \bar { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde { \mathbf { n } } \tilde  \mathbf  n \end{array}
$$

![](images/appendix/c87249c1fe612a6b3a1340531f5d95267fe2fdc9d919b3cbb7afe280c7277ee8.jpg)

เมื่อ $E [ . ]$ คือตัวดำเนินการค่าคาดหมาย (expectation operator) และเนื่องจาก $\mathrm { P r } \big [ \Phi ( \mathbf { c } ) = 0 \big ] =$ $1 - \mathrm { P r } \big [ \Phi ( \mathbf { c } ) = 1 \big ]$ เพราะฉะนั้นค่า LLR ของ $\Phi ( \mathbf { c } )$ มีค่าเท่ากับ

$$
\lambda _ { \Phi ( \mathbf { c } ) } = \log \left( \frac { \operatorname* { P r } \bigl [ \Phi \left( \mathbf { c } \right) = 1 \bigr ] } { \operatorname* { P r } \bigl [ \Phi \left( \mathbf { c } \right) = 0 \bigr ] } \right) = \log \left( \frac { 1 - \prod _ { i } \operatorname { t a n h } \left( - \lambda _ { i } / 2 \right) } { 1 + \prod _ { i } \operatorname { t a n h } \left( - \lambda _ { i } / 2 \right) } \right)\tag{ข.3}
$$

อาศัยคุณสมบัติที่ว่า $\operatorname { t a n h } \left( - \lambda / 2 \right) = \left( 1 - e ^ { \lambda } \right) / \left( 1 + e ^ { \lambda } \right)$ และให้ $\Psi = \prod _ { i = 1 } ^ { n } \operatorname { t a n h } \left( - \lambda _ { i } / 2 \right)$ ดังนั้น

$$
\operatorname { t a n h } \left( \frac { - \lambda _ { \Phi ( \mathbf { c } ) } } { 2 } \right) = \frac { 1 - \left( \displaystyle \frac { 1 - \Psi } { 1 + \Psi } \right) } { 1 + \displaystyle \left( \frac { 1 - \Psi } { 1 + \Psi } \right) } = \frac { ( 1 + \Psi ) - \left( 1 - \Psi \right) } { ( 1 + \Psi ) + ( 1 - \Psi ) } = \Psi = \prod _ { i = 1 } ^ { n } \operatorname { t a n h } \left( \frac { - \lambda _ { i } } { 2 } \right)\tag{ข.4}
$$

ซึ่งตรงกับสมการ (4.30) ตามที่ต้องการ

![](images/appendix/bf800668762ad4f63171637ffb183d3d10d9c014ed6ecd42a7e705e6452422ed.jpg)
