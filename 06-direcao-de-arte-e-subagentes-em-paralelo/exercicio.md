# Exercício: três frentes no protótipo da Loja Aurora

## Objetivo

Dividir o pedido da gerente em três frentes (arte, vida e página) e escrever a instrução de cada uma. Escrever a direção de arte antes de abrir as frentes. Juntar o que voltou e anotar o que precisou de ajuste.

## O pedido

A gerente quer o protótipo "bonito de verdade, com as cores da loja". Quer gente andando na calçada. E quer uma página para mandar aos clientes, com um botão para entrar no passeio. Eu mostrei na aula a minha direção de arte, a instrução da frente Vida, o pedido ao agente principal e a juntada da pasta `amostra`. Agora é a sua vez, no seu protótipo, com o agente.

Na pasta dessa aula no kit estão `frentes.md`, `DIRECAO-DE-ARTE.md`, `juntada.md` e `conferir_juntada.py`. Copie os quatro para a pasta do seu protótipo, com os mesmos nomes.

## O que entregar

1. **A direção de arte**, no `DIRECAO-DE-ARTE.md`, escrita antes de abrir as frentes, com a data. Ela tem a regra-mãe e as cinco perguntas das três fotos, com "a foto não diz" onde a foto não responde. Tem também o traço, a luz e a sombra, e uma paleta com pelo menos 5 cores em hex, cada uma com onde usa. E tem as regras de pessoas e bichos, as regras da página e pelo menos 3 itens de "como eu reviso". Sem o nome de um jogo ou de uma marca.
2. **A divisão e as três instruções**, no `frentes.md`. Na tabela "A divisão", cada arquivo de código da pasta tem uma dona só. E o arquivo em que tudo se encontra (o `index.html`) fica com a principal. Cada instrução tem as seis partes. Em "Como testar sozinha", cada frente tem pelo menos uma regra com número ou com sim e não. Em "O que devolver", cada uma pede o que não foi testado e as cores fora da paleta.
3. **O pedido ao agente principal**, copiado no fim do `frentes.md`. Ele diz como dividir, que o principal espera as três frentes e o que devolver no fim.
4. **A juntada**, no `juntada.md`. Ela traz o que cada frente entregou, o que testou e o que não testou, e a saída do `python3 conferir_juntada.py --prototipo .` antes dos ajustes. Traz também a tabela dos ajustes: cada problema do portão e pelo menos uma coisa que você olhou e o portão não lê, como o texto da página. Se uma frente não precisou de ajuste, escreva "nenhum" na linha dela. Fecha com a saída do portão depois dos ajustes, sem nenhuma linha `FALTA`.
5. **A sua conta**: a data e o que a tela mostrou de cada frente. Diga também se o Codex abriu os subagentes ou se as frentes rodaram uma depois da outra.

## Como avaliar o que você fez

Leia cada instrução como se fosse o ajudante. Ele não viu a mensagem da gerente nem a aula. Com a instrução e os arquivos de "Leia antes", ele sabe o que fazer, onde mexer e quando parar? Se uma linha depende de algo que só está na sua cabeça, escreva essa coisa na instrução.

Depois abra o protótipo e a página lado a lado. Ache uma cor de cada frente na paleta. Leia a página inteira contra a seção 6 da direção de arte.

<details><summary>Dica 1</summary>

Para a divisão, faça as três perguntas da aula a cada pedaço: anda sem o resultado do outro, mexe em arquivos só dele, dá para testar sozinho. O que você já tem das aulas anteriores, como os dados do bairro e o desenho do mapa, fica na linha da principal. Assim nenhuma frente mexe no que já funciona.

</details>

<details><summary>Dica 2</summary>

Na primeira vez, o portão deve acusar cores que vieram das aulas anteriores, como o fundo e o texto do seu `index.html`. Para cada uma, decida: ou ela entra na paleta, com nome e lugar de uso, ou o código troca para uma cor que já está lá. Apagar a seção "Paleta" não resolve: o portão pede pelo menos 3 cores nela.

</details>
