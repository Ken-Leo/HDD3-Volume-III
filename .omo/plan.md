# 翻译执行计划：HDD3-Volume III

**源文件**：`HDD3-Volume Ill - Advanced Receiver Design.pdf`（348页，唯一源文件）  
**提取环境**：`mineru`（已在系统可用）  
**目标**：逐字直译泰语技术书籍为中文，保留所有公式、图片和格式

---

## 第一章：历史失败教训（必须熟记）

| 过去的错误 | 造成的后果 | 本次必须遵守的规则 |
|---|---|---|
| 一次翻译过多内容 → 变成概括性重写 | 中文内容大量丢失，翻译率仅5-33% | **每次只翻译1-2段**，逐字直译，不增不减 |
| 自己画 mermaid 图替代原图 | 读者看不到书籍原图 | **必须从PDF提取原图**，中文文件保留原图引用 |
| 在 `/tmp` 创建临时提取文件 | 数据丢失，系统杂乱 | **所有文件只在本项目目录下创建** |
| 用 `write` 覆盖已有中文文件 | 数据永久丢失 | **只能用 append 方式追加**，永不覆盖 |
| 源文件还未提取完整就开始翻译 | 翻译基于残缺源文件 | **先保证源文件和图片完整，再开始翻译** |
| 提取结果与PDF页范围不匹配（页码偏移） | 章节内容缺失或重复 | **建立物理页码→逻辑页码映射表** |

---

## 第二章：PDF物理页码与逻辑页码映射

### 2.1 偏移量计算

```
PDF物理第1页 = 封面页（非书籍内容）
PDF物理第2-7页 = 版权页、前言、序言
PDF物理第8-13页 = 目录（Table of Contents）
PDF物理第14页 = 第1章开始 → 书籍逻辑第1页

偏移量 offset = 物理页 - 逻辑页 = 14 - 1 = 13
```

### 2.2 章节页范围对照表

| 章节 | 逻辑页码范围 | 物理页码范围 | 物理页数 |
|:----:|:-----------:|:-----------:|:--------:|
| Ch1 概述 | 1-15 | P14-P28 | 15页 |
| Ch2 Turbo均衡 | 17-63 | P30-P76 | 47页 |
| Ch3 软输出算法 | 65-105 | P78-P118 | 41页 |
| Ch4 LDPC码 | 107-154 | P120-P167 | 48页 |
| Ch5 迭代解码应用 | 155-194 | P168-P207 | 40页 |
| Ch6 BPMR技术 | 195-228 | P208-P241 | 34页 |
| Ch7 BPMR系统设计 | 229-262 | P242-P275 | 34页 |
| Ch8 HAMR | 263-305 | P276-P318 | 43页 |
| 附录A（公式） | 307-308 | P320-P321 | 2页 |
| 附录B（格林函数） | 309 | P322 | 1页 |
| 附录C（公式证明） | 311 | P324 | 1页 |
| 附录D（PR2推导） | 313 | P326 | 1页 |
| 参考文献 | 317-325 | P330-P338 | 9页 |
| 索引 | 327-348 | P340-348 | 9页 |

### 2.3 翻译范围

**只翻译正文部分（Ch1-Ch8 + 附录A/B/C/D）**，参考文献和索引不翻译。

| 章节 | 物理页范围 | MinerU提取命令 |
|:----:|:---------:|:--------------:|
| Ch1 | P14-P28 | `--page_ranges "14-28"` |
| Ch2 | P30-P76 | `--page_ranges "30-76"` |
| Ch3 | P78-P118 | `--page_ranges "78-118"` |
| Ch4 | P120-P167 | `--page_ranges "120-167"` |
| Ch5 | P168-P207 | `--page_ranges "168-207"` |
| Ch6 | P208-P241 | `--page_ranges "208-241"` |
| Ch7 | P242-P275 | `--page_ranges "242-275"` |
| Ch8 | P276-P318 | `--page_ranges "276-318"` |
| 附录A | P320-P321 | `--page_ranges "320-321"` |
| 附录B | P322 | `--page_ranges "322"` |
| 附录C | P324 | `--page_ranges "324"` |
| 附录D | P326 | `--page_ranges "326"` |

---

## 第三章：Phase 0 — 初始化项目结构

### 3.1 创建目录

