![](images/chapter_1/101a561f5954e478fb5d49c33c99d1fea42c3920fe28dea0b50421fbe4550cc8.jpg)

## 概述

本章将介绍用于替代硬盘驱动器中磁记录系统的读通道（read channel）[1] 的数学模型，使读者了解作为后续章节学习基础的硬盘驱动器信号处理系统。此外，还解释了迭代解码技术（iterative decoding）[2-5] 在硬盘驱动器信号处理系统中的概念和基础知识，使读者理解迭代解码技术在新型硬盘驱动器 [6] 中已开始实际应用的优势，因为它能有效提升系统性能。

## 1.1 数字数据存储系统

硬盘驱动器中的数字数据存储系统（digital data storage system）可以用图1.1 [1, 5, 7] 中的框图来表示。消息比特（message bits）被发送到纠错编码器（ECC encoder），其中 RS 码（Reed Solomon）[2, 8] 是硬盘驱动器中常用的编码。随后，编码后的数据再次通过调制编码器（modulation encoder）进行编码，以调整数据特性使其适应硬盘驱动器信道。常用的调制编码是 RLL 码（run-length limited code）[5, 9]。来自调制编码器的输出数据被视为将被写入存储介质的"记录比特（recorded bit）"。之后，记录比特被发送到调制器（modulator），将比特数据转换为写入电流波形（write current waveform），然后输入写磁头以将数据写入存储介质。

![](images/chapter_1/b9868fd3a61a1ea8b10e73293f5afe0f83e935b2d5849bb63cfe9c6229095a96.jpg)  
1.2  
图1.1 硬盘驱动器数字数据存储系统的框图 [9, 10]

对于读取过程，读磁头（read head）从存储介质读取数据。当读磁头移动到磁化状态变化的区域时，会产生电压波形信号，通常称为"读回信号（readback signal）"。然后，读回信号被送入读通道进行处理，读通道由各种组件组成，如低通滤波器（LPF）、采样器（sampler 或模数转换器）、均衡器（equalizer）和符号检测器（symbol detector）等。输出数据随后依次通过调制解码器（modulation decoder）和纠错解码器（ECC decoder）进行解码，以获得所需的消息比特估计值以供使用。
