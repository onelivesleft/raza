# Raza's design: the parts, the elements and the attacks

What the parts' surfaces, the elements and the attacks are for, so a change
can be checked against it. The code says how: `frames.rain` (the parts),
`elements.rain` (the elements and the attacks' looks), `motes.rain` (the
motes and the volleys' timing), and the C:\rain modules they use (Draw's
`draw_shader`, `draw_shader_image`, `add_light` and `Text_Style`, Patterns, Particles).

## The parts: each player's surface

**Goal: each player's part looks like a frame of their colour identity**,
in the manner of Magic's original frames (1993 to 2003: painterly, mottled
and dark; the Modern and M15 eras were a setting once, and are gone), and
stays behind what's on it.

- **Made, not copied.** Original generated material textures supply fine detail,
  combined with procedural movement and lighting, drawn by a shader of
  the part's own (`part_shade`) as the screen is. No Wizards of the Coast
  art, fan scans or other games' assets are used: the look is evoked, not
  reproduced.
- **No colour outside the player's identity appears.** One colour: that
  colour's surface. None: an artifact's. Several: gold, shaded across the
  part toward each of the player's colours in turn.
- **Clean colour, low contrast.** A surface lightens toward a warm light and
  darkens toward a cool shade, not toward white and black, so colours never
  go grey and muddy; at 60% of each look's contrast, every part's features
  one size.
- **Depth.** Each part darkens toward its player's edge (a vignette, so
  the middle comes forward), and has a thin bevel along its edges, lit where
  an edge faces the light from the screen's top left and shaded where it
  faces away, so it reads as a framed panel.
