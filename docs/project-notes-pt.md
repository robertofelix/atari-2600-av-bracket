# Notas do projeto: suporte RCA para AV mod do Atari 2600 (Autodesk Fusion + impressão 3D)

Notas de trabalho de um pequeno suporte impresso em 3D que segura os conectores de um AV mod de Atari 2600. Sou iniciante em Fusion, paquímetro digital e Git, então estas notas incluem os caminhos de menu e os passos que tive que descobrir pelo caminho.

**Setup:** Mac, Creality Ender 5 S1 (bico 0,4 mm, volume de impressão 220×220×280 mm, mesa PEI texturizada), PLA, fatiado no Creality Print.

O script Python em `portuguese/av_bracket_pt.py` (com `av_bracket_pt.manifest`) é a fonte da verdade para a geometria.

## Objetivo

Reproduzir um pequeno suporte impresso em 3D que encaixa na traseira de um **Atari 2600** e segura os conectores de um **AV mod**. A peça original que estou copiando segura 1 S-Video e 3 RCA. **Minha versão troca o recorte do S-Video por um 4º furo RCA, então tem 4 furos RCA idênticos.** O cabo flat do mod entra no suporte por uma abertura na face de cima, e um gancho em "L" ao lado dessa abertura prende o suporte ao console.

## Como a peça é construída

A peça é gerada por um **script Python do Fusion** (não é modelada à mão). Ele roda em *Utilities > Add-Ins > Scripts and Add-Ins* (Shift+S), abre um novo design e cria features paramétricas na linha do tempo, nesta ordem. As medidas ao longo de x partem da ponta original x = 0, que é a ponta da abertura (a direita vista de cima com a face RCA no topo).

1. **Corpo:** um trapézio desenhado no plano XY (comprimento × altura) e extrudado em Z (profundidade). O topo tem 76,2 mm e a base 66,2 mm, porque as duas pontas são inclinadas 5 mm. `ENCURTAR_PONTA` (4,8 mm) encurta a peça na ponta da abertura sem mover mais nada.
2. **Casca:** paredes de 2 mm. A face removida é a **traseira** (oposta aos furos), então a caixa fica aberta atrás.
3. **Traseira inclinada:** um corte em cunha no plano YZ, de modo que a profundidade vai de 24,89 mm embaixo até 19,30 mm em cima (~15,5°). Isso acompanha a traseira inclinada da carcaça do Atari. O lado mais estreito fica em cima, junto ao Atari.
4. **Recorte quadrado opcional:** a antiga abertura do S-Video, agora desligada (`USAR_ABERTURA = False`).
5. **4 furos RCA:** cortados só na parede frontal. `DISTRIBUIR_FUROS` espaça os furos por igual na altura deles, com folgas iguais (7,28 mm) entre os furos e entre os furos e as pontas inclinadas.
6. **Abertura de cima:** um quadrado de 12,10 × 12,10 mm cortado na parede de cima, para o cabo. `USAR_BRACO` pode acrescentar um braço até a ponta, e vem desligado.
7. **Gancho em L:** começa na aresta de 12,10 mm da abertura, do lado do centro, e segue para o centro. O pino tem 2,5 mm de comprimento e 3,10 mm de altura, a placa 9,15 mm de comprimento e 2,5 mm de espessura, e o gancho tem 6 mm de largura, centralizado nessa aresta.

## Parâmetros atuais (mm)

| Parâmetro | Valor | Origem |
|---|---|---|
| COMPRIMENTO_TOPO / ENCURTAR_PONTA | 81,0 / 4,8 (topo = 76,2) | medido |
| comprimento da base | 66,2 | derivado (inclinação de 5 mm em cada ponta) |
| INCLINACAO_ESQ / INCLINACAO_DIR | 5,0 / 5,0 | derivado da primeira medida, 81 vs 71 |
| ALTURA | 20,21 | medido |
| LARGURA (profundidade embaixo) | 24,89 | medido |
| PROFUNDIDADE_TOPO | 19,30 | medido |
| PAREDE | 2,0 | escolhido |
| FURO_DIAMETRO / FURO_FOLGA | 8,4 / 0,3 | anel RCA medido 8,38; furos impressos encolhem |
| FURO_QTD | 4 | escolha minha |
| furos (DISTRIBUIR_FUROS) | centros em x = 18,93 / 34,91 / 50,89 / 66,87 | calculado |
| FURO_ALTURA_CENTRO | 10,1 | centralizado na vertical |
| ABERTURA_DA_FRENTE / ABERTURA_DA_DIREITA | 2,70 / 9,30 (4,50 da ponta encurtada) | medido |
| ABERTURA_LARGURA / ABERTURA_PROF | 12,10 / 12,10 | medido |
| ABA_PLACA_COMP / ABA_POSTE_COMP | 9,15 / 2,5 | medido / escolhido |
| ABA_POSTE_ALTURA / ABA_PLACA_ESP | 3,10 / 2,5 | medido / escolhido |
| ABA_PROFUNDIDADE | 6,0, centralizada na aresta da abertura (frente a 5,75 da borda da frente) | medido |
| PARAFUSOS_D | False | os conectores entram por pressão, sem parafusos |

