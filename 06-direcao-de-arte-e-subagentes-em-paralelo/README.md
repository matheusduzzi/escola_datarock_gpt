# Kit da aula: Direção de arte e subagentes em paralelo

Essa pasta faz parte do módulo bônus do curso ChatGPT no trabalho. O portão roda com o Python 3 do seu computador, sem instalar nada. As frentes você roda com o Codex, na pasta do seu protótipo.

| Arquivo | Para quê |
|---|---|
| [frentes.md](frentes.md) | O modelo da divisão: a tabela "A divisão", as três instruções em seis partes e o pedido ao agente principal |
| [DIRECAO-DE-ARTE.md](DIRECAO-DE-ARTE.md) | O modelo da direção de arte: regra-mãe, as cinco perguntas de cada foto, traço, paleta em hex e como revisar |
| [juntada.md](juntada.md) | O modelo da juntada: o que cada frente entregou, o portão antes e depois e os ajustes |
| [conferir_juntada.py](conferir_juntada.py) | O portão: diz se as três frentes estão na divisão, se algum arquivo tem duas donas ou nenhuma e se alguma cor em hex está fora da paleta |
| `amostra/` | Uma juntada pronta para a prática guiada, com a minha direção de arte, as instruções, os arquivos das três frentes e os relatórios |
| [exercicio.md](exercicio.md) | O enunciado do exercício, igual ao da página da aula |

## Como rodar

Copie `frentes.md`, `DIRECAO-DE-ARTE.md`, `juntada.md` e `conferir_juntada.py` para a pasta do seu protótipo, com os mesmos nomes. Preencha a direção de arte e o `frentes.md` antes de pedir ao agente. Depois que as frentes voltarem, dentro da pasta do protótipo:

```text
python3 conferir_juntada.py --prototipo .
```

Ele sai com 0 quando não falta nada e com 1 quando falta algo, com uma linha `FALTA` para cada problema. Ele lê os `.html`, `.js` e `.css` da pasta e pula as pastas `dados`, `amostra`, `dist`, `node_modules` e `.git`.

O portão só lê cor escrita em hex, como `#3f7d4e`. Cor em `rgb()`, em `hsl()` ou sorteada no código passa sem aviso. E ele não lê o sentido do texto: uma promessa na página passa. Essas partes ficam com você.

## A prática guiada

Dentro dessa pasta do kit:

```text
python3 conferir_juntada.py --prototipo amostra
```

A amostra tem problemas de propósito. A aula traz as perguntas e a resposta. Para ver a loja, abra `amostra/index.html` no navegador; a barra de espaço abre e fecha a conversa com o seu Dito.

## Ajuda

Para pedir ajuda, deixe um comentário na aula com o seu objetivo, o comando que você rodou, a saída e o que já tentou, sem dados pessoais.
