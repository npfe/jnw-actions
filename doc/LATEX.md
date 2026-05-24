# LaTeX / standalone PDF generation

The `makeMarkdown` script can generate **pandoc** commands and **standalone .tex** files using the same pipeline as the aic2026 lecture PDFs.

## Combined markdown (README + all docs)

The default `makeMarkdown` run also writes **`docs/combined.md`**, which merges in order: Overview (index/README), Install, Schematics (with SVGs), Simulations, Layout. Jekyll frontmatter is stripped. To get a LaTeX-friendly version with SVGs converted to PDF, run:

```bash
cd work && python3 makeMarkdown combined-latex --info ../info.yaml
```

This produces **`docs/assets/combined_latex.md`** and **`docs/assets/media_pdf/*.pdf`** using rsvg-convert, inkscape, or ImageMagick. Add `combined_latex` to `doc.latex.sources` to build a single PDF from the combined docs.

## Template

The LaTeX wrapper template is shipped in **jnw-actions** (and was originally from aic2026):

- **`jnw-actions/doc/templates/short_tmplt.tex`** (and `pandoc_3.4.tex`, `pandoc_3.6.tex`, `aic.bib`, `authors.tex`)
- Or **`aic2026/pdf/short_tmplt.tex`** if you use that repo

Placeholders in the template:

- `__title__` – document title (e.g. "The Story of Jayn")
- `__file__` – basename of the body file (e.g. `the_story_of_jayn_fiximg`), which is `\input{__file__}` in the template
- `__version__` – version string (e.g. from `pdf/version_short.tex`)

The full pipeline in aic2026 is:

1. **Markdown** → `py/lecture.py latex` → `pdf/<name>.md` (filtered) and `pdf/<name>.tex` (from template)
2. **Pandoc**: `pandoc --citeproc --bibliography=pdf/aic.bib --csl=pdf/ieee-with-url.csl -o pdf/<name>.latex pdf/<name>.md`
3. **Fix images**: `pdf/fix_svg.py` on each `.latex` → `*_fiximg.tex`
4. **Build**: `pdflatex pdf/<name>.tex` (which `\input`s `pandoc.tex` and `*_fiximg.tex`)

## Using makeMarkdown for LaTeX

Add a `doc.latex` section to your **info.yaml**:

```yaml
doc:
  latex:
    template_path: "/path/to/short_tmplt.tex"   # e.g. ${DOC_SCRIPT_PATH}/templates/short_tmplt.tex in CI
    output_dir: pdf
    sources:
      - l00_jayn
      - lectures/l01_intro.md
    # optional:
    bibliography: pdf/aic.bib
    csl: pdf/ieee-with-url.csl
    version_tex: pdf/version_short.tex
    titles:
      l00_jayn: "The Story of Jayn"
```

Then:

- **Print pandoc commands and hints** (no writes):
  ```bash
  python3 makeMarkdown latex --info ../info.yaml --makefile
  ```

- **Run pandoc and write the full .tex** from the template:
  ```bash
  python3 makeMarkdown latex --info ../info.yaml --run
  ```

Output: for each entry in `sources`, the script generates `output_dir/<basename>.latex` (if `--run`) and `output_dir/<basename>.tex` (filled template). You still need to run the **fix_svg** step (e.g. aic2026’s `pdf/fix_svg.py`) on each `.latex` to produce `*_fiximg.tex` before building the PDF.

## Summary

| What you want | Command / location |
|---------------|---------------------|
| Combined markdown (README + docs) | Auto: `docs/combined.md` |
| SVGs → PDF for LaTeX | `makeMarkdown combined-latex` → `docs/assets/combined_latex.md` + `docs/assets/media_pdf/*.pdf` |
| Template file | `jnw-actions/doc/templates/short_tmplt.tex` (or aic2026/pdf/short_tmplt.tex) |
| Pandoc command | `makeMarkdown latex --makefile` or above pipeline |
| Full .tex (wrapper) | `makeMarkdown latex --run` (with `doc.latex` in info.yaml) |
| Image-fix step | aic2026 `pdf/fix_svg.py` (run in `pdf/` on each `.latex`) |
| Build PDF | `cd pdf && pdflatex <name>.tex` |
