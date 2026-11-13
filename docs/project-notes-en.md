# Project notes: Atari 2600 AV-mod RCA bracket (Autodesk Fusion + 3D printing)

Working notes for a small 3D-printed bracket that holds the jacks of an Atari 2600 AV mod. I'm new to Fusion, digital calipers and Git, so these notes include the menu paths and steps I had to figure out along the way.

**Setup:** Mac, Creality Ender 5 S1 (0.4 mm nozzle, 220×220×280 mm build volume, textured PEI bed), PLA, sliced in Creality Print.

The STL files in the `exports/` folders are the main deliverable. The Fusion scripts (`av_bracket_4h_en`, `av_bracket_3h_en`, `av_bracket_svideo_en`, `av_bracket_recessed_en`, `av_bracket_din5_en` and `av_arch_plug_en`, in `4-holes/`, `3-holes/`, `3rca-1svideo/`, `3-holes-recessed/`, `1din5-1rca/` and `arch-plug/`) are kept only for convenience and as a reference for the geometry. The STL files were later generated directly, without Fusion, and the scripts have only been syntax-checked.

## Goal

Reproduce a small 3D-printed bracket that clips under the back of an **Atari 2600** and holds the jacks of an **AV mod**. The original I'm copying holds 1 S-Video and 3 RCA jacks. **My first version replaces the S-Video cutout with a 4th RCA hole, so it has 4 identical RCA holes.** The repository later grew other versions of the same case (3 holes, 3 RCA + 1 S-Video, a recessed one, and a 5-pin DIN + RCA one). The flat ribbon cable from the mod runs into the bracket through an opening in the top face, and an "L" hook next to that opening locks the bracket to the console.

## How the part is built

The geometry is described by a **Fusion Python script** (not modeled by hand), which is kept as a reference. It runs from *Utilities > Add-Ins > Scripts and Add-Ins* (Shift+S), opens a new design and builds parametric timeline features in this order. Lengths along x are measured from the original x = 0 end, which is the end with the opening (the right end when you look from above with the RCA face at the top).

1. **Body:** a trapezoid sketched on the XY plane (length × height) and extruded along Z (depth). The top is 76.2 mm and the base 66.2 mm, because both ends slant 5 mm (85.2 and 75.2 mm in the 4-hole and S-Video versions). `TRIM_END` (4.8 mm) shortens the part at the opening end without moving anything else.
2. **Shell:** 2 mm walls. The removed face is the **back** (opposite the holes), so the box is open at the back.
3. **Slanted back:** a wedge cut on the YZ plane so the depth goes from 24.89 mm at the bottom to 19.30 mm at the top (~15.5°). This matches the slanted rear of the Atari case. The narrow side is at the top, against the Atari.
4. **Optional square cutout:** a generic square cutout in the front wall, off by default (`USE_CUTOUT = False`). The `3rca-1svideo` version has its own round S-Video hole (`USE_SVIDEO`).
5. **4 RCA holes** (3 in the `3-holes` version, with 11.27 mm gaps; 3 RCA + 1 S-Video in `3rca-1svideo`, with the S-Video hole at the opening end; 3 widened 12.0 mm holes in the recessed version; 1 RCA hole plus the DIN holes in `1din5-1rca`): cut through the front wall only. `DISTRIBUTE_HOLES` spaces them evenly at hole height, with equal gaps between holes and between the holes and the slanted ends. It is on only in the 3-hole version. In the 4-hole and S-Video versions the centers are set by hand (`FIRST_HOLE_X`, `HOLE_SPACING`, and `SVIDEO_SPACING`).
6. **Top opening:** a 12.10 × 12.10 mm square cut through the top wall, for the cable. `USE_OPEN_ARM` can add an arm toward the end, which is off.
7. **L hook:** it starts at the opening's 12.10 mm edge on the center side and runs toward the center. The post is 2.5 mm long and 3.10 mm tall, the plate 9.15 mm long and 2.5 mm thick, and the hook is 6 mm wide, centered on that edge.

## Current parameters (mm)

