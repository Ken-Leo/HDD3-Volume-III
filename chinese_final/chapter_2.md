# 第2章

## Turbo 码

目前，纠错码 [1-3] 有多种类型可供选择，具体取决于每个应用的使用特性。一般来说，需要高纠错能力的应用也必须使用高度复杂的编码和解码电路。一个简单的解决方法是使用级联编码（concatenated coding），即使用多个编码器以串联或并联方式级联，借助交织器（interleaver）的帮助。随后，编码后的数据由每个解码器分别解码。虽然这种方法的结果被认为是次优的（sub-optimal），但它在纠错能力和编解码过程的复杂度之间取得了权衡。

迭代解码技术（iterative decoding）[2, 3] 是一种能够显著降低系统误比特率（BER: bit-error rate）的技术。Turbo 码（turbo code）[3] 的数据解码是迭代解码的一个例子，目前已广泛应用于移动电话系统和卫星通信系统等应用中。此外，用于 Turbo 数据解码的 Turbo 原理还可以应用于均衡（equalization）过程，这种技术称为"Turbo 均衡（turbo equalization）" [21]，这是一种已在新型硬盘驱动器 [6] 中实际应用的迭代解码过程，其性能优于过去未使用迭代解码技术的硬盘驱动器。

本章将从解释卷积码和 BCJR 算法 [18] 开始，它们是 Turbo 码的重要组成部分，使读者理解硬盘驱动器信号处理系统中使用的迭代编解码技术。

## 2.1 卷积码

纠错码，或称为前向纠错码（FEC: forward error correction code），常用于处理信道产生的噪声和错误。一般来说，纠错码可分为两类：分组码（block code）和卷积码（convolutional code）[2]。此外，还有利用迭代解码技术的新型 ECC 码，如 Turbo 码 [3] 和 LDPC 码 [17] 等，它们的性能更接近香农的信道容量（Shannon's channel capacity），优于卷积码。本节将总结卷积码的工作原理，因为它是 Turbo 码的重要组成部分，将在第2.3节中进一步讨论。

### 2.1.1 编码

卷积编码器（convolutional encoder）使用移位寄存器（shift register）和模二加法器（modulo-2 adder）进行数据编码。它对一个输入数据序列进行编码，并生成一个或多个输出数据序列。如果卷积编码器对1比特输入数据进行编码，产生 n 比特输出数据，则该卷积编码器的码率（code rate）为 $R = 1 / n$。图2.1显示了码率为 $R = 1 / 2$ 的卷积编码器示例，其中 D 是单位延迟算子（unit delay operator），用于表示移位寄存器。在实际中，卷积编码器用生成多项式（generator polynomial）表示，其方程为 [1]

$$
G ( D ) = \sum _ { i = 0 } ^ { \mu } g _ { i } D ^ { i }\tag{2.1}
$$

其中 $\mu$ 是卷积编码器的存储器数（或移位寄存器数量），如果延迟 i 个单位的输入比特对当前时刻的输出比特有影响，则 $g _ { i } = 1$。例如，图2.1(a)中的卷积编码器的生成多项式为

$$
G \big ( D \big ) = \big [ G _ { 1 } \big ( D \big ) , G _ { 2 } \big ( D \big ) \big ] = \big [ 1 \oplus D , 1 \oplus D ^ { 2 } \big ]\tag{2.2}
$$

![](images/chapter_2/fdd6f0486f8903842f50ee814e393ac2a6981accc0a8426c8ea4b7e701803dc6.jpg)  
(ก)

![](images/chapter_2/a3d4cc6da421c13685ce322cdd8c8e8fe290a429d8214753d8444f9d974b5327.jpg)  
(ข)

![](images/chapter_2/61ca9ff0fd72dd7f40498c12d0794e5037e661d264e3421c88e74ec8404c2948.jpg)  
(ค)  
图2.1 (a) 卷积编码器, (b) 系统卷积编码器, 以及 (c) 递归系统卷积编码器

其中 $\oplus$ 是模二加法算子，$G _ { 1 } ( D )$ 是输出数据 $y _ { k } ^ { 1 }$ 的生成多项式，$G _ { 2 } ( D )$ 是输出数据 $y _ { k } ^ { 2 }$ 的生成多项式，存储器数为 $\mu = 2$。

