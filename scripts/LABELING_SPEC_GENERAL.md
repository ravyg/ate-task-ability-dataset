# Task→Ability Labeling Spec (GENERAL — all SOC groups). Replicates the published ATE dataset method.

Label each O*NET task with the subset of the **52 O*NET abilities** it genuinely requires.
Must be methodologically identical to the frozen 4,577 mappings so new rows are consistent.

## Output schema (CSV rows)
`task_id,occupation,task_text,ability_name,weight,uncertain`
- One row per (task, ability). Typically **3–7 abilities** per task (dataset mean ≈ 5.4; range 1–12).
- `ability_name`: MUST be one of the 52 exact strings below. No invented abilities.
- `weight`: integer **1, 2, or 3** — 1 = mild/incidental, 2 = moderate/clearly needed, 3 = critical/central.
- `uncertain`: `1` only if genuinely borderline, else `0`. Use sparingly.

## Labeling rules
1. Label ONLY abilities the specific TASK invokes — not abilities the occupation broadly has. Task-level, not occupation-level. Anchor on the verb + object.
2. **Match abilities to the real physical/cognitive demands of the task.** This corpus spans the whole economy — many tasks are MANUAL/PHYSICAL and MUST receive the physical, psychomotor, and sensory abilities they require:
   - Lifting/carrying/pushing heavy loads → Static Strength, Dynamic Strength, Trunk Strength, Stamina.
   - Operating tools/machinery/vehicles, welding, assembly, precise handwork → Manual Dexterity, Finger Dexterity, Arm-Hand Steadiness, Control Precision, Multilimb Coordination, Reaction Time, Rate Control.
   - Climbing, balancing, working at height, crouching → Gross Body Coordination, Gross Body Equilibrium, Extent/Dynamic Flexibility.
   - Inspecting, driving, monitoring visually → Near Vision, Far Vision, Depth Perception, Visual Color Discrimination, Peripheral Vision.
   - Listening for equipment faults, responding to sounds → Auditory Attention, Hearing Sensitivity, Sound Localization.
   Do NOT under-label physical work as if it were cognitive. A construction/production/transport/maintenance task that is physically demanding should look physically demanding in its ability profile.
3. Conversely, do NOT add physical abilities to purely cognitive/clerical tasks. A planning, analysis, or documentation task is cognitive even in a manual occupation.
4. Weights reflect centrality to THIS task, not general importance.
5. Keep the exact `task_id`, `occupation`, `task_text` from the input unchanged.

## The 52 abilities (name → family). Use ONLY these exact names.
COGNITIVE: Category Flexibility, Deductive Reasoning, Flexibility of Closure, Fluency of Ideas, Inductive Reasoning, Information Ordering, Mathematical Reasoning, Memorization, Number Facility, Oral Comprehension, Oral Expression, Originality, Perceptual Speed, Problem Sensitivity, Selective Attention, Spatial Orientation, Speed of Closure, Time Sharing, Visualization, Written Comprehension, Written Expression
PSYCHOMOTOR: Arm-Hand Steadiness, Control Precision, Finger Dexterity, Manual Dexterity, Multilimb Coordination, Rate Control, Reaction Time, Response Orientation, Speed of Limb Movement, Wrist-Finger Speed
PHYSICAL: Dynamic Flexibility, Dynamic Strength, Explosive Strength, Extent Flexibility, Gross Body Coordination, Gross Body Equilibrium, Stamina, Static Strength, Trunk Strength
SENSORY: Auditory Attention, Depth Perception, Far Vision, Glare Sensitivity, Hearing Sensitivity, Near Vision, Night Vision, Peripheral Vision, Sound Localization, Speech Clarity, Speech Recognition, Visual Color Discrimination

## Few-shot examples (match this style)
Cognitive task "Monitor and analyze sales records, trends, or economic conditions to anticipate consumer buying patterns":
- Inductive Reasoning,3 ; Mathematical Reasoning,2 ; Number Facility,2 ; Written Comprehension,2 ; Deductive Reasoning,2

Communication task "Consult with managers about budgets or goods to be purchased":
- Oral Comprehension,3 ; Oral Expression,2 ; Written Comprehension,2 ; Deductive Reasoning,2 ; Speech Recognition,2 ; Speech Clarity,1

Manual task "Operate hoisting equipment to lift and position heavy structural steel members":
- Control Precision,3 ; Multilimb Coordination,3 ; Depth Perception,3 ; Reaction Time,2 ; Arm-Hand Steadiness,2 ; Far Vision,2 ; Selective Attention,2

Manual task "Lift and carry heavy loads of materials to work areas":
- Static Strength,3 ; Trunk Strength,3 ; Stamina,2 ; Dynamic Strength,2 ; Gross Body Equilibrium,1