| Parameter | Value | Source |
|---|---|---|
| TOP_LENGTH / TRIM_END | 81.0 / 4.8 (top = 76.2). 90.0 / 4.8 (top = 85.2) in the 4-hole and S-Video versions | measured |
| bottom length | 66.2 | derived (5 mm slant each end) |
| LEFT_SLANT / RIGHT_SLANT | 5.0 / 5.0 | derived from the first 81 vs 71 measurement |
| HEIGHT | 20.21 | measured |
| DEPTH (bottom) | 24.89 | measured |
| TOP_DEPTH | 19.30 | measured |
| WALL | 2.0 | chosen |
| HOLE_DIAMETER / HOLE_CLEARANCE | 8.4 / 0.3 | measured RCA ring 8.38; printed holes shrink |
| HOLE_COUNT | 4 (3 in the `3-holes`, `3rca-1svideo` and recessed versions, 1 RCA in the DIN version) | my choice |
| holes (DISTRIBUTE_HOLES) | 4 holes: centers at x = 18.93 / 37.91 / 56.89 / 75.87 (18.98 spacing). 3 holes: 22.93 / 42.90 / 62.87. 3 RCA + 1 S-Video: 19.41 (S-Video) / 38.73 / 57.46 / 76.19 | calculated |
| recessed version | Front holes 12.0 at x = 22.9 / 42.9 / 62.9 (20.0 pitch), HOLE_CENTER_Y 9.905. Inner panel: PANEL_FROM_FRONT 9.0, PANEL_THICK 3.0, PANEL_X 16.35, PANEL_WIDTH 53.0, PANEL_HOLE_DIAMETER 6.57, PANEL_BEVEL 7.58 | taken from the STL by Jonatã Mariani (see the credits in `3-holes-recessed/README.md`) |
| DIN version | `1din5-1rca/`: DIN hole 15.3 (15 + 0.3) at x = 34.1, M3 holes 3.5 (3.2 + 0.3) at x = 23.4 / 44.8 (21.4 pitch), RCA 8.7 at x = 58.0, length 76.2 | from retailer listings and a product photo, not measured |
| SVIDEO_DIAMETER | 10.0 + 0.3 clearance, at the x = 0 end (`3rca-1svideo` version) | from retailer listings, not measured on my jack |
| HOLE_CENTER_Y | 10.1 | vertically centered |
| OPEN_FROM_FRONT / OPEN_FROM_RIGHT | 2.70 / 9.30 (4.50 from the trimmed end) | measured |
| OPEN_WIDTH / OPEN_DEPTH | 12.10 / 12.10 | measured |
| TAB_PLATE_LENGTH / TAB_POST_LENGTH | 9.15 / 2.5 | measured / chosen |
| TAB_POST_HEIGHT / TAB_PLATE_THICK | 3.10 / 2.5 | measured / chosen |
| TAB_DEPTH | 6.0, centered on the opening edge (front at 5.75 from the front edge) | measured |
| D_SERIES_SCREWS | False | the jacks press-fit (or, in the recessed version, screw onto the inner panel), no extra screws |

Clearances were checked on the generated model: the L hook (z from the front edge 5.75 to 11.75 mm) and the opening (2.70 to 14.80 mm) stay 4.50 mm in front of the slanted back at the top.

## Important context and lessons learned

- **In the press-fit versions the RCA jacks only press-fit into the holes.** Hole size is the most critical fit. A small test plate with holes at 8.2 / 8.4 / 8.6 mm is a good idea before reprinting the whole part.
- **Early estimates were about 2× too big** (150 mm long) because I worked from screenshots without scale. All dimensions are now real caliper measurements.
- **Top-view orientation trap:** looking from above with the RCA face at the top, the opening end is on the *right*. Looking at the RCA face, it is on the *left*. Parameters named "right" refer to the top view.
- **Caliper units:** once the display was accidentally in inches ("in" shown on the display). My caliper's **mm/in/F** button changes units. Always check that "mm" is shown, and zero the caliper with the jaws closed.
- **The first print didn't fit perfectly** because the Atari's back is slanted. That was fixed with the slanted-back cut (TOP_DEPTH). If it's still slightly off, adjust TOP_DEPTH in 0.5 mm steps.
- **Script assumptions** I haven't confirmed: both ends slant equally, and the narrow (19.30 mm) side is at the top, against the Atari.

## Printing setup

- Orientation: **RCA-hole face down on the bed**, open back facing up. The holes come out round with no support.
- **No supports needed** for the press-fit versions. The L hook has the same cross-section along the print direction, so it prints without them. The recessed version has an inner panel that is a bridge of about 16 mm, which was printed and validated by Jonatã Mariani (his support and cooling settings are not recorded). Check the layer preview for the 12.10 mm bridge over the opening.
- PLA starting point: 0.2 mm layers, 200–210 °C nozzle, 60 °C bed, 3 walls, 15–20% infill. A brim helps the first layers.

## Fusion how-tos we already solved

- **Run a script:** Shift+S → select the script → Run.
- **Add a script from a folder** (for example a Git repo): Shift+S → **+** → add an existing script from the computer. The folder name, `.py` and `.manifest` must all have the same name. Scripts live in `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/` (Finder: Cmd+Shift+G).
- **Export STL:** right-click the body **Bracket** in the Browser → **Save As Mesh** → STL (Binary), Millimeter, Refinement High. In *Utilities > Make > 3D Print*, the OK button stays greyed out unless **Preparation Type = Save to Local File**.
- **Rename or delete a script:** create a new script with the desired name and paste the code in, or rename or delete the folder in the Scripts directory.

## Repository

**Name:** `atari-2600-av-bracket`

> 3D-printable bracket for the Atari 2600 AV mod. Mounts RCA, S-Video or 5-pin DIN jacks at the rear of the console. Ready-to-print STL files, with optional Autodesk Fusion scripts.

**Topics:** `atari-2600`, `av-mod`, `3d-printing`, `fusion360`, `retro-gaming`, `rca`

