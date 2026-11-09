# Backlog: passeio pela Loja Aurora

Cada história tem o pedido de quem pediu, a frase "Como, quero, para", um critério com número e o jeito de medir. O estado vai de "a fazer" para "a medir" (o código entrou, falta um número do critério) ou "feita" (tudo medido). O estado e o "Medido" mudam no mesmo commit da história.

## US-01: Calçada sem trancos no celular
- Pedido: "No meu celular, a calçada anda aos trancos." (gerente)
- História: Como cliente, quero ver a calçada andar sem trancos no celular, para passear pela loja sem desistir no meio.
- Critério: no máximo 150 chamadas de desenho por quadro, no npm test; pior quadro abaixo de 16 ms no contador da página, no celular da gerente, medido antes e depois.
- Medido:
- Estimativa: M
- Depende de: US-05
- Estado: a fazer

## US-02: O carteiro na calçada
- Pedido: "Põe o carteiro passando. Ele passa aqui todo dia de manhã." (gerente)
- História: Como gerente, quero o carteiro passando na calçada, para a rua parecer a de verdade.
- Critério: 1 carteiro na calçada; a calçada continua com no máximo 4 figuras e 1 bicho; ninguém sai da calçada em 2000 passos. Tudo no npm test.
- Medido:
- Estimativa: P
- Depende de: US-05
- Estado: a fazer

## US-03: Falar com o seu Dito pelo celular
- Pedido: "Uma cliente abriu no celular e não conseguiu falar com o seu Dito. Celular não tem barra de espaço." (gerente)
- História: Como cliente no celular, quero um botão para abrir e fechar a conversa com o seu Dito, para não ficar presa nela.
- Critério: um botão na página abre e fecha a conversa, 3 de 3 vezes no npm test; com a conversa aberta, 0 figuras andam.
- Medido:
- Estimativa: P
- Depende de: US-05
- Estado: a fazer

## US-04: A vitrine da semana
- Pedido: "A vitrine tem que mostrar os três jogos de cama da semana." (gerente)
- História: Como gerente, quero as três peças da semana na vitrine, para o cliente ver o que tem de novo antes de entrar.
- Critério: exatamente 3 peças na vitrine, as 3 com cor da paleta, no npm test.
- Medido:
- Estimativa: P
- Depende de: US-05
- Estado: a fazer

## US-05: Teste antes de cada commit
- Pedido: "Ontem o agente mexeu no vida.js e a pausa da conversa quebrou. Ninguém viu até a gerente reclamar." (eu)
- História: Como mantenedor, quero o teste rodando antes de cada commit, para nenhuma mudança quebrar o que já funcionava sem eu ver.
- Critério: um commit com o teste falhando é recusado e não entra no git log; o npm test leva menos de 2 segundos.
- Medido:
- Estimativa: P
- Depende de: nenhuma
- Estado: a fazer
