"""Baixa as vias (OpenStreetMap) e os prédios e lugares (Overture Maps) de uma caixa pequena.

Uso:
    python3 baixar_bairro.py --caixa SUL,OESTE,NORTE,LESTE --saida dados
    python3 baixar_bairro.py --caixa ... --saida dados --so-osm      # sem o Overture (sem DuckDB)

A caixa vai em graus decimais, com ponto: sul e norte são latitudes, oeste e leste são longitudes.
Cada arquivo baixado fica em --saida e não é baixado de novo (use --de-novo para forçar).
Créditos dos dados: veja README.md.
"""
import argparse
import datetime as dt
import json
import math
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

OVERPASS = 'https://overpass-api.de/api/interpreter'
RELEASE = '2026-10-21.0'  # release do Overture fixada; troque só de propósito e anote
S3 = f's3://overturemaps-us-west-2/release/{RELEASE}'
LADO_MAX_KM = 3.0  # primeira camada: um bairro. Para a cidade, use --grande


def caixa(texto, grande=False):
    try:
        sul, oeste, norte, leste = (float(v) for v in texto.split(','))
    except ValueError:
        sys.exit('caixa inválida: use SUL,OESTE,NORTE,LESTE em graus, com ponto (ex.: -27.5995,-48.5525,-27.5945,-48.5465)')
    if not (-90 <= sul < norte <= 90 and -180 <= oeste < leste <= 180):
        sys.exit('caixa inválida: o sul precisa ser menor que o norte e o oeste menor que o leste')
    alto = (norte - sul) * 111.32
    largo = (leste - oeste) * 111.32 * math.cos(math.radians((sul + norte) / 2))
    if max(alto, largo) > LADO_MAX_KM and not grande:
        sys.exit(f'caixa de {largo:.1f} km × {alto:.1f} km: comece por um bairro (até {LADO_MAX_KM:.0f} km de lado) '
                 'ou use --grande quando a camada do bairro já estiver funcionando')
    return sul, oeste, norte, leste


def consulta_osm(sul, oeste, norte, leste):
    c = f'{sul},{oeste},{norte},{leste}'
    return ('[out:json][timeout:90];\n'
            f'( way["highway"]({c});\n'
            f'  way["waterway"]({c});\n'
            f'  way["natural"="water"]({c});\n'
            f'  way["leisure"="park"]({c}); );\n'
            'out geom;')


def baixar_osm(cx, destino):
    """Manda a consulta à Overpass com curl, como no case; sem curl, usa o urllib do Python."""
    consulta = consulta_osm(*cx)
    if shutil.which('curl'):
        r = subprocess.run(['curl', '-sS', '--fail', '-m', '120', '-A', 'kit-escola-datarock/1.0',
                            '--data-urlencode', 'data=' + consulta, OVERPASS, '-o', str(destino)],
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(f'a Overpass não respondeu ({r.stderr.strip()}). Sem rede? Espere 30 s e tente de novo')
    else:
        corpo = urllib.parse.urlencode({'data': consulta}).encode()
        pedido = urllib.request.Request(OVERPASS, data=corpo, headers={'User-Agent': 'kit-escola-datarock/1.0'})
        with urllib.request.urlopen(pedido, timeout=120) as r:
            destino.write_bytes(r.read())
    dados = json.loads(destino.read_text())
    return len(dados.get('elements', [])), dados.get('osm3s', {}).get('timestamp_osm_base')


def baixar_overture(cx, pasta):
    try:
        import duckdb
    except ImportError:
        sys.exit('falta o DuckDB para o Overture: pip3 install duckdb (ou rode com --so-osm)')
    sul, oeste, norte, leste = cx
    con = duckdb.connect()
    con.sql("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
    na_caixa = (f'bbox.xmin < {leste} AND bbox.xmax > {oeste} AND bbox.ymin < {norte} AND bbox.ymax > {sul}')
    predios = con.sql(f"""
        SELECT id, height, num_floors, class, sources[1].dataset, ST_AsGeoJSON(geometry)
        FROM read_parquet('{S3}/theme=buildings/type=building/*', hive_partitioning=1)
        WHERE {na_caixa}""").fetchall()
    lista = [{'id': i, 'altura': h, 'andares': a, 'classe': c, 'fonte': f, 'geometria': json.loads(g)}
             for i, h, a, c, f, g in predios]
    (pasta / 'overture-predios.json').write_text(json.dumps(lista, ensure_ascii=False))
    lugares = con.sql(f"""
        SELECT id, names.primary, basic_category, confidence, sources[1].dataset, sources[1].license,
               ST_X(geometry), ST_Y(geometry)
        FROM read_parquet('{S3}/theme=places/type=place/*', hive_partitioning=1)
        WHERE {na_caixa}""").fetchall()
    lista2 = [{'id': i, 'nome': n, 'categoria': c, 'confianca': cf, 'fonte': f, 'licenca': l, 'lon': x, 'lat': y}
              for i, n, c, cf, f, l, x, y in lugares]
    (pasta / 'overture-lugares.json').write_text(json.dumps(lista2, ensure_ascii=False))
    return len(lista), len(lista2)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--caixa', required=True)
    p.add_argument('--saida', default='dados')
    p.add_argument('--so-osm', action='store_true')
    p.add_argument('--grande', action='store_true')
    p.add_argument('--de-novo', action='store_true')
    a = p.parse_args()
    cx = caixa(a.caixa, a.grande)
    pasta = Path(a.saida)
    pasta.mkdir(parents=True, exist_ok=True)
    info_arq = pasta / 'baixado.json'
    info = json.loads(info_arq.read_text()) if info_arq.exists() else {}
    if info and info.get('caixa') != list(cx):
        sys.exit(f'{pasta} já tem dados de outra caixa {info.get("caixa")}: use outra pasta em --saida')
    agora = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    info.update({'caixa': list(cx), 'gerado_por': 'baixar_bairro.py'})

    osm = pasta / 'osm.json'
    if osm.exists() and not a.de_novo:
        print(f'osm.json já existe, não baixei de novo ({info.get("osm_baixado_em")})')
    else:
        n, base = baixar_osm(cx, osm)
        info.update({'osm_baixado_em': agora, 'osm_base': base})
        print(f'OpenStreetMap: {n} elementos (vias, água, parques), base de {base}')

    if a.so_osm:
        print('Overture pulado (--so-osm): o protótipo fica sem prédios até você baixar')
    elif (pasta / 'overture-predios.json').exists() and not a.de_novo:
        print(f'Overture já existe, não baixei de novo ({info.get("overture_baixado_em")})')
    else:
        n_p, n_l = baixar_overture(cx, pasta)
        info.update({'overture_baixado_em': agora, 'overture_release': RELEASE})
        print(f'Overture {RELEASE}: {n_p} prédios e {n_l} lugares')
    info_arq.write_text(json.dumps(info, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
