![](images/chapter_1/101a561f5954e478fb5d49c33c99d1fea42c3920fe28dea0b50421fbe4550cc8.jpg)

## 概述

本章将介绍用于替代硬盘驱动器中磁记录系统的读通道（read channel）[1] 的数学模型，使读者了解作为后续章节学习基础的硬盘驱动器信号处理系统。此外，还解释了迭代解码技术（iterative decoding）[2-5] 在硬盘驱动器信号处理系统中的概念和基础知识，使读者理解迭代解码技术在新型硬盘驱动器 [6] 中已开始实际应用的优势，因为它能有效提升系统性能。

## 1.1 数字数据存储系统

硬盘驱动器中的数字数据存储系统（digital data storage system）可以用图1.1 [1, 5, 7] 中的框图来表示。消息比特（message bits）被发送到纠错编码器（ECC encoder），其中 RS 码（Reed Solomon）[2, 8] 是硬盘驱动器中常用的编码。随后，编码后的数据再次通过调制编码器（modulation encoder）进行编码，以调整数据特性使其适应硬盘驱动器信道。常用的调制编码是 RLL 码（run-length limited code）[5, 9]。来自调制编码器的输出数据被视为将被写入存储介质的"记录比特（recorded bit）"。之后，记录比特被发送到调制器（modulator），将比特数据转换为写入电流波形（write current waveform），然后输入写磁头以将数据写入存储介质。

![](images/chapter_1/b9868fd3a61a1ea8b10e73293f5afe0f83e935b2d5849bb63cfe9c6229095a96.jpg)  
1.2  
图1.1 硬盘驱动器数字数据存储系统的框图 [9, 10]

对于读取过程，读磁头（read head）从存储介质读取数据。当读磁头移动到磁化状态变化的区域时，会产生电压波形信号，通常称为"读回信号（readback signal）"。然后，读回信号被送入读通道进行处理，读通道由各种组件组成，如低通滤波器（LPF）、采样器（sampler 或模数转换器）、均衡器（equalizer）和符号检测器（symbol detector）等。输出数据随后依次通过调制解码器（modulation decoder）和纠错解码器（ECC decoder）进行解码，以获得所需的消息比特估计值以供使用。

## 1.2 硬盘驱动器的信道模型

图1.1中的子系统A可以表示为如图1.2 [1, 10] 所示的数学模型。二进制输入数据序列 $a _ { k } \in \{ 0 , 1 \}$ 的比特周期为 T，经过理想微分器（ideal differentiator），其多项式形式为 $1 - D$，其中 D 是延迟 T 的延迟算子，得到转换序列（transition sequence） $b _ { k } \in \{ - 1 , 0 , 1 \}$，其中 $b _ { k } = \pm 1$ 表示正或负的转换（positive or negative transition），$b _ { k } = 0$ 表示无转换（no transition）。然后转换序列 $b _ { k }$ 被发送到冲激响应等于转换脉冲信号 g(t) 的信道，并受到噪声 n(t) 的干扰，得到读回信号 r(t)，其数学方程为

![](images/chapter_1/22cf38fc96755f268ada1f9befec29f4bc2ef1e83aedafd2acfe98d6eeb02ebb.jpg)  
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

![](images/chapter_1/f12f19d57353d4e14a24979bab6cb112a74b79676d1e012a5c2c2905b14a2637.jpg)

![](images/chapter_1/db7b09ca3e31da008c8dd990aa82fb3c943b0120b9c368cd3dd62d736f83c45f.jpg)

![](images/chapter_1/7b0d126c9a23eb9a0616ec6df95ed7b9e542e13e589c29541fae0c5ea73843e1.jpg)  
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

![](images/chapter_1/015766f8c3c730647a699382fa7e56054b5066d5cc460d43cb4d289eef81877b.jpg)

![](images/chapter_1/7f6579e14bea5e9d0fee7129a59941689d4bef6d109ea813ffa4dbba065766d5.jpg)

![](images/chapter_1/3166dd462f6694b673431e7d2081291dedaea9e58ea612b71dca58071b3e57a4.jpg)  
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

![](images/chapter_1/a890c7af11a4cbeab45332d11f4dfaf606c6f0db22b2d6f46100e90d53ab8dcd.jpg)

![](images/chapter_1/aff673ec985bb849abbca7483ff837c956d57273e3c04fca72e5bd7c94d6030d.jpg)

![](images/chapter_1/81d91bb79074986f9b7a49339a048e6c71c086be375c9bba2b6305de2d4e8d68.jpg)