```
atari-2600-av-bracket/
├── 4-holes/          english/, portuguese/ (av_bracket_4h scripts), exports/ (av_bracket_4h_print.stl, .stl, .step)
├── 3-holes/          english/, portuguese/ (av_bracket_3h scripts), exports/ (av_bracket_3h_print.stl, .stl, .step)
├── 3rca-1svideo/     english/, portuguese/ (av_bracket_svideo scripts), exports/ (av_bracket_svideo_print.stl, .stl, .step)
├── 3-holes-recessed/ english/, portuguese/ (av_bracket_recessed scripts), exports/ (av_bracket_recessed_print.stl, .stl, .step)
├── 1din5-1rca/       english/, portuguese/ (av_bracket_din5 scripts), exports/ (av_bracket_din5_print.stl, .stl, .step)
├── arch-plug/        english/, portuguese/ (av_arch_plug scripts), exports/ (av_arch_plug.stl, .step)
├── docs/
└── README.md
```

## Longer 4-hole and S-Video versions

The first prints of the 4-hole version had the jack nuts almost touching: the hex nuts are 14.82 mm across the corners and the spacing was 15.98 mm, a gap of 1.2 mm. The ground solder lug of each jack also reaches 17.70 mm from its center, so it reached the neighbor's nut. Both versions were made 9 mm longer (`TOP_LENGTH` 90.0), extended only on the side opposite the L hook, which gives a gap of about 4.2 mm between nuts in the 4-hole version (spacing 18.98 mm). In the S-Video version the S-Video nut was not measured. I assumed 16 mm across the corners and set the spacings to get a gap of about 3.9 mm (19.32 mm from the S-Video to the first RCA, 18.73 mm between RCA). The lugs are bent 90° toward the open back, because straight lugs would need a spacing of about 25 mm. The S-Video hole stays at 10.3 mm, the smallest size found (10 mm plus 0.3 mm clearance), and it is provisional until validated with a real jack: it can be enlarged with a rotary tool. The sizes in retailer listings range from 10 to 11 mm, and one chassis-mount jack lists a 9/16 in (14.3 mm) hole, so it must be checked against the real jack.

## Recessed version (inner mounting panel)

`3-holes-recessed/` keeps the 3-hole case but widens the front holes to 12.0 mm and adds a 3.0 mm panel inside, 9.0 mm behind the RCA face. The jacks are screwed to the panel through 6.57 mm holes, so the plugs sit recessed. The panel spans the full height of the cavity and is joined to the top and bottom walls. Its corner next to the top opening has a 45° bevel of 7.58 mm, so the panel does not block the cable path.

This version was designed by Jonatã Mariani, from the YouTube channel [Veim dos Game](https://www.youtube.com/c/VeimdosGame), based on the original version of this project. The STL came from his design, made outside the Fusion script. It had the panel as a second shell overlapping the walls, so the print STL was merged into a single solid (volume 11333.6 mm³). The STEP is rebuilt from the parameters and matches it within about 2 mm³. The scripts follow the same parameters but have not been run in Fusion. The 12.0 and 6.57 mm sizes are design values, not from a datasheet.

## 5-pin DIN + RCA version

`1din5-1rca/` keeps the 3-hole case and holds one 5-pin DIN jack (180°, the type used for the Atari 800 monitor port) plus one RCA jack. A threaded nut does not fit in the 16.2 mm inner height, so it uses the flange-mount type: a 15 mm body hole and two M3 screws 21.4 mm apart (figures from a Maplin listing). The flange is estimated at 27 × 18 mm from a PUREVOLT A-1462-5 photo, which leaves about 1 mm above and below it on the 20.21 mm face, and about 2.8 mm to the RCA nut. The pair is centered on the face. This version has not been printed and the flange was not measured, so check it against the real jack first. In the scripts, `USE_DIN` adds the DIN and screw holes to the same sketch as the RCA hole.

## Arch closure

A separate part that fills the arched notch in the console's rear edge. It goes in from inside, and its arm rests against the base of the L hook, which locks the bracket in place. Files: `arch-plug/exports/av_arch_plug.stl` and the Fusion script `av_arch_plug_en`. It is shared by all the bracket versions.

- Body: 5.70 base, 4.60 top, 7.75 high, 3.28 long. The notch is 5.69 × 8.02, so the clearance in width is about 0.01 mm. Sand if needed.
- Protrusion: 6.33 × 8.00, 3.22 thick, against the inner face of the wall.
- Arm: 10.70 from the notch edge, 2.5 high, 3.22 thick.
- Whole part: 16.71 × 8.00 × 6.50, printed flat with no supports.

## Open next steps

1. Fine-tune the hole fit for the press-fit RCA jacks with a test plate (8.2 / 8.4 / 8.6 mm).
2. Test-print the S-Video version and check the 10.3 mm hole against the real jack.
3. Test-print the DIN version and check the flange against the real jack.
4. Optionally add embossed labels under each jack, like the original's "Y", "C", "Audio".
