# Raza's design: the parts, the elements and the attacks

What the parts' surfaces, the elements and the attacks are for, so a change
can be checked against it. The code (in `src/`) says how: `frames.rain` (the parts),
`elements.rain` (the elements' colours and how the volleys are drawn),
`motes.rain` (the volleys' paths and timing), and the C:\rain modules they
use (Draw's `draw_shader`, `draw_shader_image`, `fill_glow`, `add_light`
and `Text_Style`, and Patterns).

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
  and a little to their right. Nothing behind it is softened. Its place
  is one width whatever its digits: the widest digit's for each, two at
  least (and its minus below 0), the number centred in it, so its chips,
  shortcuts and tax don't move as it goes from 40 to 39 or 9, only past 99
  or below 0 (life_area_width). Every life
  total is one size: as big as the smallest part's room allows (so each
  fits its part), from a cell up to six, and no bigger than lets each
  player's spinner, open with its cross and tick, fit on the screen (it's
  moved onto the screen as it opens; its glass may lie over another's
  part). Each attack spot is far enough above its life total for a
  commander chip between them; where the controls in the middle hold it
  back, the life total moves down toward its player instead, as far as
  still keeps it in its part.
- **Readable.** The colour toggles sit on soft shadows; commander damage
  chips sit in a row below the life total, or where they fit clear of the
  toggles and inside the part.
- **The colour toggles** are a pentagon at each player's near left, as a
  card's back has Magic's five colours: white at its top as they see it,
  then blue, black, red and green clockwise. Folded, they're the five-colour
  icon (the card back's five dots, textures/five-colour-dots-96.png, as
  wide as a toggle, turned to face them) right in the player's bottom left
  corner, as near it as fits; the icon stays while they're open, and the
  pentagon is as near it as fits, clear of it, so it moves out as little as
  it can. After a reset (every seat its starting colours) they're open, and
  stay so until the player sets one; then they fold 2 s after the last one
  set (each set starts it again), drawing in to the icon, 0.2 s. The icon
  touched opens them for 3 s, each one set then giving 2 s from then;
  touched while they're open, or the pentagon's middle touched, folds them
  at once. They, and the options, are drawn over everything else. A restart or a new count keeps the colours,
  and leaves the toggles as they were; when Raza starts, carrying
  on a game, they're folded.
