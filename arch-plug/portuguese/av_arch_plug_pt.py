# av_arch_plug_pt - fecho do arco para o suporte AV do Atari 2600
# Cria a peça no Autodesk Fusion.
#
# Peça separada que preenche o recorte em arco na borda traseira do console. Ela entra por
# dentro do console: o corpo atravessa a parede, a protrusão fica contra a face interna da
# parede e o braço encosta na base do gancho em L do suporte.
# Recorte medido com paquímetro: 5,69 de largura (base) x 8,02 de altura, parede de 3,28.
# Ajuste os valores abaixo e rode o script de novo para gerar uma nova versão.
# Todas as medidas em milímetros.
#
# IMPRESSÃO: deite a peça, com a protrusão e o braço na mesa. Não precisa de suporte.

import adsk.core, adsk.fusion, traceback

# ================= PARÂMETROS (mm) =================
CORPO_BASE         = 5.70   # largura do corpo na base (o recorte tem 5,69)
CORPO_TOPO         = 4.60   # largura do corpo onde começa o topo arredondado
CORPO_ALTURA       = 7.75   # altura total do corpo (o recorte tem 8,02)
PAREDE             = 3.28   # comprimento do corpo = espessura da parede

PROTRUSAO_BASE     = 6.33   # largura da protrusão na base
PROTRUSAO_TOPO     = 5.10   # largura da protrusão onde começa o topo arredondado
PROTRUSAO_ALTURA   = 8.00
PROTRUSAO_ESPESSURA = 3.22  # por dentro, contra a parede

RECORTE_LARGURA    = 5.69   # o recorte no console, usado para posicionar o braço
BRACO_DA_BORDA     = 10.70  # da borda do recorte até a ponta do braço
BRACO_ALTURA       = 2.5
# o braço tem a mesma espessura da protrusão e começa 0,5 mm dentro dela

CHANFRO            = 0.3    # aresta do corpo, na face de fora (0 = sem chanfro)
# ===================================================


def cm(v):
    return v / 10.0  # a API do Fusion trabalha em centímetros

def V(mm):
    return adsk.core.ValueInput.createByReal(cm(mm))

def plano_z(comp, z_mm):
    """Plano paralelo ao XY na altura z (mm)."""
    if abs(z_mm) < 1e-9:
        return comp.xYConstructionPlane
    inp = comp.constructionPlanes.createInput()
    inp.setByOffset(comp.xYConstructionPlane, V(z_mm))
    return comp.constructionPlanes.add(inp)

def pt(sk, x, y, z):
    return sk.modelToSketchSpace(adsk.core.Point3D.create(cm(x), cm(y), cm(z)))

def arco(sk, base, top, height, z):
    """Arco fechado centrado em x = 0: base em y = 0, laterais afuniladas, topo redondo."""
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

def retangulo(sk, x0, x1, y0, y1, z):
    lines = sk.sketchCurves.sketchLines
    p = [pt(sk, x0, y0, z), pt(sk, x1, y0, z), pt(sk, x1, y1, z), pt(sk, x0, y1, z)]
    first = lines.addByTwoPoints(p[0], p[1])
    prev = first
    for i in range(2, 4):
        prev = lines.addByTwoPoints(prev.endSketchPoint, p[i])
    lines.addByTwoPoints(prev.endSketchPoint, first.startSketchPoint)

def extrudar(comp, profile, dist_mm, operation):
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
        NOVO = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        UNIR = adsk.fusion.FeatureOperations.JoinFeatureOperation

        # 1) Protrusão: fica contra a face interna da parede (z = 0 até PROTRUSAO_ESPESSURA)
        sk = comp.sketches.add(plano_z(comp, 0))
        sk.name = "Protrusao"
        arco(sk, PROTRUSAO_BASE, PROTRUSAO_TOPO, PROTRUSAO_ALTURA, 0)
        feat = extrudar(comp, sk.profiles.item(0), PROTRUSAO_ESPESSURA, NOVO)
        feat.bodies.item(0).name = "Fecho do arco"

        # 2) Braço: corre rente à face interna da parede, em direção ao gancho em L
        x_ini = PROTRUSAO_BASE / 2.0 - 0.5
        x_fim = RECORTE_LARGURA / 2.0 + BRACO_DA_BORDA
        sk = comp.sketches.add(plano_z(comp, 0))
        sk.name = "Braco"
        retangulo(sk, x_ini, x_fim, 0, BRACO_ALTURA, 0)
        extrudar(comp, sk.profiles.item(0), PROTRUSAO_ESPESSURA, UNIR)

        # 3) Corpo: atravessa a parede, em cima da protrusão
        sk = comp.sketches.add(plano_z(comp, PROTRUSAO_ESPESSURA))
        sk.name = "Corpo"
        arco(sk, CORPO_BASE, CORPO_TOPO, CORPO_ALTURA, PROTRUSAO_ESPESSURA)
        extrudar(comp, sk.profiles.item(0), PAREDE, UNIR)

        # 4) Chanfro pequeno na aresta de fora do corpo (opcional)
        if CHANFRO > 0:
            try:
                z_top = cm(PROTRUSAO_ESPESSURA + PAREDE)
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
                    inp.chamferEdgeSets.addEqualDistanceChamferEdgeSet(edges, V(CHANFRO), True)
                    ch.add(inp)
            except:
                pass  # o chanfro é estético; se falhar, a peça é mantida

        app.activeViewport.fit()
        ui.messageBox("Fecho do arco criado! Confira as medidas e exporte com "
                      "botão direito no corpo > Save As Mesh.")
    except:
        if ui:
            ui.messageBox("Erro:\n{}".format(traceback.format_exc()))
