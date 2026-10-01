# av_bracket_pt - suporte de conectores RCA no Autodesk Fusion
# Medido com paquímetro: topo 81,0 | base 71,0 | altura 20,65 (0,813 in) |
# profundidade 24,94 embaixo e 22,00 em cima (traseira inclinada ~8°) | anel RCA 8,38 mm.
# Posições dos furos e da aba estimadas por foto. Ajuste os valores abaixo
# e rode o script de novo para gerar uma nova versão.
# Todas as medidas em milímetros.
# IMPRESSÃO: apoie na mesa a face com os furos RCA (abertura para cima).
# Com a aba recuada da borda, ative suporte só embaixo dela.

import adsk.core, adsk.fusion, traceback

# ================= PARÂMETROS (mm) =================
COMPRIMENTO_TOPO   = 81.0  # comprimento da face superior
ALTURA             = 20.65
LARGURA            = 24.94  # profundidade embaixo (face dos furos até a traseira)
PROFUNDIDADE_TOPO  = 22.0   # profundidade em cima, junto ao Atari (traseira inclinada)
INCLINACAO_ESQ     = 5.0    # quanto a base recua na ponta esquerda
INCLINACAO_DIR     = 5.0    # quanto a base recua na ponta direita (0 = reta)

FURO_DIAMETRO      = 8.4   # furo dos conectores RCA
FURO_FOLGA         = 0.3    # a impressora fecha um pouco os furos; somado ao diâmetro
FURO_QTD           = 4
FURO_PRIMEIRO_X    = 18.0   # centro do 1o furo, medido da ponta esquerda do topo
FURO_ESPACAMENTO   = 15.0   # entre centros
FURO_ALTURA_CENTRO = 10.3   # medido a partir da base
PARAFUSOS_D        = False  # True = 2 furos M3 por conector (padrão D-series, ex. Neutrik NF2D)
PARAFUSO_DIAMETRO  = 3.2
PARAFUSO_DX        = 19.0   # distância horizontal entre os 2 furos (confira no datasheet)
PARAFUSO_DY        = 24.0   # distância vertical entre os 2 furos (em diagonal)

USAR_ABERTURA      = False  # abertura quadrada (ex. S-Video); False = só furos RCA
REBAIXO_X          = 10.0  # início, medido da ponta esquerda do topo
REBAIXO_LARGURA    = 25.0
REBAIXO_Y          = 12.0   # início, medido a partir da base
REBAIXO_ALTURA     = 26.0
REBAIXO_VAZADO     = True   # True = abertura atravessando a parede; False = só rebaixo
REBAIXO_PROF       = 1.0    # usado só se REBAIXO_VAZADO = False (menor que PAREDE)

ABA_X              = 13.0   # início da aba, medido da ponta esquerda do topo
ABA_POSTE_COMP     = 2.5
ABA_POSTE_ALTURA   = 4.5
ABA_PLACA_COMP     = 16.0   # parte de cima do "L" (fica em balanço)
ABA_PLACA_ESP      = 2.5
ABA_PROFUNDIDADE   = 12.0   # medida no sentido da largura da caixa
ABA_RECUO          = 5.0   # distância da aba até a face dos furos (0 = na borda)

OCA                = True   # caixa oca, aberta na face oposta aos furos
PAREDE             = 2.0    # NÃO pode passar da espessura máxima de painel do conector
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

def poligono(sk, pontos, z):
    linhas = sk.sketchCurves.sketchLines
    p = [pt(sk, x, y, z) for (x, y) in pontos]
    primeira = linhas.addByTwoPoints(p[0], p[1])
    anterior = primeira
    for i in range(2, len(p)):
        anterior = linhas.addByTwoPoints(anterior.endSketchPoint, p[i])
    linhas.addByTwoPoints(anterior.endSketchPoint, primeira.startSketchPoint)

def extrudar(comp, perfis, dist_mm, operacao, atravessar=False):
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(perfis, operacao)
    if atravessar:
        inp.setAllExtent(adsk.fusion.ExtentDirections.SymmetricExtentDirection)
    else:
        inp.setDistanceExtent(False, V(dist_mm))
    return ext.add(inp)

