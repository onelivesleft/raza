# Raza: surfaces and damage motes review

Reviewed 2026-11-23 against DESIGN.md, frames.rain, motes.rain, raza.rain,
raza.tests.rain, and rain's Patterns, Particles and Draw implementations.

Generated snapshots with the existing Raza.exe and inspected the Original and
M15 frame sheets, two- and three-player layouts, and the volley image. Output
is in C:/rain/build/raza-review/. Snapshot generation completed successfully.
No source was changed or rebuilt and no test suite was run. Motion judgments
below are based on the implementation, not observation of a live animation;
frame rate, battery use and perceptual timing remain unmeasured.

## Overall judgment

The implementation establishes colour identity and the idea of drawing damage
from a player's own energy convincingly. The large life totals remain readable
in the inspected images. It is less successful at the more specific goals:
fine card-frame material, recognizable frame eras, and six distinct physical
kinds of particles.

The surfaces currently read more as enlarged procedural materials than the
fine texture of a card frame. The motes communicate coloured magic well, but
several promised materials collapse into glowing dots or blurred streaks.
The most useful next work is art direction and temporal clarity, not more
noise layers or more particles.

## Background surfaces

### What works

- Original has clearly different material families: blue droplets, red cracks,
  black and gold veins, green mottling, and pale white clouding. This meets the
  goal of more than simply recolouring one common texture.
- The gold mixtures remain recognizably gold in the inspected multicolour
  layouts. The code derives their tint stops only from the selected identity.
- Large numerals remain prominent, and opaque commander-damage badges protect
  their own text. No obvious gradient banding was visible in the inspected
  snapshots; Draw also contains explicit dithering support.
- M15 has lower surface contrast than Original, which moves in the intended
  direction of a smoother presentation.

### 1. Feature scale is still too large for the stated goal

Original's gold and black veins form broad, flowing islands. Blue has fairly
large, repeated, bead-like drops. Green has conspicuous cloudy clumps. These
look like close-up surfaces, the exact reading DESIGN.md says to avoid.

SURFACE_SCALE reduces the nominal scale, but the material formulas contain
lower-frequency structure too. A single multiplier does not make the whole
material fine-grained. Marble's slow wave and broad warp remain particularly
prominent.

Recommendation: separate broad colour variation, material structure, and fine
surface grain. Keep broad variation weak; make the characteristic material
features smaller; add restrained fine detail. Compare at the tablet's actual
viewing distance rather than only zooming into a large screenshot. Tune each
material independently instead of shrinking every layer together.

### 2. M15 is quieter, but the scale settings do not make it finer

For shared material kinds, several later-era scale values increase: white
clouds go from 2.5 to 3.5 and green mottle from 1.6 to 2.5. Patterns evaluates
coordinates as p / scale, so larger scale makes features larger, not finer.
Lower strength makes them subtler, which is a different property.

The M15 sheet consequently looks softer and broader rather than consistently
finer. Distinguish feature size from contrast in both tuning and comments.

Recommendation: give each era explicit targets for feature size, contrast,
edge sharpness and roughness. The goal is not merely three saturation levels.
The current material swaps help, but do not by themselves establish a strong
era-specific visual identity. This review judges that against Raza's written
brief, not a side-by-side audit of historical card scans.

### 3. Some surfaces are too literal or too synthetic

Blue's uniformly rounded, highlighted droplets resemble embossed beads on a
blue panel. Red communicates cracked earth clearly, but the strong, clean
crack network looks more diagrammatic than worn rock. Marble has a conspicuous
liquid-noise appearance.

Recommendation: vary drop shape and prominence, reduce the uniform rim effect,
break up crack contrast, and make marble veins more sparse and subordinate to
the ground. Preserve the material cues without making every feature demand
attention.

### 4. Identity differences weaken in gold, and controls compete with texture

Gold is correctly dominant, but a 25% tint contribution gives different
multicolour identities fairly similar overall surfaces. The colour toggles
carry much of the identification burden. Some inactive toggles are difficult
to distinguish against the more textured backgrounds.

Recommendation: test all two-colour pairs side by side. Tune the spatial tint
variation while keeping gold dominant; do not simply turn saturation up across
the whole panel. Give small controls a more consistent contrast treatment and
keep local surface variation quieter around them.

### Motion needs a separate review

The code implements different motion formulas and a Slow rate of 0.04 surface
units per second. That supports the intent, but a scalar rate does not ensure
that every material feels equally slow: high-frequency detail and narrow
edges can change visibly at the same nominal speed.

Observe each material for 10-20 seconds on the intended device. Slow should be
noticed on inspection, not continually compete with the life total. Check
spatial shimmer and aliasing as well as gradient banding. Texture motion is
screen-coordinate based; decide explicitly whether water should fall in screen
space or toward the player viewing that panel.

## Motes and damage

### What works

- The miasmas occupy a consistent location and visually suggest a source of
  energy. Mixed identities visibly combine different particle colours.
- Red's small, sparse hot streaks are the strongest match to its stated
  material. White and blue are immediately distinguishable as light effects.
- Steering the drag stream to the target's life total is a good interaction
  choice: targeting stays clear even when the finger is elsewhere in the part.
- The implementation separates committed game state from pending visual
  damage, supports undo cancellation, and emits a splash per arrival. Existing
  tests cover representative endpoint, landing, cancellation and lethal-tag
  behavior, though those tests were read rather than rerun here.

### 1. One soft-ellipse primitive limits material identity

Particles.draw renders every mote through fill_glow. Different sizes, alpha,
additive blending, elongation and motion provide variety, but they cannot
fully supply the promised shapes.

