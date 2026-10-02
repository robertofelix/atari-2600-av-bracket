# av_bracket_en - 3D-printable RCA jack bracket for the Atari 2600 AV mod
# Builds the part in Autodesk Fusion.
#
# Measured with calipers: top 81.0 | bottom 71.0 | height 20.21 (0.796 in) |
# depth 24.89 at the bottom and 20.41 at the top (slanted back, ~12.5 deg) | RCA ring 8.38 mm.
# Hole and tab positions were estimated from photos. Adjust the values below
# and run the script again to generate a new version.
# All dimensions in millimeters.
#
# PRINTING: place the face with the RCA holes on the bed (open side up).
# Since the tab is set back from the edge, enable supports only under it.

import adsk.core, adsk.fusion, traceback

# ================= PARAMETERS (mm) =================
TOP_LENGTH         = 81.0   # length of the top face
HEIGHT             = 20.21
DEPTH              = 24.89  # depth at the bottom (hole face to back)
TOP_DEPTH          = 20.41  # depth at the top, against the Atari (slanted back)
LEFT_SLANT         = 5.0    # how far the bottom is inset at the left end
RIGHT_SLANT        = 5.0    # how far the bottom is inset at the right end (0 = straight)

HOLE_DIAMETER      = 8.4    # RCA jack hole
HOLE_CLEARANCE     = 0.3    # printers shrink holes slightly; added to the diameter
HOLE_COUNT         = 4
FIRST_HOLE_X       = 18.0   # center of the 1st hole, from the left end of the top
HOLE_SPACING       = 15.0   # center to center
HOLE_CENTER_Y      = 10.1   # measured from the bottom
D_SERIES_SCREWS    = False  # True = 2 M3 holes per jack (D-series, e.g. Neutrik NF2D)
SCREW_DIAMETER     = 3.2
SCREW_DX           = 19.0   # horizontal distance between the 2 holes (check datasheet)
SCREW_DY           = 24.0   # vertical distance between the 2 holes (diagonal)

USE_CUTOUT         = False  # square cutout (e.g. S-Video); False = RCA holes only
CUTOUT_X           = 10.0   # start, from the left end of the top
CUTOUT_WIDTH       = 25.0
CUTOUT_Y           = 12.0   # start, measured from the bottom
CUTOUT_HEIGHT      = 26.0
CUTOUT_THROUGH     = True   # True = opening through the wall; False = shallow pocket
CUTOUT_DEPTH       = 1.0    # only used if CUTOUT_THROUGH = False (less than WALL)

TAB_X              = 13.0   # tab start, from the left end of the top
TAB_POST_LENGTH    = 2.5
TAB_POST_HEIGHT    = 4.5
TAB_PLATE_LENGTH   = 16.0   # upper part of the "L" (overhang)
TAB_PLATE_THICK    = 2.5
TAB_DEPTH          = 12.0   # measured along the depth of the box
TAB_INSET          = 5.0    # distance from the tab to the hole face (0 = flush)

HOLLOW             = True   # hollow box, open on the face opposite the holes
WALL               = 2.0    # must NOT exceed the jack's maximum panel thickness
# ===================================================


def cm(v):
    return v / 10.0  # the Fusion API works in centimeters

def V(mm):
    return adsk.core.ValueInput.createByReal(cm(mm))

def z_plane(comp, z_mm):
    """Plane parallel to XY at height z (mm)."""
    if abs(z_mm) < 1e-9:
        return comp.xYConstructionPlane
    inp = comp.constructionPlanes.createInput()
    inp.setByOffset(comp.xYConstructionPlane, V(z_mm))
    return comp.constructionPlanes.add(inp)

def pt(sk, x, y, z):
    return sk.modelToSketchSpace(adsk.core.Point3D.create(cm(x), cm(y), cm(z)))

def polygon(sk, points, z):
    lines = sk.sketchCurves.sketchLines
    p = [pt(sk, x, y, z) for (x, y) in points]
    first = lines.addByTwoPoints(p[0], p[1])
    prev = first
    for i in range(2, len(p)):
        prev = lines.addByTwoPoints(prev.endSketchPoint, p[i])
    lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)

def extrude(comp, profiles, dist_mm, operation, through_all=False):
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(profiles, operation)
    if through_all:
        inp.setAllExtent(adsk.fusion.ExtentDirections.SymmetricExtentDirection)
    else:
        inp.setDistanceExtent(False, V(dist_mm))
    return ext.add(inp)

