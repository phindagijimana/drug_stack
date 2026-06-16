# Tutorial 3 — Docking walkthrough

> Receptor prep, library prep, dock 1000 compounds with AutoDock Vina, rescore the top 100, triage to the top 20.

**Prerequisites**: [Structural biology](../fundamentals/foundations/structural-biology.md), [Docking](../molecular-design/docking.md), [Hit triage](../screening/hit-triage.md).

## Pick a receptor

For a tutorial use a well-resolved co-crystal:

- **PDB 5C50**: Janus kinase 2 (JAK2) with a kinase inhibitor.
- Resolution 2.0 Å; clean pocket; representative ATP-competitive ligand.

```bash
wget https://files.rcsb.org/download/5C50.pdb
```

## Receptor prep

```bash
# install ADFR suite or use Meeko + open-source toolkit
pip install meeko

# strip waters, ions, ligand; protonate; build PDBQT
pdb4amber -i 5C50.pdb -o 5C50_clean.pdb --dry --reduce
mk_prepare_receptor.py -i 5C50_clean.pdb -o 5C50.pdbqt -p 7.4
```

Confirm reasonable protonation at His residues in the pocket. Visualise in PyMOL.

## Library prep

For the tutorial, use 1000 ChEMBL kinase-like compounds (or the output of [tutorial 1](similarity-search.md)).

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path

Path("ligands_pdbqt").mkdir(exist_ok=True)
with open("library.smi") as f:
    for i, line in enumerate(f):
        smi, cid = line.strip().split()
        mol = Chem.MolFromSmiles(smi)
        if mol is None: continue
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=0xf00d)
        AllChem.MMFFOptimizeMolecule(mol)
        Chem.MolToMolFile(mol, f"ligands_pdbqt/{cid}.mol")
        # use meeko's mk_prepare_ligand.py for PDBQT
```

(Use `mk_prepare_ligand.py` per file or batch via `parallel`.)

## Dock

```bash
# define box centred on the known ligand position
# (read center_x, _y, _z, size from the cocrystal ligand)
for L in ligands_pdbqt/*.pdbqt; do
    vina --receptor 5C50.pdbqt --ligand $L \
         --center_x 12.5 --center_y -3.4 --center_z 8.1 \
         --size_x 25 --size_y 25 --size_z 25 \
         --exhaustiveness 32 --num_modes 9 \
         --out docked/$(basename $L) --log docked/$(basename $L .pdbqt).log
done
```

For 1000 compounds at exhaustiveness 32, expect ~hours on a multi-core node; or use Vina-GPU.

## Rescore + triage

```python
import polars as pl
import re

scores = []
for log in Path("docked").glob("*.log"):
    text = log.read_text()
    m = re.search(r"   1\s+(\-?\d+\.\d+)", text)   # mode-1 score
    if m:
        scores.append({"cid": log.stem, "vina_score": float(m.group(1))})

df = pl.DataFrame(scores).sort("vina_score").head(100)
df.write_parquet("top100_vina.parquet")
```

Then rescore top 100 with gnina or MM-GB/SA, and triage with the [hit-triage checklist](../screening/hit-triage.md).

## Decision points called out

- **The grid box.** Centered on the cocrystal ligand; size 25 Å is generous.
- **Exhaustiveness 32**. Production-quality; halve for screens; double for case studies.
- **Use mode 1 only**. Lower modes are alternative poses; do not rank by them across compounds.
- **Always redock the known ligand** before any prospective claim. If your pipeline does not reproduce the 5C50 pose to within 2 Å RMSD, fix the prep.

## Where to next

[Target ID from RNA-seq](target-id.md) — back to the upstream end of the pipeline.
