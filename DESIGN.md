# Raza's design: the parts, the elements and the attacks

What the parts' surfaces, the elements and the attacks are for, so a change
can be checked against it. The code says how: `frames.rain` (the parts),
`elements.rain` (the elements and the attacks' looks), `motes.rain` (the
motes and the volleys' timing), and the C:\rain modules they use (Draw's
`draw_shader`, `add_light` and `Text_Style`, Patterns, Particles).

## The parts: each player's surface

**Goal: each player's part looks like a frame of their colour identity**,
in the manner of one of Magic's frame eras, chosen in settings (Frames:
Original, Modern, M15; Original unless chosen), and stays behind what's on
it.

- **Made, not copied.** Every surface is procedural, drawn by a shader of
  the part's own (`part_shade`) as the screen is. No Wizards of the Coast
  art, fan scans or other games' assets are used: the look is evoked, not
  reproduced.
- **No colour outside the player's identity appears.** One colour: that
  colour's surface. None: an artifact's. Several: gold, shaded across the
  part toward each of the player's colours in turn.
- **Clean colour, low contrast.** A surface lightens toward a warm light and
  darkens toward a cool shade, not toward white and black, so colours never
  go grey and muddy; at 60% of each look's contrast, every part's features
  one size in an era.
- **Depth.** Each part darkens toward its player's edge (a vignette, so
  the middle comes forward), and has a thin bevel along its edges, lit where
  an edge faces the light from the screen's top left and shaded where it
  faces away, so it reads as a framed panel.
- **Some colours have a surface of their own**, in every era:
  - blue: open water seen from above, soft and painterly (in the manner of
    Order of the Sinking Star's water, written from what it looks like): a
    rich blue, darker in slow deep patches, big soft hazes of white over it
    (the clouds and glare it reflects) drifting, fine wave lines lighter on
    their crests, a few sparkles;
  - green: a forest floor: soil and moss, two layers of fallen leaves
    (green, olive, brown, yellow, dark, each with a vein, the lower in the
    upper's shade), a few twigs, dappled light drifting over it;
  - colourless: rusting metal: brushed steel weathered in patches, rust
    staining about ragged patches that streak down the player's frame,
    mottled brown to orange, a few pits in the thickest.
  - The others (white, black, red, gold) are their era's patterns: in the
    Original era an ivory's clouding, black marble, red cracked rock, gold
    marble; each later era finer and quieter (a test keeps it so).
- **Facing its player.** Each surface is turned as its player's text is.
- **Moving, slowly by default.** Motion (settings): Off, Slow (the default,
  and what Reset sets back), Medium, Fast.
- **The life total is always white with a black border and a drop shadow**,
  on any surface (half clear when the player's out). Its shadow is cast from
  the screen's centre, falling away from it (down as its player reads it)
  and a little to their right. Nothing behind it is softened.
- **Readable.** The colour toggles sit on soft shadows; commander damage
  chips sit in a row below the life total, or where they fit clear of the
  toggles and inside the part.

## The elements: each colour's damage

**Goal: damage is something a player draws from their own colours and
throws**, each colour as its own element.

- **One field per colour**, a shader each, over its whole reach, fading
  into the part (several round the player's damage spot, smaller):
  - white: a sun, its depths a starfield's (Star Nest, by Pablo Roman
    Andrioli, MIT licence), a corona of rays about it;
  - blue: a body of water, deep blue by its depth, the sky in it at a slant,
    glints and foam on its crests;
  - black: a nest of shadowy tendrils groping and writhing out of a roiling
    glob of oil (lit from behind at its steep edges, a rainbow where it's
    thin, after the liquid toy's shading);
  - red: a flame, a teardrop rising from its root, tongues climbing, white
    at its heart to red at its edges;
  - green: gusts of wind, pale streaks and dapples;
  - colourless: liquid metal, sky and ground reflected in each swell.
- **Light glows.** The sun's and fire's light go into a light layer added
  with bloom (Draw's `add_light`).
- **It reacts.** At rest it's calm; dragged from, it stirs (faster,
  brighter); aimed at, half as much.
- **Clear of the controls.** A field reaches no further than its damage spot
  is from the plus in the middle, so it's smaller where that's tight (the
  six-player top and bottom parts).
- **Its motes come from it**, born where its own procedures say: the sun's
  flecks orbiting in its corona, fire's sparks off its flame tips, water's
  drops off its crests, oil's and metal's blobs budding off their edges and
  pulled back, leaves anywhere in the wind.

## Selecting: the stream while dragging

The stream always ends at the life total of the player the finger is over,
wherever over them it is (the finger bends it); over no one, at the finger.
The amount is shown by the finger, facing the dragger, and the aimed-at life
total pulses. Each of the dragger's elements is drawn along it (several
braid), as its own:

- blue: a thin hose's spray, fanning out, breaking into droplets;
- red: crackling lightning, a jagged bolt striking anew many times a
  second, forking;
- white: a beam of light;
- green: gusts streaming along it;
- black: a single tendril from its nest, its tip following the finger,
  writhing;
- colourless: its metal drawn out, thinning.

The stream sheds each element's motes along it.

## The attack: the volley on release

The game changes at release (so undo is simple); what's shown counts down as
the attack lands. Undo, or a new game, calls attacks off. Lethal commander
damage ends in a much bigger burst.

- **Its shape is each element's** (`VOLLEY_SHAPES`): blue surges as a
  deluge, one great mass; red throws bolts of fire and white bolts of
  energy (short beams), one after another, more for more damage, all landing
  together; green a storm, a wide gust throwing off leaves and twigs as it
  flies; colourless a gob of metal. Each lands as a splash of itself.
- **Its times**: it gathers at the player's spot (their fields swell, 0.14
  s), flies along the stream's curve as it was let go (0.42 s), and lands,
  its points coming off the life shown over 0.36 s, its splash fading
  after.
- **Black is one strike.** Its strands shoot out of the nest one after
  another and plunge into the target (0.32 s), pinned there they pulse
  (0.3 s), then snap toward it, pulling the glob at their base along the
  path into it (0.26 s): all the damage in one hit, then a pool that fades.
  More damage, more strands (3 up to 20) and a bigger glob. A player who's
  black and other colours strikes as black.
- **Bounded.** Bolts, strands and the glob grow with damage within limits,
  so a huge hit costs no more to draw than a big one.

## The controls

The plus in the middle: the players in its middle (touched, the column of
counts shows over the upright arm, to drag to for a new game; left
untouched it closes after four seconds), undo and redo on its wings, a new
game above, the system's (settings and quitting) below, as a power button.
The text is Crimson Pro.

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

`Raza.exe -elements:folder` draws `raza_elements.png`: each element at rest,
its stream as it selects, and its attack in flight. `Raza.exe
-snapshot:folder` draws each count of players (`raza_2.png` to
`raza_6.png`, a drag's stream in each), `raza_frames_Original.png`
(`_Modern`, `_M15`: each colour alone and all five as gold),
`raza_volley_0.png` and `_1` (a volley in flight, then landing),
`raza_black_0.png` to `_2` (black's strike plunging, pulsing, snapping),
the grid, the counts and the settings. The tests check what can be checked
without looking: the stream's end and bend, volleys landing a point at a
time and bolts together, black's strike landing once, motes born in their
fields, fields clear of the controls, chips off the toggles, the settings'
buttons. REVIEW.md lists what's still to do.
