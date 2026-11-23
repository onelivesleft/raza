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
  grain, gold marble. Each era sets four things apart: feature size,
  contrast, how much slow variation larger than the features shows
  (broad), and fine grain. Original is painterly (broad swings, rough
  grain); Modern smoother, its features three-quarters the size, little
  grain; M15 finest and quietest (brushed silver, a fine printed grain).
  Each era's features are no bigger, and its contrast no higher, than the
  one before's (a test keeps it so).
- **No colour outside the player's identity appears.** One colour: that
  colour's frame. None: an artifact's. Several: gold, shaded across the
  part toward each of the player's colours in turn (gold stays recognisably
  gold).
- **Fine-grained.** A card's frame texture is small against the card; a
  part is far bigger, so the features are kept small (`SURFACE_SCALE`).
  Too large reads as a close-up, not a frame.
- **Facing its player.** Each part's surface is turned as its player's
  text is, so its water falls toward them and brushed metal runs across
  their view.
- **Moving, very slowly by default.** Every surface moves in its own way:
  clouds, mottle and grain swirl in place (never slide), marble's veins
  flow, water drops slide down toward the player over rippling water, cracked rock's shading
  drifts and its cracks open and close, brushed metal glides. Motion
  (settings): Off, Slow (the default: noticed only if watched), Medium,
  Fast.
- **Smooth.** Gradients and surfaces are dithered, so nothing bands.
- **Readable.** The life total, its commander damage and the colour toggles
  stay legible on every surface: the toggle row sits on a soft shadow that
  quiets the surface under it.

## The motes: damage

**Goal: damage is something a player draws from their own colours and
throws**, in place of an icon and an arrow.

- **The miasma.** Each player who isn't out has a swirling cloud of motes at
  their damage spot, in a mix of their identity's colours (an artifact's
  with none). It always swirls, whatever Motion says: it's what you touch.
- **Shaped, not just dots.** Blue's motes are drops (a head forward, a
  tail behind), green's leaves (pointed, creased, tumbling), black's wisps
  (edges broken like smoke), red's and the artifact's sparks (a sharp
  point in a faint glow), white's sparkles sparks among soft halos.
- **Every colour equally present.** Each colour's miasma keeps about its own
  number of motes alive (many tiny sparks, a few big smoke wisps), however
  long its motes live; in a mix, each colour keeps an equal share, so no
  colour buries another. Motes are born evenly over the miasma, not bunched
  at its middle.
- **A heart at each miasma.** Under its motes, each colour has a heart
  about 1.6 cells across (several smaller, round the spot), drawn as a
  surface (Draw's radial gradients and Patterns' kinds), facing its player
  and always moving. They're after shaders the user picked, made our own:
  - white: a large glowing sun, a starfield's clouds in its light (after
    Star Nest), motes of light slowly orbiting it, inner ones faster;
  - blue: a body of clear water streaming toward its player, caustics and
    foam on its crests (after a water elemental's flowing surface);
  - black: a slick of oil flowing, sharp highlights, a rainbow sheen where
    it's thin (after Leon Denise's liquid toy);
  - red: a flame, red to a white-yellow heart, its tongues climbing and its
    edge licking, sparks flying up from it (after a fire with sparks);
  - colourless: a blob of liquid chrome, a sky's reflection in its swells,
    a faint bismuth tint (after flockaroo's spilled liquid);
  - green: none yet.
- **Each colour's motes its own character:**
  - white: motes of light orbiting its sun, warm gold and white-hot sparkles;
  - blue: water, drops falling and streaking, eddying;
  - black: oily, cloudy smoke curling into tendrils, with an oil's sheen;
  - red: sparks, small, white-hot, flying up from the fire, gone quickly;
  - green: leaves blown on the wind, tumbling, now and then an autumn one;
  - colourless: metal sparks.
- **The stream, while dragging (without black).** It flows from the miasma and **always ends
  at the life total of the player the finger is over**, wherever over them
  the finger is; the finger only bends it, slightly. Over no one, it ends
  at the finger. It thickens as the amount grows, and stays bright all the
  way to its end, where the aimed-at life total pulses softly. The amount
  stays shown by the finger, facing the dragger.
- **The volley, on release (without black).** One mote per point of damage, fired a little
  apart (faster for big numbers from the grid), flying along the stream's
  curve as it was when let go (with a little spread), each landing at the
  life total with a splash. Each keeps its own material (black stays dark
  smoke) with a soft halo of its colour behind it, so it can be followed.
- **The life ticks down as they land.** The game itself changes at release
  (so undo is simple); what's shown counts down as they land (several at
  once, for a big volley in one frame). A volley is settled when it has no
  motes left, so a mote that goes without landing can never leave the life
  shown wrong. Undo, or a new game, calls volleys off.
