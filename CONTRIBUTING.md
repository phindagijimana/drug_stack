# Contributing to DrugStack

Thanks for being interested. **DrugStack** grows by accretion — small additions, corrections, and worked examples are exactly what makes it useful.

## Quick start

```bash
make install        # creates .venv and installs dev + docs extras
make test           # run the test suite
make serve          # preview the docs locally
```

## What good contributions look like

- **Pages stay focused.** A page does one thing. If it grows past ~800 lines it probably wants to split.
- **Concepts are anchored in something concrete.** When you introduce a term, give an example from a real workflow — a target, a series, an assay, a dataset name. Generic prose without examples is the failure mode.
- **Code that appears in the docs lives in the repo.** If you show a snippet meant to be runnable, it should be importable from `drug_handbook/` (or under a future `examples/`) and exercised in tests.
- **Stubs are fine.** A page with a clean scope statement and links to good external references is better than an empty file. Just keep an `!!! info "In development"` admonition until the page is done.
- **Match the depth tiering.** Pages range from beginner on-ramp to PhD/senior-engineer depth. Add an admonition tag if you're contributing material that sits at a particular tier (`!!! note "Beginner"`, `!!! info "PhD-level depth"`, `!!! tip "Senior research engineer"`).

## Style

- Markdown is rendered with **MkDocs Material**. Use admonitions (`!!! note`, `!!! tip`, `!!! warning`) liberally.
- Headings: `H1` is the page title; sub-sections use `H2` and below.
- Code blocks use language fences (` ```python `, ` ```bash `, ` ```sql `, etc.).
- Tables for any landscape comparison; bullet lists for short enumerations.
- References use footnotes with DOIs. Unsupported claims should be flagged or removed.
- Diagrams: Mermaid where appropriate; a one-line italic caption underneath.
- End each substantive chapter with an "In practice" section — the actionable summary.

## Tests

- Anything in `src/drug_handbook/` needs at least one happy-path test in `tests/`.
- For documentation-only contributions, `mkdocs build --strict` running clean in CI is the test.

## Filing issues

Use GitHub Issues. Helpful issue contents:

- Page link or section heading you're asking about.
- What's confusing, missing, or wrong.
- A suggestion (even a rough one) if you have it.

## Scope

DrugStack covers small-molecule and (where overlap helps) biologic drug discovery and development. Cell and gene therapy are mentioned but not exhaustively covered. CNS-specific topics are touched briefly here and deeply in the sibling project [NeuroStack](https://github.com/phindagijimana/neuro_stack); cross-link where you can.
