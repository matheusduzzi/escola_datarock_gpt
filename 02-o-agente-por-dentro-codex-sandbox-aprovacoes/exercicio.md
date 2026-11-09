# Exercício: o quadro do agente para o seu protótipo

## Objetivo

Montar o quadro do que o agente vai fazer no protótipo da Loja Aurora. Para cada capacidade, o que libera ou bloqueia e um exemplo do case. O quadro também traz um pedido de permissão escrito por você. Ele volta na aula «O primeiro pedido e o feedback por print».

## O pedido

A gerente da Loja Aurora perguntou o que o agente pode fazer sozinho no computador da loja. Eu respondo com um quadro de uma página. Agora é a sua vez.

Salve uma cópia de `quadro-agente.md`, na pasta dessa aula no kit, e preencha as quatro partes. Use a aula e a ficha do protótipo da aula anterior.

## O que o quadro precisa ter

1. **As cinco capacidades.** Para ler imagem, editar código, rodar comando, usar o navegador e dividir o trabalho, escreva:
   - o que o agente fez no case;
   - o que libera ou bloqueia essa capacidade (modo da sandbox, rede, aprovação, perfil do navegador ou herança da sandbox);
   - uma ação dessa capacidade no seu protótipo.
2. **A falha de rede do case.** O comando, o destino, a mensagem de erro, a causa e o que o agente fez em seguida.
3. **O seu pedido de permissão.** Uma ação do seu protótipo que precisa da internet e o pedido que você aprovaria. Ele responde às quatro perguntas: o que roda, para onde vai, por que precisa e o que fica gravado. Não vale pedir acesso total nem a rede ligada para sempre.
4. **A sua conta.** O modo da sandbox e da aprovação que o Codex mostrou, com a data. Sem o Codex, a marca "não testado".

## Como avaliar seu quadro

Leia a coluna do que libera ou bloqueia. Em cada linha, dá para dizer qual chave você mexeria para mudar o comportamento? "Depende" ou "o agente decide" ainda não responde.

Depois, leia o seu pedido de permissão como se você fosse o revisor. Você sabe para qual site vai e o que vai ficar gravado? Se precisou adivinhar, falta uma das quatro respostas.

Por último, olhe a causa da falha de rede. Se está escrito que o site estava fora do ar, volte na seção 4 da aula.

<details><summary>Dica 1</summary>

Comece pela linha de rodar comando. Separe dois comandos do case: o teste automático e o download das ruas. Os dois são comandos, mas só um precisa da internet. A diferença entre eles é o que vai na coluna do meio.

</details>

<details><summary>Dica 2</summary>

Para o pedido de permissão, pense no mapa do bairro de exemplo do seu protótipo. Escreva o site de onde ele vem, o que você pede a esse site e o nome do arquivo onde ele fica salvo. Depois, diga o que acontece com o protótipo se o pedido for negado.

</details>
