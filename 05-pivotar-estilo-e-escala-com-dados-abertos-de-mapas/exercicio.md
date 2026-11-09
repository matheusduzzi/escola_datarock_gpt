# Exercício: a Loja Aurora no bairro

## Objetivo

Mudar o estilo do protótipo sem quebrar o que funciona e levar a loja para dentro de um bairro de verdade. As ruas e os prédios vêm de um download por script. O arquivo é carregado no protótipo, e os créditos dos mapas ficam na tela e no README.

## O pedido

A gerente quer o protótipo "mais colorido, com cara de desenho" e quer que o cliente veja como chega à loja. Eu mostrei na aula o pedido em duas etapas, a consulta das vias, a montagem do arquivo e a prática com a pasta `amostra`. Agora é a sua vez, no seu protótipo, com o agente.

Na pasta dessa aula no kit estão `baixar_bairro.py`, `montar_dados.py`, `conferir.py` e o modelo `pivo.md`. Copie os quatro para a pasta do seu protótipo.

Você pode usar a caixa do kit ou a de outro bairro, com até 3 km de lado. Se usar outra caixa, escolha um ponto dentro dela para ser a loja e passe em `--origem`.

## O que entregar

1. **O `pivo.md` preenchido** antes do pedido: o estilo novo em palavras, sem nome de jogo ou de marca; pelo menos quatro linhas em "o que fica", cada uma com o teste e se passou depois da mudança; as camadas; o que é dado e o que é desenho.
2. **Os dados baixados por script**: a pasta `dados` com o `baixado.json`, que guarda a caixa e a data de cada download, e o `bairro-data.js` montado a partir dela.
3. **O protótipo com o bairro**: o `index.html` carrega `bairro-data.js` e desenha as vias e os prédios em volta da loja. Os créditos ficam num canto da tela, como texto do HTML, legíveis e sem precisar clicar. O portão não lê texto desenhado dentro do canvas.
4. **O README do protótipo** com a lista completa de créditos (as linhas de `creditos` que o `montar_dados.py` escreveu) e o link `https://www.openstreetmap.org/copyright`.
5. **A prova de que funciona**: a saída do `python3 conferir.py --prototipo .` terminando sem nenhuma linha `FALTA`, e um print da tela inteira com o canto dos créditos.
6. **A sua conta**: a data, se o Codex rodou os scripts e se ele pediu permissão de rede. Sem rede, use a pasta `amostra` do kit e escreva "dados da amostra do kit" no topo do `pivo.md`.

## Como avaliar o que você fez

Rode o portão e leia cada linha. Depois abra o protótipo e o site do OpenStreetMap lado a lado, na mesma região. Ache uma praça e duas ruas nos dois. Se uma delas está espelhada ou fora do lugar, olhe a ordem da caixa e a origem.

Por último, rode de novo cada linha de "o que fica". Se a porta de vidro mudou de lado no estilo novo, o pivô quebrou uma coisa que funcionava.

<details><summary>Dica 1</summary>

Para "o que fica", abra a sua ficha do protótipo e copie as ações da seção 4, como "o jogador entra pela porta de vidro". Some uma ou duas regras do seu `MAPEAMENTO.md`, como o balcão no fundo à direita. Cada linha ganha um teste que você faz em um minuto.

</details>

<details><summary>Dica 2</summary>

Se o portão diz "faltam na tela", procure o crédito no `index.html`. Ele pode estar num comentário, num elemento com `hidden` ou `display: none`, ou desenhado só no canvas. Ponha o texto num parágrafo fixo no canto, como "Mapa: © OpenStreetMap contributors, ODbL. Prédios e lugares: Overture Maps Foundation, ODbL e CDLA Permissive 2.0."

</details>
