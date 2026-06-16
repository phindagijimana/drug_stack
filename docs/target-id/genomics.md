# Genomics for target identification

> Human genetics is the strongest signal that modulating a target will move a disease. Programs with genetic support are roughly 2× more likely to be approved.

## Why genetics dominates

Approved drugs whose target has supporting human-genetic evidence have ~2× higher probability of clinical success than those without [Nelson et al., 2015](https://doi.org/10.1038/ng.3314)[^nelson]; the updated 2024 analysis [Minikel et al., 2024](https://doi.org/10.1038/s41586-024-07316-0)[^minikel] confirmed and refined this. No other evidence type comes close.

The underlying logic: if a natural-occurring loss-of-function variant in a gene reduces disease risk, then pharmacological inhibition of the same protein is *the* relevant experiment — and humans, not mice, ran it.

## The three pillars

### 1. GWAS

**Genome-wide association studies** test millions of common variants for association with disease.

- **Inputs**: SNP genotype + phenotype across ~10⁴–10⁶ subjects.
- **Outputs**: SNPs significantly associated at genome-wide threshold (p < 5×10⁻⁸).
- **Limitations**: most signals are in non-coding regions; mapping SNP to causal gene is non-trivial.
- **Workflow tooling**: PLINK, REGENIE, BOLT-LMM, SAIGE (for biobank-scale).

The transition from "associated locus" to "candidate target" is the **fine-mapping → gene-prioritisation** problem: methods like FINEMAP, SuSiE, and PoPS narrow loci and assign causal-gene probabilities.

### 2. Exome / whole-genome sequencing in cohorts

Beyond common variants, rare loss-of-function variants in protein-coding regions provide much stronger per-allele evidence.

- **Burden tests** group rare LoFs in a gene and test for case-control enrichment.
- **PCSK9** is the canonical success: rare LoF carriers have low LDL and reduced coronary disease → led to PCSK9 mAbs (alirocumab, evolocumab) and now siRNA (inclisiran).
- **UK Biobank**, **gnomAD**, **Regeneron–GHS**, **Million Veteran Program**, **Genomics England** are the public-ish resources.

### 3. Mendelian randomisation

A clever use of genetics for causal inference. Variants in a gene are essentially randomised at conception; if they predict both an intermediate phenotype (e.g. LDL level) and a clinical outcome, the causal link from intermediate to outcome is supported.

MR is now routine in target-ID: tools like `MR-Base` and the OpenTargets Genetics portal pre-compute it across the genome.

## OpenTargets and the right starting query

[OpenTargets Genetics](https://genetics.opentargets.org/) is the right starting point for almost every target-ID exercise. It aggregates GWAS, fine-mapping, MR, eQTL, and colocalisation analyses in a uniform API.

```python
import requests

q = """
query {
  studyLocus(studyLocusId: "GCST005195-rs10846744") {
    variant { rsId chromosome position }
    associatedGenes {
      gene { id symbol }
      overallScore
    }
  }
}
"""
r = requests.post("https://api.genetics.opentargets.org/graphql",
                  json={"query": q}).json()
```

For "give me the ten best-supported targets for type-2 diabetes" it is a 10-minute exercise; not 10 minutes of work by a PhD student going through PubMed.

## Single-variant to drug target: an example chain

PCSK9 again, because nothing else has been audited so thoroughly:

1. Familial hypercholesterolaemia patients identified with PCSK9 gain-of-function variants [Abifadel et al., 2003](https://doi.org/10.1038/ng1161)[^pcsk9-gof].
2. Rare loss-of-function carriers found to have ~30% lower LDL and ~50% lower CHD risk [Cohen et al., 2006](https://doi.org/10.1056/NEJMoa054013)[^pcsk9-lof].
3. mAb candidates developed; phase III demonstrated LDL reduction and CV benefit [Sabatine et al., 2017](https://doi.org/10.1056/NEJMoa1615664)[^fourier].
4. siRNA approach (inclisiran) approved in 2020 — different modality, same target.

This chain is the template programs aspire to.

## Pitfalls

- **GWAS lead variant ≠ causal gene.** Most lead variants are non-coding and the nearest gene is often *not* the causal one. Use coloc / PoPS / sQTL analyses to refine.
- **Pleiotropy.** A genetic variant influencing many phenotypes complicates MR.
- **Effect-direction ambiguity.** For drugs you want to mimic *loss-of-function*; for some indications you want *gain-of-function*. Get this wrong and you optimise the wrong thing.
- **Population stratification.** GWAS signals from European-ancestry cohorts under-replicate in others. Multi-ancestry analyses (e.g. PAGE, Global Biobank Meta-analysis Initiative) are the current standard.
- **Indication-creep.** A target with strong genetics for one disease may have weaker evidence for the indication you want to develop into.

## In practice

- Start every target-ID exercise at **OpenTargets Genetics**, with a defined indication and a clear effect-direction hypothesis.
- For LoF burden evidence, **gnomAD** and **UK Biobank PheWAS** are the right complementary lookups.
- **Mendelian randomisation should be the second pass**, not the first; it is hypothesis-confirming rather than hypothesis-generating.
- **Strong genetics + weak biology** is a target worth working on. **Weak genetics + strong biology** is a target worth questioning.

## References

[^nelson]: Nelson MR, Tipney H, Painter JL, et al. The support of human genetic evidence for approved drug indications. *Nat Genet.* 2015;47(8):856–860. [doi:10.1038/ng.3314](https://doi.org/10.1038/ng.3314)
[^minikel]: Minikel EV, Painter JL, Dong CC, Nelson MR. Refining the impact of genetic evidence on clinical success. *Nature.* 2024;629:624–629. [doi:10.1038/s41586-024-07316-0](https://doi.org/10.1038/s41586-024-07316-0)
[^pcsk9-gof]: Abifadel M, Varret M, Rabès J-P, et al. Mutations in PCSK9 cause autosomal dominant hypercholesterolemia. *Nat Genet.* 2003;34(2):154–156. [doi:10.1038/ng1161](https://doi.org/10.1038/ng1161)
[^pcsk9-lof]: Cohen JC, Boerwinkle E, Mosley TH, Hobbs HH. Sequence variations in PCSK9, low LDL, and protection against coronary heart disease. *N Engl J Med.* 2006;354(12):1264–1272. [doi:10.1056/NEJMoa054013](https://doi.org/10.1056/NEJMoa054013)
[^fourier]: Sabatine MS, Giugliano RP, Keech AC, et al. Evolocumab and clinical outcomes in patients with cardiovascular disease. *N Engl J Med.* 2017;376(18):1713–1722. [doi:10.1056/NEJMoa1615664](https://doi.org/10.1056/NEJMoa1615664)

## Where to next

[Transcriptomics](transcriptomics.md) — bulk and single-cell RNA-seq, perturbation atlases, and the cell-of-action problem.
