# LaTeX templates for PDF build

These templates are used by the `makeMarkdown latex` flow and can be referenced from `doc.latex.template_path` in info.yaml.

## Contents

- **short_tmplt.tex** – Standalone document wrapper. Placeholders: `__title__`, `__file__` (body `.tex` basename), `__version__`. Uses `\input{pandoc.tex}` and `\input{__file__}` for the body.
- **pandoc_3.4.tex**, **pandoc_3.6.tex** – Pandoc-generated LaTeX preamble (choose one to match your pandoc version; symlink or copy as `pandoc.tex` where you build).
- **IEEEtran.cls** – IEEE document class (included so output is consistent; no need to install from CTAN).
- **aic.bib** – Minimal placeholder bibliography (replace with your own or leave as-is if you don’t use citations).
- **authors.tex** – Optional author block (can be empty).

## Requirements

- A full TeX installation (pdflatex, bibtex, and common packages). IEEEtran.cls is included in this folder; when building, add this folder to TEXINPUTS so `\documentclass{IEEEtran}` finds it. For Unicode (e.g. Ω, μ) the template uses the newunicodechar package; if needed run: tlmgr install newunicodechar.

## Usage

1. Set `doc.latex.template_path` in info.yaml to the path to `short_tmplt.tex`, e.g.  
   `"${DOC_SCRIPT_PATH}/templates/short_tmplt.tex"` in CI or an absolute path locally.
2. When building, ensure `pandoc.tex` exists in the build directory (e.g. copy or symlink the matching `pandoc_3.x.tex` from this folder).
3. So that `\documentclass{IEEEtran}` finds **IEEEtran.cls**, either copy this folder’s contents into the build directory or set **TEXINPUTS** to include this folder (e.g. `TEXINPUTS=".:path/to/templates:" pdflatex ...`).
4. Copy `aic.bib` and `authors.tex` into the build directory if your template uses them.
