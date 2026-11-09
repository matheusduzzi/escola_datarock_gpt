"""Monta a pasta pública do protótipo e diz o que falta antes de abrir ao público.

Rode dentro da pasta que tem o DIREITOS.md e o VERSOES.md:

    python3 publicar.py montar
    python3 publicar.py conferir

montar   copia para dist/ só os arquivos do protótipo com a decisão "publicar" no DIREITOS.md.
         Arquivo sem linha fica fora, e ele avisa.
conferir lê o DIREITOS.md, o VERSOES.md e a dist/. Escreve uma linha FALTA por problema.
         Sai com 0 quando nada falta e com 1 quando falta algo.

Opções: --prototipo <pasta> (padrão: prototipo) e --dist <pasta> (padrão: dist).
Só usa a biblioteca padrão do Python 3.
"""
import argparse
import fnmatch
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

VAZIO = {'', '—', '-', '?', 'a ver', 'a preencher'}
DECISOES = {'publicar', 'fica fora'}
LIVRE = ('cc0', 'cc by', 'domínio público', 'dominio publico', 'própria', 'propria')
TEXTO = {'.html', '.htm', '.js', '.css', '.json', '.md', '.txt', '.svg'}
# Crédito que cada licença pede na tela. Cada item: (palavra que liga a regra, palavras que a tela precisa mostrar)
CREDITOS = [
    ('odbl', ['OpenStreetMap', 'ODbL']),
    ('cdla', ['Overture', 'CDLA']),
]


def celulas(linha):
    return [c.strip() for c in linha.strip().strip('|').split('|')]


def secoes(texto):
    """Separa o Markdown pelos títulos ## e devolve {título: linhas}."""
    atual, saida = '', {'': []}
    for linha in texto.splitlines():
        if linha.startswith('## '):
            atual = linha[3:].strip().lower()
            saida[atual] = []
        else:
            saida[atual].append(linha)
    return saida


def tabela(linhas):
    """Linhas de uma tabela Markdown, sem o cabeçalho e sem a linha de traços."""
    rows = [celulas(l) for l in linhas if l.strip().startswith('|')]
    return [r for r in rows[2:] if any(c for c in r)]


def campo(linhas, nome):
    for l in linhas:
        m = re.match(r'\s*' + re.escape(nome) + r'\s*:\s*(.*)$', l, re.I)
        if m:
            return m.group(1).strip()
    return ''


def vazio(c):
    return c.strip().lower() in VAZIO


class Visivel(HTMLParser):
    """Junta o texto que aparece na tela: sem comentário, script, style nem elemento com hidden."""
    PULA = {'script', 'style', 'template', 'noscript'}
    VAZIOS = {'br', 'img', 'meta', 'link', 'input', 'hr', 'source', 'area', 'base', 'col', 'embed', 'param', 'track', 'wbr'}

    def __init__(self):
        super().__init__()
        self.pilha, self.texto, self.scripts = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'script' and a.get('src'):
            self.scripts.append(a['src'])
        if tag in self.VAZIOS:
            return
        esconde = tag in self.PULA or 'hidden' in a or 'display:none' in (a.get('style') or '').replace(' ', '')
        self.pilha.append(esconde)

    def handle_endtag(self, tag):
        if tag not in self.VAZIOS and self.pilha:
            self.pilha.pop()

    def handle_data(self, data):
        if not any(self.pilha):
            self.texto.append(data)


def ler_pagina(caminho):
    p = Visivel()
    p.feed(caminho.read_text(errors='ignore'))
    return ' '.join(' '.join(p.texto).split()), p.scripts


def ler_direitos(pasta):
    arq = pasta / 'DIREITOS.md'
    if not arq.is_file():
        sys.exit('não achei o DIREITOS.md nessa pasta: copie o modelo do kit e preencha')
    s = secoes(arq.read_text())
    cab = s.get('', [])
    return {
        'endereco': campo(cab, 'Endereço privado'),
        'data': campo(cab, 'Checado em'),
        'arquivos': tabela(s.get('arquivos', [])),
        'pessoas': tabela(s.get('pessoas', [])),
        'marcas': tabela(s.get('marcas e referência visual', [])),
    }


def arquivos_do_prototipo(prot, dist):
    saida = []
    for p in sorted(prot.rglob('*')):
        rel = p.relative_to(prot).as_posix()
        if not p.is_file() or rel.split('/')[0] in {'.git', '.openai', 'node_modules'} or p.name == '.DS_Store':
            continue
        if dist.resolve() in p.resolve().parents:
            continue
        saida.append(rel)
    return saida


def linha_de(rel, linhas):
    """A linha exata vence o padrão (sprites/*.png); entre padrões, vale o primeiro."""
    for l in linhas:
        if l[0].strip('`') == rel:
            return l
    for l in linhas:
        if any(ch in l[0] for ch in '*?[') and fnmatch.fnmatch(rel, l[0].strip('`')):
            return l
    return None