- **Lethal commander damage is marked:** once every point of that volley
  has landed, it ends in a much bigger burst.
- **Cost.** The motes are GPU-drawn soft dots, so hundreds a frame are
  cheap; because the miasmas always move, Raza redraws about 30 times a
  second when idle (more battery than a still screen, accepted).

## Ideas kept for later

- **Foil.** A shader the user noted for foil effects: the plane warped by
  stacked waves (each step a tan of y nudging x and a cos of x nudging y,
  finer and weaker each time, all moving with time), then coloured in
  rainbow bands of the warped place that brighten sharply where a cosine of
  the diagonal nears zero, so streaks of light sweep across as on a foil
  card. As it was given:

  ```glsl
  void mainImage( out vec4 fragColor, in vec2 fragCoord ){
      vec2 uv =  (2.0 * fragCoord - iResolution.xy) / min(iResolution.x, iResolution.y);

      for(float i = 1.0; i < 10.0; i++){
          uv.x += 0.009 / i * tan(i * 2.5* uv.y + iTime);
          uv.y += 0.9 / i *cos(i * 1.5 * uv.x + iTime);
      }
      vec3 col = 0.5 + 0.5*sin(iTime+uv.xyx+vec3(0,2,4));
      fragColor = vec4(col/(2.1*abs(cos(iTime-uv.y-uv.x))),1.0);

  }
  ```

## Checking it

`Raza.exe -snapshot:folder` draws, among others, `raza_hearts.png` (each
heart large), `raza_frames_Original.png`
(`_Modern`, `_M15`: each colour alone and all five as gold),
`raza_3.png` (a drag's stream to a life total) and `raza_volley.png`. The
tests check the parts that can be checked without looking: the stream's end,
bend and brightness there, a volley following its curve and landing a point
at a time, the lethal burst coming only once all have landed, a volley
settling without its motes, undo calling volleys off, the miasmas staying
put, the settings' buttons. REVIEW.md lists what's still to do.

## Black's connected attack

An identity containing black uses a connected tendril strike instead of the
ordinary stream and point-by-point volley. Other colours retain their idle
hearts and motes in a mixed identity.

- At rest, black is a slowly writhing nest: tapered, searching tendrils around
  a roiling, near-black oily body, with restrained highlights and a smoke veil.
- Dragging draws one connected, writhing strand to the cursor itself. It bows
  around the central toolbar on a side chosen from the source.
- Release begins a 0.32-second extension: additional strands spear into the
  target's life total. All share the same glob at their base.
- The attached strands pulse for 0.28 seconds, then contract together over
  0.28 seconds, accelerating the glob into the target. A short oily remnant
  marks the impact.
- All damage is shown at that one impact. The underlying game still changes
  at release so undo remains immediate; pending damage hides the whole hit
  until impact, independently of smoke-particle lifetime. Lethal damage makes
  one burst. Undo and new game cancel the connected attack as well.
- Damage increases strand count and glob size, with diminishing growth and
  caps of 24 strands and 3.1 cells to bound drawing cost for very large hits.

The geometry and timing are in tendrils.rain; Volley owns the attack's age and
impact state. Black's smoke particles are secondary, not its strands or damage
clock. Its silhouettes are procedural ribbons, not separate dots.

`Raza.exe -black_snapshot:folder` writes black_0.png through black_6.png:
idle, dragging, extension, pulse, early contraction, late contraction, impact.
This uses the actual draw and damage paths with a deterministic 18-point hit.
The black_* tests cover one-hit damage, cancellation, overlapping strikes,
large frame steps and bounded visual growth. Live pacing still merits a check
on the intended tablet.