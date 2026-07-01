# 第一章

# 引言

本章将介绍用于表示硬盘驱动器中磁记录系统的读信道 (read channel) [1] 的数学模型，使读者了解硬盘驱动器的信号处理系统，为后续章节的学习奠定基础。此外，还将解释在硬盘驱动器信号处理系统中使用迭代解码技术 (iterative decoding) [2–5] 的概念和基本原理，使读者理解迭代解码技术的优势——该技术已开始应用于新型硬盘驱动器 [6] 中，因为它能显著提升系统性能。

# 1.1 数字数据存储系统

硬盘驱动器中的数字数据存储系统 (digital data storage system) 可用图 1.1 [1, 5, 7] 所示的框图进行建模。信息位 (message bits) 被送入纠错编码器 (ECC encoder)。RS (Reed-Solomon) 码 [2, 8] 是硬盘驱动器中常用的码。然后，编码后的数据再次通过调制编码器 (modulation encoder) 进行编码，以调整数据特性使其适合硬盘驱动器的信道。常用的调制码是 RLL (run-length limited) 码 [5, 9]。调制编码器的输出数据就是要写入存储介质的数据，称为"记录位 (recorded bit)"。之后，记录位被送入调制器 (modulator)，将数据位转换为写电流波形 (write current waveform)，再送入写磁头将数据写入存储介质。

![](images/6ff6eb1c06313349be9ec4dd25eca5a258ef10a4b9d162087410b95056bbaa05.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["message bits"] --> B["ECC encoder"]
    B --> C["modulation encoder"]
    C --> D["recorded bits"]
    D --> E["modulator"]
    E --> F["write current waveform"]
    F --> G["write head/medium/read head assembly"]
    G --> H["read channel"]
    H --> I["readback voltage waveform"]
    I --> J["reproduced bits"]
    J --> K["modulation decoder"]
    K --> L["ECC decoder"]
    L --> M["estimated message bits"]
    M --> N["read back voltage waveform"]
    N --> H
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#ccf,stroke:#333
    style D fill:#ccf,stroke:#333
    style E fill:#cfc,stroke:#333
    style F fill:#cfc,stroke:#333
    style G fill:#cfc,stroke:#333
    style H fill:#cfc,stroke:#333
    style I fill:#cfc,stroke:#333
    style J fill:#cfc,stroke:#333
    style K fill:#cfc,stroke:#333
    style L fill:#cfc,stroke:#333
    style M fill:#cfc,stroke:#333
    style N fill:#cfc,stroke:#333
```
</details>

1.2
图 1.1 硬盘驱动器数字数据存储系统框图 [9, 10]

在读取过程中，读磁头 (read head) 从存储介质读取数据。当读磁头移动到磁化状态发生变化的区域时，会产生电压波形信号，通常称为"回读信号 (readback signal)"。然后，回读信号被送入读信道进行处理，读信道由以下组件组成：低通滤波器 (LPF: low-pass filter)、采样器 (sampler 或模数转换器)、均衡器 (equalizer) 和符号检测器 (symbol detector) 等。输出的数据随后依次通过调制解码器 (modulation decoder) 和纠错解码器 (ECC decoder) 进行解码，以得到所需信息位的估计值。

# 1.2 硬盘驱动器的信道模型

图 1.1 中的子系统 A (System A) 可以用图 1.2 [1, 10] 所示的数学模型来表示。当二进制输入数据序列 $a_k \in \{0, 1\}$（比特周期为 $T$ 单位时间）通过一个理想微分器 (ideal differentiator)（其多项式形式为 $1 - D$，其中 $D$ 是 $T$ 单位时间的延迟算子）时，得到转换序列 (transition sequence) $b_k \in \{-1, 0, 1\}$，其中 $b_k = \pm 1$ 表示正或负的转换 (positive or negative transition)，$b_k = 0$ 表示无转换 (no transition)。然后，转换序列 $b_k$ 被送入冲激响应等于转换脉冲信号 $g(t)$ 的信道，并受到噪声 $n(t)$ 的干扰，得到回读信号 $r(t)$，其数学表达式为

![](images/3b4f33f3d2c25138aa9b95fe1ed3aa16b658ee40c77255dce6dbd686ca8a0cfa.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["a_k"] --> B["1 - D"]
    B --> C["b_k"]
    C --> D["g(t)"]
    D --> E["+"]
    E --> F["r(t)"]
    F --> G["LPF"]
    G --> H["×"]
    H --> I["equalizer"]
    I --> J["symbol detector"]
    J --> K["â_k"]
    L["Timing Recovery"] --> H
    M["Target H(D)"] --> L
    N["n(t)"] --> E
```
</details>

图 1.2 硬盘驱动器的信道模型

$$
r(t) = \sum_{k} b_k \, g(t - kT) + n(t) \tag{1.1}
$$

然后，在接收端，回读信号 $r(t)$ 通过低通滤波器 (LPF) 以滤除带外噪声，并在由定时恢复电路 (timing recovery) [10] 控制的时间点进行采样。采样器的输出数据被送入均衡器和符号检测器，以寻找最可能的输入数据序列 $\hat{a}_k$（即 $a_k$ 的估计值）。

对于水平记录系统 (longitudinal recording)，转换脉冲信号（通常称为洛伦兹脉冲 (Lorentzian pulse)）的方程为 [11]

$$
g(t) = \frac{1}{1 + \left(2t / \mathrm{PW}_{50}\right)^2} \tag{1.2}
$$

其中 $\mathrm{PW}_{50}$ 是脉冲信号 $g(t)$ 在半峰高度处测得的脉冲宽度。而对于垂直记录系统 (perpendicular recording)，转换脉冲信号的方程为 [12]

$$
g(t) = \operatorname{erf}\left(\frac{2t \sqrt{\ln 2}}{\mathrm{PW}_{50}}\right) \tag{1.3}
$$

其中 $\ln(\cdot)$ 是自然对数 (natural logarithm)，$\mathrm{PW}_{50}$ 是脉冲信号 $g'(t)$（即 $g(t)$ 的导数）在半峰高度处测得的脉冲宽度，而 $\operatorname{erf}(\cdot)$ 是误差函数 (error function)，定义为

![](images/683edd52e8661292324fb9414edd3b6ab7a2013b4dcabc90e6e841cd4553a57f.jpg)

<details>
<summary>line</summary>

| t/T | ND = 2 | ND = 2.5 | ND = 3 |
|-----|--------|----------|--------|
| -5.0 | 0.05 | 0.06 | 0.07 |