def plano(pasta, prot, dist):
    d = ler_direitos(pasta)
    linhas = [l + [''] * (6 - len(l)) for l in d['arquivos']]
    vai, fora, sem = [], [], []
    for rel in arquivos_do_prototipo(prot, dist):
        l = linha_de(rel, linhas)
        if l is None:
            sem.append(rel)
        elif l[5].strip().lower() == 'publicar':
            vai.append((rel, l))
        else:
            fora.append(rel)
    return d, linhas, vai, fora, sem


def montar(pasta, prot, dist):
    if not prot.is_dir():
        sys.exit(f'não achei a pasta do protótipo: {prot}')
    d, linhas, vai, fora, sem = plano(pasta, prot, dist)
    erros = 0
    for l in linhas:
        nome = l[0].strip('`')
        tem = any(ch in nome for ch in '*?[') or (prot / nome).is_file()
        if not tem:
            print(f'FALTA: a linha "{nome}" do DIREITOS.md não acha arquivo no protótipo')
            erros += 1
    if dist.resolve() in (pasta.resolve(), prot.resolve()) or prot.resolve() in dist.resolve().parents \
            or dist.resolve() in prot.resolve().parents:
        sys.exit('a pasta da dist precisa ser separada da pasta do protótipo')
    if dist.exists():
        shutil.rmtree(dist)
    total = 0
    for rel, _ in vai:
        destino = dist / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(prot / rel, destino)
        total += destino.stat().st_size
        print(f'vai: {rel}')
    for rel in fora:
        print(f'fica fora: {rel}')
    for rel in sem:
        print(f'SEM LINHA: {rel} (ficou fora; escreva a linha dele no DIREITOS.md)')
    print(f'{dist.name}/: {len(vai)} arquivo(s), {total / 1024:.0f} KB')
    return 1 if erros else 0


