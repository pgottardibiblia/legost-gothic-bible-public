Encoding Scheme
===============

This document describes how the LegOst editions of the Gothic Bible are encoded in TEI XML. For each phenomenon recorded in the manuscripts, it gives two things:

- the **Word convention** used by the editors in their transcriptions;
- the **TEI encoding** into which that convention is converted by `scripts/Gothic_scripts.py`.

The examples are taken from the published files, mainly `CArg_Mt_TEI.xml` and `CCar_Rm_TEI.xml`. The validation schema is in this folder.


1 - Document structure
--------------------

Each file contains a single biblical book of a single witness. The hierarchy is the following:

    <TEI>
    ├── <teiHeader>                         bibliographic and encoding metadata
    ├── <facsimile>                         one <surface>/<graphic> per page
    └── <text>/<body>
        └── <div type="book" ana="#Matthew">
            └── <div type="chapter" n="5">
                └── <ab type="verse" n="15">
                    ├── <pb/>, <cb/>, <lb/>       page, column, line
                    ├── <fw>                     running titles, canon tables
                    ├── <w>, <pc>, <num>         words, punctuation, numerals
                    └── <add>, <del>, <choice>, <unclear>, <gap>, <supplied>, <note>, …

The manuscript description is kept in separate files (`[Siglum]_TEI_SourceDesc_IT.xml` and `_EN.xml`).

### 1.1 - Identifiers

Every significant element carries an `xml:id` of the form `[Siglum]_[element]_[folio]_[line]_[position]`, for example:

| Element | Example |
|---------|---------|
| page | `CArg_pb_1_1r` |
| line | `CArg_lb_1r_1` |
| word | `CArg_w_1r_1_3` (folio 1r, line 1, third token) |
| punctuation | `CArg_comma_1r_1_4` |
| verse | `CArg_Mt_5_verse_15` |
| chapter | `CArg_Mt_chapter_5` |
| book | `CArg_book_Mt` |

In the two-column Codex Carolinus, the folio part also includes the column (`277ra`, `277rb`).


2 - Structure and layout
--------------------

| Phenomenon | Word convention | TEI encoding |
|------------|-----------------|--------------|
| Biblical book | `{lib.X}`, where X is the abbreviation of the book | `<div type="book" ana="#Matthew">` |
| Chapter and verse | `[c.:X;v.:Y]`, where X is the chapter and Y the verse | `<div type="chapter" n="X">` and `<ab type="verse" n="Y">` |
| Folio | `{f.XY}` before the text of the leaf, where X is the folio number and Y is `r` or `v` | `<pb n="1r" facs="#CArg_facs_1_1r"/>` |
| Column (CCar) | — | `<cb n="1"/>` for column a, `<cb n="2"/>` for column b |
| New line | line break | `<lb n="[progressive number]"/>` |
| Blank space (CCar) | — | `<space dim="horizontal"/>` |
| Quire signature | `[fasc.:p.Y;X]`, where Y is the position and X the text | `<gb n="3"/>` and `<add type="quire" place="bottom_left" rend="silver_ink" value="3">·g·</add>` |

The link between the text and the images is made through `@facs` on `<pb>`. This attribute points to a `<surface>` in `<facsimile>`, which is a child of `<TEI>`:

```xml
<facsimile xml:id="CCar_facs_Rm">
   <surface xml:id="CCar_facs_1_277r">
      <graphic url="CCar_fol._1_277r.jpeg" height="1800px" width="1200px"/>
   </surface>
   …
</facsimile>
```


3 - Words, punctuation and numerals
--------------------

| Phenomenon | Word convention | TEI encoding |
|------------|-----------------|--------------|
| Word | — | `<w rend="silver_ink" xml:lang="got">` |
| Word divided across lines | hyphen at the end of the first part | the two parts are linked through `<seg corresp="…">` (see below) |
| Occasional compound | tilde `~` joining the members | `<w>` containing one `<seg type="composite-word" n="…">` per member |
| Punctuation | five types: colon `[:]`, comma `[,]`, diple `[>]`, small diple `[˒]`, arrow `[→]` | `<pc type="colon\|comma\|full_diple\|quick_diple" rend="…">` |
| Numeral | `[num.:X]`, where X is the numeral in letters | `<num value="[Arabic numeral]">` |

