# TODO

What's wanted next. Each item says enough to start on; one in the user's
own shorthand, whose detail isn't written down yet, says so: ask before
starting it.

## The user's (ask for the detail)

- [ ] **Particle attack.** (The user's words; detail not written down.)
- [ ] **Life count hits.** (The user's words: perhaps how a life total
  shows a hit as a volley lands. Ask.)
- [ ] **Fix life count spinners.** (The user's words: the life drums.
  Since this was written, a drum opened again after a ticked turn showed
  that turn as its change (fixed), and its tick gained + and - squares.
  Ask what's still wrong.)
- [ ] **Digit positions.** (The user's words: perhaps where a life total's
  digits sit, now that its place is a fixed width for its count of digits.
  Ask.)
- [ ] **21s.** (The user's words: perhaps what's shown at 21 commander
  damage from one commander, the lethal amount. Ask.)

## Known follow-ups

- [ ] **One slow start after the surface shader changes.** A release
  build shows its first frame 0.6 s from the start. But the first start
  after the parts' surface shader changes (every colour's material, the
  halves of two and the lit gold of three or more, in one shader) compiles
  it cold: measured 2026-11-25 on this machine's
  Intel GPU (the shader changed by one constant, so neither Raza's cache,
  `%LOCALAPPDATA%\Raza\vulkan_pipelines.bin`, nor the driver's own,
  `%USERPROFILE%\AppData\LocalLow\Intel\ShaderCache`, had it), the window
  opened at 0.5 s and stayed empty until 3.6 s, one frame of 3.1 s; the
  next start, 0.63 s. So on the tablet it's the first start after a
  release that changes that shader. Make the shader smaller, or draw
  something (the parts in plain colours) while it compiles.
- [ ] **Draw_Vulkan's pipeline cache only grows.** Raza's
  `vulkan_pipelines.bin` had reached 70 MB; made again from nothing it's
  260 KB. It seems to keep every pipeline compiled since it was first
  written, through every shader change, none ever dropped. That's rain's
  Draw_Vulkan (C:\rain): keep only what's used now, or start the file
  again when the shaders change.
- [ ] **Placing toggles while a divider's dragged.** Still about a third
  of a debug build's frame (the two parts beside the line are placed again
  each frame); a release build's isn't measured. Profile a release build
  while dragging, and cut it if it shows.
- [ ] **Linux and Android.** Raza is Windows' alone for now (Vulkan, the
  tablet's display and touch). Android is rain's TODO 94.

## Done

- [x] Input in `src/input.rain`: what each key and touch does (the
  settings, a confirm, options, a number grid, an open drum, the pill, a
  part's controls, a divider line) and how each held gesture follows its
  finger, apart from `main`.
- [x] Damage picker: the number grid opens centred where it's asked for
  (a drag let go on ?, life+ and life-, a drum's + or -), its tick adding,
  taking or dealing the number chosen.
