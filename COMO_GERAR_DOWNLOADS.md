# Distribuição em cinco arquivos — Cyberpunk RED PT-BR v14.369

Este repositório **não contém o instalador nem os compêndios binários**. Os scripts baixam e compilam o projeto comunitário em GitHub Actions e criam os seguintes cinco ZIPs após sucesso da build:

1. `cyberpunk-red-ptbr-v14-369-pacote-completo.zip`
2. `cyberpunk-red-ptbr-v14-369-foundry-instalacao.zip`
3. `cyberpunk-red-ptbr-v14-369-repositorio-github.zip`
4. `cyberpunk-red-ptbr-v14-369-patch.zip`
5. `cyberpunk-red-ptbr-v14-369-compendios-ptbr.zip`

**Executar:** envie os arquivos para a raiz de `tulioscost/cyberpunk-red-ptbr`, abra **Actions**, selecione **Compilar Cyberpunk RED PT-BR para Foundry 14.369** e execute **Run workflow**. Baixe o artifact `cyberpunk-red-ptbr-v14-369`. **Não publique a release** até validar no Foundry VTT 14.369.

A base do PATCH binário é o *port* comunitário V14, commit `69163c70aebf8a669d7c6f7e44084564846938ce`. Ele não funciona como atualização direta da distribuição oficial V12. Para migrar desta, use o ZIP completo em mundo de teste, após backup.

A licença GPL-3.0 e os créditos dos autores originais estão incluídos nos arquivos de fonte/instalação gerados. Esta adaptação não possui certificação funcional no Foundry 14.369.
