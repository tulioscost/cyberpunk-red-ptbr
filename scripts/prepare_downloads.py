#!/usr/bin/env python3
"""Prepare five honest, static packages from a fully compiled Cyberpunk RED release.

Requires build.mjs to have completed. This does not claim Foundry runtime testing.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
RELEASE = ROOT / "release"
DIST = RELEASE / "dist"
OUT = ROOT / "downloads"
VERSION = "v0.92.4-v14.369-ptbr.1"
PREFIX = "cyberpunk-red-ptbr-v14-369"


def checked_zip(target, paths, *, stored_zips=False):
    """Write stable ZIP paths from (archive path, local Path) records."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as z:
        for name, file in sorted(paths, key=lambda item: item[0]):
            if not file.is_file():
                raise FileNotFoundError(f"Required source file missing: {file}")
            z.write(file, name, compress_type=(zipfile.ZIP_STORED if stored_zips and file.suffix == ".zip" else zipfile.ZIP_DEFLATED))
    with zipfile.ZipFile(target) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"Invalid ZIP member: {bad}")
    return target


def folder_files(folder, *, prefix=""):
    return [(prefix + f.relative_to(folder).as_posix(), f)
            for f in folder.rglob("*") if f.is_file()]


def archive_source_as_repo(archive, destination):
    # Build a proper GitHub-repository ZIP, containing source at its root, plus
    # the PT-BR tools. Do not write to the live GitHub repo.
    with zipfile.ZipFile(archive) as source:
        names = source.namelist()
        for mandatory in ["src/system.json", "src/cpr.js", "package.json", "LICENCE.md"]:
            if mandatory not in names:
                raise RuntimeError(f"Source archive missing {mandatory}")
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as final:
            for member in names:
                if (member.endswith("/") or member.startswith(".github/")
                        or member.startswith("scripts/")
                        or member in {"README.md", "RELEASE_NOTES.md", ".gitignore"}):
                    continue
                final.writestr(member, source.read(member))
            for prefix in ("scripts", ".github"):
                for name, file in folder_files(ROOT / prefix, prefix=prefix + "/"):
                    final.write(file, name)
            for name in ("README.md", "RELEASE_NOTES.md", "COMO_GERAR_DOWNLOADS.md", ".gitignore"):
                final.write(ROOT / name, name)
    with zipfile.ZipFile(destination) as z:
        assert z.testzip() is None
        assert "src/system.json" in z.namelist()
        assert ".github/workflows/build-release.yml" in z.namelist()
    return destination


def main():
    # Guard against constructing simulated 'installers' from bare bootstrap files.
    for name in ("system.json", "cpr.js", "main.css", "lang/pt-BR.json"):
        if not (DIST / name).is_file():
            raise RuntimeError("Distribution incomplete: missing " + name + ". Run node scripts/build.mjs first.")
    manifest = json.loads((DIST / "system.json").read_text(encoding="utf-8"))
    if manifest.get("id") != "cyberpunk-red-core" or len(manifest.get("packs", [])) < 50:
        raise RuntimeError("Wrong or incomplete Foundry distribution")
    if manifest.get("version") != VERSION:
        raise RuntimeError("Wrong package version")
    upstream = RELEASE / "cyberpunk-red-core-source.zip"
    installer = RELEASE / "cyberpunk-red-core.zip"
    if not installer.is_file() or not upstream.is_file():
        raise RuntimeError("Missing compiled installation ZIP or GPL source ZIP")
    with zipfile.ZipFile(installer) as z:
        if "cpr.js" not in z.namelist() or "system.json" not in z.namelist():
            raise RuntimeError("Installation ZIP does not contain Foundry root files")
    OUT.mkdir(parents=True, exist_ok=True)
    install_target = OUT / (PREFIX + "-foundry-instalacao.zip")
    shutil.copyfile(installer, install_target)
    repo_target = OUT / (PREFIX + "-repositorio-github.zip")
    archive_source_as_repo(upstream, repo_target)

    # Overlay patch: only for the COMMUNITY V14 baseline, NOT the official V12
    # or earlier package variants; overwrites listed files in data/systems/.
    patch_target = OUT / (PREFIX + "-patch.zip")
    patch_parts = [(name, DIST / name) for name in (
        "system.json", "modules/system/overrides.js", "PORTABILITY_NOTES.md",
        "LICENCE.md", "CREDITS.md")]
    patch_readme = OUT / "INSTRUCOES-PATCH.txt"
    patch_readme.write_text(
        "PATCH EXPERIMENTAL DE CYBERPUNK RED PT-BR, Foundry 14.369\n\n"
        "BASE EXIGIDA: port comunitario Jesperhh01, commit\n"
        "69163c70aebf8a669d7c6f7e44084564846938ce\n"
        "NAO aplicar sobre a versao oficial do Foundry 12.\n"
        "Com o Foundry DESLIGADO, realize backup e extraia os arquivos para\n"
        "Data/systems/cyberpunk-red-core/, sobrescrevendo.\n"
        "O PATCH NAO substitui o pacote de instalacao completa.\n"
        "Nao foi realizado teste funcional no Foundry 14.369.\n",
        encoding="utf-8")
    patch_parts += [("INSTRUCOES-PATCH.txt", patch_readme)]
    checked_zip(patch_target, patch_parts)

    # Standalone data bundle. Not itself a Foundry system installation.
    packs_target = OUT / (PREFIX + "-compendios-ptbr.zip")
    files = folder_files(DIST / "packs", prefix="packs/")
    if not files:
        raise RuntimeError("No built compendiums found")
    pt_babele = DIST / "babele" / "pt-BR"
    if pt_babele.exists():
        files += folder_files(pt_babele, prefix="babele/pt-BR/")
    files.append(("lang/pt-BR.json", DIST / "lang/pt-BR.json"))
    instructions = OUT / "LEIA-ME-COMPENDIOS.txt"
    instructions.write_text(
        "Dados de compendios e traducao incluidos no sistema completo.\n"
        "Este arquivo nao e um modulo Foundry instalavel isoladamente.\n"
        "Copie para a instalacao correspondente apenas com o Foundry desligado\n"
        "e apos realizar backup.\n",
        encoding="utf-8")
    files += [("LEIA-ME-COMPENDIOS.txt", instructions)]
    checked_zip(packs_target, files)

    complete_target = OUT / (PREFIX + "-pacote-completo.zip")
    complete = [install_target, repo_target, patch_target, packs_target]
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in complete)
    checksum_path = OUT / "SHA256SUMS.txt"
    checksum_path.write_text(checksums, encoding="utf-8")
    to_bundle = [(p.name, p) for p in complete]
    to_bundle += [("system.json", RELEASE / "system.json"),
                  ("README.md", ROOT / "README.md"),
                  ("RELEASE_NOTES.md", ROOT / "RELEASE_NOTES.md"),
                  ("SHA256SUMS.txt", checksum_path)]
    checked_zip(complete_target, to_bundle, stored_zips=True)
    print("\nDownloads para publicacao:")
    for f in [complete_target, install_target, repo_target, patch_target, packs_target]:
        print(f"  {f.name}: {f.stat().st_size / (1024 * 1024):.2f} MiB")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, FileNotFoundError) as exc:
        sys.exit(str(exc))
