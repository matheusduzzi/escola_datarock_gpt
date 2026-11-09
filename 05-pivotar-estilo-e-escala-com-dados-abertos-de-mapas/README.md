# Kit da aula: Pivotar estilo e escala com dados abertos de mapas

Essa pasta faz parte do módulo bônus do curso ChatGPT no trabalho. Os scripts rodam com o Python 3 do seu computador. O protótipo você faz com o Codex, numa pasta sua.

| Arquivo | Para quê |
|---|---|
| [pivo.md](pivo.md) | O modelo do pivô: estilo novo, o que fica, o que muda, camadas e créditos. Salve uma cópia antes |
| [baixar_bairro.py](baixar_bairro.py) | Baixa as vias do OpenStreetMap (pela Overpass) e os prédios e lugares do Overture (pelo DuckDB) de uma caixa |
| [montar_dados.py](montar_dados.py) | Monta `bairro-data.js`, o arquivo que o protótipo carrega, com os créditos tirados dos dados |
| [conferir.py](conferir.py) | O portão: diz se o arquivo tem vias e prédios, se o `index.html` carrega o arquivo e se os créditos estão na tela e no README |
| `amostra/` | O que eu baixei com `baixar_bairro.py` em 08/11/2026, para quem estiver sem rede |
| [exercicio.md](exercicio.md) | O enunciado do exercício, igual ao da página da aula |

## O que precisa

- Python 3 e o `curl`. O `curl` já vem no macOS, no Windows 10 ou mais novo e em quase todo Linux; sem ele, o script usa o próprio Python.
- Para os prédios e lugares do Overture: o DuckDB para Python, com `pip3 install duckdb`. Na primeira vez, ele baixa duas extensões dele mesmo (`httpfs` e `spatial`).
- Rede, para o download. Sem rede, use a pasta `amostra`.

## Como rodar

Dentro da pasta do seu protótipo, com os scripts copiados para lá:

```text
python3 baixar_bairro.py --caixa=-27.5995,-48.5525,-27.5945,-48.5465 --saida dados
python3 montar_dados.py --entrada dados --saida bairro-data.js
python3 conferir.py --prototipo .
```

A caixa vai como sul, oeste, norte e leste, em graus, com ponto. Use o `=` depois de `--caixa`, porque o número começa com o sinal de menos. A caixa do kit é um pedaço do centro de Florianópolis, em volta da Praça XV, com uns 590 metros de leste a oeste e 560 de norte a sul. A Loja Aurora é inventada; as ruas e os prédios são de verdade.

O `baixar_bairro.py` não baixa de novo o que já está na pasta. Para baixar de novo, use `--de-novo`. Para uma caixa com mais de 3 km de lado, use `--grande`, depois que a camada do bairro estiver funcionando. Sem o DuckDB, use `--so-osm`: as ruas chegam e os prédios ficam para depois.

Sem rede:

```text
python3 montar_dados.py --entrada amostra --saida bairro-data.js
```

## Créditos dos dados da pasta amostra

Os arquivos de `amostra/` são trechos de bases abertas, baixados em 08/11/2026, e seguem as licenças delas.

- Vias, água e parques (`osm.json`): © OpenStreetMap contributors, disponível sob a Open Database License (ODbL). https://www.openstreetmap.org/copyright
- Prédios (`overture-predios.json`): Overture Maps Foundation, overturemaps.org, release 2026-10-21.0, tema de prédios sob ODbL. Fontes: OpenStreetMap (© OpenStreetMap contributors, Open Database License), Microsoft (Licensed by Microsoft under the Open Database License) e Google Open Buildings (Available under CC BY 4.0).
- Lugares (`overture-lugares.json`): Overture Maps Foundation, overturemaps.org, release 2026-10-21.0. Dados de Meta, Microsoft e Uberall, Available under CDLA Permissive 2.0. O arquivo traz também lugares da Foursquare (Copyright 2024 Foursquare Labs, Inc. All rights reserved. Available under Apache 2.0) e da AllThePlaces (Available under CC0 1.0); o `montar_dados.py` deixa esses fora do `bairro-data.js`.

Quem distribui uma base alterada a partir do OpenStreetMap distribui sob a mesma ODbL. Os textos completos de crédito de cada fonte estão em https://docs.overturemaps.org/attribution/.

## Ajuda

Para pedir ajuda, deixe um comentário na aula com o seu objetivo, o comando que você rodou, a saída e o que já tentou, sem dados pessoais.
