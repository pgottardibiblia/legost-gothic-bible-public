The Gothic Bible: LegOst Digital Editions
===============

This is the distribution site for the TEI-encoded digital editions of the witnesses to the Gothic Bible produced within the PRIN 2022 project **LegOst – *The Textual Legacy of the Ostrogoths in Italy: The Gothic Bible and Other Texts*** (PI: Carla Falluomini). The editions are diplomatic-interpretative, and they are published online with [EVT 3](https://github.com/evt-project/evt-viewer-angular) on the bilingual (Italian/English) platform [Archivum Gothicum](https://archivumgothicum.eu).

The repository makes available, under open licences, everything needed to read, reuse, validate and republish the editions: the XML files, the encoding documentation, the conversion scripts and the customisations made to EVT 3.

**PLEASE NOTE:** the reference edition is the one published on [Archivum Gothicum](https://archivumgothicum.eu). The files here correspond to numbered releases of that edition. Users who need a stable text for citation should always refer to a release (see *How to cite*), not to the current state of the `main` branch. Facsimile images of the manuscripts are **not** distributed here: their rights belong to the holding institutions, and they can be consulted on the institutions' own websites.


1 - Introduction
--------------------

### 1.1 - About the project

The Gothic version of the Bible, traditionally attributed to Vulfila (4th century), survives in a small number of manuscripts. Almost all of them were produced in Ostrogothic Italy in the first half of the 6th century. LegOst sets out to re-examine this textual legacy directly on the manuscripts and to provide new digital editions of each witness. The editions record the layout of the page and the scribal phenomena (corrections, erasures, ligatures and abbreviations), alongside an interpretative reading of the text.

Each witness is edited as an autonomous edition. Its manuscript description is provided in both Italian and English.

### 1.2 - The witnesses

Volume 1 comprises the following witnesses:

| Siglum  | Manuscript | Contents |
|---------|------------|----------|
| `CArg`  | Codex Argenteus (Uppsala, Universitetsbibliotek, DG 1) and Speyer fragment | Matthew, John, Luke, Mark |
| `CCar`  | Codex Carolinus (Wolfenbüttel, Herzog August Bibliothek, Cod. Guelf. 64 Weiss.) | Romans (Gothic–Latin, in two columns) |
| `CGis`  | Codex Gissensis (formerly Gießen, Universitätsbibliothek; lost) | Luke (Gothic–Latin) |
| `CAmbC` | ms. Ambrosianus C (Milan, Biblioteca Ambrosiana, E 147 sup.) | Matthew (palimpsest) |
| `CAmbD` | ms. Ambrosianus D (Milan, Biblioteca Ambrosiana, G 82 sup.) | Nehemiah (palimpsest) |

Volume 2, in preparation, will cover the Ambrosiani A, B and E and the remaining witnesses.

### 1.3 - What this repository contains

- the **TEI XML editions**, one file per biblical book and per witness;
- a separate **manuscript description** (`sourceDesc`) for each witness, in Italian and in English;
- the **schema** used to validate the files;
- the **documentation** (`schema/README.md`) of the encoding conventions and of the character declarations (`charDecl`), which are mapped to [MUFI](https://mufi.info) and to the [Junicode](https://github.com/psb1558/Junicode-font) font;
- the **Python scripts** that convert the editors' Word documents into TEI XML;
- the **customisations to EVT 3** (JavaScript, CSS and configuration files) used for publication on Archivum Gothicum.

The EVT 3 application itself is not included. It is distributed by its developers on the [EVT release page](https://github.com/evt-project/evt-viewer-angular/releases).


2 - A short guide
--------------------

If you are interested in **reading or reusing the texts**, you need only the files in `data/`. These are standard TEI P5 documents and can be processed with any XML tool, such as XSLT, XQuery, Python with `lxml`, or oXygen.

If, on the other hand, you are interested in **republishing an edition** with EVT 3, or in adapting our customisations to an edition of your own, see sections 2.2 and 5.

If you find an error in the text or in the encoding, please open an [issue](../../issues). Proposed corrections are welcome as **pull requests**.

### 2.1 - Repository structure

    legost-gothic-bible-public/
    ├── data/
    │   ├── CArg/      CArg_Mt_TEI.xml, CArg_Gv_TEI.xml, CArg_Lc_TEI.xml, CArg_Mc_TEI.xml,
    │   │              CArg_TEI_SourceDesc_IT.xml, CArg_TEI_SourceDesc_EN.xml
    │   ├── CCar/      CCar_Rm_TEI.xml, CCar_TEI_SourceDesc_IT.xml, CCar_TEI_SourceDesc_EN.xml
    │   ├── CGis/      CGis_Lc_TEI.xml, …
    │   ├── CAmbC/     CAmbC_Mt_TEI.xml, …
    │   └── CAmbD/     CAmbD_Ne_TEI.xml, …
    ├── schema/        validation schema and encoding documentation (README.md)
    ├── scripts/       Word → TEI conversion, one file per function (MIT, see scripts/LICENSE)
    ├── evt/           (AGPL-3.0, see evt/LICENSE)
    │   ├── custom/    JavaScript modules
    │   ├── styles/    custom-styles-updated.css
    │   ├── config/    EVT configuration files, one set per siglum
    │   └── index.snippet.html
    ├── LICENSE        CC BY 4.0 (texts, encoding and documentation)
    └── README.md


Files are named according to the pattern `[Siglum]_[Book]_TEI.xml`. The book abbreviations follow Italian usage (`Mt`, `Mc`, `Lc`, `Gv`, `Rm`, `Ne`).

### 2.2 - Running an edition locally

1. Download the release package of EVT 3 from the [EVT release page](https://github.com/evt-project/evt-viewer-angular/releases) and unzip it.
2. Copy the following into the corresponding folders of the EVT package:
   - the XML files of the chosen witness, from `data/[Siglum]/` to `assets/data/text/`;
   - its configuration files, from `evt/config/[Siglum]/` to `assets/config/`;
   - the files in `evt/custom/` to `assets/custom/`;
   - `evt/styles/custom-styles-updated.css` to `assets/config/`.
3. Insert the contents of `evt/index.snippet.html` into `index.html`, immediately after `<app-root>`.
4. EVT has to be served over HTTP, so opening `index.html` directly from the file system will not work. From the root of the EVT package, run for example

        $ python -m http.server 8000

   and then open `http://localhost:8000/` in your browser.

Facsimile images are not included (see the note above). Without them the edition works in text-only mode.

### 2.3 - Configuration

Each edition has its own set of EVT configuration files (`edition_config`, `ui_config`, `file_config`, `editorial_conventions_config`). For the meaning of each option, see the [Configuration section](https://github.com/evt-project/evt-viewer-angular/wiki/Configuration) of the EVT Wiki.


3 - Encoding
--------------------

The editions follow the [TEI P5 Guidelines](https://tei-c.org/guidelines/p5/). The main conventions are listed below. A full account, with the correspondence between the editors' Word conventions and the TEI encoding, is given in [`schema/README.md`](schema/README.md).

* **Biblical structure**: `<div type="book">` and `<div type="chapter">`, with each verse encoded as `<ab type="verse">`.
* **Page and line**: `<pb>`, `<cb>` and `<lb>` record the layout of the manuscript. In the bilingual Codex Carolinus, `<cb n="1">` opens column a.
* **Facsimiles**: `<facsimile>` is a child of `<TEI>`. The text is linked to the images through `@facs` on `<pb>`.
* **Special characters**: they are declared in the `<charDecl>` of each file and mapped to MUFI codepoints (hexadecimal). Uncertain correspondences are flagged in the documentation.
* **Manuscript description**: it is kept in separate files (`[Siglum]_TEI_SourceDesc_IT.xml` / `_EN.xml`), which EVT loads as the edition's codicological apparatus.

### 3.1 - Validation

All files can be validated against the schema in `schema/`, for example with [Jing](https://relaxng.org/jclark/jing.html):

    $ java -jar jing.jar schema/[schema].rng data/CCar/CCar_Rm_TEI.xml

The files are also validated automatically at every push (see `.github/workflows/`).


4 - The conversion pipeline
--------------------

The editions are prepared by the editors as Word documents and converted into TEI XML by the scripts in `scripts/`. The output is then published with EVT 3:

    Word (.docx)  →  TEI XML (scripts/evolve_goth.py)  →  EVT 3

Each function of the pipeline is kept in its own file, named after the function (for example `evolve_goth.py`, `glyphanger.py`, `insert_notes.py`). The scripts import one another, so they should be run from within `scripts/`, or with that folder on the Python path.

### 4.1 - Requirements

- Python 3.10 or higher;
- the packages listed in `scripts/requirements.txt`, which you can install with

        $ pip install -r scripts/requirements.txt


5 - Customisations to EVT 3
--------------------

The publication on Archivum Gothicum extends EVT 3 without modifying its bundle. All customisations are JavaScript and CSS files, which are injected into `index.html` after `<app-root>` and loaded from `assets/custom/` and `assets/config/`. They can therefore be applied to any EVT 3 release package.

| File | Function |
|------|----------|
| `columns.js` | layout of two-column texts (Codex Carolinus) |
| `verse_navigator.js` | navigation by book, chapter and verse |
| `page_label_enhancer.js` | folio labels in the page navigation |
| `image_folder_selector.js` | switching between sets of images |
| `pdf_export.js` | export of the edition to PDF |
| `custom.js` | general adjustments to the interface |
| `custom-styles-updated.css` | styles for all of the above |

EVT 3 is an Angular application, so the scripts read its data by searching `__ngContext__`, and they react to navigation through a `MutationObserver` with debounce. EVT reuses DOM nodes when the user moves between pages, and the scripts are written to take this into account.


6 - Licence
--------------------

The repository contains material of different kinds, which is released under three licences:

| Content | Licence | Licence file |
|---------|---------|--------------|
| Texts, encoding and documentation (`data/`, `schema/`) | [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE`](LICENSE) |
| Customisations to EVT 3 (`evt/`) | [GNU Affero General Public License v3.0 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.html) | [`evt/LICENSE`](evt/LICENSE) |
| Conversion scripts (`scripts/`) | [MIT License](https://opensource.org/licenses/MIT) | [`scripts/LICENSE`](scripts/LICENSE) |

The editions may be freely reused, adapted and redistributed, also for commercial purposes, provided that the editors and the LegOst project are credited (see *How to cite*). The customisations to EVT 3 follow the licence of EVT 3 itself, which is released under AGPL-3.0. Anyone who modifies them and makes them available over a network must therefore also make the modified source code available.

EVT 3 and Junicode (SIL Open Font License) are distributed by their developers under their own licences. The images of the manuscripts are not covered by these licences, and their rights remain with the holding institutions.


7 - How to cite
--------------------

Each release of this repository is archived on Zenodo with its own DOI. Please cite the specific release you have used. GitHub's *Cite this repository* button, generated from `CITATION.cff`, provides the reference in several formats.

> Falluomini, Carla, and Pierandrea Gottardi (2026). *The Gothic Bible: LegOst Digital Editions* (Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

For the online edition, please cite [Archivum Gothicum](https://archivumgothicum.eu):

> Falluomini, Carla, and Pierandrea Gottardi (2026). *Archivum Gothicum: edizione delle fonti in lingua gotica*. Venice: Edizioni Ca' Foscari. https://doi.org/10.30687/979-12-5742-031-4


8 - Acknowledgements
--------------------

EVT edition of the Gothic Bible, PRIN project 2022 “The Textual Legacy of the Ostrogoths in Italy: The Bible Version and Other Texts”, funded by the European Union – NextGenerationEU, Mission 4, Component 1 – CUP J53D23013530006.

We are grateful to the institutions that hold the manuscripts for permission to consult and reproduce them. We also thank the developers of [EVT](http://evt.labcd.unipi.it/) and of [Junicode](https://github.com/psb1558/Junicode-font), on whose work the editions depend.


9 - Feedback
--------------------

Comments, corrections and suggestions are very much appreciated. Please use the [issue tracker](../../issues), or write to pgottardi.biblia@gmail.com.
