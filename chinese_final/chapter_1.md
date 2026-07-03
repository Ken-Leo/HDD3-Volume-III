![](../images/chapter_1/101a561f5954e478fb5d49c33c99d1fea42c3920fe28dea0b50421fbe4550cc8.jpg)

## 概述

本章将介绍用于替代硬盘驱动器中磁记录系统的读通道（read channel）[1] 的数学模型，使读者了解作为后续章节学习基础的硬盘驱动器信号处理系统。此外，还解释了迭代解码技术（iterative decoding）[2-5] 在硬盘驱动器信号处理系统中的概念和基础知识，使读者理解迭代解码技术在新型硬盘驱动器 [6] 中已开始实际应用的优势，因为它能有效提升系统性能。

## 1.1 数字数据存储系统

硬盘驱动器中的数字数据存储系统（digital data storage system）可以用图1.1 [1, 5, 7] 中的框图来表示。消息比特（message bits）被发送到纠错编码器（ECC encoder），其中 RS 码（Reed Solomon）[2, 8] 是硬盘驱动器中常用的编码。随后，编码后的数据再次通过调制编码器（modulation encoder）进行编码，以调整数据特性使其适应硬盘驱动器信道。常用的调制编码是 RLL 码（run-length limited code）[5, 9]。来自调制编码器的输出数据被视为将被写入存储介质的"记录比特（recorded bit）"。之后，记录比特被发送到调制器（modulator），将比特数据转换为写入电流波形（write current waveform），然后输入写磁头以将数据写入存储介质。

![](../images/chapter_1/b9868fd3a61a1ea8b10e73293f5afe0f83e935b2d5849bb63cfe9c6229095a96.jpg)  
1.2  
图1.1 硬盘驱动器数字数据存储系统的框图 [9, 10]

对于读取过程，读磁头（read head）从存储介质读取数据。当读磁头移动到磁化状态变化的区域时，会产生电压波形信号，通常称为"读回信号（readback signal）"。然后，读回信号被送入读通道进行处理，读通道由各种组件组成，如低通滤波器（LPF）、采样器（sampler 或模数转换器）、均衡器（equalizer）和符号检测器（symbol detector）等。输出数据随后依次通过调制解码器（modulation decoder）和纠错解码器（ECC decoder）进行解码，以获得所需的消息比特估计值以供使用。

## 1.2 硬盘驱动器的信道模型

图1.1中的子系统A可以表示为如图1.2 [1, 10] 所示的数学模型。二进制输入数据序列 $a _ { k } \in \{ 0 , 1 \}$ 的比特周期为 T，经过理想微分器（ideal differentiator），其多项式形式为 $1 - D$，其中 D 是延迟 T 的延迟算子，得到转换序列（transition sequence） $b _ { k } \in \{ - 1 , 0 , 1 \}$，其中 $b _ { k } = \pm 1$ 表示正或负的转换（positive or negative transition），$b _ { k } = 0$ 表示无转换（no transition）。然后转换序列 $b _ { k }$ 被发送到冲激响应等于转换脉冲信号 g(t) 的信道，并受到噪声 n(t) 的干扰，得到读回信号 r(t)，其数学方程为

![](../images/chapter_1/22cf38fc96755f268ada1f9befec29f4bc2ef1e83aedafd2acfe98d6eeb02ebb.jpg)  
图1.2 硬盘驱动器的信道模型

$$
r \left( t \right) = \sum _ { k } b _ { k } g \left( t - k T \right) + n \left( t \right)\tag{1.1}
$$

然后在接收端，读回信号 $r ( t )$ 被送入低通滤波器（LPF）以滤除带外噪声，并在受定时恢复（timing recovery）[10] 系统控制的时刻进行采样。采样器的输出数据随后被送入均衡器和符号检测器，以找出最可能的输入数据序列 $\hat { a } _ { k }$（即 $a _ { k }$ 的估计值）

对于纵向记录（longitudinal recording）系统，转换脉冲信号通常称为 Lorentzian 脉冲，其方程如下 [11]

$$
g \big ( t \big ) = \frac { 1 } { 1 + \big ( 2 t / \mathrm { P W } _ { 5 0 } \big ) ^ { 2 } }\tag{1.2}
$$