**Words divided across lines.** Each part is encoded at its own position in the line. `@corresp` points to the other part, and `<seg type="corresp-text">` holds the complementary letters, so that the full form can be searched and displayed:

```xml
<w rend="silver_ink" xml:lang="got" xml:id="CArg_w_1r_1_6">
   <seg corresp="CArg_seg_2_1r_2_1" xml:id="CArg_seg_1_1r_1_6">liu<seg type="corresp-text">teiþ</seg></seg>
</w>
```

**Occasional compounds.**

```xml
<w xml:id="CArg_w_3r_5_3">
   <seg type="composite-word" n="1" rend="silver_ink">sijaiþ</seg><seg type="composite-word" n="2" rend="silver_ink">þan</seg>
</w>
```


4 - Script and ink
--------------------

| Phenomenon | Word convention | TEI encoding |
|------------|-----------------|--------------|
| Silver ink | `{s.i.}` before the portion of text | `@rend="silver_ink"` |
| Gold ink | `{g.i.}` before the portion of text | `@rend="gold_ink"` |
| Black ink | — | `@rend="black_ink"` |
| Enlarged or capital letters | capital letter in the text | capital letter |
| Letters of smaller module | comment → `[small:]` | `<hi rend="small">ei</hi>` |
| Abbreviation | round brackets `()`, used only for nasal *tituli* at the end of the line and for a few standard abbreviations | `<choice>` with `<abbr>`/`<am>` and `<expan>`/`<ex>` (see below) |
| Ligature | comment, with round brackets `()` enclosing the second element → `[leg.:]` | glyph declared in `<charDecl>` (see section 7) |

`@rend` for the ink is given on `<w>`, `<pc>`, `<num>`, `<fw>`, `<label>` and `<add>`.

**Abbreviations.**

```xml
<choice><abbr>himin<am><g ref="#amacr"/></am></abbr><expan>himina<ex>m</ex></expan></choice>
```


5 - Scribal interventions and condition of the leaf
--------------------

| Phenomenon | Word convention | TEI encoding |
|------------|-----------------|--------------|
| Interlinear addition, or addition at the end of the line | comment, with round brackets `()` enclosing the addition → `[add.:p.Y;X]` | `<add place="above\|below">` |
| Marginal addition | comment → `[marg.:p.Y;X]`, where Y is the position and X the text | `<w type="add_or_gloss"><add place="margin_right">…</add></w>` |
| Erasure | `[r.:X]`, where X is the erased text | `<del rend="erasure">X</del>` |
| Correction | `[corr.:X;Y]`, where X is the erased or expunged text and Y the correction | `<subst><del rend="erasure">X</del><add rend="overwritten">Y</add></subst>` |
| Damaged, barely legible text | underlined text, enclosed in `[un.:c.:r;X]`, where X is the text and r the cause of the damage | `<unclear reason="damage">` |
| Lacuna caused by damage to the leaf | obelus in square brackets, `[†;e.:X]`, where X is the conjectured text | `<gap unit="char" extent="n"/>`, followed by `<supplied resp="…">X</supplied>` |

**Corrections.**

```xml
<subst><del rend="erasure">a</del><add rend="overwritten">o</add></subst>
```

**Lacunae.** `<gap>` records the extent of the loss in characters. The conjecture goes in `<supplied>`, and `@resp` names the editors who proposed it:

```xml
<w rend="silver_ink" xml:lang="got">fa<gap unit="char" extent="2"/><supplied resp="Uppström,Streitberg">ir</supplied>njana</w>
```


6 - Editorial interventions and paratext
--------------------

