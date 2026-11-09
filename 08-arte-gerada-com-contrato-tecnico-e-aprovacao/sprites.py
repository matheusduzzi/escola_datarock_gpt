"""Arte gerada com contrato: referência ampliada, importador, prancha, conferência e integração.

Uso, dentro da pasta da arte (a que tem ARTE.md, ORIGEM.md e APROVACAO.md):

  python3 sprites.py refs                         # referência ampliada de cada sprite, em refs/
  python3 sprites.py importar <nome> <imagem>     # normaliza a imagem gerada e grava importados/<nome>.png
  python3 sprites.py codigo <arquivo> [...]       # o código de 12 letras e números de cada arquivo
  python3 sprites.py prancha                      # prancha.png para você olhar e aprovar
  python3 sprites.py conferir                     # o que falta no contrato, no registro e nos importados
  python3 sprites.py integrar --jogo <pasta>      # copia para o jogo só o que foi aprovado

Todos aceitam --pasta <pasta da arte> (padrão: a pasta atual). Precisa do Pillow.
Saída 0: tudo certo. Saída 1: falta algo, com uma linha por problema.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError:
    sys.exit('Falta o Pillow. Instale uma vez com: python3 -m pip install pillow')

MAGENTA = (255, 0, 255)
LONGE = 40          # diferença máxima num canal (0 a 255) para a cor contar como da paleta
ESCALA_PRANCHA = 4


# ---------- leitura dos arquivos de texto ----------

def tabela(texto, titulo):
    """Linhas da primeira tabela Markdown depois do título '## titulo', como dicionários."""
    m = re.search(r'^##\s+' + re.escape(titulo) + r'\s*$(.*?)(?=^##\s|\Z)', texto, re.M | re.S | re.I)
    if not m:
        return None
    linhas = [l.strip() for l in m.group(1).splitlines() if l.strip().startswith('|')]
    if len(linhas) < 2:
        return []
    celulas = lambda l: [c.strip() for c in l.strip().strip('|').split('|')]
    cab = [c.lower() for c in celulas(linhas[0])]
    out = []
    for l in linhas[2:]:
        c = celulas(l)
        if any(c):
            out.append(dict(zip(cab, c + [''] * (len(cab) - len(c)))))
    return out


def ler(pasta, nome):
    p = pasta / nome
    return p.read_text(encoding='utf-8') if p.is_file() else None


def codigo(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()[:12]


def data_br(texto):
    m = re.fullmatch(r'(\d{2})/(\d{2})/(\d{4})', (texto or '').strip())
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def hex_rgb(h):
    h = h.strip().lower()
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


class Arte:
    """O contrato (ARTE.md), o registro (ORIGEM.md) e as decisões (APROVACAO.md) de uma pasta."""

    def __init__(self, pasta):
        self.pasta = Path(pasta)
        self.faltas = []
        arte = ler(self.pasta, 'ARTE.md')
        if arte is None:
            self.faltas.append('ARTE.md não existe nessa pasta')
            arte = ''
        self.quadro = (tabela(arte, 'Quadro de estilo') or [{}])[0]
        pal = tabela(arte, 'Paleta') or []
        self.paleta = [hex_rgb(l['hex']) for l in pal if re.fullmatch(r'#[0-9a-fA-F]{6}', l.get('hex', ''))]
        self.sprites = []
        for l in tabela(arte, 'Sprites') or []:
            try:
                self.sprites.append({'nome': l['nome'], 'w': int(l['largura']), 'h': int(l['altura']),
                                     'onde': l.get('onde aparece', ''), 'o que': l.get('o que é', '')})
            except (KeyError, ValueError):
                self.faltas.append(f'ARTE.md: a linha do sprite "{l.get("nome", "?")}" precisa de largura e altura em números')
        if arte and not self.sprites:
            self.faltas.append('ARTE.md sem nenhum sprite na tabela Sprites')
        if arte and len(self.paleta) < 3:
            self.faltas.append('ARTE.md com menos de 3 cores em hex na tabela Paleta')
        self.origem = tabela(ler(self.pasta, 'ORIGEM.md') or '', 'Registro')
        if self.origem is None:
            self.faltas.append('ORIGEM.md sem a tabela Registro')
            self.origem = []
        self.decisoes = tabela(ler(self.pasta, 'APROVACAO.md') or '', 'Decisões')
        if self.decisoes is None:
            self.faltas.append('APROVACAO.md sem a tabela Decisões')
            self.decisoes = []

    def sprite(self, nome):
        return next((s for s in self.sprites if s['nome'] == nome), None)

    def ultima(self, linhas, chave, valor):
        achadas = [l for l in linhas if l.get(chave, '').strip().lower() == valor.lower()]
        return achadas[-1] if achadas else None


# ---------- imagens ----------

def normalizar(imagem, w, h, paleta):
    """Tira o fundo, põe cada pixel na cor mais próxima da paleta, recorta, encaixa pela base no tamanho
    final pegando a cor do meio de cada quadradinho e deixa o alfa 0 ou 255."""
    im = Image.open(imagem).convert('RGBA')
    rgb, alfa = im.convert('RGB'), im.getchannel('A')
    cores = list(paleta) + [MAGENTA]
    tabela_cores = Image.new('P', (1, 1))
    tabela_cores.putpalette([v for c in cores for v in c] + [0] * 3 * (256 - len(cores)))
    q = rgb.quantize(palette=tabela_cores, dither=Image.Dither.NONE)
    indices = Image.frombytes('L', q.size, q.tobytes())
    fundo_m = len(cores) - 1
    mascara = ImageChops.multiply(indices.point(lambda i: 0 if i == fundo_m else 255),
                                  alfa.point(lambda a: 255 if a >= 128 else 0))
    caixa = mascara.getbbox()
    if not caixa:
        raise ValueError('a imagem só tem fundo')
    # quanto da imagem estava longe da paleta (o quadro não foi seguido, ou foi outra paleta)
    d = ImageChops.difference(rgb, q.convert('RGB'))
    r, g, b = d.split()
    longe = ImageChops.multiply(ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda v: 255 if v > LONGE else 0), mascara)
    opacos = mascara.histogram()[255]
    cw, ch = caixa[2] - caixa[0], caixa[3] - caixa[1]
    k = min(w / cw, h / ch)
    nw, nh = max(1, round(cw * k)), max(1, round(ch * k))
    idx = indices.crop(caixa).resize((nw, nh), Image.NEAREST)
    msk = mascara.crop(caixa).resize((nw, nh), Image.NEAREST)
    final = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    fp, ip, mp = final.load(), idx.load(), msk.load()
    x0, y0 = (w - nw) // 2, h - nh
    for y in range(nh):
        for x in range(nw):
            if mp[x, y] and ip[x, y] != fundo_m:
                fp[x0 + x, y0 + y] = cores[ip[x, y]] + (255,)
    info = {'original': im.size, 'recorte': (cw, ch), 'final': (w, h), 'desenho': (nw, nh),
            'longe': round(100 * longe.histogram()[255] / max(opacos, 1)), 'proporcao': (cw / ch, w / h)}
    return final, info


def bytes_png(im):
    import io
    buf = io.BytesIO()
    im.save(buf, 'PNG', optimize=False)
    return buf.getvalue()


# ---------- comandos ----------

def cmd_refs(arte, args):
    destino = arte.pasta / 'refs'
    destino.mkdir(exist_ok=True)
    e = args.escala
    for s in arte.sprites:
        w, h = s['w'] * e, s['h'] * e
        im = Image.new('RGB', (w, h + 2 * e), MAGENTA)
        d = ImageDraw.Draw(im)
        d.rectangle([e, e, w - e - 1, h - 1], fill=(200, 200, 200), outline=(60, 60, 60), width=max(1, e // 2))
        d.rectangle([0, h, w - 1, h + e // 2], fill=(0, 200, 0))   # linha verde: a base, onde o sprite pisa
        im.save(destino / f'{s["nome"]}.png')
        print(f'refs/{s["nome"]}.png: {w} x {h + 2 * e} pixels, para o sprite de {s["w"]} x {s["h"]}')
    return 0


def cmd_importar(arte, args):
    s = arte.sprite(args.nome)
    if not s:
        print(f'FALTA: o sprite "{args.nome}" não está na tabela Sprites do ARTE.md')
        return 1
    if len(arte.paleta) < 3:
        print('FALTA: ARTE.md com menos de 3 cores em hex na tabela Paleta')
        return 1
    try:
        final, info = normalizar(args.imagem, s['w'], s['h'], arte.paleta)
    except (OSError, ValueError) as erro:
        print(f'FALTA: {args.nome}: não consegui ler a imagem ({erro})')
        return 1
    destino = arte.pasta / 'importados'
    destino.mkdir(exist_ok=True)
    (destino / f'{s["nome"]}.png').write_bytes(bytes_png(final))
    ow, oh = info['original']
    cw, ch = info['recorte']
    nw, nh = info['desenho']
    print(f'{s["nome"]}: {ow} x {oh} -> recorte {cw} x {ch} -> {nw} x {nh} dentro de {s["w"]} x {s["h"]}')
    pd, pc = info['proporcao']
    if abs(pd - pc) / pc > 0.15:
        print(f'  AVISO: o desenho tem outra proporção que o contrato; ele ficou com {nw} x {nh} dentro de {s["w"]} x {s["h"]}')
    if info['longe'] > 10:
        print(f'  AVISO: {info["longe"]}% dos pixels estavam longe de qualquer cor da paleta. Veja se o quadro foi anexado')
    return 0


def cmd_codigo(arte, args):
    for f in args.arquivos:
        print(f'{codigo(f)}  {f}')
    return 0


def cmd_prancha(arte, args):
    pecas = [s for s in arte.sprites if (arte.pasta / 'importados' / f'{s["nome"]}.png').is_file()]
    if not pecas:
        print('FALTA: nenhum sprite em importados/. Rode importar antes')
        return 1
    k = ESCALA_PRANCHA
    margem = 16
    largura = max(s['w'] * (1 + k) + 3 * margem for s in pecas)
    altura = sum(s['h'] * k + 3 * margem for s in pecas) + margem
    fundo = arte.paleta[0]
    prancha = Image.new('RGB', (max(largura, 360), altura), (255, 255, 255))
    d = ImageDraw.Draw(prancha)
    y = margem
    print('| peça | código |')
    print('|---|---|')
    quadro = arte.pasta / arte.quadro.get('arquivo', '')
    if arte.quadro.get('arquivo') and quadro.is_file():
        print(f'| quadro de estilo | {codigo(quadro)} |')
    for s in pecas:
        arq = arte.pasta / 'importados' / f'{s["nome"]}.png'
        im = Image.open(arq).convert('RGBA')
        cod = codigo(arq)
        d.text((margem, y), f'{s["nome"]}  {s["w"]} x {s["h"]}  {cod}', fill=(43, 42, 46))
        y0 = y + margem
        # em 1x, sobre o chão da paleta, como no jogo; em 4x, para ver pixel por pixel
        d.rectangle([margem - 4, y0 - 4, margem + s['w'] + 4, y0 + s['h'] + 4], fill=fundo)
        prancha.paste(im, (margem, y0), im)
        x4 = 2 * margem + s['w']
        d.rectangle([x4 - 4, y0 - 4, x4 + s['w'] * k + 4, y0 + s['h'] * k + 4], fill=fundo)
        grande = im.resize((s['w'] * k, s['h'] * k), Image.NEAREST)
        prancha.paste(grande, (x4, y0), grande)
        y += s['h'] * k + 3 * margem
        print(f'| {s["nome"]} | {cod} |')
    prancha.save(arte.pasta / 'prancha.png')
    print(f'prancha.png: {len(pecas)} peça(s), em 1x e em {k}x')
    return 0


def faltas_do_sprite(arte, s, quadro_aprovado):
    nome, f = s['nome'], []
    o = arte.ultima(arte.origem, 'sprite', nome)
    if not o:
        return [f'{nome} sem linha na ORIGEM.md']
    for campo in ('data', 'ferramenta', 'prompt', 'quadro anexado', 'imagem gerada', 'código da imagem', 'o que eu vi'):
        if not o.get(campo, '').strip():
            f.append(f'{nome}: a coluna "{campo}" está vazia na ORIGEM.md')
    quando = data_br(o.get('data'))
    if o.get('data', '').strip() and not quando:
        f.append(f'{nome}: data "{o["data"]}" na ORIGEM.md fora do formato DD/MM/AAAA')
    prompt = arte.pasta / o.get('prompt', '').strip('` ')
    if o.get('prompt', '').strip():
        if not prompt.is_file():
            f.append(f'{nome}: o prompt {o["prompt"]} não existe')
        else:
            pt = prompt.read_text(encoding='utf-8')
            m = re.search(r'FINAL SIZE:\s*(\d+)\s*x\s*(\d+)', pt, re.I)
            if not m:
                f.append(f'{nome}: o prompt não diz o tamanho final (FINAL SIZE)')
            elif (int(m.group(1)), int(m.group(2))) != (s['w'], s['h']):
                f.append(f'{nome}: o prompt pede {m.group(1)} x {m.group(2)} e o contrato diz {s["w"]} x {s["h"]}')
            if not re.search(r'\bno text\b', pt, re.I):
                f.append(f'{nome}: o prompt não proíbe texto (No text)')
    anexado = o.get('quadro anexado', '').strip('` ').lower()
    if quadro_aprovado and anexado and anexado != quadro_aprovado[0]:
        f.append(f'{nome}: gerado sem o quadro aprovado (quadro anexado: {anexado})')
    if quadro_aprovado and quando and quadro_aprovado[1] and quando < quadro_aprovado[1]:
        f.append(f'{nome}: gerado em {o["data"]}, antes da aprovação do quadro')
    gerada = arte.pasta / o.get('imagem gerada', '').strip('` ')
    if o.get('imagem gerada', '').strip():
        if not gerada.is_file():
            f.append(f'{nome}: a imagem gerada {o["imagem gerada"]} não existe')
        elif o.get('código da imagem', '').strip('` ').lower() != codigo(gerada):
            f.append(f'{nome}: a imagem gerada não é a do registro (código {codigo(gerada)} no arquivo)')
    imp = arte.pasta / 'importados' / f'{nome}.png'
    if not imp.is_file():
        f.append(f'{nome}: falta o importado; rode importar')
    else:
        im = Image.open(imp)
        if im.size != (s['w'], s['h']):
            f.append(f'{nome}: o importado tem {im.size[0]} x {im.size[1]} e o contrato diz {s["w"]} x {s["h"]}')
        elif gerada.is_file() and len(arte.paleta) >= 3:
            refeito, _ = normalizar(gerada, s['w'], s['h'], arte.paleta)
            if bytes_png(refeito) != imp.read_bytes():
                f.append(f'{nome}: o importado não saiu da imagem gerada registrada; rode importar de novo')
    return f


def quadro_aprovado(arte):
    """(código, data) do quadro de estilo aprovado, ou None com as faltas."""
    faltas = []
    arq = arte.quadro.get('arquivo', '').strip('` ')
    if not arq:
        return None, ['ARTE.md sem o arquivo do quadro de estilo']
    if not (arte.pasta / arq).is_file():
        return None, [f'o quadro de estilo {arq} não existe']
    d = arte.ultima(arte.decisoes, 'peça', 'quadro de estilo')
    if not d or d.get('decisão', '').strip().lower() != 'aprovado':
        return None, ['quadro de estilo sem aprovação na APROVACAO.md']
    atual = codigo(arte.pasta / arq)
    if d.get('código', '').strip('` ').lower() != atual:
        faltas.append(f'o quadro de estilo mudou depois da aprovação (aprovado: {d.get("código", "")}, arquivo: {atual})')
    quando = data_br(d.get('data'))
    if not quando:
        faltas.append('a aprovação do quadro de estilo está sem data DD/MM/AAAA')
    return (atual, quando), faltas


def conferir(arte):
    gerais = list(arte.faltas)
    qa, fq = quadro_aprovado(arte)
    gerais += fq
    por_sprite = {s['nome']: faltas_do_sprite(arte, s, qa) for s in arte.sprites}
    return gerais, por_sprite


def cmd_conferir(arte, args):
    gerais, por_sprite = conferir(arte)
    todas = gerais + [x for s in arte.sprites for x in por_sprite[s['nome']]]
    print(f'sprites no contrato: {len(arte.sprites)} | cores na paleta: {len(arte.paleta)} | '
          f'linhas na ORIGEM.md: {len(arte.origem)}')
    for x in todas:
        print('FALTA: ' + x)
    if todas:
        print(f'{len(todas)} problema(s) para resolver antes de aprovar')
        return 1
    print('nada falta: monte a prancha e olhe cada peça')
    return 0


def cmd_integrar(arte, args):
    gerais, por_sprite = conferir(arte)
    if gerais:
        for x in gerais:
            print('FALTA: ' + x)
        print('nada foi para o jogo')
        return 1
    jogo = Path(args.jogo)
    if not jogo.is_dir():
        print(f'FALTA: a pasta do jogo {jogo} não existe')
        return 1
    entram, fora = {}, []
    for s in arte.sprites:
        nome = s['nome']
        imp = arte.pasta / 'importados' / f'{nome}.png'
        if por_sprite[nome]:
            fora.append(por_sprite[nome][0])
            continue
        d = arte.ultima(arte.decisoes, 'peça', nome)
        o = arte.ultima(arte.origem, 'sprite', nome)
        if not d:
            fora.append(f'{nome}: sem decisão na APROVACAO.md')
        elif d.get('decisão', '').strip().lower() != 'aprovado':
            fora.append(f'{nome}: a última decisão é "{d.get("decisão", "")}"')
        elif not data_br(d.get('data')):
            fora.append(f'{nome}: aprovação sem data DD/MM/AAAA')
        elif data_br(d['data']) < data_br(o['data']):
            fora.append(f'{nome}: aprovado em {d["data"]}, antes da geração registrada em {o["data"]}')
        elif d.get('código', '').strip('` ').lower() != codigo(imp):
            fora.append(f'{nome}: a aprovação é da versão {d.get("código", "")} e o importado agora é {codigo(imp)}')
        else:
            entram[nome] = s
    pasta = jogo / 'sprites'
    pasta.mkdir(exist_ok=True)
    for velho in pasta.glob('*.png'):
        if velho.stem not in entram:
            velho.unlink()
    atlas = {}
    for nome, s in entram.items():
        dados = (arte.pasta / 'importados' / f'{nome}.png').read_bytes()
        (pasta / f'{nome}.png').write_bytes(dados)
        atlas[nome] = {'arquivo': f'sprites/{nome}.png', 'w': s['w'], 'h': s['h'],
                       'codigo': hashlib.sha256(dados).hexdigest()[:12]}
        print(f'NO JOGO: {nome} ({atlas[nome]["codigo"]})')
    (jogo / 'atlas.js').write_text('// Escrito por sprites.py integrar. Só entra aqui o que foi aprovado.\n'
                                   'window.ATLAS = ' + json.dumps(atlas, ensure_ascii=False, indent=1) + ';\n',
                                   encoding='utf-8')
    for x in fora:
        print('FICOU DE FORA: ' + x)
    print(f'{len(entram)} de {len(arte.sprites)} sprite(s) no jogo')
    return 0 if not fora else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--pasta', default='.', help='pasta da arte (padrão: a atual)')
    sub = ap.add_subparsers(dest='comando', required=True)
    r = sub.add_parser('refs')
    r.add_argument('--escala', type=int, default=8)
    i = sub.add_parser('importar')
    i.add_argument('nome')
    i.add_argument('imagem')
    c = sub.add_parser('codigo')
    c.add_argument('arquivos', nargs='+')
    sub.add_parser('prancha')
    sub.add_parser('conferir')
    g = sub.add_parser('integrar')
    g.add_argument('--jogo', required=True)
    args = ap.parse_args(argv)
    arte = Arte(args.pasta)
    return {'refs': cmd_refs, 'importar': cmd_importar, 'codigo': cmd_codigo, 'prancha': cmd_prancha,
            'conferir': cmd_conferir, 'integrar': cmd_integrar}[args.comando](arte, args)


if __name__ == '__main__':
    sys.exit(main())
