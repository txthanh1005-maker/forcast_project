---
name: deep-logic-audit
description: Thể thức kiểm tra sâu (3 bước) dành cho đánh giá logic vật lý, AC-OPF, tìm "Missing Links", diệt "Fluff", và chứng minh bản chất thuật toán trong các chương Luận văn khoa học.
---

# Deep Logic Audit Workflow (Quy trình Review 3 Bước của Tư lệnh)

This skill provides a rigorous, 3-step auditing framework specifically designed to evaluate complex scientific writing (such as AC-OPF, Grid Stability, and P2P Trading chapters) for logical consistency, cross-linking, academic depth, and algorithmic proof.

## Trigger
Use this skill when the user asks to "audit", "review the logic", "tìm missing link", "lọc fluff", "chứng minh thuật toán", or "rà soát sâu" a specific chapter or document.

## Execution Steps

You must follow this exact 3-step process. Do NOT skip steps or merge them.

### Step 1: The Skim (Xác định Xương sống Logic)
- **Action:** Read through the entire text of the target document/chapter quickly.
- **Purpose:** Do not look for spelling or minor errors. Focus entirely on identifying the overarching logic, system configuration, and major physical phenomena being described (e.g., Load Shedding, Voltage Limits, P2P Pricing).
- **Output:** Establish a "Global Baseline" of the system's intended behavior.

### Step 2: The Deep Dive & Roll-up (Review Cuốn chiếu từng Section)
- **Action:** Go back to the beginning and review the document section-by-section. For each section, you MUST open and cross-reference the corresponding charts/data images.
- **Questions to Answer per Section:**
  1. **Missing Links (Đứt gãy liên kết):** Does the input/data in this section have implications for downstream sections that the author failed to analyze?
  2. **Isolated Islands (Đoạn văn Cô lập):** Are there any paragraphs or analyses that stand completely independent without linking to the sections above or below them? If an insight is isolated, trigger a WARNING and propose a method to weave it into the broader narrative or connect it to subsequent results.
  3. **Physical Logic Contradictions (Mâu thuẫn Vật lý):** Does the text contradict the actual plotted data or the fundamental laws of Power Systems (e.g., AC-OPF limits, $I^2X$ losses, Economic Dispatch principles)?
  4. **Mathematical Cross-Validation:** Which specific constraint or mathematical equation is driving this phenomenon? Explicitly link the observed behavior to the AC-OPF formulation.
  5. **Hostile Examiner (Red Teaming):** If you were a hostile committee member trying to reject this thesis based on this specific chart/paragraph, what weakness would you attack? Provide preemptive defenses.
  6. **[NEW] Fluff Filtration (Lọc văn dài dòng/Vô giá trị):** Are there paragraphs that are unnecessarily long-winded, overly descriptive, or lack academic weight? Identify sentences that merely state the obvious without adding physical or economic insight, and propose brutal condensation.
  7. **[NEW] Core Algorithmic Proof (Chứng minh Bản chất Thuật toán):** Is the text merely a superficial "number comparison" (e.g., "A is 10, B is 5, so A is better")? The text MUST prove the underlying core mechanics of the proposed algorithm (e.g., *WHY* did the MPC behave this way? *HOW* did decentralized ATC achieve consensus?). Flag any section that compares outcomes without proving the algorithmic mechanisms driving those outcomes.

### Step 3: The Audit Report
- **Action:** Output a structured report to the user.
- **Format:**
  - Break down the report by Section.
  - Clearly identify any [LOGIC BUGS], [MISSING LINKS], and [FLUFF].
  - Provide actionable, deep AC-OPF academic recommendations to deepen the analysis and prove the core algorithmic properties.
  - Suggest footnotes or preemptive defenses for any vulnerabilities identified in the Red Teaming phase.
  - If a section is mathematically, logically, and academically perfect, explicitly state [PASS].
- **Constraint:** Do not auto-edit the user's code/LaTeX unless explicitly commanded. Just provide the specialized audit analysis.
