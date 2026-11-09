# Exercício: quatro peças do seu protótipo com contrato e aprovação

## Objetivo

Gerar a arte de quatro peças do seu protótipo com um quadro de estilo, um prompt técnico e o tamanho final. Passar cada imagem pelo importador. E só levar para o jogo o que você aprovou na prancha.

## O pedido

A gerente quer ver no seu protótipo as peças de verdade no lugar das caixas. Eu mostrei na aula o contrato da loja do Centro, a prancha e o que entrou no jogo. Agora é a sua vez, no seu protótipo, com o ChatGPT ou com o Codex.

Na pasta dessa aula no kit estão `ARTE.md`, `ORIGEM.md`, `APROVACAO.md`, `sprites.py` e a pasta `prompts`. Crie uma pasta `arte` no seu protótipo e copie tudo para ela, com os mesmos nomes. Os comandos abaixo rodam dentro dessa pasta.

O protótipo precisa ler o que o `integrar` escreve. Veja como o protótipo da `amostra` faz: o `index.html` carrega o `atlas.js` antes do `arte.js`, e o `arte.js` desenha cada peça com a função `peca`. Peça ao agente a mesma mudança no seu, com o ponto em que cada peça pisa.

## O que entregar

1. **O contrato**, no `ARTE.md`. A paleta tem pelo menos 5 cores em hex, cada uma com onde usa. A tabela Sprites tem quatro peças do seu protótipo, com largura e altura em pixels e onde cada uma aparece. Cada peça substitui algo que hoje é desenhado por código.
2. **O quadro de estilo**, gerado antes dos sprites, com o prompt salvo na pasta `prompts`. Ele traz quatro objetos do mesmo mundo que não são os seus sprites. Ele entra no `APROVACAO.md` como `aprovado`, com o código e uma data igual ou anterior à do primeiro sprite.
3. **Os quatro sprites**, gerados com o quadro aprovado e a referência do `sprites.py refs` anexados. Cada prompt é o prompt mestre com o bloco do sprite. O bloco tem o `FINAL SIZE` igual ao do `ARTE.md`, e o prompt proíbe texto. Cada imagem fica salva em `geradas/`.
4. **O registro de origem**, no `ORIGEM.md`. Uma linha por imagem gerada, inclusive as refeitas, com todas as colunas preenchidas. Na coluna "quadro anexado" vai o código do quadro aprovado.
5. **A saída do `python3 sprites.py conferir`**, sem nenhuma linha `FALTA`, depois de importar as quatro.
6. **A prancha e as decisões**: a `prancha.png` e o `APROVACAO.md` com uma decisão por peça. Cada decisão traz o código da versão que você olhou, a data e o porquê. Em pelo menos uma linha, o porquê diz algo que você viu na prancha e o `conferir` não lê. Por exemplo: sombra pintada, texto ou a peça não parecer com a da foto.
7. **A integração**: a saída do `python3 sprites.py integrar --jogo ..` com "4 de 4 sprite(s) no jogo", e um print do protótipo com as quatro peças.
8. **A sua conta**: a data, onde você gerou (app, navegador ou linha de comando) e o que a tela mostrou.

Sem o nome de um jogo, de uma marca ou de um artista nos prompts. Sem pessoa real nas peças.

## Como avaliar o que você fez

Abra a `prancha.png` ao lado do quadro de estilo. Cubra o 4× com a mão e olhe só o 1×. Dá para saber o que é cada peça? O traço é o do quadro? Depois abra o protótipo: as quatro peças pisam no lugar certo, com a sombra do código embaixo?

Por fim, leia o `ORIGEM.md` como se fosse outra pessoa. Dá para refazer qualquer uma das quatro peças só com o que está escrito ali?

<details><summary>Dica 1</summary>

Comece pelo quadro e pare nele. Gere, olhe, aprove ou gere de novo. Só depois escreva a linha dele no `APROVACAO.md`, com o código que o `python3 sprites.py codigo quadro-de-estilo.png` mostrar. Todo sprite gerado antes dessa data, ou com outro quadro anexado, vai aparecer como `FALTA` no `conferir`.

</details>

<details><summary>Dica 2</summary>

Se o `conferir` acusar um prompt ou um quadro errado, não arrume a linha do `ORIGEM.md` nem o arquivo do prompt. Gere a peça de novo com o prompt certo, salve com outro nome em `geradas/` e escreva uma linha nova embaixo. A última linha de cada sprite é a que vale, e as antigas mostram o que você já tentou.

</details>
