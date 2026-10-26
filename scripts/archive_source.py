#!/usr/bin/env python3
"""Bundle corresponding GPL source code, without dependencies or generated assets."""
import pathlib
import sys
import zipfile

root = pathlib.Path(sys.argv[1]).resolve()
target = pathlib.Path(sys.argv[2]).resolve()
target.parent.mkdir(parents=True, exist_ok=True)
exclude = {'.git', 'node_modules', 'dist', '__pycache__', '.venv'}
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for file in sorted(root.rglob('*')):
        rel = file.relative_to(root)
        if file.is_file() and not any(part in exclude for part in rel.parts):
            archive.write(file, rel.as_posix())
with zipfile.ZipFile(target) as z:
    assert {'src/system.json', 'src/cpr.js', 'package.json', 'LICENCE.md'} <= set(z.namelist())
    assert z.testzip() is None
print(f'Arquivo de código-fonte GPL: {target} ({target.stat().st_size:,} bytes)')
