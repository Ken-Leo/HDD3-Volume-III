# HDD3-Volume III - Advanced Receiver Design

---

## 中文版

本书是 **"HDD3-Volume III - Advanced Receiver Design"**（泰语原版）的中文翻译版。原书由泰国先皇技术学院拉卡邦校区（KMITL）的 Piya Kovintavewat 教授等人编写，是硬盘驱动器中迭代接收机设计的进阶教材。

### 版权声明

I have tried to get in touch with Prof. Piya but I failed. Considering the copyright, I would appreciate it if those who may concern contact me.

### 目录结构

| 目录 | 说明 |
|------|------|
| `source_final/` | 泰语原文 Markdown 章节 |
| `chinese_final/` | 中文翻译章节 |
| `images/` | 全书图片资源（按章节分目录） |

### 翻译状态

| 章节 | 内容概要 | 源文件 | 中文翻译 | 图片 | 状态 |
|------|---------|--------|----------|------|------|
| **Ch1** 概述与迭代解码基础 | 数字存储系统、信道模型、迭代解码基础、LLR、SISO解码器 | [source](source_final/chapter_1.md) | [中文](chinese_final/chapter_1.md) | 51 | ✓ |
| **Ch2** Turbo均衡 | 卷积码、BCJR算法、前向/后向递归、Turbo码编解码 | [source](source_final/chapter_2.md) | [中文](chinese_final/chapter_2.md) | 186 | ✓ |
| **Ch3** 软输出算法 | Max-Log-MAP、Log-MAP、SOVA、Bi-Directional SOVA 算法 | [source](source_final/chapter_3.md) | [中文](chinese_final/chapter_3.md) | 316 | ✓ |
| **Ch4** LDPC码 | 线性分组码、校验矩阵、规则/非规则LDPC、消息传递算法 | [source](source_final/chapter_4.md) | [中文](chinese_final/chapter_4.md) | 479 | ✓ |
| **Ch5** 迭代解码应用 | 迭代定时恢复、PSP-BCJR、热粗糙度降低 | [source](source_final/chapter_5.md) | [中文](chinese_final/chapter_5.md) | 562 | ✓ |
| **Ch6** BPMR技术 | 图形介质记录、二维脉冲响应、岛/读头效应、轨道偏移 | [source](source_final/chapter_6.md) | [中文](chinese_final/chapter_6.md) | 672 | ✓ |
| **Ch7** BPMR系统设计 | 一维/二维目标响应与均衡器、维特比检测器、迭代BPMR系统 | [source](source_final/chapter_7.md) | [中文](chinese_final/chapter_7.md) | 786 | ✓ |
| **Ch8** HAMR技术 | 热辅助磁记录、Williams-Comstock模型、水平/垂直HAMR、微磁道模型 | [source](source_final/chapter_8.md) | [中文](chinese_final/chapter_8.md) | 54 | ✓ |
| **附录A** 雅可比对数函数 | Jacobian对数函数的推导与近似 | [source](source_final/appendix_a.md) | [中文](chinese_final/appendix_a.md) | — | ✓ |
| **附录B** 双曲正切规则 | 双曲正切恒等式与LDPC解码中的应用 | [source](source_final/appendix_b.md) | [中文](chinese_final/appendix_b.md) | — | ✓ |
| **附录C** 方程等价性证明 | 关键方程等价性证明 | [source](source_final/appendix_c.md) | [中文](chinese_final/appendix_c.md) | — | ✓ |
| **附录D** PR2信道软估计 | PR2信道下软估计的推导 | [source](source_final/appendix_d.md) | [中文](chinese_final/appendix_d.md) | — | ✓ |
| **参考文献** | 文献 [1]-[144]（英文） | [source](source_final/References.md) | [原文](chinese_final/References.md) | — | ✓ |
| **索引** | 术语索引 | [source](source_final/index.md) | — | — | ✗ |

### 统计

| 指标 | 数值 |
|------|------|
| PDF 总页数 | 335 页（P14-P348） |
| 源文件 | 14 个 .md 文件 |
| 中文翻译 | 13 个 .md 文件（索引未译） |
| 图片引用 | 451 张 |
| 翻译状态 | 13/14 章节完成（92.9%） |

### 翻译说明