此外，系统卷积编码器（systematic convolutional encoder）是一种输出数据序列之一等于输入数据的卷积编码器，如图2.1(b)所示，其生成多项式为 $[1, 1 \oplus D ^ { 2 }]$。带有反馈的系统卷积编码器称为递归系统卷积编码器（recursive systematic convolutional encoder），如图2.1(c)所示，其生成多项式为 $\left[ 1 , 1 / \left( 1 \oplus D ^ { 2 } \right) \right]$。通常，递归系统卷积编码器比其他类型的卷积编码器更常用 [2]。

一般来说，卷积码的分析借助有限状态机（FSM: finite state machine），这是一个展示系统输入数据、起始状态（start state）、下一状态（next state）和输出数据变化的模型（详见 [10] 第4.3.1节）。图2.2（左）显示了图2.1(a)中卷积编码器的有限状态机，共有 $2 ^ { \mu } = 4$ 个状态：00、01、10 和 11。箭头线表示状态转移路径，箭头旁的值 $x / y ^ { 1 } y ^ { 2 }$ 表示输入比特 x 和输出比特 $y ^ { 1 }$、$y ^ { 2 }$ 的值。此外，网格图（trellis diagram）用于表示每个时刻的状态转移，也可以用来解释卷积码的工作原理。图2.2（右）显示了图2.1(a)中卷积编码器的网格图。即在第 k 阶段的网格图显示了编码器从时刻 k 的一个状态到时刻 k+1 的另一个状态的所有可能状态转移。箭头旁的值与有限状态机中的 $x / y ^ { 1 } y ^ { 2 }$ 相同。由于沿着网格图行走的路径（path）由一组分支（branch）组成，每个阶段一个分支，因此每个码字（codeword）（即卷积编码器的输出数据）必须对应于网格图中唯一的一条路径（unique path）（见图2.5）。

![](images/chapter_2/4660a13e31ce5fa0c221152df920b6a07f43231a1ac109d8084b1afc0d846ab6.jpg)  
图2.2 图2.1(a)的有限状态机图和网格图

例2.1 请展示图2.1(a)中卷积编码器的编码步骤，当输入数据比特为 {x0, x1, x2, x3} = {1 0 1 1} 时。

解法 图2.1(a)可重新绘制如右图所示。将比特数据 $\{ x _ { k } \}$ 用卷积编码器编码的步骤如下：

![](images/chapter_2/affcb8197897396222aa4bbbe14ffb9054eb03772958b753fe07c505eacf11dc.jpg)

第一步，将所有移位寄存器的状态，即 $\mathrm { S } _ { 1 }$ 和 $\mathrm { S } _ { 2 }$ 设为 0（使其处于状态 00）。此步骤仅用于编码器的准备工作，尚未输入任何数据比特。

第二步，开始输入第一个比特，值为 1（即 $x _ { 0 } = 1$），使得 $\mathrm { Y } _ { 1 } = \mathrm { X } \oplus \mathrm { S } _ { 1 } = 1 \oplus 0 = 1$ 和 $\mathrm { Y } _ { 2 } = \mathrm { X } \oplus \mathrm { S } _ { 2 } = 1 \oplus 0 = 1$，这就是第一个比特编码得到的输出数据。

第三步，开始输入第二个比特，值为 0。电路中的各值向右移位一个比特：$\mathbf { S } _ { 1 } = 1$，$\mathbf { S } _ { 2 } = 0$，使得 $\mathrm { Y } _ { 1 } = \mathrm { X } \oplus \mathrm { S } _ { 1 } = 0 \oplus 1 = 1$ 和 $\mathrm { Y } _ { 2 } = \mathrm { X } \oplus \mathrm { S } _ { 2 } = 0 \oplus 0 = 0$，这就是第二个比特编码的结果。

第四步，开始输入第三个比特，值为 1。电路中的所有值再向右移位一个比特（此时 $\mathbf { S } _ { 1 } = 0$，$S _ { 2 } = 1$），使得 $\mathrm { Y } _ { 1 } = \mathrm { X } \oplus \mathrm { S } _ { 1 } = 1 \oplus 0 = 1$ 和 $\mathrm { Y } _ { 2 } = \mathrm { X } \oplus \mathrm { S } _ { 2 } = 1 \oplus 1 = 0$，这就是第三个比特编码的结果。

