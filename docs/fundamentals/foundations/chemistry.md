# Chemistry

> Organic, physical, and analytical chemistry priors. Enough chemistry to talk to a synthetic chemist credibly.

## Atoms, bonds, and hybridisation

- **Covalent bonds** — sharing of electron pairs. Bond strengths: C–H ~99 kcal/mol, C–C ~83, C–N ~70, C=C ~146, C≡C ~200, C=O ~178. Determines stability and ease of cleavage.
- **Hybridisation** — sp³ (tetrahedral), sp² (trigonal planar), sp (linear). sp³ fraction (Fsp³) is a well-loved drug-likeness indicator [Lovering et al., 2009](https://doi.org/10.1021/jm901241e)[^fsp3] — more sp³ → more 3D → often better selectivity.
- **Aromaticity** — Hückel's 4n+2 π-electrons in a planar ring. Aromatic rings are stable, planar, and π-stack with protein aromatic residues.

## Functional groups, conceptually

Every functional group has a characteristic:

- **Geometry** (planar carbonyl, tetrahedral sp³ centre, trigonal sp² amine).
- **Electronics** (electron-withdrawing or -donating, dipole, polarisability).
- **Reactivity** (nucleophile, electrophile, hydrogen-bond donor / acceptor, redox).
- **pKa** (acidity / basicity, protonation state in vivo).
- **Metabolic fate** (CYP soft spot, glucuronidation site, glutathione conjugate).

Train yourself to read each substituent through all five lenses. A medicinal chemist does this automatically.

## pKa and protonation state

Drugs live at pH 7.4 in plasma. At that pH, the protonation state of an ionisable group depends on its pKa:

\[
\text{fraction protonated} = \frac{1}{1 + 10^{\text{pH} - \text{pKa}}}
\]

So a primary amine of pKa 10 is > 99% protonated at pH 7.4; a carboxylic acid of pKa 4 is > 99% deprotonated. The neutral and ionised forms differ enormously in permeability, partition, and binding mode. **Always reason about the species that exists in solution, not the cartoon you drew on paper.**

## LogP, logD, polarity

- **LogP** — partition between octanol and water, neutral species.
- **LogD** — same but accounting for ionisation at a given pH; logD_7.4 is the usual one.
- **PSA / TPSA** — polar surface area; the count of polar (N, O, optionally S) atoms accessible. < 90 Å² for CNS, < 140 Å² for oral.
- **Polarisability** — second-order response to electric field; matters for halogen bonds and dispersion interactions.

## Stereochemistry

- **R / S** — Cahn-Ingold-Prelog absolute stereodescriptors.
- **E / Z** — double-bond geometry.
- **Diastereomers** (different physical properties), **enantiomers** (mirror images, same physical properties except optical activity), **atropisomers** (rotational isomers locked by steric clash).
- Most drug targets are chiral; one enantiomer is usually 10–1000× more active. *Thalidomide is the classical "wrong enantiomer can kill you"* cautionary tale.

## Thermodynamics

- **Free energy** \(\Delta G = \Delta H - T \Delta S\).
- **Binding equilibrium** — \(\Delta G = -RT \ln K\). Binding affinity in kcal/mol vs. K_d: each 1 kcal/mol ≈ 10× change in K.
- **Enthalpy / entropy split** — a binder with favourable ΔH (H-bonds, electrostatics) and slight ΔS penalty is "good"; pure ΔS-driven binding (hydrophobic) often gives weaker selectivity.

## Analytical chemistry as data

You will see assay outputs from:

- **NMR** — connectivity, conformation, dynamics. The most decisive structural characterisation.
- **Mass spectrometry** — molecular weight and fragmentation; the workhorse of proteomics and metabolomics.
- **HPLC / UPLC** — separation; gives purity and (with detection) quantification.
- **X-ray crystallography** — the original ground truth for protein-ligand structure.
- **Cryo-EM** — increasingly the dominant structural tool for large complexes.
- **SPR / ITC / BLI** — kinetic and thermodynamic binding parameters.
- **NMR fragment screening** — primary fragment-based hit ID.

You do not need to run these instruments — you need to know what *output* each one gives and roughly how trustworthy it is.

## In practice

- Reasoning about chemistry without thinking about protonation state, stereochemistry, and hybridisation is reasoning about cartoons.
- Free-energy intuitions (1 kcal/mol ≈ ~10×) are the unit of medicinal-chemistry intuition.
- An ML scientist who can read NMR, HPLC, and an X-ray-electron-density map even superficially has a massive collaboration advantage.

## References

[^fsp3]: Lovering F, Bikker J, Humblet C. Escape from flatland: increasing saturation as an approach to improving clinical success. *J Med Chem.* 2009;52(21):6752–6756. [doi:10.1021/jm901241e](https://doi.org/10.1021/jm901241e)

## Where to next

[Cheminformatics](cheminformatics.md) — the RDKit / fingerprint / descriptor working layer.