- **Each colour has a surface of its own**:
  - blue: open water seen from above, soft and painterly (in the manner of
    Order of the Sinking Star's water, written from what it looks like): a
    rich blue, darker in slow deep patches, big soft hazes of white over it
    (the clouds and glare it reflects) drifting, fine wave lines lighter on
    their crests, a few sparkles;
  - green: a single richly textured forest floor of moss and fallen leaves, under moving canopy light;
  - colourless: brushed reflective metal, with patches of rust and pitted
    erosion growing and disappearing to expose metal again;
  - white: pale marble whose fine veins evolve in place over time;
  - black: deep obsidian with contrasting brighter veins;
  - red: cracked stone;
  - gold: polished metal with small recurring studio reflections and
    reflections of its identity-coloured light sources.
- **Facing its player.** Each surface is turned as its player's text is.
- **Moving, slowly by default.** Motion (settings): paused, Slow (the
  default, and what Reset sets back), Medium or Fast.
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

The plus is cut into the parts' surface as the channels between them are: a
recess with a solid floor of its own colour (the controls' dark grey, not
see-through), its walls the channels' cosine bowl going down from the
surface to it, each shaded where it faces away from the light at the top
left and warmly lit where it faces it. Drawn by a shader of its own
(`recess_shade`) from its shape's distance, it morphs as the settings open.

The power button opens the settings in the plus itself: the plus morphs into
a rounded square (0.22 s), each arm widening so its inside corners are pushed
out to the square's, the screen behind darkened. The
plus's buttons fade out over the first half, and the settings' fade in over
the second, each at a place of a three by three grid (the plus's own
places): Reset top left; the motion top right, one button showing what it
is (pause, or play's triangles: ▶ slow, ▶▶ medium, ▶▶▶ fast), each tap the
next, round from pause to fast and back; and Quit, the power icon on red,
where the power button was. A tap anywhere
else, a blank place in the square or outside it, or Escape, closes it, the
square morphing back.

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
`raza_6.png`, a drag's stream in each), `raza_frames.png` (each colour
alone and all five as gold), `raza_volley_0.png` and `_1` (a volley in
flight, then landing), `raza_black_0.png` to `_2` (black's strike plunging,
pulsing, snapping), the grid, the counts, and the settings
(`raza_settings_0.png` part of the way open, `_1` open). The tests check
what can be checked without looking: the stream's end and bend, volleys
landing a point at a time and bolts together, black's strike landing once,
motes born in their fields, fields clear of the controls, chips off the
toggles, the plus opening into a square, the settings' buttons. REVIEW.md lists what's still to do.

## Material assets and animation

The embedded atlas in textures/materials-v1.png supplies fine material detail, including the single forest-floor texture.
Its provenance, layout and original generation prompt are recorded in textures/.
No reference game's art is included in the application.

- White: fine mineral detail and evolving seams. Stationary mineral fields
  combine over time so seams grow, widen, split, join and fade; veins are soft warm grey rather than charcoal.
- Black: restored to the original pattern and material blend, with its
  original animated illumination. A final 1.35 contrast adjustment deepens shadows without replacing its motion.
- Green: the original forest texture plus three fixed offset copies. Local opacity masks evolve independently and favour bright leaf detail, suggesting leaves appearing and fading. The base floor remains opaque, with moving canopy illumination; there are no separate plant sprites.
- Artifact: original warm grey-brown (0x9A8A76). Corrosion remains granular;
  the former pale patches and broad highlights are dark shading instead.
- Water: calm blue-green depth, fine broken directional ripples and sparse
  sun glints, made by several evolving noise fields, now viewed at twice the previous scale. Avoid large luminous
  sine-wave meshes or a uniformly scrolling bitmap.

The sunny-water visual reference inspected for the current water treatment:
https://www.onpsx.de/media/images/orderofthesinkingstar04.jpg
It shows Order of the Sinking Star's fine ripples, restrained open water and
small glints. This is a screenshot reference, not a claim about its shader.
Earlier experiments adapted the user-supplied David Hoskins/joltz0r water
turbulence and used greenbird10's supplied underwater example as a visual
reference (labelled CC BY-NC-SA 3.0); the current open_water_at uses noise
fields instead of either example's wave formulation.

Multicolour gold lights (three colours or more; two are a hybrid, below) use
the MANA_GROUNDS colours shared with the toggles. In the section's local
orientation: three form a triangle with the last at the bottom; four occupy corners clockwise from
top left; five follow WUBRG clockwise from white at the top. Their edge washes
fade into the gold interior. Coloured reflections are diffuse, elongated and
irregular rather than round spots; black makes a dark reflection. Small studio
reflections drift continuously in one direction at 80% of their earlier peak
speed. Motion controls all material animation; Off freezes it.

Grooves are confined to shared player boundaries. Each half is 0.075 cells
wide, with a smooth cosine bowl profile, no channel around the screen edge,
and a thin highlight marking the divider being dragged.

Drag damage projects the pointer onto the line from the attacker's source
icon to the target's life counter. Nine equal bands run from its entry into
that region (1) to the counter (9); beyond it is ?. Sideways movement does
not change the amount. Releasing on ? opens the picker at 10.

The snapshot command writes raza_materials_0.png and raza_materials_2.png:
all five colours plus artifact at two surface times with fixed particles,
so material evolution can be inspected independently of the attacks.

Two-colour identities use Ravnica-inspired hybrid surfaces: the actual two
materials, in WUBRG order from left to right in the section's local frame.
Their centre blend spans 35% to 65% of the section width; each retains its
own texture and animation. Three or more colours keep the lit gold surface.
The snapshot command writes raza_hybrids_0.png and raza_hybrids_1.png to
show all ten pairs alongside gold.

## Restrained attack effects

Idle handles are compact, with no emitted motes. They enlarge when engaged; multicolour handles keep fixed positions. Green rests as a readable leaf and becomes wind when drawn out. Targeting trails are narrower, less widely braided, and emit eight motes per second across their colours. Motes are smaller and bloom is weaker and tighter. Blue uses smooth volume shading without a flat water bitmap overlay; artifact reflections are warm and softened. Blue and green attacks have smaller, shorter bodies. Black retains its strand, plunge, pulse and single-hit strike sequence. Damage timing and hit testing are unchanged.

The central controls and player-count selector use textures/card-back-v1.png, a warm mottled brown card-back-inspired material. Their existing rounded geometry and recessed lighting remain. Asset prompts and the separate transparent five-colour dot icon are documented in textures/CARD-BACK-ASSETS.md.