第五步，按上述步骤继续处理第四个比特。

第六步，观察到卷积编码器的状态并未回到全零的初始状态（目前处于状态 11）。因此需要准备适当的 2 个尾比特（tail bit），使电路回到全零状态，编码过程才算完成。

最后一步，选择尾比特的值的简单原则是：考虑哪些数据比特能使移位寄存器中的值全为零。此处输入两个 0 比特到电路中即可使编码器回到状态 00，编码过程结束。第一个尾比特输出 $\mathrm { Y } _ { 1 } = 1$ 和 $\mathrm { Y } _ { 2 } = 1$，第二个尾比特输出 $\mathrm { Y } _ { 1 } = 0$ 和 $\mathrm { Y } _ { 2 } = 1$。

上述编码示例如图2.3所示。若以状态转移图表示则如图2.4所示，若以网格图表示则如图2.5所示。可以看出图2.3至图2.5给出了相同的结果。

此外，卷积编码还可以通过 D 变换（D transform）[1] 实现。即卷积编码器得到的输出数据等于

$$
Y _ { i } \left( D \right) = G _ { i } \left( D \right) X \left( D \right)\tag{2.3}
$$

![](images/chapter_2/6e7b0ebeb9893e77b0aa77a03ea8849fad88b70ea6e7c053b8538d363c9d27d1.jpg)

![](images/chapter_2/289ee4152f9c5f680bd44480601538dbec672dc6d82a14890c01d44d7136a564.jpg)  
图2.3 例2.1中卷积编码的步骤

![](images/chapter_2/b10e85b46aae178f077f51211c97346c53eec561c2d68cad39820511dd061442.jpg)  
图2.4 例2.1中的状态转移图

其中 $Y _ { i } \left( D \right) = \sum _ { k } y _ { k } ^ { i } D ^ { k }$ 是输出数据 $y _ { k } ^ { i }$ 的 D 变换结果，$i \in \left\{ 1 , 2 \right\}$，$G _ { i } ( D )$ 是输出数据 $y _ { k } ^ { i }$ 的生成多项式，$X ( D ) = \sum _ { k } x _ { k } D ^ { k }$ 是输入数据的 D 变换结果。例如，从例2.1（图2.1(a)）可得 $X \left( D \right) = 1 + D ^ { 2 } + D ^ { 3 }$，$G _ { i } \left( D \right)$ 由方程(2.2)给出。因此两组编码输出数据 $\left\{ y _ { k } ^ { 1 } , y _ { k } ^ { 2 } \right\}$ 为

![](images/chapter_2/f939713de2b94ad187298ae69983a48655f694b8026c8780d9ff5872bfcde68f.jpg)  
图2.5 例2.1中的网格图（显示码字的唯一可能路径）

$$
\begin{array} { c } { { Y _ { 1 } \bigl ( D \bigr ) = G _ { 1 } \bigl ( D \bigr ) X \bigl ( D \bigr ) = \bigl ( 1 \oplus D \bigr ) \bigl ( 1 + D ^ { 2 } + D ^ { 3 } \bigr ) } } \\ { { { } } } \\ { { { } = \bigl ( 1 + D ^ { 2 } + D ^ { 3 } \bigr ) \oplus \bigl ( D + D ^ { 3 } + D ^ { 4 } \bigr ) } } \\ { { { } } } \\ { { { } = 1 + D + D ^ { 2 } + D ^ { 4 } } } \end{array}
$$

$$
\begin{array} { c } { { Y _ { 2 } \left( D \right) = G _ { 2 } \left( D \right) X \left( D \right) = \left( 1 \oplus { D ^ { 2 } } \right) \left( 1 + { D ^ { 2 } } + { D ^ { 3 } } \right) } } \\ { { { } } } \\ { { { } = \left( 1 + D ^ { 2 } + D ^ { 3 } \right) \oplus \left( { D ^ { 2 } } + { D ^ { 4 } } + { D ^ { 5 } } \right) } } \\ { { { } } } \\ { { { } = 1 + D ^ { 3 } + D ^ { 4 } + D ^ { 5 } } } \end{array}
$$

