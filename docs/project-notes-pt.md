# Notas do projeto: suporte RCA para AV mod do Atari 2600 (Autodesk Fusion + impressão 3D)

Notas de trabalho de um pequeno suporte impresso em 3D que segura os conectores de um AV mod de Atari 2600. Sou iniciante em Fusion, paquímetro digital e Git, então estas notas incluem os caminhos de menu e os passos que tive que descobrir pelo caminho.

**Setup:** Mac, Creality Ender 5 S1 (bico 0,4 mm, volume de impressão 220×220×280 mm, mesa PEI texturizada), PLA, fatiado no Creality Print.

O script Python em `portuguese/av_bracket_pt.py` (com `av_bracket_pt.manifest`) é a fonte da verdade para a geometria.

## Objetivo

Reproduzir um pequeno suporte impresso em 3D que encaixa na traseira de um **Atari 2600** e segura os conectores de um **AV mod**. A peça original que estou copiando segura 1 S-Video e 3 RCA. **Minha versão troca o recorte do S-Video por um 4º furo RCA, então tem 4 furos RCA idênticos.** O cabo flat do mod entra no suporte, e a aba em "L" na parte de cima funciona como clipe/gancho.

## Como a peça é construída

A peça é gerada por um **script Python do Fusion** (não é modelada à mão). Ele roda em *Utilities > Add-Ins > Scripts and Add-Ins* (Shift+S), abre um novo design e cria features paramétricas na linha do tempo, nesta ordem:

1. **Corpo:** um trapézio desenhado no plano XY (comprimento × altura) e extrudado em Z (profundidade). A face frontal tem 81 mm em cima e 71 mm embaixo, porque as duas pontas são inclinadas 5 mm.
2. **Casca:** paredes de 2 mm. A face removida é a **traseira** (oposta aos furos), então a caixa fica aberta atrás.
3. **Traseira inclinada:** um corte em cunha no plano YZ, de modo que a profundidade vai de 24,94 mm embaixo até 22,00 mm em cima (~8,1°). Isso acompanha a traseira inclinada da carcaça do Atari. O lado mais estreito fica em cima, junto ao Atari.
4. **Recorte quadrado opcional:** a antiga abertura do S-Video, agora desligada (`USAR_ABERTURA = False`).
5. **4 furos RCA:** cortados só na parede frontal.
6. **Aba em "L":** na face superior, recuada em relação à face dos furos. O poste vertical fica à esquerda e a placa avança para a direita.

## Parâmetros atuais (mm)

| Parâmetro | Valor | Origem |
|---|---|---|
| COMPRIMENTO_TOPO | 81,0 | medido |
| comprimento da base (COMPRIMENTO_TOPO − inclinações) | 71,0 | medido |
| INCLINACAO_ESQ / INCLINACAO_DIR | 5,0 / 5,0 | derivado de 81 vs 71 (assumido simétrico) |
| ALTURA | 20,65 | medido (0,8130 in) |
| LARGURA (profundidade embaixo) | 24,94 | medido |
| PROFUNDIDADE_TOPO | 22,00 | medido |
| PAREDE | 2,0 | escolhido |
| FURO_DIAMETRO | 8,4 | medido; anel frontal do RCA = 8,38 |
| FURO_FOLGA | 0,3 | escolhido (furos impressos encolhem) |
| FURO_QTD | 4 | escolha minha |
| FURO_ESPACAMENTO | 15,0 | estimado a partir da original |
| FURO_PRIMEIRO_X | 18,0 | centros em 18 / 33 / 48 / 63, grupo centralizado |
| FURO_ALTURA_CENTRO | 10,3 | centralizado na vertical |
| ABA_X | 13,0 | estimado por fotos |
| ABA_POSTE_COMP / ABA_POSTE_ALTURA | 2,5 / 4,5 | estimado |
| ABA_PLACA_COMP / ABA_PLACA_ESP | 16,0 / 2,5 | estimado |
| ABA_PROFUNDIDADE / ABA_RECUO | 12,0 / 5,0 | estimado, recuo de 5 mm da face dos furos |
| PARAFUSOS_D | False | os conectores entram por pressão, sem parafusos |

As folgas foram verificadas. Os furos ocupam x = 13,7–67,4 dentro das paredes internas em cerca de 4,4–76,6. A faixa z da aba (−4,5 a 7,5) fica na frente da traseira inclinada (−9,5 em cima).

## Contexto importante e lições aprendidas

- **Os conectores RCA entram só por pressão nos furos.** O tamanho do furo é o ajuste mais crítico. Vale fazer uma plaquinha de teste com furos de 8,2 / 8,4 / 8,6 mm antes de reimprimir a peça inteira.
- **As primeiras estimativas estavam ~2× grandes** (150 mm de comprimento) porque eu trabalhei com prints de tela sem escala. Todas as dimensões principais agora são medidas reais com paquímetro. Só as posições da aba e dos furos são estimadas por foto.
- **Unidade do paquímetro:** uma vez o display estava em polegadas ("in" no visor). O botão **mm/in/F** do meu paquímetro troca a unidade. Sempre confira se aparece "mm" e zere o paquímetro com as garras fechadas.
- **A primeira impressão não encaixou perfeitamente** porque a traseira do Atari é inclinada. Isso foi corrigido com o corte da traseira inclinada (PROFUNDIDADE_TOPO). Se ainda ficar um pouco fora, ajuste PROFUNDIDADE_TOPO em passos de 0,5 mm.
- **Suposições do script** ainda não confirmadas: as duas pontas têm a mesma inclinação, e o lado estreito (22 mm) fica em cima, junto ao Atari.

## Configuração de impressão

- Orientação: **face dos furos RCA para baixo na mesa**, traseira aberta para cima. Os furos saem redondos sem suporte.
- Ative **suporte só embaixo da aba em L**, porque ela é recuada da borda e a parte de baixo fica em balanço.
- Ponto de partida para PLA: camadas de 0,2 mm, bico 200–210 °C, mesa 60 °C, 3 paredes, preenchimento 15–20%. Brim ajuda na área pequena da aba.

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
├── exports/          (STL / STEP)
└── README.md
```

## Próximos passos

1. Reimprimir com a traseira inclinada e conferir o encaixe no Atari.
2. Ajustar o encaixe dos furos para os conectores RCA por pressão e, se precisar, PROFUNDIDADE_TOPO.
3. Opcionalmente confirmar a posição da aba com o paquímetro.
4. Opcionalmente fazer o script exportar STL/STEP automaticamente para `exports/`.
5. Opcionalmente adicionar textos em relevo embaixo de cada conector, como o original ("Y", "C", "Audio").
