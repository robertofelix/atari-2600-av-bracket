# av_bracket_pt - suporte de conectores RCA no Autodesk Fusion
# Medido com paquímetro: topo 81,0 | base 71,0 | altura 20,21 (0,796 in) |
# profundidade 24,89 embaixo e 19,30 em cima (traseira inclinada ~15,5°) | anel RCA 8,38 mm.
# Posições dos furos e da aba estimadas por foto. Ajuste os valores abaixo
# e rode o script de novo para gerar uma nova versão.
# Todas as medidas em milímetros.
# IMPRESSÃO: apoie na mesa a face com os furos RCA (abertura para cima).
# Ative suporte só embaixo da placa da aba em L.

import adsk.core, adsk.fusion, traceback

# ================= PARÂMETROS (mm) =================
COMPRIMENTO_TOPO   = 81.0  # comprimento da face superior, antes de ENCURTAR_PONTA
ENCURTAR_PONTA     = 4.8   # encurta a peça na ponta da abertura (x = 0). A inclinação de 5 mm da ponta anda para dentro sem mudar
ALTURA             = 20.21
LARGURA            = 24.89  # profundidade embaixo (face dos furos até a traseira)
PROFUNDIDADE_TOPO  = 19.30  # profundidade em cima, junto ao Atari (traseira inclinada)
INCLINACAO_ESQ     = 5.0    # quanto a base recua na ponta esquerda
INCLINACAO_DIR     = 5.0    # quanto a base recua na ponta direita (0 = reta)

FURO_DIAMETRO      = 8.4   # furo dos conectores RCA
FURO_FOLGA         = 0.3    # a impressora fecha um pouco os furos; somado ao diâmetro
FURO_QTD           = 4
DISTRIBUIR_FUROS   = True   # True = folgas iguais entre os furos e as pontas inclinadas, na altura dos furos
FURO_PRIMEIRO_X    = 18.0   # só se DISTRIBUIR_FUROS = False: centro do 1o furo, medido da ponta x = 0
FURO_ESPACAMENTO   = 15.0   # só se DISTRIBUIR_FUROS = False: entre centros
FURO_ALTURA_CENTRO = 10.1   # medido a partir da base
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

USAR_ABERTURA_TOPO = True   # abertura na face de cima (caminho do cabo), veja o desenho no README
ABERTURA_DA_FRENTE = 2.70   # da borda da frente (face RCA) até o lado perto do quadrado
ABERTURA_LARGURA   = 12.10  # quadrado, no comprimento (esquerda para direita)
ABERTURA_PROF      = 12.10  # quadrado, na profundidade (frente para trás)
ABERTURA_DA_DIREITA = 9.30  # da ponta da peça até o lado do quadrado mais perto dela (a ponta x = 0: a DIREITA vista de cima com a face RCA no topo, a ESQUERDA de frente para a face RCA)
USAR_BRACO         = False  # False = só o quadrado (a ponta fica fechada). True = com o braço até a ponta
ABERTURA_BRACO_PROF = 5.66  # braço para a direita, medido de frente para trás (começa no lado da frente do quadrado)
ABERTURA_BRACO_FIM = 3.45   # da mesma ponta até o fim do braço

USAR_ABA           = True   # aba em L (gancho de encaixe na face de cima)
ABA_POSTE_COMP     = 2.5
ABA_POSTE_ALTURA   = 3.10
ABA_PLACA_COMP     = 9.15   # parte de cima do "L" (fica em balanço)
ABA_PLACA_ESP      = 2.5
ABA_PROFUNDIDADE   = 6.0    # medida no sentido da largura da caixa; centralizada na aresta de 12,10 mm da abertura
# A aba acompanha a abertura: começa na aresta esquerda de 12,10 mm da abertura e
# segue para o centro, sobre a face de cima. A frente dela fica alinhada com a da abertura.

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


def plano_xz(comp, y_mm):
    """Plano paralelo ao XZ na altura y (mm). Confere o sentido do deslocamento."""
    for sinal in (1, -1):
        inp = comp.constructionPlanes.createInput()
        inp.setByOffset(comp.xZConstructionPlane, V(sinal * y_mm))
        plano = comp.constructionPlanes.add(inp)
        if abs(plano.geometry.origin.y - cm(y_mm)) < 1e-4:
            return plano
        plano.deleteMe()
    raise RuntimeError("Não foi possível posicionar o plano XZ em y = %s mm" % y_mm)

def poligono_xz(sk, pontos, y):
    """Polígono fechado com pontos (x, z) no plano na altura y (mm)."""
    linhas = sk.sketchCurves.sketchLines
    p = [sk.modelToSketchSpace(adsk.core.Point3D.create(cm(x), cm(y), cm(z)))
         for (x, z) in pontos]
    primeira = linhas.addByTwoPoints(p[0], p[1])
    anterior = primeira
    for i in range(2, len(p)):
        anterior = linhas.addByTwoPoints(anterior.endSketchPoint, p[i])
    linhas.addByTwoPoints(anterior.endSketchPoint, primeira.startSketchPoint)

