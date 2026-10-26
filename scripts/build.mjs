#!/usr/bin/env node
/**
 * Build the GPL-3.0 Cyberpunk RED v14 community port and preserve pt-BR.
 * This is a reproducible bootstrap, not a claim of Foundry runtime verification.
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SOURCE_URL = 'https://github.com/Jesperhh01/fvtt-cyberpunk-red-core-v14-port.git';
const SOURCE_REV = '69163c70aebf8a669d7c6f7e44084564846938ce';
const REPOSITORY = 'https://github.com/tulioscost/cyberpunk-red-ptbr';
const TAG = 'v0.92.4-v14.369-ptbr.1';
const ZIP_NAME = 'cyberpunk-red-core.zip';
const TITLE = 'Cyberpunk RED - PT-BR (Foundry V14 experimental)';
const DIST_DIR = path.join(ROOT, 'release', 'dist');
const options = process.argv.slice(2);
const sourceIndex = options.indexOf('--source');
const sourceOverride = sourceIndex === -1 ? null : options[sourceIndex + 1];
const skipNpm = options.includes('--skip-npm');
if (sourceIndex !== -1 && (!sourceOverride || sourceOverride.startsWith('--'))) {
  throw new Error('Uso: node scripts/build.mjs [--source CAMINHO] [--skip-npm]');
}

function run(cmd, args, cwd, env = process.env) {
  const result = spawnSync(cmd, args, {cwd, env, stdio: 'inherit', shell: false});
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${cmd} ${args.join(' ')} falhou (código ${result.status})`);
}
function saveJson(file, object) {
  fs.writeFileSync(file, JSON.stringify(object, null, 2) + '\n');
}
function requireFile(file) {
  if (!fs.existsSync(file)) throw new Error(`Arquivo obrigatório ausente: ${file}`);
}
function patchSource(work) {
  const manifestPath = path.join(work, 'src', 'system.json');
  requireFile(manifestPath);
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  if (manifest.id !== 'cyberpunk-red-core') throw new Error('ID de sistema não corresponde à base esperada');
  if (!manifest.languages?.some(lang => lang.lang === 'pt-BR' && lang.path === 'lang/pt-BR.json')) {
    throw new Error('Esta versão do código-fonte não fornece localização pt-BR');
  }
  requireFile(path.join(work, 'src', 'lang', 'pt-BR.json'));
  manifest.version = TAG;
  manifest.title = TITLE;
  manifest.compatibility = {minimum: '14', verified: '14', maximum: '14.369'};
  manifest.manifest = 'https://raw.githubusercontent.com/tulioscost/cyberpunk-red-ptbr/main/system.json';
  manifest.download = `${REPOSITORY}/releases/download/${TAG}/${ZIP_NAME}`;
  manifest.url = REPOSITORY;
  manifest.authors = [...(manifest.authors || []), {name: 'Portabilidade PT-BR (versão experimental)', url: REPOSITORY}];
  saveJson(manifestPath, manifest);

  // O port v14 herdou um override de método interno do Ruler. Em builds onde
  // a API não o expõe, é mais seguro desativar apenas o recurso de DV do régua.
  const overridePath = path.join(work, 'src', 'modules', 'system', 'overrides.js');
  requireFile(overridePath);
  let code = fs.readFileSync(overridePath, 'utf8');
  const before = '  const RulerClass = foundry.canvas.interaction.Ruler;\n  const foundryPrototype = RulerClass.prototype._getSegmentLabel;';
  const after = [
    '  const RulerClass = foundry.canvas?.interaction?.Ruler;',
    '  const foundryPrototype = RulerClass?.prototype?._getSegmentLabel;',
    '  if (typeof foundryPrototype !== "function") {',
    '    console.warn("Cyberpunk RED PT-BR: método interno da régua indisponível; DV da régua desabilitada.");',
    '    return;',
    '  }',
  ].join('\n');
  if (!code.includes(before)) throw new Error('A assinatura do override mudou; revisão manual obrigatória');
  code = code.replace(before, after);
  const oldClone = 'foundry.utils.duplicate(DvTable.table)';
  if (!code.includes(oldClone)) throw new Error('Clone do DV mudou; revisão manual obrigatória');
  code = code.replace(oldClone, 'foundry.utils.deepClone(DvTable.table)');
  fs.writeFileSync(overridePath, code);
}
function patchDist(work) {
  // A build da origem gera metadata via variáveis de ambiente. Valide em vez de confiar.
  const manifestFile = path.join(DIST_DIR, 'system.json');
  requireFile(manifestFile);
  const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'));
  manifest.version = TAG;
  manifest.title = TITLE;
  manifest.compatibility = {minimum: '14', verified: '14', maximum: '14.369'};
  manifest.manifest = 'https://raw.githubusercontent.com/tulioscost/cyberpunk-red-ptbr/main/system.json';
  manifest.download = `${REPOSITORY}/releases/download/${TAG}/${ZIP_NAME}`;
  manifest.url = REPOSITORY;
  saveJson(manifestFile, manifest);
  for (const file of ['LICENCE.md', 'CREDITS.md']) {
    requireFile(path.join(work, file));
    fs.copyFileSync(path.join(work, file), path.join(DIST_DIR, file));
  }
  fs.copyFileSync(path.join(ROOT, 'RELEASE_NOTES.md'), path.join(DIST_DIR, 'PORTABILITY_NOTES.md'));
  fs.copyFileSync(manifestFile, path.join(ROOT, 'release', 'system.json'));
}

fs.mkdirSync(path.join(ROOT, 'release'), {recursive: true});
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'cpr-v14-'));
try {
  const work = path.join(temp, 'source');
  if (sourceOverride) {
    const absolute = path.resolve(sourceOverride);
    if (!fs.existsSync(absolute)) throw new Error(`Origem não encontrada: ${absolute}`);
    fs.cpSync(absolute, work, {recursive: true});
    console.log(`Usando fonte local: ${absolute}`);
  } else {
    run('git', ['clone', '--filter=blob:none', SOURCE_URL, work], ROOT);
    run('git', ['checkout', '--detach', SOURCE_REV], work);
    const rev = spawnSync('git', ['rev-parse', 'HEAD'], {cwd: work, encoding: 'utf8'});
    if (rev.status !== 0 || rev.stdout.trim() !== SOURCE_REV) {
      throw new Error('Revisão upstream inesperada: build cancelado');
    }
  }
  patchSource(work);
  if (fs.existsSync(DIST_DIR)) fs.rmSync(DIST_DIR, {recursive: true, force: true});
  const env = {
    ...process.env,
    CI: 'true',
    SYSTEM_VERSION: TAG,
    SYSTEM_TITLE: TITLE,
    REPO_URL: REPOSITORY,
    ZIP_FILE: ZIP_NAME,
  };
  if (!skipNpm) {
    run('npm', ['ci', '--no-audit', '--no-fund'], work, env);
    run('npm', ['run', 'build'], work, env);
  } else {
    // For local static test, permit dist in provided fixture.
    requireFile(path.join(work, 'dist', 'system.json'));
  }
  fs.cpSync(path.join(work, 'dist'), DIST_DIR, {recursive: true});
  patchDist(work);
  run('python3', [path.join(ROOT, 'scripts', 'archive_source.py'), work, path.join(ROOT, 'release', 'cyberpunk-red-core-source.zip')], ROOT);
  run('python3', [path.join(ROOT, 'scripts', 'validate_and_zip.py'), DIST_DIR, path.join(ROOT, 'release', ZIP_NAME)], ROOT);
  console.log(`\nArquivos prontos em ${path.join(ROOT, 'release')}`);
  console.log('AVISO: não houve teste funcional dentro do Foundry 14.369.');
} finally {
  fs.rmSync(temp, {recursive: true, force: true});
}