- **The life drum.** A life total tapped opens into wheels, a digit each,
  as an odometer's: each a cylinder with its digits round it, one more each
  row up and one less down, and beside them (to the player's right) a wheel
  of the change since it opened, 0 at the middle, +1 up, -1 down. A wheel
  dragged turns with the finger (down brings the bigger digits to the
  middle), the life changing by its place, the units' by one and the tens'
  by ten, a row at a time; the others turn only as it carries into them,
  and the change's wheel counts in its place. A turn takes the life no
  lower than 0 (a wheel stops at the last whole row above it, a spin back
  settles on it); damage can take it lower, and a life below 0 tapped
  opens its drum at 0, the change it adds (+4 from -4) on the change's
  wheel (the cross takes it back, and with nothing done since, takes back
  the opening's step to undo too, rather than making another); so the
  leading wheel shows no digits
  below its 0 (nor, below 10, does the units'), nor the change's wheel
  changes past that. There are always at least the units' and the tens'
  wheels: a life below 10 has its tens' wheel, blank at 0, so it can be
  turned by ten too (flat, the drum's digits are where the life's drawn,
  the blank wheel to their left). Each squashes and darkens
  toward its edges as a cylinder turns away, with a gleam above the middle.
  Let go, the number at the middle is the life (undo brings each turn
  back). Only its cross or its tick closes it (a touch elsewhere in the
  player's part does nothing while it's open, but for a line there, which
  is still dragged except where the drum covers it, its glass or its cross
  and tick; the settings opening leaves it open, and the count can't be
  changed while it's open, as undo can't): the wheels flatten (0.15 s), and the
  change stays flat beside the life 1 s, then fades over 1.5 s. As it
  rounds, the whole drum (its wheels and the change's) slides to be
  centred on the life total (and, where that would put any of it, cross
  and tick too, off the screen, onto it), sliding back as it flattens, over blurred
  glass, with a glass button either side as tall as that glass: the cross
  (red, on the player's left: the life as it opened) and the tick (green,
  on their right: the life as turned), each closing it. A square as wide
  as the tick is taken off each of its ends, a hair apart: a + at the end
  away from the player and a - toward them, each the life as turned, the
  drum closed, and the number grid centred where it was touched, its tick
  adding its number to that life or taking it away. A press
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
throws**, each colour as its own element, as damage or commander damage.

- **Attack icons per player**, at their damage spot, in a line as they see
  it, each white with a black outline and drop shadow, turned to face them:
  plain damage's leftmost (a spell's, an ability's, another creature's: life
  alone, never toward the 21), then each attack they've turned on in their
  options, in this order: commander damage (Mana ms-commander, bronze, with
  the power symbol's badge at its lower right: their commander's combat
  damage, taking life and counting toward the 21 from that commander, as
  the rules count only that; on to start with), commander damage with
  lifelink (the same, with lifelink's badge at its lower left too: and they
  gain as much life), lifelink (ms-ability-lifelink, its heart white and
  the hands holding it bronze, drawn from the glyph's own two outlines,
  with the power symbol's badge: life taken, and as much gained), and
  poison (ms-ability-infect: poison counters, ten and the player is out).
  Badges are white; the options' toggles show the same symbols. The line is centred on the spot; one
  too wide for their part wraps, the rest in lines above it (further from
  them), never below it, each centred; where they don't fit so they're
  pulled closer together (to 0.8 of their spacing), and only where even
  that won't fit (every option on, in a narrow part) is the whole moved
  down toward them, its lines still going up. Every attack drags
  the same way (1 to 9 out to the life total, poison 1 to 3, past it the
  picker); the one dragged from is lit. Nothing else is drawn there at rest.
- **Options**, in each player's bottom right corner, mirroring the colour
  toggles in their bottom left: the options button (Mana's
  ms-ability-improvise alone, at the attack icons' size, outlined, at 80%
  opacity) opens a panel of toggles, four across and three down: +1, +2,
  life+ and commander damage along the top; -1, -2, life- and commander
  damage with lifelink below them (each gain above its loss); then
  lifelink and poison, and commander damage alone (counted toward the 21,
  no life taken: the commander with no badge) under the other commanders.
  Each is its symbol in a dark circle, white and ringed in white when it's
  on, dim when it's off. The life shortcuts stand by the life total as
  hearts in columns, the ones nearest it, then the twos, then life+ and
  life- (a heart with + or -), which open the number grid, centred where
  they're touched, its tick adding its number to that player's life or
  taking it away.
  The button stays while they're open, and they stay open until it's
  touched again (or their middle is): they don't fold by themselves. They're
  undone as the colours are, a run of taps one step. An attack turned off
  ends its player's drag of it, or its number grid, without making it.
  The options and the colours, their buttons too, take a touch only where
  they're drawn: not in a part too thin for them, while its drum's open, or
  while the count column has the table. They
  belong to the seat, kept with the game and across a new game; Reset turns
  every seat's back to damage and commander damage.
- **Poison** flies as poison tokens (a green counter with poison's symbol)
  in place of the damage dots, with no number flying off as each lands
  (they're no life lost), and the player's
  count shows as a green counter once they have any. It and their
  commander tax sit either side of their centre line (the line through
  their life total, straight toward them), the poison on their left and
  the tax on their right, each's near edge as far from that line (the
  wide poison counter's middle further out than the tax's), just below
  their life total, or just above it
  where there's no room below, or further out along that line; where the
  line has no room for them (a part dragged thin), off it, the nearest
  place to just below that's clear of the life total; every place clear of
  the attack icons' rows too; the commander damage chips keep clear of
  both. Lifelink's life counts up for the attacker as its dots land.
- **Each colour's element** gives the colour of the damage it throws (the
  volley, below): white's sun a pale gold, blue's water blue, black's oil
  violet, red's fire orange-red, green's wind green, and colourless metal
  a dull gold.
- **Light glows.** Each dot's light goes into a light layer added with
  bloom (Draw's `add_light`).

## Selecting: the arrow while dragging

A white arrow with a black outline starts just above the pressed attack
button in its player's frame. It curves up from the button, over the table,
and down onto the chosen victim's life total. A soft down-right shadow falls
over everything beneath it, including the table, controls and life counts.
The arrow is drawn after those layers. Its shaft is 80% of an attack button's diameter. Before a victim is selected, its head points along the drag direction, away from the pressed button. It appears immediately on dragging, pointing at the finger until an eligible victim is selected. Its shadow lifts only through the arch, with both ends touching the table. The pending amount, on foil glass, sits just beyond the arrow's tip (its nearest edge a little past it, along the way the arrow points), in the attacker's frame, facing the attacker, and kept on the screen (near an edge it may overlap the arrowhead). The same label lies over the attack icon the drag began at, so it's read where the drag started too.
Nothing else is drawn while selecting.

## Confirming: the buttons on release

Let go over a player, a drag doesn't strike at once: where the finger let
go (moved onto the screen if it must be), facing the attacker, are glass
buttons of the number grid's, a hair apart: the amount's, tinted green as
the grid's tick, a square as wide as the drag's amount label (which is one
width whatever the amount: room for two digits), its number twice the
grid's; above it (as the attacker sees it) one more's and below one
less's, as wide and half as tall; and beyond those two more's and two
less's, half as wide and half as tall as the amount's (none below 1).
The arrow stays aimed at the victim. A button touched strikes with its
damage (a step to undo); a touch anywhere else calls it off and does
nothing more. While it's open something's under way, so undo waits. A
drag past the life total still opens the number grid instead.

## The attack: the volley on release

The game changes as the damage is confirmed (so undo is simple); what's shown counts down as
the attack lands (life, and a commander damage attack's chip). Undo,
or a new game, calls attacks off. Damage's attack looks the same as commander
damage's, and every colour's the same but for its dots' colours.

- **A dot a point.** Each point of damage is a small bright dot with a
  coloured aura and a soft shadow, drawn out a little along its flight, its
  colour each of the attacker's colours in turn (WUBRG; colourless's own
  for none).
- **Along an arc.** The dots fly from the attacker's damage icon (damage's
  or commander damage's) to the victim's life total, along an arc raised above the
  table, each dot's arc swung a little to one side or the other so they
  don't fly in single file.
- **Its times**: it gathers at the player's spot (0.14 s), then the dots
  leave one after another (0.065 s apart, closer for a big volley, so all
  of them have left within 2 s), each flying 0.42 s.
- **Landing.** As each dot lands the life shown goes down a point (and a
  combat attack's commander damage chip up one), a "-1" flies off the life
  total along the dot's way, and the life total recoils from the hit (a
  damped spring, moved but not turned; hits at once add). A second after
  the last lands, the volley's gone.
- **Bounded.** A volley's dots all leave within 2 s, so a huge hit takes
  no longer to land than a big one.

## The controls

The pill in the middle, across the screen, its buttons 1.2 cells apart:
from the left, undo and redo, the players in the middle, a new game, and the
system's (settings and quitting) at the right end, as a power button. Its
edge is raised bronze piping (0.06 cells), a round bead lit from the top
left with a highlight along it, casting a soft shadow down and to the right. The text is Crimson Pro.

The settings' channel has a brightness slider between the orientation's
button and Quit, as the count runner is: a narrow bronze-lined groove in
the steel, and a round domed bronze knob riding in it with a sun engraved
on it (dimmest at its left, full at its right). Touched, or dragged, it dims everything drawn toward black,
from full down to 30%; it's kept between runs, as the motion is, and isn't
undone. A portrait screen has no room for it there.

The orientation's button, a place right of Reset, goes round auto,
landscape and portrait, showing which (a screen turning; a tablet, on its
side or upright), kept between runs. Auto draws as the window is, the
display turning as the tablet's held (Window's keep_orientation(.ANY)).
Landscape or portrait asks the display to keep to it (keep_orientation:
Windows then keeps a tablet turned on its side as it was, and turns one
held the other way); where its window is still the other way about
(Linux's desktops, which turn a display only by their own settings, or
Windows refusing), it draws the table that way into a canvas of its own
and turns that onto the window a quarter turn clockwise (the Turn shader),
the fingers turned back with it.

A line between parts is dragged by its end along the screen's edge. A
second finger on a line while one's dragged turns every line together about
the screen's centre, by as much as the two fingers' middle goes round it, so
each player's part moves round the table with them; a turn that would crowd
an attack button against a line stops where it is. Lifting either finger
ends it. Each count keeps its lines for a landscape screen and its own for a
portrait one, so turning the tablet over to the other and back finds them as
they were.

Undo goes back a step, and redo forward: damage dealt, a life drum's turn,
a player's colours (their taps one after another, while their toggles stay
open, one step), a line dragged or the lines turned, a new count, a new game and a reset (the
colours, the players off the table and the lines it forgot). Each step keeps
the game and every count's lines (the screen's way round's: a step's lines
come back only on a screen the same way round as it was); the motion's a
setting, and isn't undone. The game is kept between runs, each player's
attacks a bit each of Attack's values, in a u16 (a game kept when they
were a byte is read as it was, from_bytes').
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
place right of the menu button, which closes the table, then resets; the
orientation's button a place right of Reset; the brightness slider; and
Quit, the power icon, at the channel's far right. The menu button, touched
again, closes the table, as a tap anywhere else, or Escape, does.

## Ideas kept for later

- **Foil.** (Now the glass of a drag's damage label, just beyond the
  arrow's tip at the target during an attack drag, not over the arrow:
  `glass_foil`, moving with time, its tan nudges held and its streaks
  softened so its lines are less pronounced, brighter through the glass,
  and swirling (waves pushing across as much as up and down, moving
  opposite ways) rather than drifting up and down.) A shader the user noted for foil effects: the plane warped by
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

`Raza.exe -snapshot:folder` draws each count of players (`raza_2.png` to
`raza_6.png`, a drag's arrow in each), `raza_confirm.png` and
`raza_confirm_portrait.png` (that drag let go, its damage asked for), `raza_frames.png` (each colour
alone and all five as gold), `raza_volley_0.png` and `_1` (a volley in
flight, then landing), `raza_black_0.png` to `_2` (a volley from a white,
black and green player, its dots in their three colours, in flight and
landing), the grid, the counts, and the settings
(`raza_settings_0.png` part of the way open, `_1` open). The tests check
what can be checked without looking: volleys arcing from the damage icon
to the life total, landing a point at a time, their bolts in sequence,
the life's recoil settling, chips off the toggles, the toggles' pentagon and its folding, the pill's
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
(none while Motion's off); a part again at once when anything else it
shows changes (its shape as a line beside it moves, its colours, whether
it's out or its channels lit), over what was there, so a line's drag
redraws its two parts alone, and all of them from clear once nothing's
changed for a quarter of a second; and all of them when the size or the
count changes.
The light layer and its bloom are drawn only while something's lit (a
volley). Draw_Vulkan keeps the driver's compiled pipelines in
%LOCALAPPDATA%\Raza\vulkan_pipelines.bin, saved only when one was compiled
(it used to be kept only when it grew, so once the shaders changed every
start compiled them again: 7 to 12 s). The part shader asks Patterns for
marble by name, the only kind that reaches it, so the driver leaves the
other kinds out: its cold compile went from 5.3 s to 1.8 s on Intel (a cold
start, 2.7 s to the first frame, happens after the shaders change, or
when Intel's own shader cache has dropped them).

The four textures' PNGs are decoded on threads of their own while the
window and the device are made (materials.rain's start_textures and
take_textures). Text with an outline or a shadow is drawn by Draw_Vulkan
once a glyph (its outline and shadow kept in its atlas), upright, and drawn
turned at any angle; icons likewise (Icons makes each once, upright). A
new size is new glyphs, so while a line's dragged the life totals keep
their size until it's 15% out, fitting exactly once it's let go. Placing
the toggles and options is a search, so each part's are kept until the
part changes (a line's drag, its two parts'), the search going out from
the button in rings and stopping once nothing nearer can fit.

`Raza.exe -quit_after:8` prints when the first frame was shown, and the
frames' work after it; `-busy` (with it) is a busy table to measure: a
strike between two players every half second and two players dragging,
nothing stored. Measured at 2160×1440 on Intel's GPU, with the pipelines
cached: the first frame 0.6 s from the start; idle, each frame's work about
1 ms; busy, the frames as fast as the display (120 Hz, its present waiting
for the display: the work shows about 8.3 ms). The frames a second show top
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
icon to the target's life counter. Twelve equal slots run from its entry into
that region to the counter, the amounts 1 to 9 taking 3, 2, 1, 1, 1, 1, 1, 1
and 1 of them (the small amounts, the commonest, are wider to hit); beyond
it is ?. Sideways movement does
not change the amount. Releasing on ? opens the number grid, five keys
across and four up (a cell apart), facing the dragger to the nearest
quarter turn and kept on the screen:

```
50 60 70 80 90
00 10 20 30 40
 5  6  7  8  9
 0  1  2  3  4
```

The grid (its keys and buttons together) is centred on where it was asked
for (where the finger let go, or the life+, life- or drum's + or - was
touched), moved onto the screen if it must be; the player's damage icons,
shortcuts and tax stay as they are, and work as they do without it. Below its keys are two glass buttons, each half the grid's
width: the cross on their left, its glass tinted red, and on their right one
tinted green showing the attack it makes (the damage icon's symbol, the
commander's or plain damage's). It opens at 10 (10 and 0 chosen, shown
green). A tens or a units touched is chosen; the green button deals the two
together (00 and 0, nothing) and the cross cancels. Only those two end it:
a touch anywhere else does whatever it would without the grid. Behind the grid
is a pane of frosted glass (the table under it blurred, seven by seven
samples 0.05 cells apart, a little paler and darker, a fine rim lit from
the top left: `glass_shade`, reading the table's own canvas); the screen
isn't darkened. The numbers are Crimson Pro, white, outlined in black with
a drop shadow, as the life totals are.

The snapshot command writes raza_materials_0.png and raza_materials_2.png:
all five colours plus artifact at two surface times, so material
evolution can be inspected independently of the attacks.

Two-colour identities use Ravnica-inspired hybrid surfaces: the actual two
materials, in WUBRG order from left to right in the section's local frame.
Their centre blend spans 35% to 65% of the section width; each retains its
own texture and animation. Three or more colours keep the lit gold surface.
The snapshot command writes raza_hybrids_0.png and raza_hybrids_1.png to
show all ten pairs alongside gold.

## Restrained attack effects

At rest there are no element handles: each player's damage spot is its two damage icons (damage, and commander damage). Selecting draws only the arrow, and an attack only its volley's dots, the "-1"s and the life's recoil: no element fields, streams, splashes or particles. Bloom is weak and tight (0.25 cells, 0.65 strength).

The central controls and player-count selector use textures/control-metal-v1.png, a dark brushed gunmetal material. Their existing rounded geometry and recessed lighting remain. The metal prompt is in textures/DARK-METAL-PROMPT.md; the separate transparent five-colour dot icon is documented in textures/CARD-BACK-ASSETS.md.

The player-count control is a circular brushed-bronze button surrounded by a raised metal ring 0.07 cells thick, with a soft shadow cast down and right onto the table and slider by top-left light. The ring has complementary diagonal cuts: the top joins slightly right of centre, the bottom slightly left. The left table half also casts a soft down-right shadow into the gulley and onto the bar. Holding the button separates the entire table into left and right halves, including the control bar and ring. The full-length count slider sits above a thin bronze-lined guide groove in medium blue-grey cold-rolled steel (textures/under-table-steel-v1.png). The quiet steel stays bright enough to show the down-right shadow from the left table edge. The table cutout reaches under the ring, exposing this steel inside the split halves rather than the dark-metal control backing. The slider keeps its engraved people rings; there are no selection arrows. Release brings the halves and ring together over 220 ms (opening takes 120 ms). The slider stays full length beneath the table at all times, visible through the ring hole when closed; only the table masks it. Newly exposed cut edges use the same rounded cosine profile and lighting as the player channels. Snapshots include closed and intermediate states as raza_count_morph_0.png through _2.png.

The count slider stays full length and rides above a narrow bronze-lined groove beneath the table. The groove is 0.18 cells wide, with a dark interior and bronze lining. Its rounded-end centres coincide with the slider end-cap centres at the limits of travel; the exposed steel surrounds it. Count spacing is 0.95 cells; the ring hole and table opening reveal the slider. Player UI (life totals, colour controls, damage icons and effects) fades out as the table opens, stays hidden during closing, then fades back in over 180 ms after the halves reconnect. Surfaces and the central controls stay visible. During the fade, a complete UI frame is blended over the same bare surfaces to preserve background brightness.

The disk and extended count slider share a softly domed bronze finish, with warm reflections curving over the full face rather than a straight cylindrical stripe.

### Multicolour background

The gold background's look (its surface's relief and ripples, the moving
reflections, the ambient light and each colour's perimeter light) is
`Gold_Look` in src/frames.rain, its values the defaults the live tuner left
(the tuner, F8, is gone).