即 $\left\{ y _ { 0 } ^ { 1 } , y _ { 1 } ^ { 1 } , y _ { 2 } ^ { 1 } , y _ { 3 } ^ { 1 } , y _ { 4 } ^ { 1 } , y _ { 5 } ^ { 1 } \right\} = \left\{ 1 \ 1 \ 1 \ 0 \ 1 \ 0 \right\}$ 和 $\left\{ y _ { 0 } ^ { 2 } , y _ { 1 } ^ { 2 } , y _ { 2 } ^ { 2 } , y _ { 3 } ^ { 2 } , y _ { 4 } ^ { 2 } , y _ { 5 } ^ { 2 } \right\} = \left\{ 1 \ 0 \ 0 \ 1 \ 1 \ 1 \right\}$，与图2.3至图2.5得到的输出数据一致。

例2.2 考虑图2.6中的卷积编码器，其生成多项式以八进制数表示为 $(g _ { 1 } , g _ { 2 } ) = ( 1 7 , 1 1 )$，即二进制(001111, 001001)。其中 $g _ { 1 }$ 称为反馈多项式（feedback polynomial），$g _ { 2 }$ 称为前馈多项式（feedforward polynomial）。在某些书籍中，生成多项式以 D 域的分数形式表示为 $\frac { g _ { 2 } ( D ) } { g _ { 1 } ( D ) } = \frac { 1 + D ^ { 3 } } { 1 + D + D ^ { 2 } + D ^ { 3 } }$。请绘制有限状态机图，并对数据比特 11011100 进行编码（最左边的比特是第一个被编码的数据）。

解法 该卷积编码器的有限状态机图如图2.7所示。对于数据比特 11011100 的编码，步骤与例2.1类似：首先将所有移位寄存器的状态设为 0，然后逐比特输入数据到电路中，逐一计算编码器的输出数据。当所有输入数据比特输入完毕后，再输入若干尾比特，直到所有移位寄存器的值恢复为 0。

![](images/chapter_2/a7669eeb48b0121dcbde8d0fe7a39adf1364758b56d935abc59cf80bf687e581.jpg)  
图2.6 生成多项式以八进制数表示的卷积编码器 (91, 92) = (17, 11)

![](images/chapter_2/8ff9e58b837269068f9c807dcb26d660e4d45b61faca34f6674f66f51ed01790.jpg)  
图2.7 图2.6中卷积编码器的有限状态机（FSM）图

若操作正确，需要输入到编码器中的尾比特为 111，编码结果为 10101110001。

![](images/chapter_2/0f7265db08ac699dff5cd34dd1ce221dd04c53eddd5c0a3b3bace5f94a56777d.jpg)  
(a) 卷积编码器

![](images/chapter_2/0f237b78c331bf9d3febf15d6fad5324092a214a2a29a82b925d71b5844349ba.jpg)  
图2.8 (a) 卷积编码器 和 (b) 网格图

### 2.1.2 解码

在实践中，用卷积码编码的数据可以使用基于维特比算法 [13] 的解码器进行解码，即维特比检测器。下面给出卷积码解码的示例。

例2.3 考虑图2.8(a)中的卷积编码器，其网格图如图2.8(b)所示。假设序列 $z _ { k }$ 是解码器需要解码的数据序列，请解码数据序列 $z _ { k } = \{ 1 1 ~ 0 1 ~ 1 0 ~ 1 1 ~ 0 0 \}$。

解法 用 $(u, q)$ 表示从状态 u 到状态 q 的状态转移。在第 k 阶段的分支度量（branch metric）定义为

$$
\rho _ { k } \left( u , q \right) = \left| z _ { k } ^ { 0 } - \tilde { x } _ { k } \left( u , q \right) \right| ^ { 2 } + \left| z _ { k } ^ { 1 } - \tilde { y } _ { k } \left( u , q \right) \right| ^ { 2 }
$$

其中 $\tilde { x } _ { k } \left( u , q \right)$ 和 $\tilde { y } _ { k } \left( u , q \right)$ 是对应于状态转移 $(u, q)$ 的比特数据 $x _ { k }$ 和 $y _ { k }$。此外，在时刻 $k+1$ 时状态 q 的路径度量（path metric）定义为

![](images/chapter_2/bfdcee2492d2e7984a48a41068316e14201c03ba80d353ab577b4acba9132c79.jpg)

