[← ← ←](../../../#full-usage)

# Complete Usage
The program has the following argument structure:
```
python3 main.py path/to/input
                [--moodle] [--learn [--file EXT [EXT ...]]   <-- at least one required
                [--output path/to/output/directory]
                [--debug] [--no_colour] [--quiet]
                [--add_nums | --remove_nums] 
```

For more information on the arguments:
- [`path/to/input`](#input-path)
- [`--moodle`, `--learn`, `--file`](#output-formats)
- [`--output`](#output-path)
- [`--debug`](#debug-mode)
- [`--no_colour`](#no-colour-mode)
- [`--quiet`](#quiet-mode)
- [`--add_nums`, `--remove_nums`](#addremove-nums)

## Input Path

|required|
|---|

The absolute or relative filepath to the input file or input directory. If a directory is provided, all top-level files in the directory are taken as input. Folders are ignored and not recursed through.

## Output Formats
|at least one requried|
|---|

The format of output created. `--moodle` or `--learn` will create a file which can be imported into the VLE, `--file EXT` will create a file of extension `EXT`. 

The following files can be created:  asciidoc, asciidoc_legacy, asciidoctor, beamer, biblatex, bibtex, chunkedhtml, commonmark, commonmark_x, context, csljson, djot, docbook, docbook4, docbook5, docx, dokuwiki, dzslides, epub, epub2, epub3, fb2, gfm, haddock, html, html4, html5, icml, ipynb, jats, jats_archiving, jats_articleauthoring, jats_publishing, jira, json, latex, man, markdown, markdown_github, markdown_mmd, markdown_phpextra, markdown_strict, markua, mediawiki, ms, muse, native, odt, opendocument, opml, org, pdf, plain, pptx, revealjs, rst, rtf, s5, slideous, slidy, tei, texinfo, textile, typst, xwiki, zimwiki.

## Output Path
|optional|
|---|

A path to a directory to write files to. Default is `/output`, can not be `/program`.
Files will be overwritten is necessary in provided directory.
If provided directory doesn't exist, a new one will be created.

## Debug Mode
|optional|
|---|

Shows debug output.