其中 $\mathrm { P W } _ { 5 0 }$ 是脉冲信号 $g ( t )$ 的半高全宽宽度（半峰值宽度）。而对于垂直记录（perpendicular recording）系统的转换脉冲信号，其方程如下 [12]

$$
g \big ( t \big ) = \mathrm { e r f } \left( \frac { 2 t \sqrt { \mathrm { l n } 2 } } { \mathrm { P W } _ { 5 0 } } \right)\tag{1.3}
$$

其中 ln(.) 是自然对数（natural logarithm），$\mathrm { P W } _ { 5 0 }$ 是脉冲 $g ^ { \prime } ( t )$（即 $g ( t )$ 的导数）的半高全宽宽度，erf() 是误差函数（error function），其定义为

![](../images/chapter_1/f12f19d57353d4e14a24979bab6cb112a74b79676d1e012a5c2c2905b14a2637.jpg)

![](../images/chapter_1/db7b09ca3e31da008c8dd990aa82fb3c943b0120b9c368cd3dd62d736f83c45f.jpg)

![](../images/chapter_1/7b0d126c9a23eb9a0616ec6df95ed7b9e542e13e589c29541fae0c5ea73843e1.jpg)  
图1.3 转换脉冲信号（a）纵向记录（b）垂直记录 2

$$
\mathrm { e r f } \left( x \right) = \frac { 2 } { \sqrt { \pi } } \int _ { 0 } ^ { x } e ^ { - t ^ { 2 } } d t\tag{1.4}
$$

在硬盘驱动器的记录系统中，归一化记录密度（ND: normalized recording density）定义如下 [11]

$$
\mathrm { N D } = { \frac { \mathrm { P W } _ { 5 0 } } { T } }\tag{1.5}
$$

它表示记录数据的密度，其中 $T$ 是一个比特数据的周期，也称为比特单元（bit cell）。ND 值指示在 $\mathrm { P W } _ { 5 0 }$ 范围内可以存储多少比特。图1.3显示了在不同 ND 值下纵向和垂直记录的转换响应。可以看出两种记录的转换脉冲信号都覆盖了多个比特单元的时间范围，特别是当 ND 值增加时。换句话说，符号间干扰（ISI: intersymbol interference）在 ND 值增加时会变得更加严重，因为相邻转换脉冲信号重叠的可能性更高。

当读磁头连续两次到达磁化转换区域时，合成脉冲信号称为"双比特脉冲信号（dibit pulse）"或双比特响应（dibit response）[11]，其值等于（见图1.2）

$$
m ( t ) = g ( t ) - g ( t - T )\tag{1.6}
$$

![](../images/chapter_1/015766f8c3c730647a699382fa7e56054b5066d5cc460d43cb4d289eef81877b.jpg)

![](../images/chapter_1/7f6579e14bea5e9d0fee7129a59941689d4bef6d109ea813ffa4dbba065766d5.jpg)

![](../images/chapter_1/3166dd462f6694b673431e7d2081291dedaea9e58ea612b71dca58071b3e57a4.jpg)  
图1.4 双比特脉冲信号（a）纵向记录（b）垂直记录

如图1.4所示，该双比特响应被视为硬盘驱动器记录系统中"信道（channel）"的代表。

通常，磁记录系统中常用的符号检测器是维特比检测器（Viterbi detector）[10, 13]。由于维特比检测器的复杂度随信道存储器（channel memory）长度呈指数增长，因此必须使用均衡器来调整整个系统的联合响应，使其符合所需的"目标响应（target response）" H(D) [10, 11, 14]，从而降低维特比检测器的复杂度。在实际应用中，此目标通常称为"部分响应目标"或PR目标（partial response）。在纵向记录系统中被广泛接受的 PR 目标具有以下形式 [11]

$$
H ( D ) = ( 1 - D ) { ( 1 + D ) } ^ { n }\tag{1.7}
$$

在垂直记录系统中则有如下形式 [14, 15]

$$
H \left( D \right) = \left( 1 + D \right) ^ { n }\tag{1.8}
$$

其中 n 是正整数。

![](../images/chapter_1/a890c7af11a4cbeab45332d11f4dfaf606c6f0db22b2d6f46100e90d53ab8dcd.jpg)

![](../images/chapter_1/aff673ec985bb849abbca7483ff837c956d57273e3c04fca72e5bd7c94d6030d.jpg)

