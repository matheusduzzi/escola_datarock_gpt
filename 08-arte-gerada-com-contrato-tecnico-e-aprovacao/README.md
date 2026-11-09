# Kit da aula: Arte gerada com contrato técnico e aprovação antes de integrar

Essa pasta faz parte do módulo bônus do curso ChatGPT no trabalho. O `sprites.py` roda com o Python 3 do seu computador e precisa do Pillow, a biblioteca de imagem do Python. Se ele reclamar que falta o Pillow, instale uma vez:

```text
python3 -m pip install pillow
```

As imagens você gera no ChatGPT ou no Codex, com a sua conta.

| Arquivo | Para quê |
|---|---|
| [ARTE.md](ARTE.md) | O modelo do contrato da arte, em branco: quadro de estilo, paleta em hex e o tamanho final de cada sprite |
| [ORIGEM.md](ORIGEM.md) | O modelo do registro de origem: uma linha por imagem gerada |
| [APROVACAO.md](APROVACAO.md) | O modelo das decisões: uma linha por peça, com o código da versão que você olhou |
| [sprites.py](sprites.py) | A ferramenta: referência ampliada, importador, código de cada arquivo, prancha, conferência e integração |
| `prompts/` | O prompt mestre de sprite, o modelo do bloco de cada sprite, o prompt do quadro de estilo, um prompt de mascote original e o modelo de prancha de personagem |
| `amostra/` | A loja do Centro com o contrato pronto, o quadro aprovado, os prompts, quatro imagens para importar e o protótipo da Loja Aurora que lê o `atlas.js` |
| [exercicio.md](exercicio.md) | O enunciado do exercício, igual ao da página da aula |

## Os comandos

Rode dentro da pasta da arte, a que tem o `ARTE.md`. Na `amostra`, o `sprites.py` está uma pasta acima, então o comando começa com `python3 ../sprites.py`.

| Comando | O que faz |
|---|---|
| `python3 sprites.py refs` | Cria em `refs/` a referência ampliada de cada sprite: um retângulo cinza do tamanho da peça, sobre magenta, com uma linha verde na base |
| `python3 sprites.py importar <nome> <imagem>` | Tira o fundo magenta, põe cada cor na paleta, recorta, encolhe até o tamanho do contrato com a base no chão e grava `importados/<nome>.png` |
| `python3 sprites.py codigo <arquivo>` | Mostra o código do arquivo: as 12 primeiras letras e números do `SHA-256`. Muda se o arquivo mudar um pixel |
| `python3 sprites.py prancha` | Monta a `prancha.png` com cada peça em 1× e em 4×, e mostra a tabela com o código de cada uma |
| `python3 sprites.py conferir` | Lê o contrato, a origem e os importados. Uma linha `FALTA` por problema |
| `python3 sprites.py integrar --jogo <pasta>` | Copia para `<pasta>/sprites/` só as peças aprovadas na versão de agora e escreve `<pasta>/atlas.js` |

O `conferir` e o `integrar` saem com 0 quando está tudo certo e com 1 quando falta algo. O `integrar` tira do jogo a peça que perdeu a aprovação, como uma peça importada de novo depois de aprovada.

O que eles não fazem: olhar o desenho. Sombra pintada, texto, peça que não parece com a da foto ou traço diferente do quadro passam pelo `conferir`. Isso fica com você, na prancha.

## A prática guiada

Dentro da pasta `amostra`:

```text
python3 ../sprites.py importar mesa-cama geradas/mesa-cama.png
python3 ../sprites.py importar balcao geradas/balcao.png
python3 ../sprites.py importar banco-alto geradas/banco-alto.png
python3 ../sprites.py importar floreira geradas/floreira.png
python3 ../sprites.py conferir
python3 ../sprites.py prancha
```

As imagens da amostra foram desenhadas por código, para a prática, e têm problemas de propósito. A aula traz as perguntas e a resposta. Para ver a loja, abra `amostra/prototipo/index.html` no navegador. Sem nada aprovado, ela sai com as caixas de antes.

## Ajuda

Para pedir ajuda, deixe um comentário na aula. Conte o seu objetivo, o comando que você rodou, a saída e o que já tentou, sem dados pessoais.
