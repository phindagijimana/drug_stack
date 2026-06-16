# 4. Your first figure

> A 4×5 grid of the top 20 hits, with similarity values as captions. Suitable for a slide, a paper supplement, or an internal triage email.

## Render an aligned grid

```python
from rdkit import Chem
from rdkit.Chem import Draw, AllChem

# top20 from the previous page
mols  = [Chem.MolFromSmiles(smi) for _, smi, _ in top20]
legends = [f"{cid}\nT={s:.2f}" for cid, _, s in top20]

# common scaffold for alignment (here: 2-amino-pyrimidine, present in imatinib)
core = Chem.MolFromSmiles("Nc1nccc(-c2cccnc2)n1")
for m in mols:
    AllChem.Compute2DCoords(m)
    if m.HasSubstructMatch(core):
        AllChem.GenerateDepictionMatching2DStructure(m, core)

img = Draw.MolsToGridImage(
    mols,
    legends=legends,
    molsPerRow=4,
    subImgSize=(300, 250),
    useSVG=False,
)
img.save("hits_grid.png")
```

Three details that make this look professional:

- **Aligned 2D coordinates.** Without `GenerateDepictionMatching2DStructure`, similar molecules are drawn in random rotations and the reader cannot scan-compare scaffolds.
- **Stable captions.** Always include the ID *and* the similarity (or activity, or whatever you ranked on). A grid without numbers is decoration, not data.
- **Reasonable size.** 300×250 per cell is sharp at 4×5; anything smaller becomes unreadable in slide projection.

## Interactive variant

For exploration in a Jupyter notebook, `mols2grid` gives a searchable, filterable HTML widget:

```python
import mols2grid

mols2grid.display(
    [{"smiles": smi, "id": cid, "sim": s} for cid, smi, s in top20],
    subset=["id", "img", "sim"],
    tooltip=["smiles"],
)
```

Use the widget while triaging; export the static PNG for the deck.

## Captioning rules

For external audiences, a molecule grid is incomplete without:

- The **query** (drawn somewhere) — otherwise "Top 20 by similarity to X" has no X.
- The **library**, version, and date.
- The **similarity metric**, fingerprint, and parameters (e.g. "Tanimoto on ECFP4, radius 2, 2048 bits").
- A note on whether stereo was considered (usually not, for ECFP4).
- The **filters** applied before ranking, if any.

A figure caption that just says "Top hits" is not a figure caption; it is a placeholder.

## Where to next

You now have an environment, you can read and compare molecules, and you can run and render a basic screen.

- If you came in as a **researcher**, go to [Fundamentals](../fundamentals/index.md) and follow [Path A](../paths/index.md#path-a--brand-new-researcher-eg-first-year-graduate-student).
- If you came in as a **software / data engineer**, go to [Fundamentals → Drug-discovery pipeline](../fundamentals/pipeline.md) and follow [Path B](../paths/index.md#path-b--software--data-engineer-pivoting-in).
- If you came in as a **medicinal chemist**, go to [Molecular design](../molecular-design/index.md) and follow [Path C](../paths/index.md#path-c--medicinal-chemist-learning-the-computational-side).
- If you came in as an **ML engineer**, go to [AI / ML](../ai/index.md) and follow [Path D](../paths/index.md#path-d--ml-engineer-building-drug-ai-products).
- If you came in as a **senior research engineer**, [Path E](../paths/index.md#path-e--senior-research-engineer--tech-lead).