![](../images/chapter_1/81d91bb79074986f9b7a49339a048e6c71c086be375c9bba2b6305de2d4e8d68.jpg)

![](../images/chapter_1/a45bbe1ca5bc724659d741f9e46e6017660a15fd9c3b2c191f473e329c90e8be.jpg)  
(b) 归一化频率 (fT)  
图1.5 各种目标对于记录信道的频率响应 (a) 纵向 (b) 垂直

图1.5比较了各种目标的频率响应（frequency response），信道的频率响应即为双比特脉冲 [1] 在方程 (1.6) 中的傅里叶变换结果。方括号 [-] 中的数字表示目标每个抽头的系数。例如：

PR4 [1 0 –1] 表示 PR4 目标（PR class-IV），其 D 域传递函数 [1] 为 $H ( D ) = 1 - D ^ { 2 }$

EEPR2 [1 4 6 4 1] 表示 EEPR2 目标，其 D 域传递函数 H(D) $= 1 + 4 D + 6 D ^ { 2 } + 4 D ^ { 3 } + D ^ { 4 }$ 等。

从图1.5可以看出，当信道的 ND 值增加时，所使用的目标应具有更多抽头（n 值更大），以使目标的响应尽可能接近信道的响应，这将有助于维特比检测器更有效地工作（详见 [10] 第3章）。

此外，从方程 (1.7) 和 (1.8) 可以看出，所有 PR 目标的系数均为整数。然而，如果使用系数为实数的目标，称为"广义部分响应目标（GPR: generalized partial response target）"，则系统的整体性能将优于使用 PR 目标。感兴趣的读者可以在 [10, 14, 15] 中学习适用于硬盘驱动器信道的均衡器和目标设计技术。

![](../images/chapter_1/877833063d93e864a3eb26a5a92b62d515d738f6fd306999ae19143f30b70cd5.jpg)

![](../images/chapter_1/ba8a70aaccdedb1893288a3c36bc89756b15e0c4a6c891b664f73118e95eba42.jpg)  
图1.6 理想信道模型

## 1.3 理想信道模型

图1.2中的信道模型被认为是"真实信道模型（realistic channel model）"，因其工作特性接近包含硬盘驱动器读通道架构中重要组件的实际系统 [1]。本节将介绍"理想信道模型（ideal channel model）"，该模型常用于研究和分析硬盘驱动器信号处理系统的基本工作原理，因为它不复杂且易于理解。

因此，假设系统具有完美的均衡（perfect equalization）过程，则图1.2中的模型可以简化为图1.6中的理想信道模型。其中，比特周期为 T 的二进制输入数据序列 $a _ { k }$ 被送入信道 $H \left( D \right) = \sum _ { i } h _ { i } D ^ { i }$，$h _ { i }$ 是信道的第 i 个系数，并与理想奈奎斯特脉冲（ideal Nyquist pulse）q(t) = sin(πt/T)/(πt/T) [16] 进行调制，并受到噪声 w(t) 的干扰，得到读回信号

$$
r ( t ) { = } \sum _ { k } s _ { k } q { \big ( } t { - } k T { \big ) } { + } w { \big ( } t { \big ) }\tag{1.9}
$$

其中 $s _ { k } = a _ { k } * h _ { k }$ 是信道的输出数据，* 是卷积算子（convolution operator）。然后在接收端，读回信号 r(t) 被送入低通滤波器并在受定时恢复系统控制的时刻进行采样，之后将采样器的输出数据送到符号检测器以找出最可能的输入数据序列。

## 1.4 迭代解码

图1.2中的信道模型是"未编码系统（uncoded system）"的模型。然而，实际应用的接收端在许多应用中既使用均衡（equalization）来处理信道失真（distortion），也使用纠错编码（error correction coding）来处理信道产生的错误。通常，使用 ECC 编码的系统称为"编码系统（coded system）"。

实际的硬盘驱动器信号处理系统（见图1.1）也使用纠错编码（使用 RS 码，因为它可以纠正多个连续比特错误）。也就是说，消息比特被送入纠错编码器和调制编码器，得到图1.2中的输入数据序列 $a _ { k }$。然后在接收端，图1.2中检测到的输入数据序列 $\hat { a } _ { k }$ 被送到调制解码器和纠错解码器，以获得可用的消息比特估计值。这种硬盘驱动器信号处理系统的工作方式从过去一直沿用至今，被认为是"单向处理（one-way processing）"，即符号检测器独立于 ECC 解码器工作。

