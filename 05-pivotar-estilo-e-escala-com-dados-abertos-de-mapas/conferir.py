"""Portão do protótipo: os dados do bairro carregam e os créditos estão na tela e no README.

Uso:
    python3 conferir.py --prototipo caminho/da/pasta/do/prototipo

A pasta precisa ter index.html, bairro-data.js (saído de montar_dados.py) e README.md.
Sai com 0 quando tudo passa e com 1 quando falta alguma coisa, dizendo o quê.
Ele não abre o navegador: olhar a tela e o canto dos créditos continua com você.
"""
import argparse
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

CREDITOS = {'OpenStreetMap': r'OpenStreetMap', 'ODbL': r'ODbL|Open Database License',
            'Overture': r'Overture', 'CDLA': r'CDLA'}


class Pagina(HTMLParser):
    """Separa o texto que aparece na tela dos scripts carregados. Comentário, <script> e <style> não contam."""
    def __init__(self):
        super().__init__()
        self.scripts, self.texto, self._fora, self._escondido = [], [], 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script' and a.get('src'):
            self.scripts.append(a['src'])
        if tag in ('script', 'style', 'template'):
            self._fora += 1
        estilo = (a.get('style') or '').replace(' ', '').lower()
        self._escondido.append('hidden' in a or 'display:none' in estilo or 'visibility:hidden' in estilo)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template'):
            self._fora -= 1
        if self._escondido:
            self._escondido.pop()

    def handle_data(self, d):
        if not self._fora and not any(self._escondido):
            self.texto.append(d)


def ler_dados(arq):
    texto = arq.read_text(encoding='utf-8').strip()
    m = re.fullmatch(r'window\.BAIRRO\s*=\s*(\{.*\})\s*;?', texto, re.S)
    if not m:
        raise ValueError('bairro-data.js precisa ser window.BAIRRO = {...}; como sai de montar_dados.py')
    return json.loads(m.group(1))


def pontos_ok(lista):
    return all(len(f['pontos']) >= 4 and len(f['pontos']) % 2 == 0 and
               all(isinstance(v, int) and math.isfinite(v) for v in f['pontos']) for f in lista)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--prototipo', default='.')
    pasta = Path(p.parse_args().prototipo)
    falhas, oks = [], []

    def checa(cond, ok, falta):
        (oks if cond else falhas).append(ok if cond else falta)

    dados = None
    arq = pasta / 'bairro-data.js'
    if not arq.exists():
        falhas.append('falta bairro-data.js na pasta do protótipo')
    else:
        try:
            dados = ler_dados(arq)
        except ValueError as e:
            falhas.append(str(e))
    if dados is not None:
        checa(dados.get('gerado_por') == 'montar_dados.py' and dados.get('osm_baixado_em'),
              f'dados gerados por script, OSM baixado em {dados.get("osm_baixado_em")}',
              'bairro-data.js sem gerado_por/osm_baixado_em: gere com baixar_bairro.py e montar_dados.py')
        checa(len(dados.get('vias', [])) > 0 and pontos_ok(dados['vias']),
              f'{len(dados.get("vias", []))} vias com pontos inteiros', 'vias vazias ou com ponto que não é número inteiro')
        checa(len(dados.get('predios', [])) > 0 and pontos_ok(dados['predios']),
              f'{len(dados.get("predios", []))} prédios com pontos inteiros',
              'prédios vazios ou com ponto que não é número inteiro (o Overture foi baixado?)')
        cred = ' '.join(dados.get('creditos', []))
        sem = [k for k, r in CREDITOS.items() if not re.search(r, cred)]
        checa(not sem, 'créditos ODbL e CDLA dentro dos dados', f'faltam nos créditos dos dados: {", ".join(sem)}')

    html = pasta / 'index.html'
    if not html.exists():
        falhas.append('falta index.html na pasta do protótipo')
    else:
        pg = Pagina()
        pg.feed(html.read_text(encoding='utf-8'))
        checa(any(Path(s).name == 'bairro-data.js' for s in pg.scripts),
              'index.html carrega bairro-data.js', 'index.html não tem <script src="bairro-data.js">')
        tela = ' '.join(' '.join(pg.texto).split())
        sem = [k for k, r in CREDITOS.items() if not re.search(r, tela)]
        checa(not sem, 'créditos OpenStreetMap/ODbL e Overture/CDLA no texto da tela',
              f'faltam na tela (comentário, script e elemento escondido não contam): {", ".join(sem)}')

    readme = pasta / 'README.md'
    if not readme.exists():
        falhas.append('falta README.md na pasta do protótipo')
    else:
        r = readme.read_text(encoding='utf-8')
        sem = [k for k, rx in CREDITOS.items() if not re.search(rx, r)]
        if 'openstreetmap.org/copyright' not in r:
            sem.append('link openstreetmap.org/copyright')
        checa(not sem, 'créditos e link de licença no README', f'faltam no README: {", ".join(sem)}')

    for o in oks:
        print('ok   ', o)
    for f in falhas:
        print('FALTA', f)
    sys.exit(1 if falhas else 0)


if __name__ == '__main__':
    main()
