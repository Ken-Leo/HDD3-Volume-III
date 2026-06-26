# Skill: Technical Book Translation

This skill provides a rigorous, end-to-end pipeline for converting technical books (PDF) into high-fidelity, equation-accurate translated Markdown files. It is designed to prevent data loss, maintain mathematical integrity, and ensure session-agnostic continuity.

## 0. Project Setup (Onboarding)
Before initiating the pipeline, the agent must ensure the project environment is configured to match the skill's expected structure.

### Required Directory Structure:
- `source_final/`: Storage for extracted raw Markdown chapters.
- `target_final/`: Storage for the final translated Markdown chapters.
- `.omo/`: Project metadata folder.
- `.omo/progress.md`: The state-tracking file (must be initialized).

### Initialization Workflow:
1. **Directory Creation**: Create `source_final/` and `target_final/` if they do not exist.
2. **Progress File Init**: Create `.omo/progress.md` with the following template:
   ```markdown
   # Translation Progress
   Overall Status: [Source Path] -> [Target Path]
   Goal: [Full Book Translation]

   ## Chapter Tracking
   - [ ] Chapter 1: Pending
   - [ ] Chapter 2: Pending
   ...
   Current Pointer: Chapter 1, Section 1, Line 1
   ```

## 1. Core Objective

Convert a technical PDF into a structured set of translated Markdown files where:

- **Mathematical Equations**: All $\LaTeX$ notation is preserved exactly.
- **Visual Assets**: Images are extracted, organized by chapter, and linked correctly.
- **Structure**: The output is split by chapters for manageability and review.
- **Fidelity**: Technical terminology remains consistent across the entire volume.

## 2. Phase 0: Structural Decomposition (NLU-Driven)

Before extraction, the book's architecture must be mapped to avoid monolithic files and ensure organized translation.

### Workflow:

1. **TOC Analysis**: Use NLU to parse the book's Table of Contents to establish logical page ranges.
2. **Physical Page Calibration**: 
   - Identify the physical page index where Chapter 1 actually begins.
   - Account for front matter (cover, preface, copyright, abstract, etc.) that shifts the starting point.
   - Calculate the **Offset**: `Physical Start Page - Logical Start Page`.
3. **Page Mapping**: Convert logical page ranges from the TOC into absolute physical page ranges using the calculated offset.
4. **Blueprint Creation**: Create a mapping file or log that defines the absolute `chapter_n.md` physical boundaries.

## 3. Phase 1: Targeted Extraction (MinerU)

Convert the PDF into Markdown using the structural map from Phase 0.

### Workflow:

1. **Targeted Conversion**: Run `mineru` on the PDF, specifying the mapped page ranges for each chapter.
2. **Organization**:
   - Save raw extractions to `source_final/` (e.g., `chapter_1.md`, `chapter_2.md`).
   - Extract images into a global `images/` folder.
3. **Path Sanitization**: 
   - Use the standardized tool `.opencode/skills/technical-book-translation/scripts/fix_paths.py` to organize images into chapter-specific subfolders: `images/chapter_n/`.
   - **Execution**: Run `python .opencode/skills/technical-book-translation/scripts/fix_paths.py <source_final_dir>`.
   - Update all image references in the Markdown files to match these new paths.
4. **Validation**: Verify that all chapters are present and that image references in the Markdown match the extracted files.

## 4. Phase 2: The Recursive Atomic Translation Loop (MANDATORY)
This phase processes the files generated in Phase 1. To prevent "hallucinated progress," context overflow, or data loss, translation is performed as a **recursive loop** of small, atomic sections. 

**The agent must execute this loop repeatedly**—one section per turn—until the entire source file is processed. Do not attempt to translate the entire chapter in a single session.

### The Atomic Loop Sequence (Repeat for every section):

**Step 1: Physical Grounding (Loop Entry)**
Read the last 5-10 lines of the current target file (e.g., `target_final/chapter_n.md`) and the current status in `.omo/progress.md`.
- **Goal**: Confirm the exact line number and content where the previous iteration ended to ensure a seamless transition.
- **Blocker**: If the target file end does not match the progress log, resolve the discrepancy before proceeding.

**Step 2: Source Section Extraction**
Read the specific next section from the pre-extracted source file (e.g., `source_final/chapter_n.md`) using `offset` and `limit`.
- **Goal**: Isolate a small, manageable text block to maintain maximum translation fidelity.

**Step 3: High-Fidelity Translation**
Translate the extracted text into the target language.
- **Equations**: $\LaTeX$ equations must be preserved **verbatim**.
- **Terminology**: Use the project-wide glossary; ensure consistency with previous sections.
- **Layout**: Maintain all headings, lists, and table structures.

**Step 4: Safe Append**
Append the translated content to the target file.
- **FORBIDDEN**: Never use `write` to overwrite an existing chapter file.
- **REQUIRED**: Use the `edit` tool to replace a specific "end-of-file" anchor or use a safe append mechanism that preserves all prior content.

**Step 5: Progress Sync (Loop State Update)**
Immediately update the project tracking file (`.omo/progress.md`).
- **Action**: Mark the translated section as `Completed` and update the `Current` pointer to the exact line/section for the **next iteration of the loop**.

**Step 6: Verifiable Commit (Loop Snapshot)**
Perform an atomic git commit.
- **Command**: `git add <file> && git commit -m "Translate Chapter X Section Y"`
- **Goal**: Create a permanent, recoverable snapshot of every atomic unit of work.

### Loop Control & Termination:
- **Recurrence**: After Step 6, the agent must automatically return to **Step 1** for the next section.
- **Termination**: The loop for a specific chapter terminates ONLY when the entire `source_final/chapter_n.md` has been read and translated.
- **Transition**: Once a chapter loop terminates, the agent updates the chapter-level status in `.omo/progress.md` and moves to the first section of the next chapter.

## 5. Phase 3: Quality Gates & Finalization

### Equation Audit

Perform a final pass over the translated files. Ensure no $\LaTeX$ delimiters were lost and that all subscripts/superscripts are rendered correctly.

### Linked Table of Contents

Create a `README.md` that serves as the project landing page:

- **Bilingual**: Provide both English and Target Language versions.
- **Linked TOC**: Every chapter in the TOC must be a relative link to the corresponding `.md` file in `target_final/`.

### Final Verification

Compare the final target file's line count and structure against the source to ensure no sections were accidentally omitted.

## 6. State Management (`.omo/progress.md`)

The `progress.md` file is the "Source of Truth" for the agent.

- **Structure**:
  - `Overall Status`: Source path, Target path, Goal.
  - `Chapter Tracking`: Checkboxes for each chapter and a detailed list of completed/pending sections.
  - `Remaining Tasks`: High-level milestones.
- **Constraint**: No translation work may begin without first reading the `progress.md` file.