def extrudar_simetrico(comp, perfis, total_mm, operacao):
    ext = comp.features.extrudeFeatures
    inp = ext.createInput(perfis, operacao)
    inp.setSymmetricExtent(V(total_mm), True)
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
        CORTE = adsk.fusion.FeatureOperations.CutFeatureOperation
        UNIR = adsk.fusion.FeatureOperations.JoinFeatureOperation

        # 1) Corpo: perfil trapezoidal extrudado na largura
        z0 = -LARGURA / 2
        sk = comp.sketches.add(plano_z(comp, z0))
        sk.name = "Perfil do corpo"
        poligono(sk, [(ENCURTAR_PONTA + INCLINACAO_ESQ, 0),
                      (COMPRIMENTO_TOPO - INCLINACAO_DIR, 0),
                      (COMPRIMENTO_TOPO, ALTURA),
                      (ENCURTAR_PONTA, ALTURA)], z0)
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
        if DISTRIBUIR_FUROS:
            # largura útil na altura dos centros dos furos (as pontas são inclinadas)
            borda_e = ENCURTAR_PONTA + INCLINACAO_ESQ * (1 - FURO_ALTURA_CENTRO / ALTURA)
            borda_d = COMPRIMENTO_TOPO - INCLINACAO_DIR * (1 - FURO_ALTURA_CENTRO / ALTURA)
            d = FURO_DIAMETRO + FURO_FOLGA
            folga = (borda_d - borda_e - FURO_QTD * d) / (FURO_QTD + 1)
            furo_x = [borda_e + folga + d / 2 + i * (d + folga) for i in range(FURO_QTD)]
        else:
            furo_x = [FURO_PRIMEIRO_X + i * FURO_ESPACAMENTO for i in range(FURO_QTD)]
        for i in range(FURO_QTD):
            cx = furo_x[i]
            sk.sketchCurves.sketchCircles.addByCenterRadius(
                pt(sk, cx, FURO_ALTURA_CENTRO, zf), cm(raio))
            if PARAFUSOS_D:
                rp = (PARAFUSO_DIAMETRO + FURO_FOLGA) / 2
                for sx, sy in ((-1, 1), (1, -1)):
                    sk.sketchCurves.sketchCircles.addByCenterRadius(
                        pt(sk, cx + sx * PARAFUSO_DX / 2,
                           FURO_ALTURA_CENTRO + sy * PARAFUSO_DY / 2, zf), cm(rp))
        extrudar(comp, todos_perfis(sk), PAREDE + 2.0, CORTE)

        # 4b) Abertura na face de cima: um quadrado mais um braço até perto da ponta direita
        if USAR_ABERTURA_TOPO:
            z_perto = LARGURA / 2 - ABERTURA_DA_FRENTE
            x_ponta = ABERTURA_DA_DIREITA          # lado do quadrado mais perto da ponta (x = 0)
            x_centro = x_ponta + ABERTURA_LARGURA  # lado do quadrado voltado para o centro
            x_braco = ABERTURA_BRACO_FIM           # fim do braço
            y_meio = ALTURA - PAREDE / 2
            sk = comp.sketches.add(plano_xz(comp, y_meio))
            sk.name = "Abertura de cima"
            if USAR_BRACO:
                contorno = [(x_centro, z_perto), (x_braco, z_perto),
                            (x_braco, z_perto - ABERTURA_BRACO_PROF), (x_ponta, z_perto - ABERTURA_BRACO_PROF),
                            (x_ponta, z_perto - ABERTURA_PROF), (x_centro, z_perto - ABERTURA_PROF)]
            else:
                contorno = [(x_centro, z_perto), (x_ponta, z_perto),
                            (x_ponta, z_perto - ABERTURA_PROF), (x_centro, z_perto - ABERTURA_PROF)]
            poligono_xz(sk, contorno, y_meio)
            extrudar_simetrico(comp, todos_perfis(sk), PAREDE + 1.0, CORTE)

        # 5) Aba em "L": começa na aresta da abertura voltada para o centro e segue para o centro
        if USAR_ABA:
            aba_perto = ABERTURA_DA_DIREITA + ABERTURA_LARGURA   # aresta da abertura voltada para o centro
            aba_longe = aba_perto + ABA_PLACA_COMP
            za = LARGURA / 2 - ABERTURA_DA_FRENTE - (ABERTURA_PROF - ABA_PROFUNDIDADE) / 2 - ABA_PROFUNDIDADE
            sk = comp.sketches.add(plano_z(comp, za))
            sk.name = "Aba em L"
            topo_poste = ALTURA + ABA_POSTE_ALTURA
            topo_placa = topo_poste + ABA_PLACA_ESP
            poligono(sk, [(aba_perto, ALTURA),
                          (aba_perto + ABA_POSTE_COMP, ALTURA),
                          (aba_perto + ABA_POSTE_COMP, topo_poste),
                          (aba_longe, topo_poste),
                          (aba_longe, topo_placa),
                          (aba_perto, topo_placa)], za)
            extrudar(comp, sk.profiles.item(0), ABA_PROFUNDIDADE, UNIR)

        app.activeViewport.fit()
        ui.messageBox("Peça criada! Confira as medidas e exporte com "
                      "botão direito no corpo > Save As Mesh.")
    except:
        if ui:
            ui.messageBox("Erro:\n{}".format(traceback.format_exc()))