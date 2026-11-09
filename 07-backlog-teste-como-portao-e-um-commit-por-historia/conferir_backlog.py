"""Confere se o BACKLOG.md e o git log do protótipo batem.

Uso, dentro da pasta do protótipo:
    python3 conferir_backlog.py --repo .

Sai com 0 quando nada falta e com 1 quando falta algo, com uma linha FALTA para cada problema.

O que ele lê:
- no BACKLOG.md, cada história "## US-NN: título" e as linhas Pedido, História, Critério,
  Medido, Estimativa, Depende de e Estado;
- no git, o gancho configurado em core.hooksPath e o assunto de cada commit (git log).

O que ele não lê: se o número do critério é o certo, se o teste mede o que o critério diz e
se o commit mudou só o que a história pede. Isso fica com você (git show --stat de cada commit).
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

CAMPOS = ['Pedido', 'História', 'Critério', 'Medido', 'Estimativa', 'Depende de', 'Estado']
ESTADOS = ['a fazer', 'a medir', 'feita']
ID = re.compile(r'\bUS-\d+\b')


def ler_backlog(arquivo):
    historias, atual = [], None
    for linha in arquivo.read_text(encoding='utf-8').splitlines():
        m = re.match(r'^##\s+(US-\d+)\s*:\s*(.+?)\s*$', linha)
        if m:
            atual = {'id': m.group(1), 'titulo': m.group(2)}
            historias.append(atual)
            continue
        m = re.match(r'^-\s*([^:]+?)\s*:\s*(.*?)\s*$', linha)
        if atual is not None and m and m.group(1) in CAMPOS:
            atual[m.group(1)] = m.group(2)
    return historias


def git(repo, *args):
    r = subprocess.run(['git', '-C', str(repo)] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def conferir(repo):
    faltas = []
    backlog = repo / 'BACKLOG.md'
    if not backlog.is_file():
        return ['não achei o BACKLOG.md em ' + str(repo)], None
    historias = ler_backlog(backlog)
    ids = [h['id'] for h in historias]
    if len(historias) < 5:
        faltas.append('o backlog tem %d história(s); o pedido é pelo menos 5' % len(historias))
    for i in sorted(set(i for i in ids if ids.count(i) > 1)):
        faltas.append(i + ' aparece mais de uma vez no backlog')

    for h in historias:
        i = h['id']
        for campo in CAMPOS:
            if campo not in h:
                faltas.append('%s não tem a linha "%s"' % (i, campo))
        if not re.search(r'(?i)\bcomo\b.+,\s*quero\b.+,\s*para\b', h.get('História', '')):
            faltas.append(i + ': a história não está no formato "Como ..., quero ..., para ..."')
        if 'Critério' in h and not re.search(r'\d', h['Critério']):
            faltas.append(i + ': o critério não tem número')
        if 'Estimativa' in h and h['Estimativa'] not in ('P', 'M', 'G'):
            faltas.append(i + ': estimativa "%s"; use P, M ou G' % h['Estimativa'])
        if 'Estado' in h and h['Estado'] not in ESTADOS:
            faltas.append(i + ': estado "%s"; use a fazer, a medir ou feita' % h['Estado'])
        dep = h.get('Depende de', '')
        if dep and dep != 'nenhuma':
            for d in ID.findall(dep):
                if d not in ids:
                    faltas.append('%s depende de %s, que não está no backlog' % (i, d))
            if not ID.findall(dep):
                faltas.append(i + ': "Depende de" precisa de ids (US-NN) ou "nenhuma"')
        if h.get('Estado') in ('a medir', 'feita') and not re.search(r'\d', h.get('Medido', '')):
            faltas.append(i + ' está "%s", mas o Medido não tem número' % h['Estado'])

    criterios = [h.get('Critério', '') for h in historias]
    if not any(re.search(r'\d+\s*ms\b', c) for c in criterios):
        faltas.append('nenhum critério mede tempo (por exemplo, "pior quadro abaixo de 16 ms")')
    if not any(re.search(r'\d(?!\d*\s*ms\b)', c) for c in criterios):
        faltas.append('nenhum critério conta alguma coisa (por exemplo, "no máximo 4 figuras")')

    # O gancho
    codigo, raiz = git(repo, 'rev-parse', '--show-toplevel')
    if codigo != 0:
        faltas.append('a pasta não é um repositório git (rode git init)')
        return faltas, {'historias': len(historias)}
    codigo, caminho = git(repo, 'config', '--get', 'core.hooksPath')
    if codigo != 0 or not caminho:
        faltas.append('o gancho não está ligado: falta core.hooksPath (rode npm run prepare)')
    else:
        gancho = Path(raiz) / caminho / 'pre-commit'
        if not gancho.is_file():
            faltas.append('core.hooksPath aponta para %s, mas não tem pre-commit lá' % caminho)
        elif not os.access(gancho, os.X_OK):
            faltas.append('o %s/pre-commit não é executável: o git ignora o gancho (rode chmod +x)' % caminho)

    # O log
    codigo, log = git(repo, 'log', '--reverse', '--format=%h %s')
    commits = [l.split(' ', 1) for l in log.splitlines()] if codigo == 0 and log else []
    if not commits:
        faltas.append('o repositório ainda não tem commit')
    por_id, ordem = {}, {}
    for n, (h, assunto) in enumerate(commits):
        citados = sorted(set(ID.findall(assunto)))
        if len(citados) > 1:
            faltas.append('o commit %s cita %d histórias (%s); é um commit por história' % (h, len(citados), ', '.join(citados)))
        for c in citados:
            por_id.setdefault(c, []).append(h)
            ordem.setdefault(c, n)
            if c not in ids:
                faltas.append('o commit %s cita %s, que não está no backlog' % (h, c))
    estado = {h['id']: h.get('Estado') for h in historias}
    for h in historias:
        i, e = h['id'], h.get('Estado')
        n = len(por_id.get(i, []))
        if e in ('a medir', 'feita') and n == 0:
            faltas.append('%s está "%s", mas nenhum commit cita %s' % (i, e, i))
        if n > 1:
            faltas.append('%s tem %d commits (%s); é um commit por história' % (i, n, ', '.join(por_id[i])))
        if e == 'a fazer' and n:
            faltas.append('%s tem commit (%s), mas o backlog ainda diz "a fazer"' % (i, por_id[i][0]))
        for d in ID.findall(h.get('Depende de', '')):
            if i in ordem and (d not in ordem or ordem[d] > ordem[i]):
                faltas.append('o commit de %s veio antes do commit de %s, de que ela depende' % (i, d))
    resumo = {
        'historias': len(historias),
        'feitas': sum(1 for e in estado.values() if e == 'feita'),
        'a_medir': sum(1 for e in estado.values() if e == 'a medir'),
        'commits': len(commits),
        'commits_com_historia': sum(1 for _, s in commits if ID.search(s)),
    }
    return faltas, resumo


def main():
    p = argparse.ArgumentParser(description='Confere se o BACKLOG.md e o git log batem.')
    p.add_argument('--repo', default='.', help='pasta do protótipo (padrão: a pasta atual)')
    repo = Path(p.parse_args().repo).resolve()
    faltas, resumo = conferir(repo)
    if resumo:
        print('histórias: %d | feitas: %d | a medir: %d' % (resumo['historias'], resumo.get('feitas', 0), resumo.get('a_medir', 0)))
        if 'commits' in resumo:
            print('commits: %d | com história: %d' % (resumo['commits'], resumo['commits_com_historia']))
    for f in faltas:
        print('FALTA: ' + f)
    print('%d problema(s) no backlog ou no log' % len(faltas) if faltas else 'nada falta: backlog e log batem')
    return 1 if faltas else 0


if __name__ == '__main__':
    sys.exit(main())