In the inspected images:

- White merges into a clipped-looking bright centre rather than clearly
  separated soft halos and sparkles.
- Blue reads as luminous cyan sparks more readily than falling water.
- Black reads as dark blurred blobs; an oily sheen and curling tendrils are
  much less apparent.
- Green suggests airborne flecks, but its bright soft ovals read more as
  magical wisps than leaves with a tumbling surface.
- Red is closest to the brief. The artifact spark palette is plausible, but
  its material distinction would benefit from a dedicated colourless sheet.

Recommendation: retain the cheap common renderer, but add a few procedural
shape profiles: a tapered drop, a pointed leaf with a subtle central crease,
a low-opacity irregular smoke wisp, and a sharper spark core. Give white a
broader faint halo with fewer overlapping bright cores. Shape and contrast
will buy more distinction than increasing particle count.

### 2. Equal birth rates do not produce equal visual presence

Every miasma emits 70 motes per second, but mean lifetimes range from about
0.5 seconds for red to 2.4 for black. Ignoring transients, that means roughly
35 live red particles versus 168 black ones. White combines long life with
additive blending; the snapshot shows the resulting bright central mass.
Mixed identities choose styles equally at birth, not equally by visible
coverage or time on screen.

Recommendation: tune each colour to a target visible density and brightness.
Keep the lifetime differences that define its motion, but compensate with
emission rate, size and alpha. Test white-black and red-black mixtures: equal
identity membership should not mean one material hides the other.

### 3. The stream loses some clarity before reaching its target

All particles fade out over their final third. Stream positions progress by
age/life, so they approach the target while becoming invisible. The preview
therefore has less visual emphasis at the exact endpoint it is meant to
communicate. The central toolbar also visibly occludes the stream in inspected
layouts.

Recommendation: use a stream-specific visibility envelope, retaining enough
brightness near the endpoint to make targeting unmistakable. Consider a small
arrival cue during dragging. Route around or otherwise account for the central
controls without drawing over controls in a way that harms their readability.

### 4. The volley does not actually follow the preview curve

The stream uses a quadratic curve. fire_volley only uses the bend to choose
its initial direction; afterward motes follow a spring toward the target,
with random lateral velocity and residual colour-specific swirl. This is not
the same path as the preview, although it may look pleasantly organic.

Recommendation: decide whether preview-path fidelity or a free physical throw
is the desired behavior. For the written goal, carry the curve into the volley
and put bounded variation around it. A consistent path would also make flight
time and arrival ordering easier to control.

### 5. Damage timing should not rely solely on incidental particle arrival

The lethal tag is attached to the last emitted mote, not necessarily the last
to arrive. Random trajectories and colour-specific dynamics can change arrival
order. Also, Particles.update removes a mote at the end of its life before
arrival handling; an expired volley mote has no corresponding pending-damage
decrement in land_volleys. This is a code-path risk, not an observed stuck
volley in this review.

The existing landing test checks that displayed life never increases and that
all seven points eventually land in one scenario. It does not require exactly
one point per rendered frame or prove arrival ordering across styles and
layouts. At large damage amounts, several arrivals per frame are inevitable;
the design should describe that as batched visual ticks, not promise separately
perceptible ticks for every point.

Recommendation: give each volley explicit completion accounting and a defined
expiry/cancellation policy. Trigger its final lethal emphasis when the relevant
visual damage has completed, if that is the intended meaning. Test all styles,
large volleys, low frame rates, resizing and delayed frames. Preserve immediate
game-state changes and undo semantics.

### 6. Brightening the volley weakens black's character

fire_volley forces additive contribution to at least 0.6 and enlarges every
mote with a common extra size. This makes damage easier to follow, but shifts
black smoke toward the same luminous treatment as the other styles.

Recommendation: separate visibility from material. Give dark projectiles a
rim, halo or supporting wake rather than making their body additive. Keep
colour-specific silhouettes during flight and use a common arrival emphasis
only where it helps explain the damage.

## Performance and validation

GPU-drawn dots are only part of the cost. Particle simulation is CPU-side;
each swirling particle evaluates a noise-derived flow field, and each surface
uses multiple noise layers. A six-player scene can contain hundreds of motes
before dragging or impacts. The accepted 30 Hz idle redraw policy does not by
itself establish that this workload is cheap on a tablet.

Measure idle, sustained drag, large volley and overlapping splashes on the
intended device. Record frame time and allocation behavior, and compare Motion
Off with Slow. Do not infer live rendering performance from snapshot export
time; export and offscreen drawing can have a different cost profile.

The current frame sheets omit a colourless-only panel, and their default
surface time is zero. The snapshots are useful for static appearance, but do
not validate subtle motion, all particle identities or lethal timing. Add
comparison captures for each identity alone, representative mixtures, each era,
and several animation times; assess motion live as well.

## Recommended order

1. Reduce broad texture contrast and feature size, particularly marble and
   green; make the era scale settings agree with the intended finer progression.
2. Balance miasma density and brightness across colours; remove white's merged
   bright core and make black more legible as smoke.
3. Add distinct drop, leaf and smoke profiles while retaining the shared cheap
   drawing path.
4. Align volley motion with its preview and make completion/lethal timing
   explicit, including expired particles.
5. Verify subtle motion, targeting clarity and cost on the actual tablet.

The foundation is sound: identity drives both the surface and the thing a
player throws. The remaining work is to make the surface feel like fine frame
material, and to make each thrown substance retain its character while clearly
explaining damage.
