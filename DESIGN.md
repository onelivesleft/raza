# Raza's design: the frames and the motes

What the parts' surfaces and the damage effects are for, so a change can
be checked against it. The code says how (`frames.rain`, `motes.rain`, and
the C:\rain modules they use: Patterns, Particles, `Draw.fill_glow`).

## The frames: each part's surface

**Goal: each player's part looks like the frame of a Magic card of their
colour identity**, in the manner of one of Magic's frame eras, chosen in
settings (Frames: Original, Modern, M15; Original unless chosen).

- **Made, not copied.** Every surface is procedural (Patterns' noise), drawn
  as the screen is. No Wizards of the Coast art or fan scans of it are
  used or shipped: the look is evoked, not reproduced.
- **Each colour its own surface, as the frames have them.** In the Original
  era: white an ivory's soft clouding, blue water drops, black marble with
  pale veins, red cracked rock, green mottling, an artifact's grey-brown
  grain, gold marble. Modern is smoother and brighter (silver artifacts);
  M15 finer and lighter still (brushed silver).
- **No colour outside the player's identity appears.** One colour: that
  colour's frame. None: an artifact's. Several: gold, shaded across the
  part toward each of the player's colours in turn (gold stays recognisably
  gold).
- **Fine-grained.** A card's frame texture is small against the card; a
  part is far bigger, so the features are kept small (`SURFACE_SCALE`).
  Too large reads as a close-up, not a frame.
- **Moving, very slowly by default.** Every surface moves in its own way:
  clouds, mottle and grain swirl in place (never slide), marble's veins
  flow, water drops slide down over rippling water, cracked rock's shading
  drifts and its cracks open and close, brushed metal glides. Motion
  (settings): Off, Slow (the default: noticed only if watched), Medium,
  Fast.
- **Smooth.** Gradients and surfaces are dithered, so nothing bands.
- **Readable.** The life total, its commander damage and the colour toggles
  stay legible on every surface.

## The motes: damage

**Goal: damage is something a player draws from their own colours and
throws**, in place of an icon and an arrow.

- **The miasma.** Each player who isn't out has a swirling cloud of motes at
  their damage spot, in a mix of their identity's colours (an artifact's
  with none). It always swirls, whatever Motion says: it's what you touch.
- **Each colour its own character:**
  - white: holy light, soft halos rising among small bright sparkles;
  - blue: water, drops falling and streaking, eddying;
  - black: oily, cloudy smoke curling into tendrils, with an oil's sheen;
  - red: sparks, small, white-hot, flung out and falling, gone quickly;
  - green: leaves blown on the wind, tumbling, now and then an autumn one;
  - colourless: metal sparks.
- **The stream, while dragging.** It flows from the miasma and **always ends
  at the life total of the player the finger is over**, wherever over them
  the finger is; the finger only bends it, slightly. Over no one, it ends
  at the finger. It thickens as the amount grows. The amount stays shown
  by the finger, facing the dragger.
- **The volley, on release.** One mote per point of damage, fired a little
  apart (faster for big numbers from the grid), following the stream's
  bend to the life total, each landing with a splash.
- **The life ticks down as they land.** The game itself changes at release
  (so undo is simple); what's shown counts down a point per landing. Undo,
  or a new game, calls volleys off.
- **Lethal commander damage is marked:** the volley's last mote bursts much
  bigger.
- **Cost.** The motes are GPU-drawn soft dots, so hundreds a frame are
  cheap; because the miasmas always move, Raza redraws about 30 times a
  second when idle (more battery than a still screen, accepted).

## Checking it

`Raza.exe -snapshot:folder` draws, among others, `raza_frames_Original.png`
(`_Modern`, `_M15`: each colour alone and all five as gold),
`raza_3.png` (a drag's stream to a life total) and `raza_volley.png`. The
tests check the parts that can be checked without looking: the stream's end
and bend, a volley's landing a point at a time, the lethal mark, undo
calling volleys off, the miasmas staying put, the settings' buttons.
