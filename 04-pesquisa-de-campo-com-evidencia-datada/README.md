# Kit da aula: Pesquisa de campo com evidência datada

Essa pasta faz parte do módulo bônus do curso ChatGPT no trabalho. A página do Guia do Bairro é do curso e abre no seu computador, sem internet. O modelo do mapeamento é texto em Markdown.

| Arquivo | Para quê |
|---|---|
| [guia-do-bairro/loja-aurora-centro.html](guia-do-bairro/loja-aurora-centro.html) | A página da loja do Centro no Guia do Bairro: horário, fotos e avaliações. É ela que o agente pesquisa |
| [guia-do-bairro/entrar.html](guia-do-bairro/entrar.html) | A tela de login do Guia do Bairro. O formulário não envia nada |
| [MAPEAMENTO.md](MAPEAMENTO.md) | O modelo do mapeamento, com as cinco partes. Salve uma cópia antes |
| [exercicio.md](exercicio.md) | O enunciado do exercício, igual ao da página da aula |

Você também vai usar o `loja-aurora.md`, com a descrição das três fotos da loja, que está na pasta da aula «Apresentação do case: de um pedido a um jogo publicado».

Copie a pasta `guia-do-bairro` e o `MAPEAMENTO.md` para a pasta do seu protótipo e abra o Codex nela. Peça ao agente para abrir o arquivo no navegador dele. Se a sua versão não abrir o arquivo direto, rode dentro de `guia-do-bairro`:

```text
python3 -m http.server 8000 --bind 127.0.0.1
```

e peça para ele abrir `http://127.0.0.1:8000/loja-aurora-centro.html`. Para parar o servidor, use Ctrl + C no terminal.

Se o Codex não abrir na sua conta, abra a página no seu navegador e preencha o mapeamento à mão, marcando "eu, à mão" no topo.

Para pedir ajuda, deixe um comentário na aula com o seu objetivo, o pedido que você mandou, o que o agente respondeu e o que já tentou, sem dados pessoais.
