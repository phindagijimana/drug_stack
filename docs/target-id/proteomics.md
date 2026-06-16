# Proteomics for target identification

> Protein abundance, post-translational modifications, and physical interactions. The layer where most drugs actually act.

mRNA is a noisy proxy for protein. Modifications matter. Interactions matter. Proteomics fills three gaps that transcriptomics alone cannot.

## What proteomics measures

- **Abundance** — how much of each protein is present, by mass spectrometry.
- **Post-translational modifications (PTMs)** — phosphorylation, acetylation, ubiquitination, glycosylation. Often the actual switch a drug flips.
- **Interactions** — affinity-purification mass spec (AP-MS), proximity labelling (BioID, TurboID), yeast two-hybrid.
- **Localisation** — fractionation MS, imaging (e.g. Human Protein Atlas).

## Why bulk-protein abundance disagrees with mRNA

The Spearman correlation between bulk mRNA and protein levels across genes is typically 0.4–0.6. Reasons:

- **Translation regulation** — uORFs, codon usage, ribosome occupancy.
- **Protein turnover** — half-lives range from minutes to days; mRNA half-lives cluster shorter.
- **Buffering** — protein complexes degrade unbound subunits.

For target-ID this matters: a disease DEG that does *not* translate to a protein change is a weaker target candidate.

## Phosphoproteomics

PTM-resolved proteomics. Phosphorylation is the most studied PTM and the one most relevant to kinase / phosphatase drug discovery.

- **Workflow**: TMT or label-free MS with phospho-peptide enrichment (TiO₂, IMAC).
- **Output**: site-resolved phospho-occupancy, often condition-vs-condition.
- For target ID, **kinase signature inference** (KSEA, KEA3) connects phospho-substrate changes back to active kinases.

## Affinity-based interactome

- **AP-MS**: tag a bait protein, pull it down with antibodies, identify co-pulldowns by MS.
- **BioID / TurboID**: bait protein fused to a promiscuous biotin ligase; nearby proteins get biotinylated and pulled down on streptavidin.
- **Crosslinking MS (XL-MS)**: covalently crosslink interacting residues, identify by MS, map to structure.

For a candidate target whose biology is poorly understood, an interactome is fast and informative. The **BioPlex 3.0** [Huttlin et al., 2021](https://doi.org/10.1016/j.cell.2021.04.011)[^bioplex] and **OpenCell** [Cho et al., 2022](https://doi.org/10.1126/science.abi6983)[^opencell] networks give you a pre-computed start.

## Chemoproteomics — orthogonal target ID

When you have a phenotypic active but no target hypothesis, chemoproteomics identifies the protein the compound binds.

- **Activity-based protein profiling (ABPP)** — a probe covalently labels a class of proteins (serine hydrolases, kinases). A drug that competes off the label tells you the target [Cravatt et al., 2008](https://doi.org/10.1146/annurev.biochem.75.101304.124125)[^abpp].
- **Thermal proteome profiling (TPP / CETSA-MS)** — drugs stabilise the proteins they bind; thermal denaturation MS picks up the stability shift. Target deconvolution without modifying the compound.
- **Photoaffinity labelling** with diazirine / benzophenone probes.

This is the right tool when the phenotype is real and the target is mysterious.

## Resources

- **Human Protein Atlas** (`proteinatlas.org`) — tissue & subcellular localisation, antibody validation.
- **PaxDb** — quantitative protein abundance compendium.
- **PhosphoSitePlus** — curated PTM database.
- **CPTAC** — clinical proteomics in cancer.
- **PRIDE** — public mass-spec repository.

## In practice

- For target ID, **add proteomics as a tiebreaker** between transcriptomic candidates: a target whose protein is up in disease is stronger than one whose mRNA is up but protein is not.
- For **phenotypic-hit deconvolution**, TPP / CETSA-MS is usually the first call.
- **Quantitative proteomics is noisy at the low-abundance tail** — kinases and TFs are often near detection limits. Multiple-test corrections matter.

## References

[^bioplex]: Huttlin EL, Bruckner RJ, Navarrete-Perea J, et al. Dual proteome-scale networks reveal cell-specific remodeling of the human interactome. *Cell.* 2021;184(11):3022–3040. [doi:10.1016/j.cell.2021.04.011](https://doi.org/10.1016/j.cell.2021.04.011)
[^opencell]: Cho NH, Cheveralls KC, Brunner A-D, et al. OpenCell: endogenous tagging for the cartography of human cellular organization. *Science.* 2022;375(6585):eabi6983. [doi:10.1126/science.abi6983](https://doi.org/10.1126/science.abi6983)
[^abpp]: Cravatt BF, Wright AT, Kozarich JW. Activity-based protein profiling: from enzyme chemistry to proteomic chemistry. *Annu Rev Biochem.* 2008;77:383–414. [doi:10.1146/annurev.biochem.75.101304.124125](https://doi.org/10.1146/annurev.biochem.75.101304.124125)

## Where to next

[Network & pathway biology](networks.md) — placing the target candidate in its biological context.