然而，研究 [2-5] 表明，"迭代解码（iterative decoding）"——即符号检测器和 ECC 解码器之间的协同工作——可以显著提高系统的整体性能。使用迭代信号处理系统的硬盘驱动器将具有如图1.7所示的结构，其中增加了迭代编码器（iterative encoder）和 SISO（soft-input soft-output）解码器。此外，子系统 A 中使用的符号检测器必须从维特比检测器更换为 SISO 检测器。迭代编码器是一种纠错编码器，常用的是 LDPC 码（low-density parity-check code）[17]，因为它是性能最强的 ECC 编码 [2, 5]（关于 LDPC 码的详细信息见第4章）。

目前，新型硬盘驱动器已经采用了迭代解码技术（如图1.7所示），其中 SISO 检测器和 SISO 解码器之间交换软信息（soft information）[2]。用于迭代解码的 SISO 检测器可以基于 BCJR 算法 [18] 或 SOVA（soft-output Viterbi algorithm）[19] 开发（详见第2-3章）。而用于解码 LDPC 编码数据的 SISO 解码器则基于消息传递算法（message passing algorithm）[17] 开发（详见第4.4.4节）。

![](../images/chapter_1/ad60e1c87a71563776e299e27d22b54b1ba34248b2070c82e52bf1c7ba7742ca.jpg)

![](../images/chapter_1/eacbc2196baf1facc1ff7d9d3dc0bc49050d1f2cc528412109a057dd95410057.jpg)  
图1.7 硬盘驱动器迭代信号处理系统的框图

迭代解码技术的工作过程从 SISO 检测器开始，它对接收到的数据进行检测，然后将结果（软信息）发送到 SISO 解码器。然后 SISO 解码器将解码后的结果发送回 SISO 检测器，用于新一轮的检测。此过程循环进行，直到达到设定的迭代次数，SISO 解码器才将输出数据送至调制解码器和 RS 解码器进行后续解码。

注意，从图1.7可以看出，系统中同时使用了 RS 码和 LDPC 码。然而，实际应用中发现 [20]，当使用 LDPC 码进行迭代解码时，可能不再需要使用 RS 码。因此，用户可以选择同时使用 RS 码和 LDPC 码，或仅使用 LDPC 码，两者都能提供相近的性能。

## 1.5 基础知识与相关术语

本节将解释与迭代解码相关的基础知识和重要术语，使读者在学习第2-4章内容之前理解这些术语的含义。

![](../images/chapter_1/efba52fc36e6e4678e0af321c59a879e1182f45b2f37dc033f77e41ed786e9a2.jpg)

## 1.5.1 硬判决与软判决

在数字通信系统的接收端，检测器和解码器可以选择使用硬判决（hard decision）和软判决（soft decision）两种方式。

硬判决是从检测器或解码器获取比特数据或符号的估计值。得到的结果称为"硬信息（hard information）"。例如，如果检测器接收到的数据值为0.9，则可以判定发送端发送的比特数据为1。

软判决是依据接收端拥有的所有数据，获取比特数据或符号的置信度（reliability）。得到的结果称为"软信息（soft information）"。例如，如果解码器输出的软信息值很大，则表明解码器得到的比特数据或符号的估计值具有很高的置信度或正确可能性。

对于二进制通信系统，比特数据的置信度由"对数似然比（LLR: log-likelihood ratio）"衡量。即，设 $x \in \{ 0 , 1 \}$ 为二进制随机变量，则 x 的 LLR 定义为

$$
\lambda { \bigl ( } x { \bigr ) } = \ln \left( { \frac { p { \bigl ( } x = 1 { \bigr ) } } { p { \bigl ( } x = 0 { \bigr ) } } } \right)\tag{1.10}
$$

其中 ln(.) 是自然对数（natural logarithm），$p ( x )$ 是 x 的概率密度函数（pdf: probability density function）。此外，$\lambda ( x )$ 的绝对值（absolute value）是比特数据 x 的软信息或置信度值，而 λ(x) 的符号则是比特数据 x 的硬信息或估计值，即

