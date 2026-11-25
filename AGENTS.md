# Working on Raza

Raza is a life and damage tracker for Commander (Magic: the Gathering),
written in 'rain, for a Windows tablet (a Surface) lying in the middle of
the table: each player has a part of the screen facing them, and deals
damage by dragging from their attack icons into another player's part.
This file is for agents (and people) picking it up; read it, then
[DESIGN.md](DESIGN.md).

- [DESIGN.md](DESIGN.md) is what each thing is meant to look like and do:
  check a change against it, and bring it up to date in the same change
  (a section that no longer matches the code is a bug).
- [TODO.md](TODO.md) is what's wanted next.
- The language: `C:\rain\AGENTS.md` (how 'rain is written, its tools and
  modules) and `C:\rain\STYLE.md` (how code is written there and here).
  Raza runs on the compiler in `C:\rain\bin\rain.exe`; when Raza needs
  something rain or a module lacks, it's added to C:\rain, not worked round
  here.

## Building, testing, looking

Run from the repository's folder (through buckram's `run` with the
compiler's path: Bash and PowerShell aren't used here).

```
rain src/raza.rain                 a dev build: build/Raza.exe (not tracked)
rain -release src/raza.rain        the tablet's: release/Raza.exe (tracked), optimized through LLVM
rain -test:src/raza.rain           the tests (raza.tests.rain, and the #tests beside the code)
rain -check:all src/raza.rain      every configuration checked (Windows only: see the declaration)
build/Raza.exe -snapshot:folder    about 30 PNGs of known states (DESIGN.md's "Checking it" lists them)
rain -profile src/raza.rain -quit_after:25    a profile, the window open 25 s (drag or play meanwhile)
build/Raza.exe -quit_after:8 -busy           a busy table, its frames' work printed
```

- Close a running Raza before building: the build can't overwrite an
  open exe. buckram's `raza` task starts release\Raza.exe.
- Look at what you change: build, snapshot, and read the PNGs (landscape
  and portrait, more than one player count). The tests check placement
  and arithmetic, not looks.
- The release exe is tracked so it's on GitHub for the tablet: rebuild it
  before committing a change meant for the tablet, and commit it with the
  change, not apart from it. Its `notices/` (FreeType's and Material
  Design Icons' licences, which a release carries) aren't tracked.
- After naming a new icon (`icon(Mdi.NAME)`), run `rain -run
  C:/rain/tools/icons/icons.rain update C:/repos/raza/src/raza.rain`,
  which writes `src/icons/` (generated: never edit it).

## The code

| File | What's in it |
|---|---|
| `src/raza.rain` | The program: its declaration, `main` and its input loop, the controls (the pill, settings, count runner's input), the life drum, the drag, the number grid and the confirm buttons, the colour toggles and options, chips, poison and tax, the fonts, the snapshots |
| `src/game.rain` | The rules: `Game` (life, commander damage, poison, tax, colours, attacks), `Attack` and `deal_attack`, how far a drag goes for how much |
| `src/layout.rain` | The screen cut into parts (`Splits`, `lay_out`, each `Seat`'s outline, middle, angle, attack spot) |
| `src/frames.rain` | Each part's surface (the `part_shade` shader: each colour's material, two colours' halves, three or more colours' gold lit by a strip of each round its edge), and the surfaces kept between frames |
| `src/materials.rain` | The textures (decoded on threads at start), the material atlas's tiles |
| `src/elements.rain`, `src/motes.rain` | A volley: how it's drawn (each colour's dots, the loss tokens), its path and timing |
| `src/count-table.rain` | The table splitting open for the count runner and for the settings, and the canvases drawn apart for it |
| `src/target-arrow.rain` | The drag's arrow (a shader) |
| `src/raza.tests.rain` | The tests |

## What must stay true

- **Saved state.** The game, each count's lines (landscape and portrait
  apart), the motion, brightness and orientation are kept between runs by
  rain's `Defaults` (the registry, HKCU\Software\Raza), as raw bytes:
  `"game"` (the whole `Game`), `"splits.N"` and `"splits.N.portrait"`,
  `"motion"`, `"brightness"`, `"orientation"`. A change to `Game`'s fields
  changes what's read back: add a migration from the old layout, as
  `from_bytes` reads a game whose attacks were a byte.
- **Attack values.** A player's attacks are a bit for each `Attack` value
  (`Attacks`, a u16), saved: a new kind goes at the end of `Attack`, never
  between, or every saved game's attacks change meaning. `OPTION_KINDS`
  and `OPTION_SLOTS` say where each shows in the options panel.
- **Every player count, both ways round.** 2 to 6 players, landscape and
  portrait (the settings' orientation button: auto, kept landscape, kept
  portrait). The tests run each; a layout change that works for four in
  landscape often doesn't for six in portrait.
- **Touch, several at once.** Each finger is followed by its id, and
  several players act at once; the count column and the settings are the
  table's alone. Undo and redo wait while anything's under way
  (`under_way`).
- **Speed.** The tablet's GPU is Intel's. A divider's drag and a busy
  table should stay at the display's rate; DESIGN.md's "Speed" says what's
  kept between frames and why (a new life size or glyph is costly, a
  part's surface shader most of all). Profile a change that touches
  drawing.
- Files use LF line endings only.

## Others working here

Another agent (Codex) works on Raza too, sometimes on the same files at
the same time (lately the parts' surfaces in `frames.rain`). Read a file
again before editing it; if the build breaks in code you didn't write,
it may be mid-edit: wait, or ask, rather than fix it. Don't commit
another's uncommitted work without the user's say-so.
