# Future Work: Human-Informed Prompt Refinement for Task→Ability Mapping

> **Status: planned (not yet run).** The original LLM mapping is released as-is with 98.5%
> human-validated precision (see `VALIDATION_RESULT.md`). This document specifies how a
> *future* paper will use the human corrections to improve the generation prompt and re-test.

## Idea

The 200-task human audit revealed **systematic, non-random** errors in the LLM mapping. Rather
than hand-patching the dataset (which would make it a human/LLM hybrid and break its "purely
LLM-generated, human-validated" provenance), we encode the *patterns* of human correction back
into the generation prompt, **re-generate the mapping from scratch**, and test whether the new
mapping already contains the additions/removals humans made — i.e., whether validated precision
rises above the current 98.5% and the coverage gap shrinks.

If the refined prompt reproduces the human corrections automatically, our confidence in the
mapping increases *without* any manual editing of the dataset.

## What the human corrections told us (from the 200-task audit)

**LLM under-lists (228 additions) — add coverage guidance:**
- **Cognitive (119)** — most common gap: *Mathematical Reasoning, Information Ordering, Number
  Facility, Selective Attention, Category Flexibility, Problem Sensitivity, Visualization.*
  The model omits "background" cognitive abilities that quantitative/ordering/attention-heavy
  tasks implicitly require.
- **Psychomotor / Physical (89)** — for hands-on tasks: *Control Precision, Manual Dexterity,
  Arm-Hand Steadiness, Gross Body Coordination, Static Strength.*

**LLM over-lists (34 removals) — add precision guidance:**
- **Sensory** — most often *Near Vision* attached to tasks that don't actually require close
  visual detail; also *Speech Recognition.*
- **Cognitive** — occasional over-reach with *Deductive Reasoning, Originality.*

## Drafted refinement prompt (to prepend to / merge into the generation prompt)

> When mapping an O*NET task to the 52 O*NET Abilities, apply these calibration rules learned
> from expert human review:
> 1. **Do not under-list implicit cognitive abilities.** If a task involves calculation,
>    ordering/sequencing, counting, or sustained attention, explicitly include *Mathematical
>    Reasoning, Number Facility, Information Ordering,* and/or *Selective Attention* even when
>    they are not the task's headline skill.
> 2. **For physical/manual tasks, include the enabling motor and strength abilities** —
>    *Control Precision, Manual Dexterity, Arm-Hand Steadiness, Gross Body Coordination,
>    Static Strength* — not only the cognitive planning abilities.
> 3. **Do not over-attach sensory abilities.** Include *Near Vision* only when the task
>    genuinely requires close-range visual detail; do not add it by default to desk or
>    interpersonal tasks. Apply the same restraint to *Speech Recognition* and *Deductive
>    Reasoning.*
> 4. Prefer **recall over caution** for cognitive/psychomotor coverage, and **precision over
>    inclusion** for sensory abilities — this mirrors where human experts most often disagreed
>    with the base model.

## Test methodology (planned)

1. **Regenerate** the task→ability mapping for the 200 audited tasks using the refined prompt
   (same model, same weight-elicitation procedure; only the calibration rules added).
2. **Score against the existing human annotations** as ground truth:
   - **Precision** = fraction of newly-generated abilities that humans endorsed (target: > 98.5%).
   - **Recall of human additions** = fraction of the 228 human-added abilities the refined
     prompt now includes on its own (this is the key metric — did we close the coverage gap?).
   - **Over-list reduction** = fraction of the 34 human-removed abilities the refined prompt
     now correctly omits.
3. **Report the delta** vs. the base prompt. Success = higher recall of human additions and
   fewer sensory over-lists, at equal-or-better precision.
4. If successful, **regenerate the full 4,577-task mapping** with the refined prompt and release
   it as v2 of the dataset, with this validation as the accompanying evidence.

## Why this belongs in a separate paper

This is a *methods contribution* (human-in-the-loop prompt refinement + re-validation), distinct
from the current resource release. The current dataset stands on its own at 98.5% validated
precision; the refinement study is the natural follow-up.