$$
\hat { x } = \left\{ { \begin{array} { l l } { 1 , } & { { \mathrm { i f } } \ \lambda ( x ) \geq 0 } \\ { 0 , } & { { \mathrm { i f } } \ \lambda ( x ) < 0 } \end{array} } \right.\tag{1.11}
$$

## 1.5.2 对数似然比

对数似然比（LLR）是迭代解码过程中各种算法（如 BCJR 算法、SOVA 和 LDPC 等）中广泛使用的度量或信息指标。本书使用符号 $\lambda ( x )$ 表示比特数据 $x \in \{ 0 , 1 \}$ 的 LLR 值

![](../images/chapter_1/833c8ee5c270e812a27aa636008fa32d14f12514d131cb5ff16eb19ba39356ae.jpg)

![](../images/chapter_1/031af0133c9a7441f11009d39759271c006e8ca5451c2707be7f9ad20ac473de.jpg)  
图1.8 比特数据 a 的 LLR 值与概率 $p ( a = + 1 )$ 的关系

即方程 (1.10) 所定义的比特1与比特0概率之比的自然对数。

对于使用双极性二进制输入数据的通信系统，即 $a \in \{ - 1 , 1 \}$，LLR 定义为

$$
\lambda { \big ( } a { \big ) } = \ln \left( { \frac { p { \big ( } a = + 1 { \big ) } } { p { \big ( } a = - 1 { \big ) } } } \right)\tag{1.12}
$$

这在解码算法中广泛使用，因为 λ(a) 的符号可以直接用作比特数据 a 的估计值（或硬信息）。类似地，λ(a) 的大小也用于指示比特数据 a 的置信度（或软信息）。图1.8显示了比特数据 a 的 LLR 值与概率 $p ( a = + 1 )$ 的关系。当 $p ( a = + 1 ) > 0.5$ 时 $\lambda ( a )$ 为正，即比特数据 a 更可能是比特1而非比特-1；当 $p ( a = + 1 ) < 0.5$ 时 λ(a) 为负，即比特数据 a 更可能是比特-1而非比特1。此外，如果 $p ( a = + 1 ) = 0.5$，则 $\lambda ( a ) = 0$，比特1和比特-1出现的概率相等。

由于 $p ( a = + 1 ) = 1 - p ( a = - 1 )$，方程 (1.12) 可重新整理为

![](../images/chapter_1/c612c1e64f66e045ea68154e28b85d4fd94e49890c160a6ecaa3210279b45c02.jpg)

![](../images/chapter_1/67dcc58c07221aa115080cae40a6681b53bda8f2f4edaf47ba4094d56d48c34b.jpg)

$$
e ^ { \lambda ( a ) } = \frac { p ( a = + 1 ) } { 1 - p ( a = + 1 ) }\tag{1.13}
$$

以及

$$
p \big ( a = + 1 \big ) = \frac { e ^ { \lambda ( a ) } } { 1 + e ^ { \lambda ( a ) } } = \frac { 1 } { 1 + e ^ { - \lambda ( a ) } } = \frac { e ^ { \lambda ( a ) / 2 } } { e ^ { \lambda ( a ) / 2 } + e ^ { - \lambda ( a ) / 2 } }\tag{1.14}
$$

$$
p \left( a = - 1 \right) = \frac { e ^ { - \lambda \left( a \right) } } { 1 + e ^ { - \lambda \left( a \right) } } = \frac { 1 } { 1 + e ^ { + \lambda \left( a \right) } } = \frac { e ^ { - \lambda \left( a \right) / 2 } } { e ^ { - \lambda \left( a \right) / 2 } + e ^ { \lambda \left( a \right) / 2 } }\tag{1.15}
$$

从方程 (1.14) 和 (1.15) 可以总结出，对于 $C \in \{ - 1 , + 1 \}$，有

$$
p \left( a = C \right) = \frac { e ^ { C \lambda \left( a \right) / 2 } } { e ^ { \lambda \left( a \right) / 2 } + e ^ { - \lambda \left( a \right) / 2 } }\tag{1.16}
$$

## 1.5.3 信道的软输出

考虑一个二进制通信系统。比特数据 $x \in \{ 0 , 1 \}$ 被发送到映射器（mapper），转换为比特数据 $u \in \{ - 1 , 1 \}$，然后通过无记忆信道传输，接收端接收到的信号为 $y = u + n$，其中 n 是均值为零、方差为 $\sigma ^ { 2 }$ 的加性高斯白噪声（AWGN: additive white Gaussian noise）。

定义条件概率密度函数（conditional probability density function） $p \big ( \boldsymbol { y } \mid \boldsymbol { x } \big )$ 为给定 x 时随机变量 y 的概率密度函数。反之，给定 y 时，作为 x 函数的 $p ( y \mid x )$ 称为"似然函数（likelihood function）" [4]。

在实际中，在接收端接收到数据 y 之前，x 的先验概率（a priori probability）为 $p ( x = 1 )$ 和 $p \big ( x = 0 \big )$。然而，在接收端接收到数据 y 之后，概率 $p ( x = 1 | y )$ 和 $p ( x = 0 | y )$ 变为后验概率（APP: a posteriori probability）。根据贝叶斯规则（Bayes' rule），有

$$
\begin{array} { c } { { p \big ( x = i \mid y \big ) = p \big ( x = i ; y \big ) / p \big ( y \big ) } } \\ { { { } } } \\ { { = p \big ( y \mid x = i \big ) p \big ( x = i \big ) / p \big ( y \big ) } } \end{array}\tag{1.17}
$$

![](../images/chapter_1/db0aeba28c74e54a71cdd51b60b75b5c61510c14003e3bd1b101f8dc1c0386d6.jpg)

其中 $i \in \{ 0 , 1 \}$，$p \big ( a ; b \big )$ 是随机变量 a 和 b 的联合概率密度函数（joint pdf）。因此，给定 y 时比特数据 x 的 LLR 定义为

$$
\lambda { \big ( } x \mid y { \big ) } = \ln \left( { \frac { p { \big ( } x = 1 \mid y { \big ) } } { p { \big ( } x = 0 \mid y { \big ) } } } \right)\tag{1.18}
$$

由贝叶斯规则可得

$$
\begin{array} { c } { \displaystyle \ln \left( \frac { p \big ( x = 1 | y \big ) } { p \big ( x = 0 | y \big ) } \right) = \ln \left( \frac { p \big ( y | x = 1 \big ) } { p \big ( y | x = 0 \big ) } \right) + \ln \left( \frac { p \big ( x = 1 \big ) } { p \big ( x = 0 \big ) } \right) } \\ { = L _ { c } y + \lambda \big ( x \big ) } \end{array}\tag{1.19}
$$

其中 $L _ { c }$ 是信道的软输出，被视为与从数据 y 获得的比特数据 x 相对应的软信息，而 $\lambda ( x )$ 称为"先验信息（a priori information）"，即接收端在接收到数据 y 之前关于比特数据 x 的信息。在接收端没有先验信息的情况下，设 $\lambda ( x ) = 0$。

通常，方程 (1.19) 中的 $L _ { c }$ 称为信道置信度（channel reliability），它取决于信道的特性。例如，在 $n _ { k }$ 为 AWGN 噪声的情况下，有

$$
\begin{array} { r l } & { \ln \left( \frac { p \left( y \mid x = 1 \right) } { p \left( y \mid x = 0 \right) } \right) \equiv \ln \left( \frac { p \left( y \mid u = + 1 \right) } { p \left( y \mid u = - 1 \right) } \right) } \\ & { \qquad = \ln \left( \frac { \exp \left( - \frac { 1 } { 2 \sigma ^ { 2 } } \left( y - 1 \right) ^ { 2 } \right) } { \exp \left( - \frac { 1 } { 2 \sigma ^ { 2 } } \left( y + 1 \right) ^ { 2 } \right) } \right) = \frac { 2 } { \sigma ^ { 2 } } y } \end{array}\tag{1.20}
$$

即 $L _ { c } = 2 / \sigma ^ { 2 }$。

## 1.5.4 SISO 解码器

SISO（soft-input soft-output）解码器是一种使用软信息进行数据解码的解码器，它接收软信息作为输入进行处理，并输出软信息作为结果。

![](../images/chapter_1/1925f72ac05757d6cc72319d9907218067280586a46824cc6b8ce5244dba00fa.jpg)

![](../images/chapter_1/023e56b726c3cf083dcfacd03c4d5c57baa2cfd892369f2c3f185d44db0d008d.jpg)  
图1.9 使用 SISO 解码器的数字通信系统

考虑图1.9中的通信系统。数据序列 $x _ { k } \in \{ 0 , 1 \}$ 被发送到编码器（encoder）和映射器（mapper），得到数据序列 $u _ { k } \in \{ - 1 , 1 \}$。然后 SISO 解码器对信号 $y _ { k } = u _ { k } + n _ { k }$（其中 $n _ { k }$ 是 AWGN 噪声）进行数据解码，并借助数据序列 ${ \lambda } _ { a } \left( x _ { k } \right)$，其中 ${ \lambda } _ { a } \left( x _ { k } \right)$ 是比特数据 $x _ { k }$ 的先验 LLR（a priori LLR），即

$$
\lambda _ { a } \left( x _ { k } \right) = \ln \left( \frac { p \left( x _ { k } = 1 \right) } { p \left( x _ { k } = 0 \right) } \right)\tag{1.21}
$$

这表示在接收端接收数据序列 y 或所有数据 $y _ { k }$ 之前关于比特数据 $x _ { k }$ 的信息（即独立于 y）。类似地，如果接收端没有先验信息，则对于所有 k 设 $\lambda _ { a } \left( x _ { k } \right) = 0$，这意味着每个比特数据 $x _ { k }$ 具有相同的出现概率。

然后 SISO 解码器输出比特数据 $x _ { k }$ 的后验 LLR（a posteriori LLR），即

$$
\lambda _ { p } \left( x _ { k } \right) = \ln \left( { \frac { p \left( x _ { k } = 1 \mid \mathbf { y } \right) } { p \left( x _ { k } = 0 \mid \mathbf { y } \right) } } \right)\tag{1.22}
$$

其中比特数据 $x _ { k }$ 的估计值可以通过将 $\lambda _ { p } \left( x _ { k } \right)$ 送入阈值检测器（threshold detector）得到，关系如下

$$
\hat { x } _ { k } = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f } ~ \lambda _ { p } \left( x _ { k } \right) \ge 0 } \\ { 0 , } & { \mathrm { i f } ~ \lambda _ { p } \left( x _ { k } \right) < 0 } \end{array} \right.\tag{1.23}
$$