```bash
# 所有目录都在项目根目录下（绝对禁止在 /tmp 操作）
mkdir -p source_final/        # 泰语提取Markdown
mkdir -p chinese_final/       # 中文翻译Markdown
mkdir -p images/              # 图片（按 chapter_n 子目录）
```

### 3.2 初始化进度文件

创建 `.omo/progress.md`：
```markdown
# Translation Progress
Overall Status: PDF HDD3-Volume III → Chinese translation
Goal: Full book translation (Ch1-8 + Appendix)

## Chapter Status
- [ ] Ch1: Pending
- [ ] Ch2: Pending
...（共12个条目）

Current: Phase 0 — 结构初始化
```

---

## 第四章：Phase 1 — 逐章PDF提取（MinerU）

### 4.1 执行顺序

从 Ch1 开始，按顺序执行，每完成一章验证后再提取下一章。

### 4.2 每章提取步骤

**Step A: 运行 MinerU 提取**

```bash
mineru extract \
  --pdf "HDD3-Volume Ill - Advanced Receiver Design.pdf" \
  --page_ranges "P14-P28" \
  --output_dir source_final/
```

MinerU 输出会包含：
- `source_final/chapter_n.md` — 泰语Markdown
- `source_final/images/` — 提取的图片（原始路径）

**Step B: 重命名提取文件**

检查 MinerU 输出的文件名，重命名为标准格式：
```bash
# 例如 mineru 输出可能是 chapter_1.md，确认后使用
mv source_final/<mineru_output>.md source_final/chapter_1.md
```

**Step C: 规范化图片路径**

```bash
python .opencode/skills/technical-book-translation/scripts/fix_paths.py source_final/
```

此脚本自动将所有图片路径改为 `![](images/chapter_n/filename.ext)` 格式。

**Step D: 验证提取完整性**

手动检查以下项目：
1. ✅ 文件存在：`source_final/chapter_n.md` 有内容
2. ✅ 图片目录：`images/chapter_n/` 已创建，有 `.jpg`/`.png` 文件
3. ✅ 图片引用：在 `source_final/chapter_n.md` 中搜索 `![](` 确认引用的图片都存在于 `images/chapter_n/` 中

**验证脚本：**
```bash
python3 -c "
import os, re
f = open('source_final/chapter_1.md').read()
imgs = re.findall(r'!\\[\\]\\(([^)]+)\\)', f)
missing = [i for i in imgs if not os.path.exists(i)]
print(f'图片引用: {len(imgs)} 张')
print(f'缺失: {len(missing)} 张')
if missing:
    for m in missing: print(f'  MISSING: {m}')
else:
    print('所有图片路径有效 ✓')
"
```

**Step E: 提交**

```bash
git add source_final/ images/
git commit -m "提取 Ch1 - 泰语原文 + 图片"
```

### 4.3 图片缺失时的处理

如果 MinerU 提取后某些图片丢失（常见于 PDF 中嵌入的公式截图）：

**方案1** — 从 PDF 手动截取：
```bash
# 使用 Python + PyMuPDF (fitz) 提取特定页面的图片
python3 -c "
import fitz
doc = fitz.open('HDD3-Volume Ill - Advanced Receiver Design.pdf')
page = doc[14]  # Ch1 第一页
images = page.get_images()
for i, img in enumerate(images):
    xref = img[0]
    base_image = doc.extract_image(xref)
    with open(f'images/chapter_1/fig_{i}.png', 'wb') as f:
        f.write(base_image['image'])
"
```

**方案2** — 如果 MinerU 输出中图片路径指向非标准位置，手动复制到 `images/chapter_n/`：
```bash
find source_final/ -name "*.jpg" -o -name "*.png" | while read f; do
    ch=$(basename $(dirname $f))
    mkdir -p "images/$ch/$(basename $f)"
    cp "$f" "images/$ch/"
done
```

**方案3** — 如果 PDF 中的图片是矢量图无法提取，用 pdftoimage：
```bash
# 安装 poppler 后用 pdftoimage
pdftoimage -f 14 -l 28 -png "HDD3-Volume Ill - Advanced Receiver Design.pdf" images/chapter_1/
```

---

## 第五章：Phase 2 — 翻译原子循环（MANDATORY）

**这是整个翻译的核心。每次只处理1-2段，完成后必须提交。**

### 5.1 工作目录

