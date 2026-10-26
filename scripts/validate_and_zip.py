#!/usr/bin/env python3
"""Static checks for a Foundry system, then a root-correct release ZIP."""
import json
import pathlib
import sys
import zipfile


def verify(dist):
    for name in ('system.json', 'cpr.js', 'main.css', 'template.json',
                 'lang/pt-BR.json', 'LICENCE.md', 'CREDITS.md'):
        file = dist / name
        assert file.is_file() and file.stat().st_size > 0, f'Arquivo obrigatório ausente: {name}'
    m = json.loads((dist / 'system.json').read_text(encoding='utf-8'))
    assert m['id'] == 'cyberpunk-red-core'
    assert m['compatibility']['minimum'] == '14'
    assert m['compatibility']['maximum'] == '14.369'
    assert 'tulioscost/cyberpunk-red-ptbr' in m['manifest']
    assert 'tulioscost/cyberpunk-red-ptbr' in m['download']
    assert 'releases/download/' in m['download']
    assert any(lang['lang'] == 'pt-BR' for lang in m['languages'])
    pt = json.loads((dist / 'lang' / 'pt-BR.json').read_text(encoding='utf-8'))
    assert len(pt) > 100, 'A localização pt-BR parece incompleta'
    assert len(m['packs']) >= 50, 'Compêndios ausentes: menos de 50 packs'
    all_packs = {pack['name'] for pack in m['packs']}
    for folder in m.get('packFolders', []):
        for pack in folder['packs']:
            assert pack in all_packs, f'Pasta referencia pack inexistente: {pack}'
    for pack in m['packs']:
        location = dist / pack['path']
        assert location.is_dir() and any(location.iterdir()), f'Pack ausente/vazio: {pack["name"]}'
    assert (dist / 'modules').is_dir()
    assert (dist / 'templates').is_dir()
    print(f'Validação estática aprovada: {len(m["packs"])} compêndios; '
          f'{len(pt)} entradas pt-BR; compatibilidade declarada até 14.369.')


def archive(dist, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=7) as z:
        for file in sorted(dist.rglob('*')):
            if file.is_file():
                z.write(file, file.relative_to(dist).as_posix())
    with zipfile.ZipFile(target) as z:
        assert 'system.json' in z.namelist() and 'cpr.js' in z.namelist()
        assert z.testzip() is None
    print(f'ZIP de instalação criado: {target} ({target.stat().st_size:,} bytes)')


if __name__ == '__main__':
    dist, target = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    verify(dist)
    archive(dist, target)
