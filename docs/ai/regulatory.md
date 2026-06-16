# Regulatory & clinical deployment

> What changes when a model touches a patient. SaMD, GMLP, IND-supporting analyses.

Most drug-discovery models live in research — predicting "make this molecule next". A growing fraction enter the regulatory path: patient-facing diagnostic models, biomarker-driven stratification, in-silico-supported IND filings. The regulatory rules are different and tighter.

## Software as a Medical Device (SaMD)

The FDA classifies software intended to diagnose, treat, or prevent disease as **SaMD**. Categories:

- **Class I (low risk)** — wellness apps, informational tools.
- **Class II (moderate risk)** — most diagnostic-support software.
- **Class III (high risk)** — software that determines treatment without clinician override.

Drug-discovery models rarely enter Class III directly. But a patient-stratification model used in trial enrolment, or a companion-diagnostic algorithm, can be Class II / III.

## Good Machine Learning Practice (GMLP)

FDA / Health Canada / MHRA jointly published [Good Machine Learning Practice principles](https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles)[^gmlp] in 2021, updated 2024. The principles (paraphrased):

1. **Multi-disciplinary expertise** through the lifecycle.
2. **Good software-engineering and security** practices.
3. **Clinical study design** representative of intended use.
4. **Training data independent of test data.**
5. **Reference standards based on best clinical practice.**
6. **Model design tailored to the data and use case.**
7. **Focus on performance of the human-AI team.**
8. **Testing demonstrating clinically relevant performance.**
9. **Users provided clear, essential information.**
10. **Deployed models monitored for performance** and updated controllably.

These are the *minimum bar* for any patient-facing model. Industry implementations of GMLP look heavyweight to a research team; the cost is non-negotiable for any deployed model.

## Predetermined Change-Control Plans (PCCPs)

The FDA's mechanism for allowing models to learn / update post-deployment without re-submitting for approval each time.

A PCCP pre-specifies:

- What parts of the model can change (e.g. retraining cadence).
- What performance thresholds must be met.
- What data the change is based on.

This is how an adaptive ML model can stay current. Without a PCCP, every model change triggers a new submission.

## What this means for drug-discovery models

A model used in drug *discovery* (target ID, hit finding, lead optimisation) is internal R&D — not regulated. A model used in *development* may need to support an IND filing.

The hierarchy:

1. **Internal R&D models** — no regulatory burden, but quality matters for project decisions.
2. **IND-supporting in-silico analyses** — included in the IND dossier as supporting evidence. Reviewable.
3. **Companion diagnostic / patient stratification** — fully regulated SaMD.
4. **Treatment-decision algorithms** — Class II/III SaMD.

## Documentation expectations

For any model touching the regulatory path:

- **Data provenance** — where every label came from, with timestamps.
- **Versioned model artefacts** — including hyperparameters and library versions.
- **Validation protocol** — held-out test, scaffold / time / series split, calibration.
- **Failure-mode analysis** — known limitations and OOD behaviour.
- **Monitoring plan** — how performance is tracked in deployment.
- **Bias analysis** — performance across demographic subgroups for patient-facing tools.

These map to MDR (EU), FDA QSR, and IEC 62304 requirements. Industry has frameworks (Model Cards [Mitchell et al., 2019](https://doi.org/10.1145/3287560.3287596)[^modelcards], Datasheets, Compliance frameworks like the FDA's pre-cert program) for capturing them.

## In practice

- **Most drug-discovery ML is unregulated**. But applying GMLP-grade practice is still good engineering.
- **For patient-facing or IND-supporting models**, work with regulatory affairs *from the start*. Retrofitting compliance is much more expensive than building it in.
- **Versioning, monitoring, and documentation** are the cheap, always-correct investments.
- **The future of adaptive ML in regulated settings** depends on PCCPs and is still developing. Watch FDA / EMA / MHRA publications.

## References

[^gmlp]: U.S. Food and Drug Administration, Health Canada, MHRA. Good Machine Learning Practice for Medical Device Development: Guiding Principles. 2021/2024. [URL](https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles)
[^modelcards]: Mitchell M, Wu S, Zaldivar A, et al. Model cards for model reporting. *FAccT.* 2019;220–229. [doi:10.1145/3287560.3287596](https://doi.org/10.1145/3287560.3287596)
