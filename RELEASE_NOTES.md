# Cyberpunk RED PT-BR — port experimental para Foundry VTT 14.369

Versão: `v0.92.4-v14.369-ptbr.1`.

- Base original: [The Project Red Team](https://gitlab.com/cyberpunk-red-team/fvtt-cyberpunk-red-core), v0.92.4.
- Port V14 comunitário (fonte fixada em commit): [Jesperhh01/fvtt-cyberpunk-red-core-v14-port](https://github.com/Jesperhh01/fvtt-cyberpunk-red-core-v14-port), `69163c70aebf8a669d7c6f7e44084564846938ce`.
- Mantido o ID original `cyberpunk-red-core` para preservar referências do sistema, compêndios e macros.
- Localização `pt-BR` e arquivos Babele do port preservados, sem promessa de tradução integral de todos os textos.
- Aplicado tratamento defensivo à sobrescrita do método interno de Ruler para evitar erro quando indisponível no Foundry 14.
- Substituído clone legado pelo método `foundry.utils.deepClone` na ferramenta de DV.
- Compêndios, templates e CSS compilados por meio da cadeia de build original.
- Metadados do manifesto preparados para Foundry 14 até a build 14.369; **compatibilidade funcional não confirmada**.

**Atenção:** experimental, não homologado em instância real do Foundry 14.369. Testar rolagens, fichas, dano, iniciativa, efeitos, netrunning, compêndios e migração de mundos antes da adoção. Realizar backup completo. Não instalar simultaneamente com a distribuição oficial: os dois usam o mesmo `system.id`.

O trabalho derivado preserva a licença GPL-3.0 do software original e os créditos de seus autores. Cyberpunk RED e sua propriedade intelectual pertencem aos respectivos titulares; sistema não oficial, sem endosso da R. Talsorian Games.

## Downloads separados na versão de publicação

Após executar a compilação em GitHub Actions, são produzidos estes arquivos:

1. `cyberpunk-red-ptbr-v14-369-pacote-completo.zip` — quatro arquivos ZIP, manifesto e documentação.
2. `cyberpunk-red-ptbr-v14-369-foundry-instalacao.zip` — sistema instalado via ZIP.
3. `cyberpunk-red-ptbr-v14-369-repositorio-github.zip` — código-fonte correspondente, scripts de build e workflow.
4. `cyberpunk-red-ptbr-v14-369-patch.zip` — atualização **somente** sobre a base comunitária v14 do commit especificado; não serve para versão oficial v12.
5. `cyberpunk-red-ptbr-v14-369-compendios-ptbr.zip` — compêndios e idioma extraídos para inspeção ou reposição (não instalável isoladamente).

Esses pacotes são gerados pelo workflow. Sua presença no README não significa que foram publicados.
