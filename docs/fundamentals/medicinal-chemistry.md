# Medicinal chemistry

> The chemistry side of drug design. Functional groups, bioisosteres, ring systems, scaffold hopping, the SAR mindset. Enough to talk to chemists credibly.

If a computational scientist cannot read a 2D structure and reason about likely modifications, every "hit" they propose to the chemistry team will be triaged as noise. This page is the minimum chemistry literacy required to participate.

## The medicinal-chemistry mindset

A chemist looks at a molecule and decomposes it into:

1. **Scaffold** — the central ring system that defines the chemical series.
2. **Decoration / vectors** — the substituents that point off the scaffold into pocket subregions.
3. **Linkers** — atoms connecting pharmacophore groups.
4. **Capping groups** — terminal aliphatics, halogens, methyls used to tune properties.

A medicinal-chemistry campaign is then an iterative process: hold the scaffold fixed, perturb one vector at a time, measure SAR, repeat. This is the *fragment-by-fragment* mindset that AI design tools are now learning to imitate.

## Functional groups every newcomer should recognise

| Group | What it does | When to worry |
| --- | --- | --- |
| **Carboxylic acid** (–COOH) | H-bond donor + acceptor; charged at physiological pH; reduces permeability | Often → ester pro-drug |
| **Amine** (1°/2°/3°) | Often protonated; binds asp/glu in pockets; basic centre raises distribution volume | hERG risk, off-target promiscuity |
| **Amide** | Robust H-bond donor / acceptor; metabolically stable | Almost universal — fine |
| **Sulfonamide** | H-bond donor; weakly acidic | Sulfa allergies; CYP interactions |
| **Aromatic halogen** | Lipophilicity boost; halogen bond; CYP block | Excess Cl/F → tox flags |
| **Trifluoromethyl** (–CF₃) | Lipophilicity, metabolic stability | Bioaccumulation, regulatory scrutiny |
| **Hydroxyl** (–OH) | H-bond donor; solubility boost | Glucuronidation, fast metabolism |
| **Nitrile** (–C≡N) | Strong dipole; H-bond acceptor; metabolic stability | Rarely a major liability |
| **Ester** | Polar + cleavable | Plasma esterases — useful for pro-drugs, harmful for drugs |
| **Michael acceptor** | Covalent warhead | Off-target covalent tox — only intentional |

## Ring systems