def conferir(pasta, prot, dist):
    if not prot.is_dir():
        sys.exit(f'não achei a pasta do protótipo: {prot}')
    d, linhas, vai, fora, sem = plano(pasta, prot, dist)
    faltas, avisos = [], []

    # 1. Cabeçalho: o endereço da versão privada e a data da checagem
    end = d['endereco']
    if vazio(end) or '<' in end or not re.match(r'https://[^\s/]+\.[^\s/]+', end):
        faltas.append('o endereço privado está vazio ou não começa com https://')
    elif re.search(r'\.example(/|$)', end):
        avisos.append('o endereço é de exemplo (.example): troque pelo que o Sites mostrar')
    if not re.match(r'\d{2}/\d{2}/\d{4}$', d['data']):
        faltas.append('falta a data da checagem (Checado em: DD/MM/AAAA)')

    # 2. A dist é a montagem de agora
    if not dist.is_dir():
        faltas.append(f'não existe {dist.name}/: rode antes python3 publicar.py montar')
    else:
        esperado = {rel for rel, _ in vai}
        tem = {p.relative_to(dist).as_posix() for p in dist.rglob('*') if p.is_file()}
        diferentes = sorted(r for r in esperado & tem if (dist / r).read_bytes() != (prot / r).read_bytes())
        if esperado != tem or diferentes:
            faltas.append(f'{dist.name}/ não bate com o protótipo e o DIREITOS.md de agora: rode python3 publicar.py montar')
    for rel in sem:
        faltas.append(f'{rel}: sem linha no DIREITOS.md')

    # 3. Arquivos: cada linha completa; foto só com licença livre ou própria; crédito na tela e no README
    paginas = [r for r, _ in vai if r.endswith(('.html', '.htm'))]
    leitura = {r: ler_pagina(prot / r) for r in paginas}
    readme = (prot / 'README.md').read_text(errors='ignore') if (prot / 'README.md').is_file() else ''
    for l in linhas:
        nome, oque, origem, licenca, onde, decisao = l[:6]
        rotulo = nome.strip('`')
        if any(vazio(c) for c in (nome, oque, origem, licenca)) or decisao.strip().lower() not in DECISOES:
            faltas.append(f'{rotulo}: linha incompleta (o que é, origem, licença e decisão publicar ou fica fora)')
            continue
        if decisao.strip().lower() != 'publicar':
            continue
        lic = licenca.lower()
        if 'foto' in oque.lower() and not any(t in lic for t in LIVRE):
            faltas.append(f'{rotulo}: foto sem licença livre nem própria marcada para publicar')
        if 'cc by' in lic and vazio(onde):
            faltas.append(f'{rotulo}: a licença pede o crédito ao autor, e a coluna "crédito onde" está vazia')
        regras = [(chave, palavras) for chave, palavras in CREDITOS if chave in lic]
        if not regras:
            continue
        if 'tela' not in onde.lower() or 'readme' not in onde.lower():
            faltas.append(f'{rotulo}: o crédito precisa ir na tela e no README (coluna "crédito onde")')
        alvos = [r for r, _ in vai if linha_de(r, [l]) is l]
        usam = [p for p in paginas if any(Path(s).name in {Path(a).name for a in alvos} for s in leitura[p][1])]
        palavras = [w for _, ws in regras for w in ws]
        for p in usam:
            sem_palavra = [w for w in palavras if w.lower() not in leitura[p][0].lower()]
            if sem_palavra:
                faltas.append(f'{p} carrega {", ".join(alvos)} e não mostra na tela: {", ".join(sem_palavra)}')
        sem_readme = [w for w in palavras if w.lower() not in readme.lower()]
        if sem_readme:
            faltas.append(f'README.md do protótipo sem o crédito: {", ".join(sem_readme)}')

    # 4. Pessoas: pessoa real só com autorização; quem fica fora não aparece em nenhum arquivo publicado
    textos = {r: (prot / r).read_text(errors='ignore') for r, _ in vai if Path(r).suffix.lower() in TEXTO}
    for l in d['pessoas']:
        l = l + [''] * (5 - len(l))
        quem, como, real, autorizacao, decisao = l[:5]
        dec = decisao.strip().lower()
        if any(vazio(c) for c in (quem, como, real)) or vazio(decisao):
            faltas.append(f'pessoa "{quem or "?"}": linha incompleta (aparece como, pessoa real, decisão)')
            continue
        if real.strip().lower().startswith('sim') and dec == 'publicar' and (vazio(autorizacao) or autorizacao.lower().startswith('não')):
            faltas.append(f'pessoa "{quem}": pessoa real sem autorização marcada para publicar')
        if dec != 'publicar':
            achou = [r for r, t in textos.items() if quem.lower() in t.lower()]
            if achou:
                faltas.append(f'pessoa "{quem}": a decisão é "{decisao}", e o nome ainda está em {", ".join(achou)}')
    if not d['pessoas']:
        faltas.append('a tabela de pessoas está vazia: anote também os personagens inventados')

    # 5. Marcas e referência visual: cada linha completa
    for l in d['marcas']:
        l = l + [''] * (5 - len(l))
        if any(vazio(c) for c in l[:5]):
            faltas.append(f'marca ou referência "{l[0] or "?"}": linha incompleta')
    if not d['marcas']:
        faltas.append('a tabela de marcas e referência visual está vazia')

    # 6. Versões: pelo menos três, cada uma com commit, o que mudou, onde testou e o mesmo endereço
    arq_v = pasta / 'VERSOES.md'
    versoes = tabela(arq_v.read_text().splitlines()) if arq_v.is_file() else []
    if len(versoes) < 3:
        faltas.append(f'VERSOES.md com {len(versoes)} versão(ões): o registro pede pelo menos 3')
    for v in versoes:
        v = v + [''] * (6 - len(v))
        num, quando, commit, mudou, onde, endv = v[:6]
        nomes = [n for n, c in (('quando', quando), ('commit', commit), ('o que mudou', mudou), ('onde testei', onde)) if vazio(c)]
        if nomes:
            faltas.append(f'versão {num}: falta {", ".join(nomes)}')
        elif not re.fullmatch(r'[0-9a-f]{7,40}', commit.strip('`')):
            faltas.append(f'versão {num}: o commit precisa ser o código do git (7 a 40 letras e números)')
        if not vazio(endv) and endv.rstrip('/') != end.rstrip('/'):
            faltas.append(f'versão {num}: o endereço é outro que o do DIREITOS.md')

    print(f'arquivos para a {dist.name}/: {len(vai)} | pessoas: {len(d["pessoas"])} | marcas e referências: {len(d["marcas"])} | versões: {len(versoes)}')
    for a in avisos:
        print('AVISO:', a)
    for f in faltas:
        print('FALTA:', f)
    if faltas:
        print(f'{len(faltas)} problema(s) para resolver antes de abrir ao público')
        return 1
    print('nada falta: abra o endereço no celular e no computador antes de mudar o acesso')
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('comando', choices=['montar', 'conferir'])
    p.add_argument('--pasta', default='.', help='a pasta com o DIREITOS.md e o VERSOES.md')
    p.add_argument('--prototipo', default='prototipo')
    p.add_argument('--dist', default='dist')
    a = p.parse_args()
    pasta = Path(a.pasta)
    prot = pasta / a.prototipo
    dist = pasta / a.dist
    sys.exit((montar if a.comando == 'montar' else conferir)(pasta, prot, dist))


if __name__ == '__main__':
    main()
