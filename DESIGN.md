# Raza's design: the parts, the elements and the attacks

What the parts' surfaces, the elements and the attacks are for, so a change
can be checked against it. The code (in `src/`) says how: `frames.rain` (the parts),
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
  - gold: polished metal with moving studio reflections, with identity-coloured perimeter strip lighting.
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
- **The colour toggles** are a pentagon at each player's near left, as a
  card's back has Magic's five colours: white at its top as they see it,
  then blue, black, red and green clockwise. Folded, they're the five-colour
  icon (the card back's five dots, textures/five-colour-dots-96.png, as
  wide as a toggle, turned to face them) right in the player's bottom left
  corner, as near it as fits; open, the pentagon is as near the icon as it
  fits, so it moves out as little as it can. After a reset (every seat its
  starting colours) they're open, and stay so until the player sets one;
  then they fold 2 s after the last one set (each set starts it again),
  drawing in to the icon as it comes, 0.2 s. The icon touched opens them for
  3 s, each one set then giving 2 s from then; the pentagon's middle
  touched folds them at once. A restart or a new count keeps the colours,
  and leaves the toggles as they were; when Raza starts, carrying
  on a game, they're folded.
- **The life drum.** A life total tapped opens into wheels, a digit each,
  as an odometer's: each a cylinder with its digits round it, one more each
  row up and one less down, and beside them (to the player's right) a wheel
  of the change since it opened, 0 at the middle, +1 up, -1 down. A wheel
  dragged turns with the finger (down brings the bigger digits to the
  middle), the life changing by its place, the units' by one and the tens'
  by ten, a row at a time; the others turn only as it carries into them,
  and the change's wheel counts in its place. Each squashes and darkens
  toward its edges as a cylinder turns away, with a gleam above the middle.
  Let go, the number at the middle is the life (undo brings each turn
  back). Tapped again it closes: the wheels flatten (0.15 s), and the
  change stays flat beside the life 1 s, then fades over 1.5 s. A press
  that moves less than 0.15 of the life's capitals is a tap. Drawn by drawing the rows flat into the light
  layer (a canvas is opaque, so their fill, border and shadow go in its
  red, green and blue) and wrapping that round the cylinder in the Drum
  shader, by Draw's draw_shader_canvas.
- **Every player is kept until a restart or reset.** A smaller count
  takes players off the table (GOING's slots, the last to go the first
  back), each kept as they were: life, colours, the damage each commander
  has done and taken. Back up, they return so. A restart starts all six
  again; a reset forgets those off the table.

## The elements: each colour's damage

**Goal: damage is something a player draws from their own colours and
throws**, each colour as its own element, as combat damage or a spell's.

- **Two damage icons per player**, at their damage spot, side by side as
  they see it, each white with a black outline and drop shadow, turned to face them: Mana ms-battle
  on their left for combat damage (commander damage: it takes life and
  counts toward the 21 from that commander), Mana ms-sorcery on their right for a
  spell's (or an ability's, or another creature's: life alone, never
  toward the 21, as the rules count only a commander's combat damage).
  Both drag the same way with the same range (1 to 9 out to the life total,
  past it the picker); the one dragged from is lit. Nothing else is drawn
  there at rest (the resting element fields and their motes are gone).
- **Each colour's element** is what's drawn as the damage is
  thrown (the volley, below):
  - white: a sun's light, its depths a starfield's (Star Nest, by Pablo
    Roman Andrioli, MIT licence);
  - blue: water;
  - black: shadowy tendrils out of a roiling glob of oil (lit from behind
    at its steep edges, a rainbow where it's thin, after the liquid toy's
    shading);
  - red: fire and lightning;
  - green: wind;
  - colourless: liquid metal, sky and ground reflected in each swell.
- **Light glows.** The sun's and fire's light go into a light layer added
  with bloom (Draw's `add_light`).

## Selecting: the arrow while dragging

A white arrow with a black outline starts just above the pressed attack
button in its player's frame. It curves up from the button, over the table,
and down onto the chosen victim's life total. A soft down-right shadow falls
over everything beneath it, including the table, controls and life counts.
The arrow is drawn after those layers. Its shaft is 80% of an attack button's diameter. Before a victim is selected, its head points along the drag direction, away from the pressed button. It appears immediately on dragging, pointing at the finger until an eligible victim is selected. Its shadow lifts only through the arch, with both ends touching the table. The pending amount sits above the victim's life total and arrow tip in the attacker's frame, facing the attacker.
Selection emits no element streams or particles; released attacks retain
their elemental volleys and impacts.
## The attack: the volley on release

The game changes at release (so undo is simple); what's shown counts down as
the attack lands (life, and a combat attack's commander damage chip). Undo,
or a new game, calls attacks off. Lethal commander damage ends in a much
bigger burst. A spell's attack looks the same as combat damage's.

- **Its shape is each element's** (`VOLLEY_SHAPES`): blue surges as a
  deluge, one great mass; red throws bolts of fire and white bolts of
  energy (short beams), one after another, more for more damage, all landing
  together; green a storm, a wide gust throwing off leaves and twigs as it
  flies; colourless a gob of metal. Each lands as a splash of itself.
- **Its times**: it gathers at the player's spot (0.14 s), flies along the stream's curve as it was let go (0.42 s), and lands,
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

The pill in the middle, across the screen, its buttons 1.2 cells apart:
from the left, undo and redo, the players in the middle, a new game, and the
system's (settings and quitting) at the right end, as a power button. Its
edge is raised bronze piping (0.06 cells), a round bead lit from the top
left with a highlight along it, casting a soft shadow down and to the right. The text is Crimson Pro.

Undo goes back a step, and redo forward: damage dealt, a life drum's turn,
a player's colours (their taps one after another, while their toggles stay
open, one step), a line dragged, a new count, a new game and a reset (the
colours, the players off the table and the lines it forgot). Each step keeps
the game and every count's lines; the motion's a setting, and isn't undone.
The steps last while Raza runs.

The players' button: touched, the count runner grows out of the pill's
middle, up and down (0.11 s), the rest of the pill and its buttons staying as
they are: a long upright groove, fixed, as long as the count bar's whole
travel, joined to the pill with rounded corners. In it, the count bar, which
the players' button stretches into, each count's ring of people engraved on
it, slides with the finger, small pointers either side of the runner marking
the count at the button; let go, that count's the game's, the same if it
didn't move, and the runner goes back into the pill.

The pill is cut into the parts' surface as the channels between them are: a
recess with a solid floor of its own (not see-through), its walls the
channels' cosine bowl going down from the surface to it, each shaded where
it faces away from the light at the top left and warmly lit where it faces
it. Drawn by a shader of its own (`recess_shade`) from its shape's distance.

The power button splits the table along its horizontal seam, as the
players' button splits it along the upright one: the halves above and below
slide apart (0.16 s), out from under the pill, each walled where it's cut,
the upper one's shadow falling into the channel; the pill stays where it
is, its buttons as they are (the count slider seen through the players'
button), lying on the halves and over the channel with a soft shadow of its
own (drawn apart, over the table drawn without it). In the steel channel that opens, each
on a chip of the pill's floor: the motion, a place left of undo, one button
showing what it is (pause, or play's triangles: ▶ slow, ▶▶ medium, ▶▶▶
fast), each tap the next, round from pause to fast and back; Reset, a
place right of the menu button, which closes the table, then resets; and
Quit, the power icon, a place right of Reset. The menu button, touched
again, closes the table, as a tap anywhere else, or Escape, does.

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

The repository: `src/` the code (and `src/icons/`, what the icons tool
writes), `fonts/` and `textures/` the art it carries; `rain src/raza.rain`
builds a dev build into `build/`, and `rain -release src/raza.rain` the
tablet's into `release/` (both ignored by git).

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
chips off the toggles, the toggles' pentagon and its folding, the pill's
buttons, the count runner, the settings' buttons, players kept across
counts, the life drum's opening, turning, closing and its wheels' carrying.
`raza_folded_0.png` and `_1` show the toggles folded and half way;
`raza_drum_0.png` to `_3` a life drum open, its units' wheel turned back
through a carry, then its tens' turned, then closing, and closed with its
change beside it.

## Speed

The parts' surfaces are the costliest thing drawn (one shader with every
material), and they move slowly, so they're kept in a canvas of their own:
each frame one part's is drawn again, in turn, if it's moved since it was
(none while Motion's off), and all of them when anything else they show
changes (the size, the lines, a part's colours, who's out or aimed at).
The light layer and its bloom are drawn only while something's lit (a
drag, a volley). Draw_Vulkan keeps the driver's compiled pipelines in
%LOCALAPPDATA%\Raza\vulkan_pipelines.bin: the part shader's took Intel's
driver about 6 s to compile at every start, and now only at a build's first
(its cache is the exe's own). `Raza.exe -quit_after:8` prints the frames'
work; measured at 2160×1440 on Intel's GPU: 58 fps (the 60 cap), each
frame's work 14 ms, the first frame 0.5 s. The frames a second show top
right in a debug build, not in a release build; F12 shows or hides them in
either (F11 is fullscreen or a window).

## Material assets and animation

The embedded atlas in textures/materials-v1.png supplies fine material detail, including the single forest-floor texture.
Its provenance, layout and original generation prompt are recorded in textures/.
No reference game's art is included in the application.

- White: fine mineral detail and evolving seams. Stationary mineral fields
  combine over time so seams grow, widen, split, join and fade; veins are soft warm grey rather than charcoal.
- Black: restored to the original pattern and material blend, with its
  original animated illumination. A final 1.35 contrast adjustment deepens shadows without replacing its motion.
- Green: the original forest texture plus three fixed offset copies. Local opacity masks evolve independently and favour bright leaf detail, suggesting leaves appearing and fading. The base floor remains opaque, with moving canopy illumination; there are no separate plant sprites.
- Red: original procedural crack shading, without the later atlas overlay or added cloud illumination.
- Artifact: bronze metal patches under animated rust. Corrosion remains granular;
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

Multicolour gold (three colours or more; two remain hybrid) uses polished gold with shallow undulations
and moving studio reflections.
The actual polygon perimeter is divided into equal arc lengths in WUBRG order,
starting at its first vertex. Each colour lights its entire strip, including
around corners, with soft inward falloff. Light retains the material shading;
black darkens its strip. The interior remains gold. Motion controls the reflected lights; Off freezes them.

Grooves are confined to shared player boundaries. Each half is 0.075 cells
wide, with a smooth cosine bowl profile, no channel around the screen edge,
and a thin highlight marking the divider being dragged.

Drag damage projects the pointer onto the line from the attacker's source
icon to the target's life counter. Nine equal bands run from its entry into
that region (1) to the counter (9); beyond it is ?. Sideways movement does
not change the amount. Releasing on ? opens the number grid, five keys
across and four up (a cell apart), facing the dragger to the nearest
quarter turn and kept on the screen:

```
50 60 70 80 90
00 10 20 30 40
 5  6  7  8  9
 0  1  2  3  4
```

The dragger's damage icons are hidden while it's open, and in their
places, at their size, are a cross (combat's place) and a tick (spell's),
the grid just above them. It opens at 10 (10 and 0 chosen, shown gold).
A tens or a units touched is chosen; only the tick deals the two together
(00 and 0, nothing); the cross, or anywhere else, cancels. Behind the grid
is a pane of frosted glass (the table under it blurred, seven by seven
samples 0.05 cells apart, a little paler and darker, a fine rim lit from
the top left: `glass_shade`, reading the table's own canvas); the screen
isn't darkened. The numbers are Crimson Pro, white, outlined in black with
a drop shadow, as the life totals are.

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

At rest there are no element handles: each player's damage spot is its two damage icons (combat and spell). Targeting trails are narrower, less widely braided, and emit eight motes per second across their colours. Motes are smaller and bloom is weaker and tighter. Blue uses smooth volume shading without a flat water bitmap overlay; artifact reflections are warm and softened. Blue and green attacks have smaller, shorter bodies. Black retains its strand, plunge, pulse and single-hit strike sequence. Damage timing and hit testing are unchanged.

The central controls and player-count selector use textures/control-metal-v1.png, a dark brushed gunmetal material. Their existing rounded geometry and recessed lighting remain. The metal prompt is in textures/DARK-METAL-PROMPT.md; the separate transparent five-colour dot icon is documented in textures/CARD-BACK-ASSETS.md.

The player-count control is a circular brushed-bronze button surrounded by a raised metal ring 0.07 cells thick, with a soft shadow cast down and right onto the table and slider by top-left light. The ring has complementary diagonal cuts: the top joins slightly right of centre, the bottom slightly left. The left table half also casts a soft down-right shadow into the gulley and onto the bar. Holding the button separates the entire table into left and right halves, including the control bar and ring. The full-length count slider sits above a thin bronze-lined guide groove in medium blue-grey cold-rolled steel (textures/under-table-steel-v1.png). The quiet steel stays bright enough to show the down-right shadow from the left table edge. The table cutout reaches under the ring, exposing this steel inside the split halves rather than the dark-metal control backing. The slider keeps its engraved people rings; there are no selection arrows. Release brings the halves and ring together over 220 ms (opening takes 120 ms). The slider stays full length beneath the table at all times, visible through the ring hole when closed; only the table masks it. Newly exposed cut edges use the same rounded cosine profile and lighting as the player channels. Snapshots include closed and intermediate states as raza_count_morph_0.png through _2.png.

The count slider stays full length and rides above a narrow bronze-lined groove beneath the table. The groove is 0.18 cells wide, with a dark interior and bronze lining. Its rounded-end centres coincide with the slider end-cap centres at the limits of travel; the exposed steel surrounds it. Count spacing is 0.95 cells; the ring hole and table opening reveal the slider. Player UI (life totals, colour controls, damage icons and effects) fades out as the table opens, stays hidden during closing, then fades back in over 180 ms after the halves reconnect. Surfaces and the central controls stay visible. During the fade, a complete UI frame is blended over the same bare surfaces to preserve background brightness.

The disk and extended count slider share a softly domed bronze finish, with warm reflections curving over the full face rather than a straight cylindrical stripe.

### Live multicolour background tuning

F8 toggles a tuning panel drawn inside Raza; `-tune` opens it at launch.
It starts at half the available height. Drag its title bar to move it, or
any edge/corner to resize it. Its size and position survive closing and
reopening within the run, and stay within the main window when it resizes.
Its 68 sliders cover ambient RGB and strength, surface curvature and relief,
reflection position/shape/colour/motion, highlight polish, perimeter-strip
reach and blending, and each WUBRG light colour. Values update the shader
uniforms and invalidate the surface cache immediately, even with Motion Off.
Large text scales for monitor DPI. A visible scrollbar supports dragging and
track clicks; the mouse wheel also scrolls. Up/Down selects a control;
Left/Right adjusts it, with Shift for a finer step. Reset selected and Reset
all restore the built-in defaults.

Every edit is saved to `background-tuning.json` in the working folder (the
project folder for normal development launches), using a temporary file and
rename. JSON keys name the individual values so agents can inspect the result.
All runs load it, whether the control panel is open or not. A different file
can be selected with `-background_tuning:path`. Missing keys retain defaults;
out-of-range values are reset to defaults; malformed input is reported and
is not overwritten during loading. The panel shows save failures and offers
a Save / retry button. Closing the control panel keeps the chosen settings.