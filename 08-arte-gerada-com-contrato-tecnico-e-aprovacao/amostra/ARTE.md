# Arte da loja do Centro

O contrato da arte: o quadro de estilo, a paleta e o tamanho final de cada sprite. O `sprites.py` lê as três tabelas.

## Quadro de estilo

| arquivo | prompt |
|---|---|
| quadro-de-estilo.png | prompts/quadro-de-estilo.txt |

## Paleta

A mesma da direção de arte. O importador troca cada cor da imagem gerada pela mais próxima daqui.

| nome | hex | onde usa |
|---|---|---|
| creme | #f3ead7 | paredes e piso do salão |
| verde | #3f7d4e | toldo e folhas |
| verdeEscuro | #2a5a37 | contorno das folhas, porta do fundo |
| madeira | #a8743f | mesas, balcão, banco |
| terracota | #c8613a | floreira, ladrilho da calçada |
| rua | #8a8f94 | asfalto |
| vidro | #8fc1d4 | vitrine, porta, tela do caixa |
| carvao | #2b2a2e | contorno de tudo |
| tecido | #fbf8f1 | jogos de cama, toalhas |
| mostarda | #d9a441 | flores, palha, jogo de casal |
| jeans | #3d5a80 | jogo de solteiro |
| vinho | #8c3b4a | jogo infantil, listras |
| sombra | #4f6f6a | sombra de contato (desenhada pelo código) |

## Sprites

O meio da base do sprite é o ponto em que ele pisa no jogo. 1 pixel do sprite é 1 pixel do jogo.

| nome | largura | altura | onde aparece | o que é |
|---|---|---|---|---|
| mesa-cama | 48 | 64 | as duas mesas baixas do meio do salão (Foto 2) | mesa de madeira vista de cima com três jogos de cama dobrados |
| balcao | 72 | 32 | o canto do fundo à direita (Foto 3) | o balcão com o caixa |
| banco-alto | 16 | 24 | na frente do balcão (Foto 3) | o banco alto de madeira |
| floreira | 24 | 24 | na calçada, ao lado da porta (Foto 1) | floreira de terracota com folhas e flores |