![](images/chapter_2/00d83815be7550f8bd3d127ac22877d31738af7978dec49a26468b9fae0b8694.jpg)  
图2.9 网格图显示数据序列 $z _ { k } = \{ 1 1 ~ 0 1 ~ 1 0 ~ 1 1 ~ 0 0 \}$ 的解码过程

$$
\Phi _ { k + 1 } \left( q \right) = \operatorname* { m i n } _ { u } \left\{ \Phi _ { k } \left( u \right) + \rho _ { k } \left( u , q \right) \right\}
$$

因此维特比检测器的解码步骤如下：

1) 对于每个阶段 k
   对于每个状态 q
   计算到达状态 q 的所有分支的分支度量 $\rho _ { k } \left( u , q \right)$
   选择具有最小路径度量的分支
   更新状态 q 在时刻 $k+1$ 的路径度量 $\Phi _ { k + 1 } \left( q \right)$
   （对所有状态 q 重复）
   （对所有阶段 k 重复）
2) 从具有最小路径度量的路径解码输入数据 $x _ { k }$

图2.9显示了网格图上的数据解码过程，其中只显示了到达每个状态的存留路径（survivor path）。每条分支旁的值是对应于状态转移 (u, q) 的分支度量 $\rho _ { k } \left( u , q \right)$，每个状态节点处的数字是路径度量 $\Phi _ { k } \left( q \right)$。从图中可以看出，卷积解码器给出的输入数据比特估计值为 $\hat { x } _ { k } = \left\{ 1 , 0 , 1 , 1 \right\}$。有关维特比检测器数据解码过程的详细步骤，可参见 [10] 的第4章。

然而，当卷积码用作 Turbo 码的组成部分时，不能在 Turbo 解码器中使用维特比检测器，因为 Turbo 解码器仅使用比特数据的软信息工作（而维特比检测器输出的是硬信息或比特数据的估计值）。因此，用于解码卷积码的 Turbo 解码器必须使用基于 BCJR 算法 [18] 或 SOVA（soft-output Viterbi algorithm）[19] 的检测器。这些内容将在第2.2节和第3章中分别说明。

## 2.2 BCJR 算法

维特比检测器 [1, 13] 是一种最大似然（ML: maximum-likelihood）检测器，用于解码卷积码。其输出数据是待检测数据序列的估计值。或者说，ML 检测器使序列错误最小化，但不保证序列中的每个比特都是最优的。即 ML 检测器不能使每个比特的错误最小化。

此外，维特比检测器不能用于迭代解码系统，因为该系统需要在检测器和纠错解码器之间交换软信息。因此，迭代解码系统必须使用最大后验概率检测器，称为"MAP 检测器（maximum a posteriori probability）"。MAP 检测器可以保证每个检测到的比特都是最优的（即每个比特的错误最小化）。

本部分将解释 BCJR 算法 [18] 的工作原理，因为它是构建 MAP 检测器所使用的算法。该算法由 Bahl、Cock、Jelinek 和 Raviv 共同发明和开发，用于检测经过具有符号间干扰（ISI）和加性高斯白噪声（AWGN）的信道后的信号的最大后验概率（APP: a posteriori probability）。

### 2.2.1 信道模型与网格图

考虑图2.10中的信道模型。接收端接收到的信号（即待解码的信号）的第 k 个序列为

![](images/chapter_2/98f482bfb4db09e868ad979b730a00ad8c3fb6261659dd759e0a9e2061a39768.jpg)

![](images/chapter_2/13288854ed7e62697483a118c3cf31b6a8fd9eaeadd2cb114dc6cc44b508b4d5.jpg)  
图2.10 信道模型

![](images/chapter_2/f7031e73ef337e6de6bd95f65b0c3267b80bfbe843f60cf64742eb4366e54336.jpg)  
图2.11 网格图第 k 阶段的状态转移 (u, q)

$$
y _ { k } = \sum _ { i = 0 } ^ { \nu } a _ { i } h _ { k - i } + n _ { k }\tag{2.4}
$$

