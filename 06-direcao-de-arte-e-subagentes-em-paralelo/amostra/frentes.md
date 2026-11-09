# As frentes do protótipo

Data: 08/11/2026.

## O pedido grande

A gerente: "Quero que fique bonito de verdade, com as cores da loja. Quero gente andando na calçada. E uma página para mandar aos clientes, com um botão para entrar no passeio."

## A divisão

| Frente | Arquivos que ela pode mexer | Lê antes | Devolve |
|---|---|---|---|
| Principal | `index.html` | Tudo | A juntada e o portão |
| Arte | `arte.js`, `DIRECAO-DE-ARTE.md` | `DIRECAO-DE-ARTE.md`, `loja-aurora.md` | A loja redesenhada e a seção 2 da direção preenchida |
| Vida | `vida.js` | `DIRECAO-DE-ARTE.md`, `MAPEAMENTO.md` | Gente e bichos na calçada |
| Página | `pagina.html`, `pagina.css` | `DIRECAO-DE-ARTE.md`, `loja-aurora.md` | A página de divulgação com o botão |

O `index.html` fica com a principal. É nele que as três frentes se encontram, e duas frentes no mesmo arquivo dão conflito.

## Instrução da frente Arte

1. **Objetivo.** Redesenhar a loja do Centro seguindo a direção de arte, para a gerente reconhecer a loja de longe.
2. **Leia antes.** `DIRECAO-DE-ARTE.md` e `loja-aurora.md`.
3. **Onde pode mexer.** `arte.js` e a seção 2 de `DIRECAO-DE-ARTE.md`. Nenhum outro arquivo. Se precisar, pare e me diga qual e por quê.
4. **Como testar sozinha.** A loja aparece com o zoom no mínimo e no máximo. O contorno é carvão. Só cores da seção 4.
5. **O que devolver.** Os arquivos que mexeu, como testou cada item, o que não testou e por quê, e as cores fora da paleta. Se não houver, escreva "nenhuma".
6. **Pare e pergunte se** uma foto não responder uma das cinco perguntas. Escreva "a foto não diz" e siga.

## Instrução da frente Vida

1. **Objetivo.** Pessoas e bichos andando sozinhos pela calçada em frente à loja, para o protótipo parecer vivo.
2. **Leia antes.** `DIRECAO-DE-ARTE.md` (paleta e tamanho das figuras) e `MAPEAMENTO.md` (onde ficam a calçada e a porta).
3. **Onde pode mexer.** `vida.js`. Nenhum outro arquivo. Se precisar, pare e me diga qual e por quê.
4. **Como testar sozinha.** No máximo 4 figuras e 1 bicho na tela. Ninguém entra na loja nem atravessa parede. Todo mundo para quando a conversa com o seu Dito abre. Roupa só com as cores da paleta.
5. **O que devolver.** Os arquivos que mexeu, como testou cada regra, o que não testou e por quê, e as cores fora da paleta. Se não houver, escreva "nenhuma".
6. **Pare e pergunte se** precisar mexer no `index.html` para testar. Ele não é seu.

## Instrução da frente Página

1. **Objetivo.** Uma página curta para a gerente mandar aos clientes, com um botão que abre o passeio.
2. **Leia antes.** `DIRECAO-DE-ARTE.md` (seções 4 e 6) e `loja-aurora.md`.
3. **Onde pode mexer.** `pagina.html` e `pagina.css`. Nenhum outro arquivo.
4. **Como testar sozinha.** O botão leva para `index.html`. A página cabe na tela do celular sem rolar para o lado. Só cores da paleta.
5. **O que devolver.** Os arquivos que mexeu, como testou, o que não testou e por quê, e as cores fora da paleta. Se não houver, escreva "nenhuma".
6. **Pare e pergunte se** quiser escrever algo que as fontes não dizem: preço, prazo, frete ou horário.

## O pedido ao agente principal

```text
Leia frentes.md e DIRECAO-DE-ARTE.md.

Abra três subagentes, um por frente: Arte, Vida e Página. Passe a cada
um a instrução da sua frente, como está em frentes.md. Cada um só mexe
nos arquivos da sua linha na tabela "A divisão". O index.html fica com
você.

Espere os três terminarem. Depois junte: carregue arte.js e vida.js no
index.html e ponha um link para pagina.html. Rode
python3 conferir_juntada.py --prototipo . e me mostre a saída.

Me devolva, para cada frente, o que ela entregou, o que testou e o que
não testou. Liste o que precisa de ajuste. Não ajuste nada antes de eu
responder.
```