所有操作仅在项目根目录 `/Volumes/Elements/HDD3-Volume-III/` 下进行。**绝对禁止写入 `/tmp` 或任何其他目录。**

### 5.2 循环协议（逐段执行）

```
┌─────────────────────────────────────────────────────────┐
│             循环开始（每次只做1-2段）                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Step 1: 读进度文件                                       │
│   → 读取 .omo/progress.md                                │
│   → 确认上次翻译到哪里（章节、行号、小节）                   │
│   → 如果文件不存在或为空，初始化它                          │
│                                                         │
│  Step 2: 读源文件定位                                    │
│   → 读取 source_final/chapter_n.md                       │
│   → 用 offset 和 limit 参数定位到上次结束位置              │
│   → 确定下一节要翻译的1-2段原文                            │
│                                                         │
│  Step 3: 读取原文                                        │
│   → 用 read(offset=X, limit=Y) 精确定位                   │
│   → 记下开始和结束的行号                                   │
│                                                         │
│  Step 4: 逐字翻译                                        │
│   → 直译，不是概括                                       │
│   → 保留所有 $$...$$ 公式原样                             │
│   → 保留所有标题层级（#, ##, ###）                         │
│   → 保留所有列表（-, *, 1.）                              │
│   → 保留所有表格结构                                       │
│   → 保留所有代码块                                        │
│   → 技术术语保持全书一致                                  │
│                                                         │
│  Step 5: 检查原文中的图片引用                              │
│   → 查看原文段落中有没有 ![](images/chapter_n/...)         │
│   → 如果有，翻译后的中文段落中也必须包含相同的图片引用        │
│   → 图片路径不变（指向 images/chapter_n/）                 │
│   → 绝对不要自己画图替代                                    │
│                                                         │
│  Step 6: 追加到中文文件                                    │
│   → 用 read 确认 chinese_final/chapter_n.md 文件的最后一行 │
│   → 用 edit 在文件末尾追加翻译内容                          │
│   → 绝不覆盖已有内容                                       │
│   → 如果文件不存在，用 write 创建（但只有第一次）             │
│                                                         │
│  Step 7: 验证追加成功                                      │
│   → 用 read 确认新内容已写入                                │
│   → 检查公式 $$...$$ 是否成对，无遗漏                       │
│                                                         │
│  Step 8: 更新进度文件                                      │
│   → 更新 .omo/progress.md：                               │
│     - 当前章节、已翻译到第几行                               │
│     - 当前翻译到哪个小节（如 1.2.3）                         │
│     - 上次翻译的行号范围                                    │
│                                                         │
│  Step 9: 提交                                            │
│   → git add chinese_final/ .omo/progress.md              │
│   → git commit -m "翻译 Ch{章节} 第{小节} - {功能描述}"     │
│   → 例如: "翻译 Ch1 1.2 - 读通道模型"                      │
│                                                         │
│  Step 10: 判断是否继续                                     │
│   → source_final/chapter_n.md 还有未翻译的内容？           │
│     → 是 → 回到 Step 1 （循环）                            │
│     → 否 → 当前章节完成，移到下一章                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 5.3 翻译规则（严格遵守）

#### 5.3.1 公式
- 所有 `$$...$$` 包裹的 LaTeX 公式**原样保留**
- 不要修改公式内的任何符号、变量名
- 行内公式 `$...$` 也原样保留
- 在公式前的文字中，可以翻译公式说明性文字

**示例：**
```markdown
源文本：
The signal model is given by $$r(t) = \sum_{k} a_k h(t - kT) + n(t)$$

中文翻译：
信号模型由下式给出 $$r(t) = \sum_{k} a_k h(t - kT) + n(t)$$
```

#### 5.3.2 图片
- 源文中的 `![](images/chapter_n/filename.png)` 必须出现在中文对应位置
- 不要改变图片路径
- 不要用文字描述替代图片
- 不要用 mermaid 或其他图表替代原图

#### 5.3.3 标题
- `# 主要标题` → 翻译后保持 `# 翻译后标题`
- `## 子标题` → 翻译后保持 `## 翻译后子标题`
- 标题层级不变，只翻译文字内容

#### 5.3.4 列表
- 有序列表 `1. xxx` → 翻译后 `1. xxx`
- 无序列表 `- xxx` → 翻译后 `- xxx`
- 保持缩进和层级

#### 5.3.5 表格
- 保留表格的 markdown 结构
- 只翻译单元格内的文字内容
- 不改变列数和行数