As folgas foram conferidas no modelo gerado: o gancho em L (z a partir da borda da frente, de 5,75 a 11,75 mm) e a abertura (de 2,70 a 14,80 mm) ficam 4,50 mm à frente da traseira inclinada, em cima.

## Contexto importante e lições aprendidas

- **Os conectores RCA entram só por pressão nos furos.** O tamanho do furo é o ajuste mais crítico. Vale fazer uma plaquinha de teste com furos de 8,2 / 8,4 / 8,6 mm antes de reimprimir a peça inteira.
- **As primeiras estimativas estavam ~2× grandes** (150 mm de comprimento) porque eu trabalhei com prints de tela sem escala. Todas as dimensões agora são medidas reais com paquímetro.
- **Armadilha da vista de cima:** olhando de cima com a face RCA no topo, a ponta da abertura fica à *direita*. Olhando de frente para a face RCA, ela fica à *esquerda*. Os parâmetros com "direita" no nome se referem à vista de cima.
- **Unidade do paquímetro:** uma vez o display estava em polegadas ("in" no visor). O botão **mm/in/F** do meu paquímetro troca a unidade. Sempre confira se aparece "mm" e zere o paquímetro com as garras fechadas.
- **A primeira impressão não encaixou perfeitamente** porque a traseira do Atari é inclinada. Isso foi corrigido com o corte da traseira inclinada (PROFUNDIDADE_TOPO). Se ainda ficar um pouco fora, ajuste PROFUNDIDADE_TOPO em passos de 0,5 mm.
- **Suposições do script** ainda não confirmadas: as duas pontas têm a mesma inclinação, e o lado estreito (19,30 mm) fica em cima, junto ao Atari.

## Configuração de impressão

- Orientação: **face dos furos RCA para baixo na mesa**, traseira aberta para cima. Os furos saem redondos sem suporte.
- **Sem suportes.** O gancho em L tem a mesma seção ao longo do sentido da impressão, então imprime sem eles. Veja no preview das camadas a ponte de 12,10 mm sobre a abertura.
- Ponto de partida para PLA: camadas de 0,2 mm, bico 200–210 °C, mesa 60 °C, 3 paredes, preenchimento 15–20%. Brim ajuda nas primeiras camadas.

## Como fazer no Fusion (já resolvido)

- **Rodar um script:** Shift+S → selecione o script → Run.
- **Adicionar um script de uma pasta** (por exemplo, um repositório Git): Shift+S → **+** → adicionar script existente do computador. O nome da pasta, do `.py` e do `.manifest` precisa ser o mesmo. Os scripts ficam em `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/Scripts/` (Finder: Cmd+Shift+G).
- **Exportar STL:** botão direito no corpo **Bracket** no Browser → **Save As Mesh** → STL (Binary), Millimeter, Refinement High. Em *Utilities > Make > 3D Print*, o botão OK fica cinza a menos que **Preparation Type = Save to Local File**.
- **Renomear ou apagar um script:** crie um novo script com o nome desejado e cole o código, ou renomeie/apague a pasta no diretório Scripts.

## Repositório

**Nome:** `atari-2600-av-bracket`

> Parametric 3D-printable bracket for the Atari 2600 AV mod. Mounts 4 RCA jacks at the rear of the console, generated by an Autodesk Fusion Python script.

**Tópicos:** `atari-2600`, `av-mod`, `3d-printing`, `fusion360`, `retro-gaming`, `rca`

```
atari-2600-av-bracket/
├── english/          av_bracket_en.py, .manifest, ScriptIcon.svg
├── portuguese/       av_bracket_pt.py, .manifest, ScriptIcon.svg
├── docs/
├── exports/          av_bracket_print.stl (orientado para imprimir), av_bracket.stl, av_bracket.step
└── README.md
```

## Próximos passos

1. Ajustar o encaixe dos furos para os conectores RCA por pressão com uma plaquinha de teste (8,2 / 8,4 / 8,6 mm).
2. Opcionalmente fazer o script exportar STL/STEP automaticamente para `exports/`.
3. Opcionalmente adicionar textos em relevo embaixo de cada conector, como o original ("Y", "C", "Audio").
