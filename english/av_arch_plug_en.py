# av_arch_plug_en - arch closure for the Atari 2600 AV bracket
# Builds the part in Autodesk Fusion.
#
# A separate part that fills the arched notch in the console's rear edge. It goes in from
# inside the console: the body passes through the wall, the protrusion sits against the inner
# face of the wall, and the arm rests against the base of the L hook on the bracket.
# Notch measured with calipers: 5.69 wide (base) x 8.02 high, wall 3.28 thick.
# Adjust the values below and run the script again to generate a new version.
# All dimensions in millimeters.
#
# PRINTING: lay it flat with the protrusion and the arm on the bed. No supports needed.

import adsk.core, adsk.fusion, traceback

# ================= PARAMETERS (mm) =================
BODY_BASE          = 5.70   # width of the body at the base (the notch is 5.69 wide)
BODY_TOP           = 4.60   # width of the body where the round top starts
BODY_HEIGHT        = 7.75   # total height of the body (the notch is 8.02 high)
WALL               = 3.28   # length of the body = wall thickness

PROTRUSION_BASE    = 6.33   # width of the protrusion at the base
PROTRUSION_TOP     = 5.10   # width of the protrusion where its round top starts
PROTRUSION_HEIGHT  = 8.00
PROTRUSION_THICK   = 3.22   # inside, against the wall

NOTCH_WIDTH        = 5.69   # the notch in the console, used to place the arm
ARM_FROM_EDGE      = 10.70  # from the notch edge to the tip of the arm
ARM_HEIGHT         = 2.5
# the arm is as thick as the protrusion and starts 0.5 mm inside it

CHAMFER            = 0.3    # edge of the body, on the outer face (0 = none)
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

def arch(sk, base, top, height, z):
    """Closed arch centered on x = 0: base on y = 0, tapered sides, round top."""
    r = top / 2.0
    lines = sk.sketchCurves.sketchLines
    p0 = pt(sk, -base / 2.0, 0, z)
    p1 = pt(sk, base / 2.0, 0, z)
    p2 = pt(sk, r, height - r, z)
    pm = pt(sk, 0, height, z)
    p3 = pt(sk, -r, height - r, z)
    l1 = lines.addByTwoPoints(p0, p1)
    l2 = lines.addByTwoPoints(l1.endSketchPoint, p2)
    a = sk.sketchCurves.sketchArcs.addByThreePoints(l2.endSketchPoint, pm, p3)
    lines.addByTwoPoints(a.endSketchPoint, l1.startSketchPoint)

def rectangle(sk, x0, x1, y0, y1, z):
    lines = sk.sketchCurves.sketchLines
    p = [pt(sk, x0, y0, z), pt(sk, x1, y0, z), pt(sk, x1, y1, z), pt(sk, x0, y1, z)]
    first = lines.addByTwoPoints(p[0], p[1])
    prev = first
    for i in range(2, 4):
        prev = lines.addByTwoPoints(prev.endSketchPoint, p[i])
    lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)

def extrude(comp, profile, dist_mm, operation):
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(profile, operation)
    inp.setDistanceExtent(False, V(dist_mm))
    return ext.add(inp)


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
        JOIN = adsk.fusion.FeatureOperations.JoinFeatureOperation

        # 1) Protrusion: sits against the inner face of the wall (z = 0 to PROTRUSION_THICK)
        sk = comp.sketches.add(z_plane(comp, 0))
        sk.name = "Protrusion"
        arch(sk, PROTRUSION_BASE, PROTRUSION_TOP, PROTRUSION_HEIGHT, 0)
        feat = extrude(comp, sk.profiles.item(0), PROTRUSION_THICK, NEW)
        feat.bodies.item(0).name = "Arch closure"

        # 2) Arm: runs along the inner face of the wall toward the L hook
        x_start = PROTRUSION_BASE / 2.0 - 0.5
        x_end = NOTCH_WIDTH / 2.0 + ARM_FROM_EDGE
        sk = comp.sketches.add(z_plane(comp, 0))
        sk.name = "Arm"
        rectangle(sk, x_start, x_end, 0, ARM_HEIGHT, 0)
        extrude(comp, sk.profiles.item(0), PROTRUSION_THICK, JOIN)

        # 3) Body: goes through the wall, on top of the protrusion
        sk = comp.sketches.add(z_plane(comp, PROTRUSION_THICK))
        sk.name = "Body"
        arch(sk, BODY_BASE, BODY_TOP, BODY_HEIGHT, PROTRUSION_THICK)
        extrude(comp, sk.profiles.item(0), WALL, JOIN)

        # 4) Small chamfer on the outer edge of the body (optional)
        if CHAMFER > 0:
            try:
                z_top = cm(PROTRUSION_THICK + WALL)
                body = comp.bRepBodies.item(0)
                face = None
                for f in body.faces:
                    if abs(f.centroid.z - z_top) < 1e-4:
                        face = f
                        break
                if face:
                    edges = adsk.core.ObjectCollection.create()
                    for e in face.edges:
                        edges.add(e)
                    ch = comp.features.chamferFeatures
                    inp = ch.createInput2()
                    inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(edges, V(CHAMFER), True)
                    ch.add(inp)
            except:
                pass  # the chamfer is cosmetic; keep the part if it fails

        app.activeViewport.fit()
        ui.messageBox("Arch closure created! Check the dimensions and export it via "
                      "right-click on the body > Save As Mesh.")
    except:
        if ui:
            ui.messageBox("Error:\n{}".format(traceback.format_exc()))
