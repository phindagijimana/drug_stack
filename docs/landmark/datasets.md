# Reference datasets

> The public resources every computational drug-discovery team uses. With access, licence, and gotcha notes.

## Chemistry

| Dataset | Size | What | Access |
| --- | --- | --- | --- |
| **ChEMBL** | ~2.4M compounds, ~22M bioactivities | curated literature bioactivity | free; quarterly releases |
| **PubChem** | ~110M compounds | aggregator, less curated | free |
| **BindingDB** | ~3M binding measurements | curated binding K, IC50, Ki | free |
| **ZINC22** | ~6 B make-on-demand | virtual + purchaseable | free |
| **Enamine REAL** | ~40 B virtual | synthesisable on demand | via Enamine licence |
| **DrugBank** | ~16k drug entries | drug-target-indication links | free for academic, paid for commercial |
| **ChEMBL-Drug Indications** | clinical-trial drug-disease links | useful for repurposing | free |
| **ChEBI** | ~58k entities | chemical entity ontology | free |

## Structure

| Dataset | What |
| --- | --- |
| **PDB** | experimentally-determined protein structures, ~220k entries |
| **AlphaFold DB** | predicted structures for ~250M sequences |
| **PDBBind** | curated protein-ligand binding affinities + structures |
| **PoseBusters** | clean test set for docking pose validation |
| **CrossDocked2020** | training set for pocket-aware ML |
| **Astex Diverse Set** | ~85 high-quality co-crystals for docking benchmark |

## Sequences

| Dataset | What |
| --- | --- |
| **UniProt** | curated protein sequences and annotations |
| **NCBI RefSeq** | reference sequences for genomes / transcripts |
| **Ensembl** | annotated genome browser data |
| **gnomAD** | genome-aggregation database; population variation |

## Bioactivity / omics

| Dataset | What |
| --- | --- |
| **LINCS L1000** | ~1.3M expression signatures across ~30k perturbagens |
| **DepMap** | genome-wide CRISPR essentiality across ~1k cell lines |
| **GTEx** | tissue-specific expression in healthy donors |
| **TCGA** | cancer-genome atlas, multi-omic |
| **HCA / Tabula Sapiens** | single-cell atlases of healthy human tissue |
| **UK Biobank** | population-scale phenotype + omics + imaging |
| **Open Targets** | aggregated target-disease evidence |

## Benchmarks

| Benchmark | Tasks |
| --- | --- |
| **MoleculeNet** | classification + regression on standard chemistry datasets |
| **Therapeutics Data Commons (TDC)** | 22+ ADMET + drug discovery tasks with proper splits |
| **OGB / OGB-LSC** | graph property prediction at scale |
| **LIT-PCBA** | unbiased virtual-screening benchmark |
| **MoleculeACE** | activity-cliff–rich benchmark |
| **PoseBusters benchmark** | physical-validity checks for docking |
| **Equibench, Boltz benchmark** | structure-prediction benchmarks |

## Gotchas

- **ChEMBL releases evolve.** A model trained on ChEMBL 33 will join differently than one trained on ChEMBL 34. Pin releases.
- **PubChem is messy.** No curation; expect malformed SMILES, duplicates, contradictory activities.
- **DUD-E inflates virtual-screening numbers** by physchem mismatch in decoys. Use LIT-PCBA where possible.
- **PDB redundancy.** Many structures are near-duplicates. Resolution-filter, deduplicate by sequence identity, leave clean test holdouts.
- **AlphaFold confidence varies.** Always check pLDDT in regions you use for docking.

## In practice

- Build your own **internal mirror / cache** of ChEMBL, PDB, BindingDB. Updated quarterly. Versioned.
- Use **InChIKey** as the join key across these resources.
- For benchmarking, **TDC + LIT-PCBA + PoseBusters** is the right modern triad.

## Where to next

[Major pipelines](pipelines.md) — software you stand on.
