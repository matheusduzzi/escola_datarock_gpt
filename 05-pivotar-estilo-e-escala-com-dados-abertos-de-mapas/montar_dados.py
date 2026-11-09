"""Monta o arquivo que o protótipo carrega (bairro-data.js) a partir do que baixar_bairro.py baixou.

Uso:
    python3 montar_dados.py --entrada dados --saida bairro-data.js
    python3 montar_dados.py --entrada dados --saida bairro-data.js --origem -27.5970,-48.5495

O que ele faz:
1. põe a origem (0, 0) no centro da caixa, ou no ponto de --origem (a sua loja, por exemplo);
2. converte latitude e longitude em decímetros a partir da origem (x para o leste, y para o sul,
   como na tela), em números inteiros;
3. separa vias, água, parques, prédios e lugares;
4. escreve os créditos a partir das fontes que vieram nos dados.
O arquivo sai como window.BAIRRO = {...}; e abre com <script src="bairro-data.js">, até por file://.
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

M_POR_GRAU = 111320  # metros por grau de latitude (aproximação esférica, boa para um bairro)

# Texto de crédito de cada fonte, como pede a página de atribuição do Overture.
CREDITO_PREDIOS = {
    'OpenStreetMap': '© OpenStreetMap contributors. Available under the Open Database License.',
    'Microsoft ML Buildings': 'Licensed by Microsoft under the Open Database License.',
    'Esri Community Maps': 'Esri Community Maps contributors. Available under CC BY 4.0.',
    'Google Open Buildings': 'Google Open Buildings. Available under CC BY 4.0.',
}
LICENCAS_LUGARES = {'CDLA-Permissive-2.0': 'Available under CDLA Permissive 2.0.'}


def projecao(lat0, lon0):
    kx = M_POR_GRAU * math.cos(math.radians(lat0)) * 10
    ky = M_POR_GRAU * 10

    def xy(lon, lat):
        return round((lon - lon0) * kx), round(-(lat - lat0) * ky)
    return xy


def achatar(pontos, xy):
    saida = []
    for lon, lat in pontos:
        saida += xy(lon, lat)
    return saida


def aneis_externos(geo):
    if geo['type'] == 'Polygon':
        return [geo['coordinates'][0]]
    if geo['type'] == 'MultiPolygon':
        return [p[0] for p in geo['coordinates']]
    return []


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--entrada', default='dados')
    p.add_argument('--saida', default='bairro-data.js')
    p.add_argument('--origem', help='LAT,LON da origem; sem isso, o centro da caixa')
    a = p.parse_args()
    pasta = Path(a.entrada)
    try:
        info = json.loads((pasta / 'baixado.json').read_text())
        osm = json.loads((pasta / 'osm.json').read_text())
    except FileNotFoundError as e:
        sys.exit(f'faltou {e.filename}: rode antes python3 baixar_bairro.py --caixa ... --saida {pasta}')
    sul, oeste, norte, leste = info['caixa']
    if a.origem:
        lat0, lon0 = (float(v) for v in a.origem.split(','))
        if not (sul <= lat0 <= norte and oeste <= lon0 <= leste):
            sys.exit('a origem precisa ficar dentro da caixa baixada')
    else:
        lat0, lon0 = (sul + norte) / 2, (oeste + leste) / 2
    xy = projecao(lat0, lon0)

    vias, agua, parques = [], [], []
    for el in osm.get('elements', []):
        if el.get('type') != 'way' or 'geometry' not in el:
            continue
        t = el.get('tags', {})
        pts = achatar([(g['lon'], g['lat']) for g in el['geometry']], xy)
        if 'highway' in t:
            vias.append({'tipo': t['highway'], 'nome': t.get('name', ''), 'pontos': pts})
        elif 'waterway' in t or t.get('natural') == 'water':
            agua.append({'pontos': pts})
        elif t.get('leisure') == 'park':
            parques.append({'nome': t.get('name', ''), 'pontos': pts})

    creditos = ['Vias, água e parques: © OpenStreetMap contributors, sob a licença ODbL '
                '(openstreetmap.org/copyright).']
    predios, lugares = [], []
    arq_p, arq_l = pasta / 'overture-predios.json', pasta / 'overture-lugares.json'
    if arq_p.exists():
        brutos = json.loads(arq_p.read_text())
        fontes = Counter(b['fonte'] for b in brutos)
        for b in brutos:
            for anel in aneis_externos(b['geometria']):
                predios.append({'altura': b['altura'], 'pontos': achatar(anel, xy)})
        partes = [CREDITO_PREDIOS.get(f, f'{f} (ver docs.overturemaps.org/attribution)') for f in sorted(fontes)]
        creditos.append('Prédios: Overture Maps Foundation, overturemaps.org. ' + ' '.join(partes))
    if arq_l.exists():
        brutos = json.loads(arq_l.read_text())
        aceitos = [l for l in brutos if l.get('licenca') in LICENCAS_LUGARES]
        for l in aceitos:
            x, y = xy(l['lon'], l['lat'])
            lugares.append({'nome': l['nome'] or '', 'categoria': l['categoria'] or '', 'x': x, 'y': y})
        if aceitos:
            nomes = sorted({l['fonte'][:1].upper() + l['fonte'][1:] for l in aceitos})
            quem = ', '.join(nomes[:-1]) + ' e ' + nomes[-1] if len(nomes) > 1 else nomes[0]
            creditos.append(f'Lugares: Overture Maps Foundation, overturemaps.org. Dados de {quem}. '
                            'Available under CDLA Permissive 2.0.')
        fora = len(brutos) - len(aceitos)
        if fora:
            print(f'lugares fora do arquivo por outra licença: {fora}')

    bairro = {
        'gerado_por': 'montar_dados.py',
        'caixa': info['caixa'],
        'origem': [lat0, lon0],
        'unidade': 'decímetro',
        'osm_baixado_em': info.get('osm_baixado_em'),
        'osm_base': info.get('osm_base'),
        'overture_baixado_em': info.get('overture_baixado_em'),
        'overture_release': info.get('overture_release'),
        'vias': vias, 'agua': agua, 'parques': parques, 'predios': predios, 'lugares': lugares,
        'creditos': creditos,
    }
    texto = 'window.BAIRRO = ' + json.dumps(bairro, ensure_ascii=False, separators=(',', ':')) + ';\n'
    Path(a.saida).write_text(texto)
    print(f'vias: {len(vias)} | água: {len(agua)} | parques: {len(parques)} | '
          f'prédios: {len(predios)} | lugares: {len(lugares)}')
    print(f'{a.saida}: {len(texto.encode()) / 1024:.0f} KB')
    for c in creditos:
        print('crédito:', c)


if __name__ == '__main__':
    main()