def all_profiles(sk):
    col = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        col.add(sk.profiles.item(i))
    return col


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        comp = design.rootComponent
        NEW = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        CUT = adsk.fusion.FeatureOperations.CutFeatureOperation
        JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation

        # 1) Body: trapezoidal profile extruded along the depth
        z0 = -DEPTH / 2
        sk = comp.sketches.add(z_plane(comp, z0))
        sk.name = "Body profile"
        polygon(sk, [(LEFT_SLANT, 0),
                     (TOP_LENGTH - RIGHT_SLANT, 0),
                     (TOP_LENGTH, HEIGHT),
                     (0, HEIGHT)], z0)
        body_feat = extrude(comp, sk.profiles.item(0), DEPTH, NEW)
        body = body_feat.bodies.item(0)
        body.name = "Bracket"

        # 2) Hollow: open the face opposite the holes (faces up when printing)
        if HOLLOW:
            back = None
            for f in body.faces:
                if abs(f.centroid.z - cm(-DEPTH / 2)) < 1e-4:
                    back = f
                    break
            if back:
                faces = adsk.core.ObjectCollection.create()
                faces.add(back)
                sh = comp.features.shellFeatures.createInput(faces, False)
                sh.insideThickness = V(WALL)
                comp.features.shellFeatures.add(sh)

        # 2b) Slanted back to match the back of the Atari
        if TOP_DEPTH < DEPTH:
            zb0 = -DEPTH / 2                  # back at the bottom (y = 0)
            zb1 = DEPTH / 2 - TOP_DEPTH       # back at the top (y = HEIGHT)
            def zl(y):
                return zb0 + (zb1 - zb0) * y / HEIGHT
            sk = comp.sketches.add(comp.yZConstructionPlane)
            sk.name = "Slanted back"
            lines = sk.sketchCurves.sketchLines
            def pyz(y, z):
                return sk.modelToSketchSpace(adsk.core.Point3D.create(0, cm(y), cm(z)))
            corners = [pyz(-1, zl(-1)), pyz(HEIGHT + 1, zl(HEIGHT + 1)),
                       pyz(HEIGHT + 1, zb0 - 1), pyz(-1, zb0 - 1)]
            l0 = lines.addByTwoPoints(corners[0], corners[1])
            l1 = lines.addByTwoPoints(l0.endSketchPoint, corners[2])
            l2 = lines.addByTwoPoints(l1.endSketchPoint, corners[3])
            lines.addByTwoPoints(l2.endSketchPoint, l0.startSketchPoint)
            extrude(comp, sk.profiles.item(0), 0, CUT, through_all=True)

        # 3) Optional square cutout on the front face
        if USE_CUTOUT:
            depth = (WALL + 1.0) if CUTOUT_THROUGH else CUTOUT_DEPTH
            zc = DEPTH / 2 - depth
            sk = comp.sketches.add(z_plane(comp, zc))
            sk.name = "Cutout"
            polygon(sk, [(CUTOUT_X, CUTOUT_Y),
                         (CUTOUT_X + CUTOUT_WIDTH, CUTOUT_Y),
                         (CUTOUT_X + CUTOUT_WIDTH, CUTOUT_Y + CUTOUT_HEIGHT),
                         (CUTOUT_X, CUTOUT_Y + CUTOUT_HEIGHT)], zc)
            extrude(comp, sk.profiles.item(0), depth + 1.0, CUT)

        # 4) RCA jack holes, front wall only
        zf = DEPTH / 2 - WALL - 1.0
        sk = comp.sketches.add(z_plane(comp, zf))
        sk.name = "RCA holes"
        radius = (HOLE_DIAMETER + HOLE_CLEARANCE) / 2
        for i in range(HOLE_COUNT):
            cx = FIRST_HOLE_X + i * HOLE_SPACING
            sk.sketchCurves.sketchCircles.addByCenterRadius(
                pt(sk, cx, HOLE_CENTER_Y, zf), cm(radius))
            if D_SERIES_SCREWS:
                rs = (SCREW_DIAMETER + HOLE_CLEARANCE) / 2
                for sx, sy in ((-1, 1), (1, -1)):
                    sk.sketchCurves.sketchCircles.addByCenterRadius(
                        pt(sk, cx + sx * SCREW_DX / 2,
                           HOLE_CENTER_Y + sy * SCREW_DY / 2, zf), cm(rs))
        extrude(comp, all_profiles(sk), WALL + 2.0, CUT)

        # 5) "L" tab, set back from the edge toward the center
        zt = DEPTH / 2 - TAB_INSET - TAB_DEPTH
        sk = comp.sketches.add(z_plane(comp, zt))
        sk.name = "L tab"
        post_top = HEIGHT + TAB_POST_HEIGHT
        plate_top = post_top + TAB_PLATE_THICK
        polygon(sk, [(TAB_X, HEIGHT),
                     (TAB_X + TAB_POST_LENGTH, HEIGHT),
                     (TAB_X + TAB_POST_LENGTH, post_top),
                     (TAB_X + TAB_PLATE_LENGTH, post_top),
                     (TAB_X + TAB_PLATE_LENGTH, plate_top),
                     (TAB_X, plate_top)], zt)
        extrude(comp, sk.profiles.item(0), TAB_DEPTH, JOIN)

        app.activeViewport.fit()
        ui.messageBox("Bracket created! Check the dimensions and export it via "
                      "right-click on the body > Save As Mesh.")
    except:
        if ui:
            ui.messageBox("Error:\n{}".format(traceback.format_exc()))