| Phenomenon | Word convention | TEI encoding |
|------------|-----------------|--------------|
| Emendation (only metathesis, dittography and haplography) | `[emend.:c:X;e:Y]`, where X is the text of the manuscript and Y the emended text | `<choice><sic>X</sic><corr resp="…">Y</corr></choice>` |
| Comment | `[comm.:X]`, where X is the text of the comment | `<note type="comment" target="#[xml:id]" resp="…">` |
| Old Testament reference | `[AT]…[fAT]` | `<ref type="Old_Testament_reference" corresp="Es20,13_Dt5,17"/>` |
| Running title | first line, separated from the following text by a blank line | `<fw type="header" place="top_center" rend="silver_ink">·þairh·</fw>` |
| Eusebian / Ammonian section | `[sez. amm.:pl.:Y;X]`, where X is the section number and Y its position | `<label type="eusebian_section" ana="Mt" place="margin_left">` containing `<num>` |
| Eusebian canons | last line, separated from the preceding text by a blank line | `<fw type="footer">` containing `<table type="eusebian_canons">` (see below) |

**Emendations.** `@resp` on `<corr>` names the editors who proposed the emendation. An empty `<sic/>` encodes an addition by the editor, and an empty `<corr/>` encodes a deletion:

```xml
<choice><sic>uste</sic><corr resp="Streitberg,Snædal">unte</corr></choice>
```

**Eusebian sections and canons.** The section number is given in Gothic letters, with `@value` holding the Arabic numeral. The canon tables at the foot of the page are encoded with `<table>/<row>`: the first row names the Gospels, and the following rows give the corresponding section numbers.

```xml
<label type="eusebian_section" ana="Mt" place="margin_left" rend="silver_ink">
   <num value="33">·lg·</num>
</label>

<fw type="footer" place="bottom_center">
   <table type="eusebian_canons">
      <row n="1">
         <w ana="Mt" rend="gold_ink">m(a)þ(þaius)</w>
         <w ana="Gv" rend="gold_ink">ïoh(annes)</w>
         …
      </row>
      <row n="2">
         <num rend="silver_ink" value="33"><w>lg</w></num>
         …
      </row>
   </table>
</fw>
```


7 - Special characters
--------------------

Characters with no standard Unicode codepoint (letters with *titulus*, abbreviation marks, ligatures) are declared in the `<charDecl>` of each file. The text refers to them with `<g ref="#…">`. Each declaration gives:

- a name (`<localProp name="Name">`);
- the codepoint or sequence of codepoints, in hexadecimal, according to [MUFI](https://mufi.info) and the [Junicode](https://github.com/psb1558/Junicode-font) font (`<mapping type="codepoint">`);
- the diplomatic form (`<mapping type="diplomatic">`);
- the normalised form (`<mapping type="normalized">`).

In `<charDecl>` the `xml:id` is written without `#`, which is used only in the references.

```xml
<glyph xml:id="þairhtachi">
   <localProp name="Name" value="TACHIGRAPHIC ÞAIRH"/>
   <mapping type="codepoint" subtype="composite">0000FE+000101+000069+000072+000304+000068</mapping>
   <mapping type="diplomatic">þāir̄h</mapping>
   <mapping type="normalized">þairh</mapping>
</glyph>
```


8 - Values of the main attributes
--------------------

| Attribute | Element | Values |
|-----------|---------|--------|
| `@rend` | `w`, `pc`, `num`, `fw`, `label`, `add` | `silver_ink`, `gold_ink`, `black_ink` |
| `@rend` | `del` | `erasure` |
| `@rend` | `add` | `overwritten` |
| `@rend` | `hi` | `small`, `italic` (only within `<note>`) |
| `@type` | `pc` | `colon`, `comma`, `full_diple`, `quick_diple` |
| `@type` | `fw` | `header`, `footer` |
| `@type` | `seg` | `corresp-text`, `composite-word` |
| `@type` | `w` | `add_or_gloss` |
| `@type` | `add` | `quire` |
| `@place` | `add`, `pc`, `label`, `fw` | `above`, `below`, `margin_left`, `margin_right`, `top_center`, `bottom_center`, `bottom_left` |
| `@reason` | `unclear` | `damage` |
| `@unit` | `gap` | `char` |