Drug-like molecules cluster around a small number of ring systems. The Ertl analysis of approved drugs [Bemis & Murcko, 1996](https://doi.org/10.1021/jm9602928)[^bemis] showed that **half of approved drugs** share one of ~30 scaffolds.

The ones you will see every day:

- Benzene, pyridine, pyrimidine, pyrazole, imidazole, indole, quinoline.
- Piperazine, piperidine, morpholine, pyrrolidine.
- Thiophene, furan, oxazole, thiazole.

A **scaffold hop** is replacing the central ring with another that preserves the 3D presentation of vectors. Computationally this is enabled by 3D pharmacophore matching, shape-based methods (ROCS), and graph-based "matched-molecular-series" analyses.

## Bioisosteres

A bioisostere is a substitution that preserves activity while perturbing one or more properties. Classical examples:

| From | To | Why |
| --- | --- | --- |
| Phenyl | Pyridine | Improve solubility, add H-bond acceptor |
| Phenyl | Bicyclo[1.1.1]pentane | Reduce lipophilicity, raise sp3 fraction |
| Carboxylic acid | Tetrazole | Same pKa, better permeability |
| Carboxylic acid | Acyl sulfonamide | Like carboxylic acid, different physchem |
| –C(=O)–NH– (amide) | –CH=CH– (vinyl) | Conformational restriction |
| Methyl | Trifluoromethyl | Block oxidative metabolism |
| –OH | –NH–OH (hydroxylamine) | Different pKa, retained donor |

Bioisostere databases like **BIRD / BISDB / SwissBioisostere** are now standard inputs to lead optimisation.

## Structure–activity relationships (SAR)

The chemist's central concept. **SAR** is the (often non-linear) mapping from chemical structure to measured activity. Three patterns to know:

- **Smooth SAR** — small structural changes produce small activity changes. The pocket is forgiving; QSAR and gradient-based design work well.
- **Activity cliffs** — small structural changes produce huge activity changes. ML models that interpolate fail; you need pocket awareness or explicit cliff-aware loss functions.
- **Flat SAR** — many structural changes leave activity unchanged. Often a sign that you are not actually hitting the proposed mode of action; check selectivity.

The Maggiora "molecular similarity principle" [Maggiora, 2006](https://doi.org/10.1021/ci060117s)[^maggiora] is the formal statement of (and warning about) SAR smoothness.

## Lead-optimisation chess

In a typical small-molecule campaign, chemists move along multiple property axes simultaneously:

| Axis | Goal | Typical lever |
| --- | --- | --- |
| Potency (IC50/EC50) | < 100 nM at target | Pocket fit, H-bonds, hydrophobic packing |
| Selectivity | > 100× vs anti-targets | Scaffold choice, vector replacement |
| Solubility | > 10 µM at physiological pH | Polar groups, salt forms, sp3 fraction |
| Permeability (PAMPA / Caco-2) | high | Reduce HBD, polar surface area |
| Metabolic stability (CLint) | low | Block CYP soft spots (–CF₃, ortho-substituents) |
| hERG | IC50 > 10 µM | Reduce basicity / lipophilicity / planarity |
| Plasma protein binding | moderate | Acid / log P trade-off |
| Synthetic accessibility | reasonable | Avoid 8+-step syntheses |

A "good lead" is rarely best on any single axis — it is the **least-bad multi-axis compromise**. This is why multi-parameter optimisation ([MPO](../molecular-design/mpo.md)) is the right computational framing.

## Reading a 2D structure quickly

A workable shortcut for a non-chemist:

1. Find the **scaffold** (the largest fused-ring system).
2. Identify each **substituent** by reading clockwise from the top-left.
3. Find **basic** centres (amines) and **acidic** centres (acids, tetrazoles) — they dominate pKa and distribution.
4. Find **stereo** indicators (wedges) — they dominate selectivity.
5. Scan for **PAINS-like motifs** (catechols, quinones, michael acceptors) and **toxicophores** (aniline, nitroaromatic, aldehyde).

If you cannot do this in 30 seconds, you cannot triage a hit list at human speed. With practice it is fast.

## In practice

- A **chemist's instinct is a high-value prior**. ML projects that ignore it tend to propose synthetically intractable or PAINS-laden molecules.
- **Reactive groups** (Michael acceptors, aldehydes, aryl halides ortho to nitro) are almost always disqualifying unless the program is specifically covalent.
- **PAINS filters** ([Baell & Holloway, 2010](https://doi.org/10.1021/jm901137j)[^pains]) catch the common nuisance hits; apply them automatically.
- **Synthetic accessibility scores** (SA score [Ertl & Schuffenhauer, 2009](https://doi.org/10.1186/1758-2946-1-8)[^sa]) are a sanity check, not a verdict — chemists overrule them constantly.

## References

[^bemis]: Bemis GW, Murcko MA. The properties of known drugs. 1. Molecular frameworks. *J Med Chem.* 1996;39(15):2887–2893. [doi:10.1021/jm9602928](https://doi.org/10.1021/jm9602928)
[^maggiora]: Maggiora GM. On outliers and activity cliffs — why QSAR often disappoints. *J Chem Inf Model.* 2006;46(4):1535. [doi:10.1021/ci060117s](https://doi.org/10.1021/ci060117s)
[^pains]: Baell JB, Holloway GA. New substructure filters for removal of pan assay interference compounds (PAINS). *J Med Chem.* 2010;53(7):2719–2740. [doi:10.1021/jm901137j](https://doi.org/10.1021/jm901137j)
[^sa]: Ertl P, Schuffenhauer A. Estimation of synthetic accessibility score of drug-like molecules. *J Cheminform.* 2009;1:8. [doi:10.1186/1758-2946-1-8](https://doi.org/10.1186/1758-2946-1-8)

## Where to next

[Pharmacology (PK / PD)](pharmacology.md) — what the body does to the drug, and the drug to the body.
