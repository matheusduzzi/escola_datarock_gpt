# Kit da aula: Backlog, teste como portão e um commit por história

Essa pasta faz parte do módulo bônus do curso ChatGPT no trabalho. Você precisa do git e do Node (o `npm` vem junto). O `conferir_backlog.py` roda com o Python 3 do seu computador. Nada aqui baixa pacote da internet.

| Arquivo | Para quê |
|---|---|
| `amostra/` | O protótipo da Loja Aurora, do jeito que ficou depois da aula anterior, com o `BACKLOG.md` das cinco histórias da aula |
| `portao/` | O portão: o `package.json` com `test` e `prepare`, o gancho `.githooks/pre-commit` e o `teste.cjs` da amostra |
| `tentativa-us-02/` | A primeira tentativa do agente para o carteiro: o `vida.js` com um problema e o `teste.cjs` com a regra nova. Ela serve para quebrar o teste de propósito na prática guiada |
| [BACKLOG.md](BACKLOG.md) | O modelo do backlog, em branco |
| [conferir_backlog.py](conferir_backlog.py) | Diz se o backlog e o `git log` batem: cinco histórias, critério com número, gancho ligado e um commit por história |
| [exercicio.md](exercicio.md) | O enunciado do exercício, igual ao da página da aula |

O `.githooks` começa com ponto. No Mac e no Linux, ele some da listagem comum; use `ls -a portao` para ver. No Windows, rode os comandos no Git Bash, que vem com o git.

## Antes de começar

O git precisa saber o seu nome e o seu e-mail para fazer commit. Se ele reclamar, rode uma vez:

```text
git config --global user.name "Seu nome"
git config --global user.email "seu@email"
```

## Como rodar

O passo a passo da prática guiada está na aula. Ele copia a `amostra` para uma pasta nova, a `pratica-loja`, dentro da sua pasta pessoal. Liga o portão e faz os commits lá. A pasta do kit não muda.

Dentro de um protótipo com o portão:

```text
npm run prepare
npm test
python3 conferir_backlog.py --repo .
```

O `npm run prepare` liga o gancho: ele manda o git procurar os ganchos na pasta `.githooks`. Essa configuração fica só na sua cópia do repositório. Quem clona precisa rodar de novo (o `npm install` também roda o `prepare`).

O `npm test` sai com 0 quando todas as regras passam e com 1 quando alguma falha. O gancho roda o `npm test` antes de cada commit e cancela o commit quando ele sai com 1.

O `conferir_backlog.py` sai com 0 quando nada falta e com 1 quando falta algo, com uma linha `FALTA` para cada problema. Ele não sabe se o número do critério é o certo, nem se o teste mede o que o critério diz. Isso fica com você.

## Se o gancho não rodar

- O git avisou que o gancho "was ignored because it's not set as executable": rode `chmod +x .githooks/pre-commit`.
- Você clonou o repositório e o commit quebrado passou: rode `npm run prepare`.
- O commit passou com `--no-verify`: essa opção pula o gancho. Não use, e peça ao agente que não use.

## Ajuda

Para pedir ajuda, deixe um comentário na aula. Conte o seu objetivo, o comando que você rodou, a saída e o que já tentou, sem dados pessoais.
