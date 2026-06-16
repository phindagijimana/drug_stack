# CLI commands

> The Unix utilities that turn a 50-line script into a one-liner.

You do not need to memorise every flag. You need to know which tool to reach for.

## `grep`

```bash
grep -F "CHEMBL25" library.csv             # fixed string
grep -E "^[CN]" smiles.txt                 # regex; lines starting with C or N
grep -c ">" sequences.fasta                # count matches (count > = sequence count)
grep -v "^#" file.txt                      # exclude comments
grep -i "kinase" annotations.tsv           # case-insensitive
```

## `awk`

The original tabular-processor.

```bash
awk -F, '{print $1, $5}' compounds.csv             # cols 1 and 5
awk -F, '$5 > 7' compounds.csv                     # rows with col 5 > 7
awk -F, 'NR>1 {sum+=$5; n++} END {print sum/n}' compounds.csv   # average col 5
awk 'NR%2==1' file.txt                             # odd-numbered lines
```

For most "ad hoc one-liner over a TSV" tasks, awk is faster than firing up pandas.

## `sed`

```bash
sed 's/old/new/g' file.txt                  # global replace
sed -i '' '/^#/d' file.txt                  # delete comment lines (BSD/mac)
sed -i '/^#/d' file.txt                     # delete comment lines (GNU)
sed -n '10,20p' file.txt                    # print lines 10–20
```

## `xargs` and `parallel`

```bash
# convert all .sdf files in cwd to SMILES in parallel (8 cores)
ls *.sdf | xargs -P 8 -I {} obabel {} -O {}.smi

# with GNU parallel
parallel -j 8 'obabel {} -O {}.smi' ::: *.sdf
```

`parallel` has a much friendlier syntax for non-trivial cases; `xargs` is ubiquitous.

## `jq`

```bash
jq '.compounds[] | select(.pIC50 > 7) | .chembl_id' results.json
jq -r 'keys[]' big.json                # raw output (no JSON quoting)
```

For nested JSON (every API output you will see), `jq` is mandatory.

## `tar` and friends

```bash
tar -czf archive.tar.gz dir/
tar -tzf archive.tar.gz                # list contents
tar -xzf archive.tar.gz -C dest/

# large files: use pigz for parallel gzip
tar -c dir/ | pigz > archive.tar.gz
```

## `find -exec` vs piping to `xargs`

```bash
# find all PDB files and gzip them
find . -name "*.pdb" -exec gzip {} \;        # one fork per file; slow on many files
find . -name "*.pdb" | xargs -P 4 gzip       # batches; much faster
```

For 10s of files, either works. For 10 000s, use `xargs -P` or `parallel`.

## `screen of the data`

Two commands that earn their keep on a Friday afternoon:

```bash
column -s, -t file.csv | less -S            # pretty CSV
csvtk pretty -d, file.csv | less -S          # if you have csvtk
```

## Where to next

[Data analysis](data-analysis.md) — pandas / Polars idioms specific to chemistry and assay data.