- 翻译由 AI 辅助完成，经人工核对
- 数学公式保持原样，引用路径已适配中文版
- 图片路径基于项目根目录的 `images/` 文件夹

---

## English Version

This is the Chinese translation of **"HDD3-Volume III - Advanced Receiver Design"** (original Thai version). The original textbook was authored by Prof. Piya Kovintavewat and colleagues at King Mongkut's Institute of Technology Ladkrabang (KMITL), Thailand. It covers advanced iterative receiver design for hard disk drive systems.

### Copyright Notice

I have tried to get in touch with Prof. Piya but I failed. Considering the copyright, I would appreciate it if those who may concern contact me.

### Repository Structure

| Directory | Description |
|-----------|-------------|
| `source_final/` | Original Thai Markdown chapters |
| `chinese_final/` | Chinese translations |
| `images/` | All book images (organized by chapter) |

### Translation Status

| Chapter | Content | Source | Chinese | Images | Status |
|---------|---------|--------|---------|--------|--------|
| **Ch1** Introduction & Iterative Decoding | Digital storage, channel models, LLR, SISO decoder | [source](source_final/chapter_1.md) | [chinese](chinese_final/chapter_1.md) | 51 | ✓ |
| **Ch2** Turbo Equalization | Convolutional codes, BCJR algorithm, forward/backward recursion, turbo codes | [source](source_final/chapter_2.md) | [chinese](chinese_final/chapter_2.md) | 186 | ✓ |
| **Ch3** Soft-Output Algorithms | Max-Log-MAP, Log-MAP, SOVA, Bi-Directional SOVA | [source](source_final/chapter_3.md) | [chinese](chinese_final/chapter_3.md) | 316 | ✓ |
| **Ch4** LDPC Codes | Linear block codes, parity-check matrix, regular/irregular LDPC, message passing | [source](source_final/chapter_4.md) | [chinese](chinese_final/chapter_4.md) | 479 | ✓ |
| **Ch5** Iterative Decoding Applications | Iterative timing recovery, PSP-BCJR, thermal roughness mitigation | [source](source_final/chapter_5.md) | [chinese](chinese_final/chapter_5.md) | 562 | ✓ |
| **Ch6** BPMR Technology | Patterned media recording, 2D pulse response, island/head effects, track misregistration | [source](source_final/chapter_6.md) | [chinese](chinese_final/chapter_6.md) | 672 | ✓ |
| **Ch7** BPMR System Design | 1D/2D targets & equalizers, Viterbi detectors, iterative BPMR system | [source](source_final/chapter_7.md) | [chinese](chinese_final/chapter_7.md) | 786 | ✓ |
| **Ch8** HAMR Technology | Heat-assisted magnetic recording, Williams-Comstock model, perpendicular HAMR, microtrack model | [source](source_final/chapter_8.md) | [chinese](chinese_final/chapter_8.md) | 54 | ✓ |
| **Appendix A** Jacobian Logarithm | Derivation and approximation of the Jacobian logarithmic function | [source](source_final/appendix_a.md) | [chinese](chinese_final/appendix_a.md) | — | ✓ |
| **Appendix B** Hyperbolic Tangent Rule | Hyperbolic tangent identities for LDPC decoding | [source](source_final/appendix_b.md) | [chinese](chinese_final/appendix_b.md) | — | ✓ |
| **Appendix C** Equation Equivalence Proof | Proofs of key equation equivalences | [source](source_final/appendix_c.md) | [chinese](chinese_final/appendix_c.md) | — | ✓ |
| **Appendix D** PR2 Channel Soft Estimate | Soft estimate derivation for PR2 channel | [source](source_final/appendix_d.md) | [chinese](chinese_final/appendix_d.md) | — | ✓ |
| **References** | References [1]-[144] (English) | [source](source_final/References.md) | [original](chinese_final/References.md) | — | ✓ |
| **Index** | Term index | [source](source_final/index.md) | — | — | ✗ |

### Key Statistics

| Metric | Value |
|--------|-------|
| Total PDF pages | 335 (P14-P348) |
| Source files | 14 .md files |
| Chinese translations | 13 .md files (index pending) |
| Image references | 451 |
| Translation coverage | 13/14 chapters complete (92.9%) |

### Translation Notes

- AI-assisted translation with manual review
- Mathematical equations preserved as-is; image paths adapted for Chinese edition
- Images reside in the `images/` directory at project root
