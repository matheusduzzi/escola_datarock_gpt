"""Portão da juntada: olha a pasta do protótipo depois que as frentes voltaram.

Uso, dentro da pasta do protótipo:
    python3 conferir_juntada.py --prototipo .

Ele lê dois arquivos da pasta:
- frentes.md, com a tabela "A divisão" (cada frente e os arquivos que ela pode mexer);
- DIRECAO-DE-ARTE.md, com a seção "Paleta" (as cores em hex, como #3f7d4e).

E diz, com uma linha FALTA para cada problema:
- se as três frentes (arte, vida e página) estão na divisão;
- se algum arquivo tem duas frentes como dona;
- se algum arquivo da divisão não existe na pasta;
- se algum .html, .js ou .css da pasta não tem dona;
- se alguma cor em hex nesses arquivos está fora da paleta.

Sai com 0 quando não falta nada e com 1 quando falta algo.
O portão só lê cor escrita em hex. Cor em rgb(), hsl() ou sorteada no código passa sem aviso.
"""
import argparse
import re
import sys
from pathlib import Path

CODIGO = {'.html', '.js', '.css'}
IGNORAR_PASTAS = {'.git', 'node_modules', 'dados', 'amostra', 'dist'}
HEX = re.compile(r'(?<![&\w])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-zA-Z_-])')


def normaliza(cor):
    cor = cor.lower()
    if len(cor) == 4:
        cor = '#' + ''.join(c * 2 for c in cor[1:])
    return cor


def secao(texto, titulo):
    """Texto de uma seção ## cujo título contém a palavra pedida, até a próxima ##."""
    partes = re.split(r'^## ', texto, flags=re.M)
    for parte in partes[1:]:
        if titulo.lower() in parte.splitlines()[0].lower():
            return parte
    return ''


def ler_divisao(frentes_md):
    tabela = secao(frentes_md, 'divisão') or secao(frentes_md, 'divisao')
    donos = {}
    for linha in tabela.splitlines():
        if not linha.startswith('|') or set(linha) <= set('|-: '):
            continue
        cols = [c.strip() for c in linha.strip('|').split('|')]
        if len(cols) < 2 or cols[0].lower() == 'frente' or not cols[0]:
            continue
        donos[cols[0]] = re.findall(r'`([^`]+)`', cols[1])
    return donos


def main():
    ap = argparse.ArgumentParser(description='Portão da juntada das frentes do protótipo.')
    ap.add_argument('--prototipo', required=True, help='pasta do protótipo')
    a = ap.parse_args()
    pasta = Path(a.prototipo).resolve()
    faltas = []

    arq_frentes, arq_direcao = pasta / 'frentes.md', pasta / 'DIRECAO-DE-ARTE.md'
    for arq in (arq_frentes, arq_direcao):
        if not arq.is_file():
            print(f'FALTA: {arq.name} não está em {pasta}')
            return 1

    donos = ler_divisao(arq_frentes.read_text(encoding='utf-8'))
    nomes = ' '.join(donos).lower()
    for frente in ('arte', 'vida', 'página'):
        if frente not in nomes and not (frente == 'página' and 'pagina' in nomes):
            faltas.append(f'FALTA: a frente {frente} não está na tabela "A divisão" de frentes.md')

    dono_de = {}
    for frente, arquivos in donos.items():
        for arq in arquivos:
            if arq in dono_de and dono_de[arq] != frente:
                faltas.append(f'FALTA: {arq} tem duas donas na divisão: {dono_de[arq]} e {frente}')
            dono_de.setdefault(arq, frente)
            if not (pasta / arq).is_file():
                faltas.append(f'FALTA: {arq}, da frente {frente}, não está na pasta')

    paleta_txt = secao(arq_direcao.read_text(encoding='utf-8'), 'paleta')
    paleta = {normaliza(c) for c in HEX.findall(paleta_txt)}
    if len(paleta) < 3:
        faltas.append('FALTA: a seção "Paleta" de DIRECAO-DE-ARTE.md tem menos de 3 cores em hex')

    codigo = sorted(p for p in pasta.rglob('*')
                    if p.is_file() and p.suffix in CODIGO
                    and not (set(p.relative_to(pasta).parts[:-1]) & IGNORAR_PASTAS))
    fora = 0
    for p in codigo:
        rel = p.relative_to(pasta).as_posix()
        if rel not in dono_de:
            faltas.append(f'FALTA: {rel} não tem dona na divisão')
        if not paleta:
            continue
        for n, linha in enumerate(p.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
            for cor in HEX.findall(linha):
                if normaliza(cor) not in paleta:
                    fora += 1
                    faltas.append(f'FALTA: cor {cor} fora da paleta em {rel}, linha {n} '
                                  f'(frente {dono_de.get(rel, "sem dona")})')

    print(f'frentes: {", ".join(f"{f} ({len(v)})" for f, v in donos.items())}')
    print(f'paleta: {len(paleta)} cores | arquivos de código: {len(codigo)} | cores fora da paleta: {fora}')
    for f in faltas:
        print(f)
    if faltas:
        print(f'{len(faltas)} problema(s) para resolver antes de juntar')
        return 1
    print('nada falta: pode juntar')
    return 0


if __name__ == '__main__':
    sys.exit(main())
