# Cyberpunk RED PT-BR — Foundry VTT 14.369 (experimental)

Este repositório de publicação prepara um build **completo** do sistema Cyberpunk RED a partir da base comunitária que já portou o código para Foundry V14. Mantém a localização `pt-BR` do projeto upstream, fichas e compêndios. **Não é** um módulo de tradução independente.

> **Status:** scripts produzidos e validados estaticamente; comportamento no Foundry VTT 14.369 não verificado em execução. Não confundir manifesto de compatibilidade com certificação funcional.

## Fonte e política de reprodução

- Sistema original: https://gitlab.com/cyberpunk-red-team/fvtt-cyberpunk-red-core (v0.92.4).
- Base V14: https://github.com/Jesperhh01/fvtt-cyberpunk-red-core-v14-port
- Commit V14 fixado: `69163c70aebf8a669d7c6f7e44084564846938ce` (garante reprodutibilidade).
- Build e distribuição herdam GPL-3.0; `LICENCE.md` e `CREDITS.md` do upstream entram no ZIP.

## Formato dos downloads

O workflow produz cinco arquivos separados, nos moldes de uma release tradicional:

| Download | Arquivo | Uso |
|---|---|---|
| Pacote completo | `cyberpunk-red-ptbr-v14-369-pacote-completo.zip` | Contém instalador, repositório, patch, compêndios, manifesto e notas |
| Instalação do Foundry | `cyberpunk-red-ptbr-v14-369-foundry-instalacao.zip` | Arquivos do sistema completos para instalação |
| Repositório GitHub | `cyberpunk-red-ptbr-v14-369-repositorio-github.zip` | Fonte GPL-3.0, arquivos do build e GitHub Actions |
| PATCH de atualização | `cyberpunk-red-ptbr-v14-369-patch.zip` | Sobrepor **somente** à instalação da base comunitária V14 descrita no patch |
| Compêndios PT-BR | `cyberpunk-red-ptbr-v14-369-compendios-ptbr.zip` | Exportação dos compêndios e da localização, não é um sistema instalável |

**Importante:** os cinco arquivos são gerados somente após o comando `python3 scripts/prepare_downloads.py`, executado automaticamente pelo GitHub Actions **depois da compilação integral**. Não são gerados ZIPs fictícios quando não há código-fonte e compêndios compilados.

## 1. Adicionar este pacote ao repositório de destino

Destino: **https://github.com/tulioscost/cyberpunk-red-ptbr** (branch `main`).

Envie para a raiz **o conteúdo** deste ZIP, preservando `.github/workflows/build-release.yml`. A pasta `.github` pode ficar oculta em alguns gerenciadores de arquivos: habilite exibição de arquivos ocultos. O repositório de destino está vazio no momento da preparação.

## 2. Compilar no GitHub Actions

1. Abra a aba **Actions** do repositório.
2. Selecione **Compilar Cyberpunk RED PT-BR para Foundry 14.369**.
3. Use **Run workflow**, mantendo `publicar_release = false`.
4. Após a conclusão, obtenha o artifact `cyberpunk-red-ptbr-v14-369`: contém o manifesto, os cinco ZIPs acima e a fonte GPL.
5. Faça uma instalação **em uma cópia de mundo**, valide as fichas, rolagens, combate, compêndios e efeitos. Não teste em seu mundo principal.
6. Só depois execute novamente o workflow com `publicar_release = true` para publicar uma **pré-release**. Isso requer Actions e a permissão `GITHUB_TOKEN` com `contents: write` nas configurações do repositório.

Após publicação, o workflow atualizará também o manifesto na branch `main` para oferecer **atualizações automáticas**. URL para instalação:

`https://raw.githubusercontent.com/tulioscost/cyberpunk-red-ptbr/main/system.json`

URL alternativa, disponível assim que a pré-release existir:

`https://github.com/tulioscost/cyberpunk-red-ptbr/releases/download/v0.92.4-v14.369-ptbr.1/system.json`

O GitHub não expõe pré-releases por `/releases/latest`; por isso o manifesto usa o arquivo da branch `main`. Se a publicação terminar mas a atualização da branch falhar, use temporariamente o endereço da tag.

## 3. Compilação local (opcional)

Requer `git`, Node.js 22+, npm, Python 3.12+ e acesso à internet:

```sh
node scripts/build.mjs
```

Execute `python3 scripts/prepare_downloads.py` após a compilação. Serão gerados `release/system.json`, o instalador, o código-fonte e os **cinco ZIPs na pasta `downloads/`**. O ZIP instalável possui `system.json` e `cpr.js` na raiz.

## Segurança e compatibilidade

- **Mesmo ID do sistema oficial:** `cyberpunk-red-core`; instalar substitui a versão atualmente instalada.
- Faça backup integral do diretório de dados do Foundry antes da atualização.
- As verificações automáticas cobrem manifesto, arquivos, 50+ compêndios, localização, estrutura do ZIP e sintaxe de pontos de entrada. Não executam Foundry.
- O port da comunidade usa APIs da V14, mas pode conservar pontos de API incompatíveis. O override da régua será desativado se o método interno deixar de existir.
- Os dados e recursos da R. Talsorian seguem as condições de uso e atribuição dos titulares; o projeto não é oficial.

## Checklist de teste manual de compatibilidade

1. Crie mundo descartável no Foundry **14.369** e ative PT-BR nas configurações do idioma.
2. Crie personagem e NPC, edite atributos, habilidades, papéis e equipamentos.
3. Faça rolagens de atributo, perícia, iniciativa, dano e ataques automáticos; confira mensagens no chat.
4. Equipe, use e recarregue armas; aplique ablação de armadura e ferimentos críticos.
5. Instale ciberware e gerencie humanidade.
6. Abra cyberdeck, programas, Black ICE e faça testes de netrunning.
7. Abra todos os compêndios, importe um item e verifique Babele.
8. Teste cenas, tokens, régua de DV, efeitos ativos e macros.
9. Teste cópia de um mundo antigo, examine o log de migração e o console (F12).

## Sobre atualizações

Ao mudar a fonte V14, atualize o commit fixado **após auditoria**. Para uma nova release, incremente `TAG` no script, workflow e notas. Não reutilize a mesma tag para diferentes builds.
