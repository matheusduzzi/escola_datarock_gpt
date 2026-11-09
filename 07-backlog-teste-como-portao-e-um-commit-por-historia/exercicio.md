# Exercício: o backlog do seu protótipo, com o teste como portão

## Objetivo

Transformar cinco pedidos em histórias com critério que dá para medir. Pôr o teste no pre-commit do seu protótipo. Fazer cada história com o agente, um commit por história.

## Os pedidos

Use o seu protótipo da Loja Aurora, o das aulas anteriores. Se você não tem um, copie a pasta `amostra` dessa aula para uma pasta nova e comece por ela. Não use a pasta da prática guiada: ela já tem o portão e dois commits.

A gerente mandou quatro mensagens nessa semana:

1. "Põe o nome da loja em cima do toldo. Tem que dar para ler no celular."
2. "Na conversa, o seu Dito tem que dizer o horário: de segunda a sábado, das 9h às 18h."
3. "Quando eu abro a vista do bairro no celular, ela engasga." Se o seu protótipo não tem essa vista, troque por "a calçada engasga".
4. "O cachorro passa por cima da floreira da calçada."

A quinta história é sua: o teste rodando antes de cada commit, no seu repositório.

## O que entregar

1. **O `BACKLOG.md` com as cinco histórias**, no modelo do kit. Cada uma tem o pedido, a frase "Como, quero, para" e o critério com número e o lugar onde mede. Tem também a estimativa, a dependência e o estado. Pelo menos um critério mede tempo por quadro, antes e depois. Pelo menos um conta alguma coisa. A história do portão vem antes das outras.
2. **O portão**: o `package.json` com `test` e `prepare`, o `.githooks/pre-commit` executável e um teste com uma regra para cada critério que dá para contar. O tempo pode ficar fora do teste, medido no contador da página.
3. **Um commit recusado**: a saída do terminal de um commit com o teste quebrado, e o `git log --oneline` logo depois, sem esse commit.
4. **O log**: o `git log --oneline` com um commit por história, cada um com o id na mensagem. O Estado e o Medido de cada história mudam no mesmo commit dela.
5. **A saída do `python3 conferir_backlog.py --repo .`**, sem nenhuma linha `FALTA`.
6. **O que cada commit mudou**: para cada história, o `git show --stat` do commit. Se o `teste.cjs` mudou, diga qual regra entrou e mostre que nenhum limite antigo ficou mais frouxo.
7. **A sua conta**: a instrução que você deu ao agente numa das histórias, a data e como o commit aconteceu. O agente pediu aprovação para gravar no git, ou você fez o commit no seu terminal?

## Como avaliar o que você fez

Leia cada critério como se fosse outra pessoa medindo. Ela sabe o número, onde medir e o que conta como passar? "Ficar legível" não tem número. "Fonte de pelo menos 16 px" tem.

Depois quebre o teste de propósito e tente um commit. Se o commit entrar, o portão não está ligado.

<details><summary>Dica 1</summary>

Antes de escrever o critério, pergunte: o que eu contaria para saber que ficou pronto? Para a floreira, é quantas vezes o cachorro passa por cima dela em 2000 passos. Para o horário, é se o texto da conversa diz exatamente o que a gerente escreveu. Para o engasgo, são duas coisas: um tempo no contador e uma contagem no teste.

</details>

<details><summary>Dica 2</summary>

Peça ao agente que escreva a regra do critério no teste antes do código, e que rode o `npm test` para ver a regra falhar. Se ela passa antes de você mexer em qualquer coisa, a regra não mede o que o critério pede. Depois do código, ela tem que passar sem você mudar o limite.

</details>