#### 5.3.6 引用/参考文献
- `[1]`、`[2-5]` 等引用标记保留原样
- 不翻译引用标记

### 5.4 章节翻译顺序

严格按照以下顺序逐章完成：

```
Ch1 → Ch2 → Ch3 → Ch4 → Ch5 → Ch6 → Ch7 → Ch8 → 附录A → 附录B → 附录C → 附录D
```

**每次只处理一个章节**。完成一个章节的全文翻译并提交后，才进入下一章。

### 5.5 中断恢复机制

如果翻译过程中断（会话超时、意外断开）：

1. 读取 `.omo/progress.md` 中的 `Current` 指针
2. 读取 `chinese_final/chapter_n.md` 的末尾5行，确认结束位置
3. 读取 `source_final/chapter_n.md` 从上次结束位置的下1行开始
4. 从中断处继续翻译

---

## 第六章：Phase 3 — 验证与完成

### 6.1 每章翻译完成后

每章全部翻译完后，执行：

```bash
# 1. 行数对比
python3 -c "
src = open('source_final/chapter_1.md').readlines()
chi = open('chinese_final/chapter_1.md').readlines()
print(f'源文件行数: {len(src)}')
print(f'中文行数: {len(chi)}')
print(f'比率: {len(chi)/len(src)*100:.0f}%')
"

# 2. 公式数量对比
python3 -c "
import re
src = open('source_final/chapter_1.md').read()
chi = open('chinese_final/chapter_1.md').read()
src_eq = len(re.findall(r'\\\$\\\$', src))
chi_eq = len(re.findall(r'\\\$\\\$', chi))
print(f'源公式数: {src_eq//2}')
print(f'中公式数: {chi_eq//2}')
print(f'公式匹配率: {min(chi_eq,src_eq)/max(src_eq,chi_eq)*100:.0f}%')
"

# 3. 图片引用对比
python3 -c "
import re
src = open('source_final/chapter_1.md').read()
chi = open('chinese_final/chapter_1.md').read()
src_imgs = len(re.findall(r'!\\[\\]\\(', src))
chi_imgs = len(re.findall(r'!\\[\\]\\(', chi))
print(f'源图片引用: {src_imgs}')
print(f'中图片引用: {chi_imgs}')
"
```

### 6.2 全书完成后的最终检查清单

- [ ] `source_final/` 包含所有12个源文件（Ch1-8 + App A/B/C/D）
- [ ] `chinese_final/` 包含所有12个中文翻译文件
- [ ] `images/chapter_1/` 到 `images/chapter_8/` 图片完整
- [ ] 每章中文行数达到源文件60%以上
- [ ] 每章公式匹配率达到90%以上
- [ ] 每章图片引用数量匹配
- [ ] 没有 mermaid 或其他自画图
- [ ] 没有在 `/tmp` 或其它目录留下中间文件
- [ ] `.omo/progress.md` 完整记录所有翻译进度
- [ ] `.gitignore` 已创建（忽略 .DS_Store、*.pdf 等）
- [ ] README.md 已更新（包含版权声明）

---

## 第七章：禁止事项（违反即返工）

1. ❌ **禁止在 `/tmp` 或任何项目外目录创建文件**
2. ❌ **禁止用 `write` 覆盖已有的中文翻译文件**（只能用 append）
3. ❌ **禁止一次翻译超过2段原文**
4. ❌ **禁止自己画图（mermaid/ascii art/diagrams）替代原图**
5. ❌ **禁止删除或修改已翻译并提交的内容**
6. ❌ **禁止跳过公式或图片引用**
7. ❌ **禁止在源文件提取不完整时开始翻译**
8. ❌ **禁止跳跃顺序翻译**（必须按 Ch1→Ch2→...→附录D 顺序）
9. ❌ **禁止在提取阶段遗漏图片**（必须验证每个图片引用都对磁盘文件）
10. ❌ **禁止笼统概括**（必须逐字直译，保留所有技术细节）

---

## 第八章：成功标准

- 所有12个章节/附录全部翻译完成
- 每个中文文件的内容都忠实于源文件（不是概括）
- 所有数学公式完整保留
- 所有原图被正确包含
- 没有自创图替代原图
- 没有创建项目外的临时文件
- 每步都有 git commit

---

**等待确认**：按此计划执行？
