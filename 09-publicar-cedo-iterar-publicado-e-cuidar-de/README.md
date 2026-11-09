# Kit da aula: Publicar cedo, iterar publicado e cuidar de direitos

Essa pasta faz parte do módulo bônus do curso ChatGPT no trabalho. O `publicar.py` roda com o Python 3 do seu computador e não precisa de nenhum pacote. O teste da amostra roda com o Node, o mesmo da aula de backlog. A publicação você faz no ChatGPT, com a sua conta.

| Arquivo | Para quê |
|---|---|
| [DIREITOS.md](DIREITOS.md) | O modelo da lista de direitos, em branco: arquivos, pessoas e marcas e referência visual |
| [VERSOES.md](VERSOES.md) | O modelo do registro de versões: uma linha por versão publicada |
| [publicar.py](publicar.py) | Monta a pasta `dist` só com o que tem "publicar" e diz o que falta antes de abrir ao público |
| `amostra/` | O passeio da loja do Centro depois de três versões privadas, com o `DIREITOS.md` e o `VERSOES.md` preenchidos e alguns problemas de propósito |
| [exercicio.md](exercicio.md) | O enunciado do exercício, igual ao da página da aula |

## Os comandos

Rode dentro da pasta que tem o `DIREITOS.md` e o `VERSOES.md`. O protótipo fica na pasta `prototipo` ao lado; se o seu estiver em outro lugar, use `--prototipo` com o caminho. Na `amostra`, o `publicar.py` está uma pasta acima, então o comando começa com `python3 ../publicar.py`.

| Comando | O que faz |
|---|---|
| `python3 publicar.py montar` | Apaga e refaz a pasta `dist` com os arquivos que têm a decisão `publicar`. Lista o que vai, o que fica fora e o que não tem linha |
| `python3 publicar.py conferir` | Lê as duas tabelas e a `dist`. Uma linha `FALTA` por problema |

O `conferir` sai com 0 quando nada falta e com 1 quando falta algo. Ele olha:
- se o endereço privado e a data da checagem estão preenchidos;
- se a `dist` é a montagem de agora;
- se cada linha de arquivo está completa, e se foto de terceiro sem licença livre vai para o ar;
- se a página que carrega dados de mapa mostra o crédito na tela, e se o README do protótipo também traz o crédito;
- se alguma pessoa real sem autorização vai para o ar, e se o nome de quem ficou de fora ainda aparece nos arquivos publicados;
- se há pelo menos três versões, cada uma com commit, o que mudou e onde testou.

O que ele não faz: olhar as imagens. Gente reconhecível numa foto, um personagem que lembra alguém e um mascote que imita uma marca passam pelo `conferir`. Isso fica com você.

## A prática guiada

Dentro da pasta `amostra`:

```text
python3 ../publicar.py montar
python3 ../publicar.py conferir
node prototipo/teste.cjs
```

A amostra não foi publicada. O endereço termina em `.example`, um domínio reservado para exemplos, e os commits do `VERSOES.md` são de exemplo. A foto da vitrine em `prototipo/referencias` é um desenho no lugar de um print de foto de terceiro. Os dados do mapa vieram do OpenStreetMap e do Overture, baixados pelo script da aula de mapas em 08/11/2026. Eles seguem as licenças deles, e os créditos estão no `prototipo/README.md`. A aula traz as perguntas e a resposta. Para ver o passeio, abra `amostra/prototipo/index.html` no navegador.

## Ajuda

Para pedir ajuda, deixe um comentário na aula. Conte o seu objetivo, o comando que você rodou, a saída e o que já tentou, sem dados pessoais.