注意，对于比特数据 x 的 LLR，即 $\lambda ( x )$，本书定义如下

![](../images/chapter_1/111481879c1a013aecc999d96d8451869f81007c80693026dabdb451b584a049.jpg)

如果 LLR 的下标为参数 a，例如 ${ \lambda } _ { a } \left( x \right)$，表示比特数据 x 的先验 LLR（a priori LLR）。

如果 LLR 的下标为参数 $p$，例如 $\lambda _ { p } \left( x \right)$，表示比特数据 x 的后验 LLR（a posteriori LLR）。

## 1.6 本章小结

本章介绍了用于替代磁记录系统的读信道模型（包括图1.2中的真实信道模型和图1.6中的理想信道模型），以使读者能够将这些模型用于分析硬盘驱动器的信号处理系统。

由于市场上销售的新型硬盘驱动器采用了迭代解码技术，因为它能有效提升系统性能，因此本章解释了迭代解码技术的概念和基础，包括 SISO、先验概率、后验概率、软信息和对数似然比（LLR）等的含义，为读者后续学习第2-4章中 SISO 检测器和 SISO 解码器的工作原理做好准备。

## 1.7 本章习题

1. 请解释图1.1中硬盘驱动器数字数据存储系统的工作原理。

2. 请使用 SCILAB 程序绘制以下图形（http://home.npru.ac.th/piya/webscilab 或 http://www.scilab.org）

2.1) 不同 ND 值下的转换脉冲信号，如图1.3所示

2.2) 不同 ND 值下的双比特响应，如图1.4所示

3. 请证明纵向记录系统中双比特响应 m(t) 在方程 (1.6) 中的傅里叶变换结果为

$$
M \left( \Omega \right) = \exp \left\{ - \pi \left| \Omega \right| \mathrm { N D } \right\} \left( 1 - \exp \left\{ - j 2 \pi \Omega \right\} \right)
$$

垂直记录系统的结果为

![](../images/chapter_1/11bc6da7d0196e469147cda14ee298d1e88f57cddd23a3d29a55c350b19f7e40.jpg)