def todos_perfis(sk):
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
        NOVO = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        CORTE = adsk.fusion.FeatureOperations.CutFeatureOperation
        UNIR = adsk.fusion.FeatureOperations.JoinFeatureOperation

        # 1) Corpo: perfil trapezoidal extrudado na largura
        z0 = -LARGURA / 2
        sk = comp.sketches.add(plano_z(comp, z0))
        sk.name = "Perfil do corpo"
        poligono(sk, [(INCLINACAO_ESQ, 0),
                      (COMPRIMENTO_TOPO - INCLINACAO_DIR, 0),
                      (COMPRIMENTO_TOPO, ALTURA),
                      (0, ALTURA)], z0)
        corpo_feat = extrudar(comp, sk.profiles.item(0), LARGURA, NOVO)
        corpo = corpo_feat.bodies.item(0)
        corpo.name = "Caixa"

        # 2) Oco: abre a face oposta à dos furos (fica para cima na impressão)
        if OCA:
            base = None
            for f in corpo.faces:
                if abs(f.centroid.z - cm(-LARGURA / 2)) < 1e-4:
                    base = f
                    break
            if base:
                faces = adsk.core.ObjectCollection.create()
                faces.add(base)
                sh = comp.features.shellFeatures.createInput(faces, False)
                sh.insideThickness = V(PAREDE)
                comp.features.shellFeatures.add(sh)

        # 2b) Traseira inclinada para acompanhar a traseira do Atari
        if PROFUNDIDADE_TOPO < LARGURA:
            zb0 = -LARGURA / 2                       # traseira embaixo (y = 0)
            zb1 = LARGURA / 2 - PROFUNDIDADE_TOPO    # traseira em cima (y = ALTURA)
            def zl(y):
                return zb0 + (zb1 - zb0) * y / ALTURA
            sk = comp.sketches.add(comp.yZConstructionPlane)
            sk.name = "Traseira inclinada"
            linhas = sk.sketchCurves.sketchLines
            def pyz(y, z):
                return sk.modelToSketchSpace(adsk.core.Point3D.create(0, cm(y), cm(z)))
            cantos = [pyz(-1, zl(-1)), pyz(ALTURA + 1, zl(ALTURA + 1)),
                      pyz(ALTURA + 1, zb0 - 1), pyz(-1, zb0 - 1)]
            l0 = linhas.addByTwoPoints(cantos[0], cantos[1])
            l1 = linhas.addByTwoPoints(l0.endSketchPoint, cantos[2])
            l2 = linhas.addByTwoPoints(l1.endSketchPoint, cantos[3])
            linhas.addByTwoPoints(l2.endSketchPoint, l0.startSketchPoint)
            extrudar(comp, sk.profiles.item(0), 0, CORTE, atravessar=True)

        # 3) Rebaixo retangular na face lateral da frente
        if USAR_ABERTURA:
            prof = (PAREDE + 1.0) if REBAIXO_VAZADO else REBAIXO_PROF
            zr = LARGURA / 2 - prof
            sk = comp.sketches.add(plano_z(comp, zr))
            sk.name = "Rebaixo"
            poligono(sk, [(REBAIXO_X, REBAIXO_Y),
                          (REBAIXO_X + REBAIXO_LARGURA, REBAIXO_Y),
                          (REBAIXO_X + REBAIXO_LARGURA, REBAIXO_Y + REBAIXO_ALTURA),
                          (REBAIXO_X, REBAIXO_Y + REBAIXO_ALTURA)], zr)
            extrudar(comp, sk.profiles.item(0), prof + 1.0, CORTE)

        # 4) Furos dos conectores RCA, só na parede da frente
        zf = LARGURA / 2 - PAREDE - 1.0
        sk = comp.sketches.add(plano_z(comp, zf))
        sk.name = "Furos RCA"
        raio = (FURO_DIAMETRO + FURO_FOLGA) / 2
        for i in range(FURO_QTD):
            cx = FURO_PRIMEIRO_X + i * FURO_ESPACAMENTO
            sk.sketchCurves.sketchCircles.addByCenterRadius(
                pt(sk, cx, FURO_ALTURA_CENTRO, zf), cm(raio))
            if PARAFUSOS_D:
                rp = (PARAFUSO_DIAMETRO + FURO_FOLGA) / 2
                for sx, sy in ((-1, 1), (1, -1)):
                    sk.sketchCurves.sketchCircles.addByCenterRadius(
                        pt(sk, cx + sx * PARAFUSO_DX / 2,
                           FURO_ALTURA_CENTRO + sy * PARAFUSO_DY / 2, zf), cm(rp))
        extrudar(comp, todos_perfis(sk), PAREDE + 2.0, CORTE)

        # 5) Aba em "L", recuada da borda em direção ao centro
        za = LARGURA / 2 - ABA_RECUO - ABA_PROFUNDIDADE
        sk = comp.sketches.add(plano_z(comp, za))
        sk.name = "Aba em L"
        topo_poste = ALTURA + ABA_POSTE_ALTURA
        topo_placa = topo_poste + ABA_PLACA_ESP
        poligono(sk, [(ABA_X, ALTURA),
                      (ABA_X + ABA_POSTE_COMP, ALTURA),
                      (ABA_X + ABA_POSTE_COMP, topo_poste),
                      (ABA_X + ABA_PLACA_COMP, topo_poste),
                      (ABA_X + ABA_PLACA_COMP, topo_placa),
                      (ABA_X, topo_placa)], za)
        extrudar(comp, sk.profiles.item(0), ABA_PROFUNDIDADE, UNIR)

        app.activeViewport.fit()
        ui.messageBox("Peça criada! Confira as medidas e exporte com "
                      "botão direito no corpo > Save As Mesh.")
    except:
        if ui:
            ui.messageBox("Erro:\n{}".format(traceback.format_exc()))