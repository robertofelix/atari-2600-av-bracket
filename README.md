# Atari 2600 AV Bracket

3D-printable bracket for the **Atari 2600 AV mod**. It holds **4 or 3 RCA jacks** at the rear of the console, in two versions of the same case. The ready-to-print **STL files** are the main deliverable. Optional **Autodesk Fusion** Python scripts are included for convenience.

> 🇧🇷 **Nota:** este README também está em português, mais abaixo (a partir de [Português (Brasil)](#-português-brasil)). Os scripts em português ficam nas pastas `portuguese/` de cada versão, e as notas estão em [`docs/project-notes-pt.md`](docs/project-notes-pt.md).

> **Fusion scripts are optional.** The parts were first modeled for [Autodesk Fusion](https://www.autodesk.com/products/fusion-360/overview), and the STL files were later generated directly, so you do not need Fusion to print them. The scripts are kept for convenience and as a reference for the geometry. They use the Fusion API (`adsk.core`, `adsk.fusion`), will not run in other CAD software, and have only been syntax-checked, not run in Fusion. This is an independent hobby project and is not affiliated with or endorsed by Autodesk or Atari.

## What it is

A small hollow bracket that clips under the back of an Atari 2600. The jacks press-fit into the front wall, the flat ribbon cable from the mod runs into the box through an opening in the top face, and an "L" hook next to that opening locks the bracket to the console.

The design is based on a commercial part that holds 1 S-Video and 3 RCA jacks. This version replaces the S-Video cutout with a fourth RCA hole.

## Versions

The same case comes in two versions, with the holes spread evenly over the width of the case (equal gaps between the holes and between the holes and the ends).

| Version | Folder | RCA holes | Gaps | Hole centers (from the opening end) |
|---|---|---|---|---|
| 4 holes | [`4-holes/`](4-holes/) | 4 | 5 of 7.28 mm | 18.93 / 34.91 / 50.89 / 66.87 |
| 3 holes | [`3-holes/`](3-holes/) | 3 | 4 of 11.27 mm | 22.93 / 42.90 / 62.87 |

Everything else is identical: size, jack hole diameter (8.4 + 0.3), opening, L hook and slanted back. The [`arch-plug/`](arch-plug/) closure is the same part for both versions.

## Compatibility

Made for these Atari 2600 models:

- Heavy Sixer
- Light Sixer
- Darth Vader

Other models may have a different rear shape, so check the measurements before printing.

**Status:** working prototype, refined through test prints. The dimensions come from caliper measurements of the console and of the printed parts. Ready-to-print files are in the `exports/` folder of each version.

## Repository layout

```
atari-2600-av-bracket/
├── 4-holes/       Bracket with 4 RCA holes
│   ├── english/       Fusion script: av_bracket_4h_en
│   ├── portuguese/    Fusion script: av_bracket_4h_pt
│   └── exports/       av_bracket_4h_print.stl, av_bracket_4h.stl, av_bracket_4h.step
├── 3-holes/       Bracket with 3 RCA holes
│   ├── english/       Fusion script: av_bracket_3h_en
│   ├── portuguese/    Fusion script: av_bracket_3h_pt
│   └── exports/       av_bracket_3h_print.stl, av_bracket_3h.stl, av_bracket_3h.step
├── arch-plug/     Arch closure, shared by both versions
│   ├── english/       Fusion script: av_arch_plug_en
│   ├── portuguese/    Fusion script: av_arch_plug_pt
│   └── exports/       av_arch_plug.stl, av_arch_plug.step
├── docs/          Project notes (EN / PT)
└── LICENSE
```

The English and Portuguese scripts build the same parts. Only the language of the comments and parameter names differs. `av_bracket_4h_*` and `av_bracket_3h_*` build the bracket with 4 or 3 holes, and `av_arch_plug_*` builds the arch closure.

## Requirements

- Autodesk Fusion (Mac or Windows)
- A 3D printer. Developed on a Creality Ender 5 S1 with PLA.

## Run the script (optional)

Skip this if you only want to print: use the files in the `exports/` folders.

1. Copy the script's `.py` and `.manifest` files and `ScriptIcon.svg` from the `english/` (or `portuguese/`) folder of the version you want into a folder named like the script, for example `av_bracket_4h_en`, `av_bracket_3h_pt` or `av_arch_plug_en`. The folder, `.py` and `.manifest` names must match.
2. Put that folder in Fusion's Scripts directory:
   `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/` on Mac (Finder: Cmd+Shift+G).
3. In Fusion, press **Shift+S** (Utilities > Add-Ins > Scripts and Add-Ins), select the script and click **Run**.

The script opens a new design and builds the part as parametric timeline features.

## Parameters

All dimensions are in millimeters and sit at the top of the script. Edit them and run it again to generate a new version.

| Parameter | Value | Source |
|---|---|---|
| Top length | 76.2 (81.0 minus 4.8 trimmed at the opening end) | measured |
| Bottom length | 66.2 (5 mm slant each end) | measured |
| Height | 20.21 | measured |
| Depth, bottom / top | 24.89 / 19.30 (slanted back, ~15.5°) | measured |
| Wall thickness | 2.0 | chosen |
| RCA hole diameter | 8.4 + 0.3 clearance | measured ring 8.38 mm |
| Holes | 4 or 3, spread evenly. 4 holes: 7.28 mm gaps, centers at x = 18.93 / 34.91 / 50.89 / 66.87. 3 holes: 11.27 mm gaps, centers at x = 22.93 / 42.90 / 62.87 | calculated |
| L tab | 9.15 long × 6.0 wide plate, 2.5 thick, 3.10 post height, centered on the 12.10 mm opening edge, so its front is 5.75 from the front edge | measured |
| Top opening (cable path) | 12.10 × 12.10 square, 2.70 from the front and 4.50 from the right end (the 5.66 mm arm is off by default) | measured |

Optional switches in the script (all off or on as listed): `DISTRIBUTE_HOLES` (on) spaces the RCA holes evenly, `USE_OPEN_ARM` (off) adds an arm to the opening toward the end, `USE_TAB` (on) builds the L hook, plus a square front cutout (for example, S-Video) and M3 screw holes for D-series jacks, both off. "Right end" means the end seen on the right when you look from above with the RCA face at the top; that is the end with the opening.

## Print settings

- **Orientation:** RCA-hole face down on the bed, open back facing up. The holes print round with no support.
- **Supports:** none needed. The L hook has the same cross-section along the print direction. Check the layer preview for the 12.10 mm bridge over the opening.
- **PLA starting point:** 0.2 mm layers, 200–210 °C nozzle, 60 °C bed, 3 walls, 15–20% infill. A brim helps the first layers.

## Ready-to-print files

For each version (`4-holes/exports/` with `4h` in the names, `3-holes/exports/` with `3h`):

- `av_bracket_4h_print.stl` / `av_bracket_3h_print.stl`: oriented for printing, with the RCA face down.
- `av_bracket_4h.stl` / `av_bracket_3h.stl`: same part in the Fusion orientation.
- `av_bracket_4h.step` / `av_bracket_3h.step`: exact geometry for other CAD tools.

Shared by both versions: [`arch-plug/exports/av_arch_plug.stl`](arch-plug/exports/av_arch_plug.stl) and [`.step`](arch-plug/exports/av_arch_plug.step), the arch closure, see below.

These files were generated from the same parameters as the scripts. To export your own from Fusion: right-click the body in the Browser, choose **Save As Mesh**, then STL (Binary), Millimeter, Refinement High.

## Arch closure

The console's rear edge has an arched notch, and the closure fills it. It is a separate part that goes in from inside the console. Its arm runs along the inner face of the wall and rests against the base of the L hook, which locks the bracket in place (a sliding mechanism). Print it flat, with the protrusion and the arm on the bed, no supports.

| Part | Size (mm) |
|---|---|
| Body (goes through the wall) | 5.70 base, 4.60 top, 7.75 high, 3.28 long (the wall thickness) |
| Protrusion (inside, against the wall) | 6.33 × 8.00, 3.22 thick |
| Arm | 10.70 from the notch edge (13.545 from the arch center), 2.5 high, 3.22 thick |
| Whole part | 16.71 × 8.00 × 6.50 |

The notch measures 5.69 × 8.02, so the body has only about 0.01 mm of clearance in width. Sand it lightly if it will not go in. It is built by its own script in `arch-plug/`, `av_arch_plug_en` (or `av_arch_plug_pt`), and exported as STL and STEP. The same closure fits both the 4-hole and the 3-hole bracket.

## Tuning the fit

- The jacks only press-fit, so hole size matters most. Print a small test plate with 8.2 / 8.4 / 8.6 mm holes before reprinting the whole part.
- If the bracket doesn't sit flush against the Atari, change the top depth (`TOP_DEPTH`) in 0.5 mm steps. The back slant follows from it.
- The L hook position follows the opening, so move the opening (`OPEN_FROM_FRONT`, `OPEN_FROM_RIGHT`) and the hook comes with it.
- Check that your caliper shows **mm**, not inches, and zero it with the jaws closed.

## Roadmap

- [x] Slanted back matched to the Atari
- [x] Opening in the top face and L hook, from measurements
- [x] Evenly spaced RCA holes
- [x] Second version with 3 holes
- [x] Arch closure with sliding arm
- [x] Portuguese README
- [ ] Fine-tune the hole fit with a test plate (8.2 / 8.4 / 8.6 mm)
- [ ] Embossed labels under each jack (Y, C, Audio)

## More details

Full project notes, with measurements and lessons learned, are in [`docs/project-notes-en.md`](docs/project-notes-en.md).

---

# 🇧🇷 Português (Brasil)

## Suporte AV para Atari 2600

Suporte imprimível em 3D para o **AV mod do Atari 2600**. Ele segura **4 ou 3 conectores RCA** na traseira do console, em duas versões da mesma case. Os **arquivos STL** prontos para imprimir são a entrega principal. Scripts Python opcionais do **Autodesk Fusion** estão incluídos por comodidade.

> **Os scripts do Fusion são opcionais.** As peças foram modeladas primeiro para o [Autodesk Fusion](https://www.autodesk.com/products/fusion-360/overview), e os arquivos STL foram gerados depois diretamente, então você não precisa do Fusion para imprimir. Os scripts ficam por comodidade e como referência da geometria. Eles usam a API do Fusion (`adsk.core`, `adsk.fusion`), não rodam em outros softwares de CAD e só passaram por checagem de sintaxe, sem rodar no Fusion. É um projeto pessoal independente, sem vínculo nem aprovação da Autodesk ou da Atari.

## O que é

Um pequeno suporte oco que encaixa embaixo da traseira de um Atari 2600. Os conectores entram por pressão na parede frontal, o cabo flat do mod passa para dentro da caixa por uma abertura na face de cima, e um gancho em "L" ao lado dessa abertura prende o suporte ao console.

O projeto é baseado numa peça comercial que segura 1 S-Video e 3 RCA. Esta versão troca o recorte do S-Video por um quarto furo RCA.

## Versões

A mesma case vem em duas versões, com os furos distribuídos por igual na largura da case (vãos iguais entre os furos e entre os furos e as pontas).

| Versão | Pasta | Furos RCA | Vãos | Centros dos furos (a partir da ponta da abertura) |
|---|---|---|---|---|
| 4 furos | [`4-holes/`](4-holes/) | 4 | 5 de 7,28 mm | 18,93 / 34,91 / 50,89 / 66,87 |
| 3 furos | [`3-holes/`](3-holes/) | 3 | 4 de 11,27 mm | 22,93 / 42,90 / 62,87 |

Todo o resto é idêntico: tamanho, diâmetro dos furos (8,4 + 0,3), abertura, gancho em L e traseira inclinada. O fecho de [`arch-plug/`](arch-plug/) é a mesma peça para as duas versões.

## Compatibilidade

Feito para estes modelos de Atari 2600:

- Heavy Sixer
- Light Sixer
- Darth Vader

Outros modelos podem ter a traseira com formato diferente, então confira as medidas antes de imprimir.

**Status:** protótipo funcional, refinado com impressões de teste. As dimensões vêm de medidas com paquímetro do console e das peças impressas. Os arquivos prontos para imprimir estão na pasta `exports/` de cada versão.

## Estrutura do repositório

```
atari-2600-av-bracket/
├── 4-holes/       Suporte com 4 furos RCA
│   ├── english/       Script do Fusion: av_bracket_4h_en
│   ├── portuguese/    Script do Fusion: av_bracket_4h_pt
│   └── exports/       av_bracket_4h_print.stl, av_bracket_4h.stl, av_bracket_4h.step
├── 3-holes/       Suporte com 3 furos RCA
│   ├── english/       Script do Fusion: av_bracket_3h_en
│   ├── portuguese/    Script do Fusion: av_bracket_3h_pt
│   └── exports/       av_bracket_3h_print.stl, av_bracket_3h.stl, av_bracket_3h.step
├── arch-plug/     Fecho do arco, comum às duas versões
│   ├── english/       Script do Fusion: av_arch_plug_en
│   ├── portuguese/    Script do Fusion: av_arch_plug_pt
│   └── exports/       av_arch_plug.stl, av_arch_plug.step
├── docs/          Notas do projeto (EN / PT)
└── LICENSE
```

Os scripts em inglês e em português geram as mesmas peças. Só muda o idioma dos comentários e dos nomes dos parâmetros. O `av_bracket_4h_*` e o `av_bracket_3h_*` criam o suporte com 4 ou 3 furos, e o `av_arch_plug_*` cria o fecho do arco.

## Requisitos

- Autodesk Fusion (Mac ou Windows)
- Uma impressora 3D. Desenvolvido numa Creality Ender 5 S1 com PLA.

## Rodar o script (opcional)

Pule esta parte se você só quer imprimir: use os arquivos das pastas `exports/`.

1. Copie o `.py`, o `.manifest` do script e o `ScriptIcon.svg` da pasta `portuguese/` (ou `english/`) da versão que você quer para uma pasta com o nome do script, por exemplo `av_bracket_4h_pt`, `av_bracket_3h_en` ou `av_arch_plug_pt`. O nome da pasta, do `.py` e do `.manifest` precisa ser o mesmo.
2. Coloque essa pasta no diretório de Scripts do Fusion:
   `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/` no Mac (Finder: Cmd+Shift+G).
3. No Fusion, pressione **Shift+S** (Utilities > Add-Ins > Scripts and Add-Ins), selecione o script e clique em **Run**.

O script abre um novo design e cria a peça como features paramétricas na linha do tempo.

## Parâmetros

Todas as medidas estão em milímetros e ficam no topo do script. Edite os valores e rode de novo para gerar uma nova versão.

| Parâmetro | Valor | Origem |
|---|---|---|
| Comprimento do topo | 76,2 (81,0 menos 4,8 cortados na ponta da abertura) | medido |
| Comprimento da base | 66,2 (inclinação de 5 mm em cada ponta) | medido |
| Altura | 20,21 | medido |
| Profundidade, base / topo | 24,89 / 19,30 (traseira inclinada, ~15,5°) | medido |
| Espessura da parede | 2,0 | escolhido |
| Diâmetro do furo RCA | 8,4 + 0,3 de folga | anel medido 8,38 mm |
| Furos | 4 ou 3, distribuídos por igual. 4 furos: folgas de 7,28 mm, centros em x = 18,93 / 34,91 / 50,89 / 66,87. 3 furos: folgas de 11,27 mm, centros em x = 22,93 / 42,90 / 62,87 | calculado |
| Aba em L | placa de 9,15 de comprimento × 6,0 de largura, espessura 2,5, pino de 3,10 de altura, centralizada na aresta de 12,10 mm da abertura, com a frente a 5,75 da borda da frente | medido |
| Abertura de cima (caminho do cabo) | quadrado de 12,10 × 12,10, a 2,70 da frente e 4,50 da ponta direita (o braço de 5,66 mm vem desligado) | medido |

Chaves no script: `DISTRIBUIR_FUROS` (ligada) espaça os furos RCA por igual, `USAR_BRACO` (desligada) acrescenta um braço na abertura até a ponta, `USAR_ABA` (ligada) cria o gancho em L, e há também um recorte quadrado na frente (por exemplo, S-Video) e furos M3 para conectores série D, ambos desligados. "Ponta direita" é a ponta que aparece à direita vista de cima com a face RCA no topo; é a ponta da abertura.

## Configuração de impressão

- **Orientação:** face dos furos RCA para baixo na mesa, traseira aberta para cima. Os furos saem redondos sem suporte.
- **Suportes:** nenhum. O gancho em L tem a mesma seção ao longo do sentido da impressão. Veja no preview das camadas a ponte de 12,10 mm sobre a abertura.
- **Ponto de partida para PLA:** camadas de 0,2 mm, bico 200–210 °C, mesa 60 °C, 3 paredes, preenchimento 15–20%. Brim ajuda nas primeiras camadas.

## Arquivos prontos para imprimir

Para cada versão (`4-holes/exports/` com `4h` nos nomes, `3-holes/exports/` com `3h`):

- `av_bracket_4h_print.stl` / `av_bracket_3h_print.stl`: orientado para imprimir, com a face RCA para baixo.
- `av_bracket_4h.stl` / `av_bracket_3h.stl`: a mesma peça na orientação do Fusion.
- `av_bracket_4h.step` / `av_bracket_3h.step`: geometria exata para outros programas de CAD.

Comum às duas versões: [`arch-plug/exports/av_arch_plug.stl`](arch-plug/exports/av_arch_plug.stl) e [`.step`](arch-plug/exports/av_arch_plug.step), o fecho do arco, veja abaixo.

Esses arquivos foram gerados a partir dos mesmos parâmetros dos scripts. Para exportar o seu no Fusion: botão direito no corpo no Browser, **Save As Mesh**, depois STL (Binary), Millimeter, Refinement High.

## Fecho do arco

A borda traseira do console tem um recorte em arco, e o fecho preenche esse recorte. É uma peça separada, que entra por dentro do console. O braço corre rente à face interna da parede e encosta na base do gancho em L, o que trava o suporte (um mecanismo deslizante). Imprima deitada, com a protrusão e o braço na mesa, sem suportes.

| Parte | Medida (mm) |
|---|---|
| Corpo (atravessa a parede) | base 5,70, topo 4,60, altura 7,75, comprimento 3,28 (a espessura da parede) |
| Protrusão (por dentro, contra a parede) | 6,33 × 8,00, com 3,22 de espessura |
| Braço | 10,70 da borda do recorte (13,545 do centro do arco), 2,5 de altura e 3,22 de espessura |
| Peça toda | 16,71 × 8,00 × 6,50 |

O recorte mede 5,69 × 8,02, então o corpo tem só uns 0,01 mm de folga na largura. Lixe de leve se não entrar. Ela é criada por um script próprio em `arch-plug/`, o `av_arch_plug_pt` (ou `av_arch_plug_en`), e exportada em STL e STEP. O mesmo fecho serve para o suporte de 4 furos e para o de 3.

## Ajustar o encaixe

- Os conectores entram só por pressão, então o tamanho do furo é o mais importante. Imprima uma plaquinha de teste com furos de 8,2 / 8,4 / 8,6 mm antes de reimprimir a peça inteira.
- Se o suporte não encostar direito no Atari, mude a profundidade do topo (`PROFUNDIDADE_TOPO`) em passos de 0,5 mm. A inclinação da traseira vem dela.
- A posição do gancho em L acompanha a abertura. Mexa na abertura (`ABERTURA_DA_FRENTE`, `ABERTURA_DA_DIREITA`) e o gancho vai junto.
- Confira se o paquímetro mostra **mm** (não polegadas) e zere-o com as garras fechadas.

## Próximos passos

- [x] Traseira inclinada ajustada ao Atari
- [x] Abertura na face de cima e gancho em L, a partir de medidas
- [x] Furos RCA distribuídos por igual
- [x] Segunda versão com 3 furos
- [x] Fecho do arco com braço deslizante
- [x] README em português
- [ ] Ajustar o encaixe dos furos com uma plaquinha de teste (8,2 / 8,4 / 8,6 mm)
- [ ] Textos em relevo embaixo de cada conector (Y, C, Audio)

## Mais detalhes

As notas completas do projeto, com medidas e lições aprendidas, estão em [`docs/project-notes-pt.md`](docs/project-notes-pt.md).

---

## License / Licença

[GPL-3.0](LICENSE)
