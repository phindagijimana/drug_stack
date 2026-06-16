# Capstone — target to lead

> The full pipeline. Pick a target with public data, identify chemical starting points, train a QSAR, design new molecules, dock them, triage. End-to-end in one workflow.

This capstone is harder than each individual tutorial. It is meant as the **synthesis exercise** — you've read the chapters and done the per-step tutorials; this puts them together.

## Goal

Produce a defensible 20-molecule shortlist for a chosen kinase target, with full provenance: target evidence, QSAR model, docking scores, ADMET predictions, scaffold-cluster summary, and a triage rationale per molecule.

## Steps (5–10 days of focused work)

1. **Pick a target** with at least 1 000 ChEMBL bioactivity points and an available co-crystal structure. Candidates: BRD4, JAK2, BTK, CDK2.

2. **Target evidence summary.** Open Targets + UniProt + one disease-specific reference. Three paragraphs explaining why this target matters.

3. **Tractability check.** Run FPocket / P2Rank on the co-crystal; report top pocket volume and druggability.

4. **Build the QSAR dataset.** Extract pIC50s, deduplicate by InChIKey, aggregate replicates (median + n). Document scaffold split.

5. **Train QSAR.** Scaffold-CV RF baseline; report metrics with bootstrapped CIs.

6. **Build the screening library.** Sample 100 000 from ChEMBL or ZINC; rule-of-5 prefilter; PAINS / Brenk filter.

7. **Dock the library.** Vina at exhaustiveness 16; if compute is tight, dock top-1 000 by QSAR prediction.

8. **Rescore.** Rerank top 1 000 with gnina or MM-GB/SA.

9. **Run generative design.** REINVENT 4 with QSAR + ADMET + SA + MPO scoring. Generate 10 000 candidates; filter to 200.

10. **Predict ADMET** for all docked + generated candidates with ADMET-AI (hERG, AMES, DILI, CYPs, BBB if relevant).

11. **Build composite score**: weighted geometric mean of QSAR + docking + ADMET + SA + novelty.

12. **Cluster** by Bemis-Murcko scaffold; pick top 5 per top 4 clusters, total 20.

13. **Per-molecule one-paragraph rationale** explaining why each made the shortlist.

14. **Reproducibility checklist** — fill in all ten items from the [checklist](../computing/reproducibility.md).

## Deliverables

- A short report (PDF or Markdown) with target rationale, methods, key tables, and the molecule grid.
- A reproducible repo (Git + Docker image hash + lockfiles).
- A presentation outline you could give to a medicinal-chemistry team.

## What "done" looks like

If a medicinal chemist could:

- Read the report in 30 minutes and understand the case.
- Pull the repo and reproduce the numbers.
- Pick 5 of the 20 to order and synthesise.

…you have completed the capstone.

## Honest verdict

The 20 molecules will not all bind. Some will be obvious failures (PAINS the filter missed, synthesisability issues the SA score got wrong). The best-case outcome is 3–5 bind at the assay; that's a normal hit rate for prospective virtual screening.

The *output* of the capstone is not "a drug". It is **fluency** — you can now plan and execute a real campaign end-to-end. That is the deliverable.

## Where to next

You're done with the tutorials. Go back to [Reading paths](../paths/index.md) and pick the depth chapter most relevant to your next project; or start contributing to the handbook.
