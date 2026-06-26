# Agent Instructions: HDD3 Book Conversion

## Core Objective
Convert `HDD3-Volume III - Advanced Receiver Design.pdf` into high-fidelity, equation-accurate Markdown files, split by chapter, and translated from Thai to Chinese.

## Project Structure
 - `source_final/`: Source Markdown chapters (extracted from PDF).
- `chinese_final/`: Target Chinese translations.
- `.omo/progress.md`: Source-of-truth for translation progress (tracks line numbers and sections).

## Technical Environment
- **PDF Extraction**: Use the pre-configured `mineru` environment.
- **Fidelity**: Mathematical equations must be preserved exactly; maintain original document layout.

## Strict Execution Loop (Translation)
Every translation task MUST follow this atomic sequence. **Do not batch sections.**

1. **Translate**: Translate one small section from Thai to Chinese.
2. **Sync**: Update `.omo/progress.md` with the exact position (line number, section, and key content).
3. **Append**: Append translated content to the target file in `chinese_final/`.
   - *Constraint*: Create if missing; **NEVER** overwrite existing content.
4. **Verify & Commit**: Verify the append was successful, then immediately execute `git commit`.

## Finalization Checklist
- [ ] **README**: Update with exactly: *"I have tried to get in touch with prof Piya but I failed. Considering the copyright, I would appreciate it if those who may concern contact me. The translation work is done with the help of Gemma-4-31B-it."*
 - [ ] **Git**: Create `.gitignore` and perform final local commit. (Do NOT push to any remote repository).