其中 $a _ { k } \in { \mathcal { A } }$ 是从字符集 $\mathcal { A }$ 中选择的输入数据比特（例如二进制系统为 $\mathcal { A } = \{ 0 , 1 \}$ 或 $\{ - 1 , 1 \}$），$H ( D ) = \sum _ { k = 0 } ^ { \nu } h _ { k } D ^ { k }$ 是离散信道（discrete channel），$h _ { k }$ 是信道的第 k 个系数，ν 是信道存储器，$n _ { k }$ 是均值为零、方差为 $\sigma ^ { 2 }$ 的 AWGN，记为 $n _ { k } \sim \mathcal { N } ( 0 , \sigma ^ { 2 } )$，$r _ { k }$ 是信道的输出数据，L 是输入数据序列 $\{ a _ { k } \}$ 的长度。通常一个扇区的数据有 L = 4096 比特。假设发送端发送了 L 比特的输入数据序列 $\mathbf { a } = \left[ a _ { 0 } , . . . , a _ { L - 1 } \right]$，每个数据比特的可能值在集合 A 内，且在 $k < 0$ 和 $k > L - 1$ 的时间段内没有数据传输。因此，由方程(2.4)，接收端接收到的所有信号以向量形式表示为 $\mathbf { y } = \left\{ y _ { l } \right\} _ { 0 } ^ { L + \nu - 1 } = \left[ y _ { 0 } , . . . , y _ { L + \nu - 1 } \right]$。

图2.11显示了信道 $h _ { k }$ 的网格图，其中 $\Psi _ { k } \equiv \left[ a _ { k - 1 } , a _ { k - 2 } , . . . , a _ { k - \nu } \right]$ 是时刻 k 的状态（state）（即时刻 k 所有移位寄存器中的值），$Q = \left| \mathcal { A } \right| ^ { \nu }$ 是所有可能的状态总数，第 k 阶段（k-th stage）是时刻 k 和时刻 $k+1$ 之间所有可能的分支（branch）组，$(u, q)$ 是表示从状态 u 到状态 q 的状态转移的符号。如果每个状态从 0 到 $Q-1$ 编号，其中状态 0 或 $\psi _ { k } \equiv \left[ 0 , 0 , . . . , 0 \right]$ 表示空闲状态（idle state），对应 $k \leq 0$ 和 $k \geq L + \nu - 1$。因此，可以说图2.11显示了网格图的第 k 阶段，对应于第 k 个输入数据比特 $a _ { k }$、第 k 个信道输出数据 $r _ { k }$ 和第 k 个接收端接收到的数据 $y _ { k }$。

### 2.2.2 最优检测器

在实践中，MAP 检测器被认为是最优检测器（optimal detector），因为它是能够保证每个数据比特的错误概率最小的数据检测器。例如，在判决第 k 个数据比特 $a _ { k }$ 时，MAP 检测器会计算后验概率（APP）即 $\operatorname* { P r } [ a _ { k } \mid \mathbf { y } ]$，它表示在给定序列 y 时数据比特 $a _ { k }$ 的概率。对于每个数据比特 $a _ { k }$，选择使 $\operatorname* { P r } [ a _ { k } \mid \mathbf { y } ]$ 最大的 $a _ { k }$ 值。MAP 检测器对 L 个数据比特逐个执行此操作。在实践中，如果知道网格图中每个状态转移 $(u, q)$ 的后验状态转移概率 $\operatorname* { P r } [ \psi _ { k } = u ; \Psi _ { k + 1 } = q \mid \mathbf { y } ]$，则 $\operatorname* { Pr } [ a _ { k } \mid \mathbf { y } ]$ 可以很容易地计算出来。

BCJR 算法是一种在求解后验状态转移概率方面非常高效的算法。它通过将时刻 k 的状态转移概率 $\operatorname* { P r } [ \psi _ { k } = u ; \Psi _ { k + 1 } = q \mid \mathbf { y } ]$ 分解为三个部分：

1) 第一部分依赖于过去接收到的所有数据，即 $\mathbf { y } _ { l < k } = \{ y _ { l } ; l < k \} = \{ y _ { l } \} _ { 0 } ^ { k - 1 }$

2) 第二部分依赖于当前接收到的数据，即 $y _ { k }$

3) 第三部分依赖于未来接收到的所有数据，即 ${ \bf y } _ { l > k } = \left\{ y _ { l } ; l > k \right\} = \left\{ y _ { l } \right\} _ { k + 1 } ^ { L + \nu - 1 }$

根据贝叶斯规则，$\operatorname* { P r } [ \psi _ { k } = u ; \psi _ { k + 1 } = q \mid \mathbf { y } ]$ 可以重新整理为
