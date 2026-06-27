# 第三章 软检测器

现代硬盘信号处理系统已开始采用迭代解码系统进行数据解码。迭代解码系统的核心组件是软检测器 (soft detector) 和软解码器 (soft decoder)，它们通过相互交换软信息 (soft information) 来提高每一轮迭代的系统性能。正如第二章所述，BCJR 算法 [18] 是一种最大后验 (MAP: maximum a posteriori) 算法，在估计马尔可夫过程 (Markov process) 的状态或输出数据时是最优的 (optimal)。因此，在迭代解码系统被发明之初 [3]，BCJR 算法被用于构建软检测器和软解码器。

尽管 BCJR 算法中的状态度量 (state metric) 计算具有递归 (recursive) 特性，便于数据解码，但由于其计算资源消耗较高（例如大量的加法和乘法运算）、涉及非线性函数（如指数函数）计算，且对系统中的噪声方差较为敏感 [23, 24]，因此在许多实际的信号处理芯片应用中并不受欢迎。为此，研究人员开发了在对数域 (logarithm domain) 运行的类 MAP 算法 (MAP-like algorithm)，这些算法不仅能解决数值计算问题，而且复杂度远低于 BCJR 算法。

本章将详细阐述这些类 MAP 算法的工作原理，包括 Max-Log-MAP [23, 24, 38, 39]、Log-MAP [23, 24] 以及 SOVA (soft-output Viterbi algorithm) [19, 42]。这些算法的性能与 BCJR 算法接近或相当，本章还将展示它们的性能对比及复杂度分析。
