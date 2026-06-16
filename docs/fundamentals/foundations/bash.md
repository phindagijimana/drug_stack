# Bash

> The shell you spend hours in even if you never admit it. The minimum competent baseline.

Most production drug-discovery work runs on a Linux cluster. The interactive surface is bash (or zsh; the differences are small for our purposes).

## Survival kit

```bash
# files & directories
ls -lh                  # human-readable sizes
ls -lhS                 # sort by size
du -sh *                # disk use of each thing in cwd
find . -name "*.sdf"    # find files
tree -L 2               # directory tree, depth 2

# inspect
head -n 5 file.csv
tail -n 5 file.csv
less +F log.txt         # follow log
wc -l file.csv          # row count
column -t -s, file.csv | less -S   # pretty-print a CSV

# transform
cut -d, -f1,3 file.csv
sort -u                 # dedupe
sort -k2,2 -t,          # sort by column 2
uniq -c | sort -rn      # frequency count

# process
ps aux | grep python
htop
kill -9 <pid>           # last resort

# network
scp file.parquet remote:~/data/
rsync -avh local/ remote:/path/    # repeatable copies, deltas only
```

## Scripting patterns

A workable cheminformatics shell script is rarely > 30 lines. Two patterns turn up everywhere.

**Set strict mode.**

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

`set -e` exits on error; `-u` errors on undefined variables; `-o pipefail` propagates failures through `|`; resetting `IFS` makes word-splitting predictable.

**Use a here-doc for embedded Python / SQL.**

```bash
python3 <<'PY'
from rdkit import Chem
import polars as pl

df = pl.read_parquet("library.parquet")
print(df.shape)
PY
```

## `&&`, `||`, `;`

- `A && B` — run B only if A succeeded.
- `A || B` — run B only if A failed (useful for fallbacks).
- `A ; B` — run B regardless (the rare correct case; usually you want `&&`).

`mkdir -p out && python3 run.py --out out/` is the right shape; `mkdir out ; python3 run.py` will fail silently if the directory already exists.

## Tmux / screen — non-optional

A long-running screen at 3 AM is the wrong place to lose your connection. Get used to one of:

```bash
tmux new -s screening
# detach: Ctrl-b d
tmux attach -t screening
```

A workflow that does not survive losing the SSH tunnel is not a real workflow.

## Where to next

[CLI commands](cli.md) — `grep`, `awk`, `xargs`, `jq` and the rest of the Unix toolbox.
