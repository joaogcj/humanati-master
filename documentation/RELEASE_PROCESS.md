# Processo de entrega

## Preparação

1. Confirme que arquivos históricos permanecem intactos.
2. Atualize documentação e inventário quando houver novos artefatos.
3. Execute validação, testes, build e build do Storybook.
4. Revise os artefatos visuais e os principais fluxos responsivos.

## Versionamento

Use versionamento semântico para código e bibliotecas. Correções compatíveis incrementam patch; funcionalidades compatíveis incrementam minor; mudanças incompatíveis incrementam major. Pacotes editoriais podem acrescentar uma data no formato `AAAA-MM-DD`.

## Publicação

As automações devem validar toda solicitação de mudança. Uma entrega aprovada gera artefatos reproduzíveis, manifesto de integridade e notas objetivas de alteração. Ambientes de produção exigem aprovação explícita e segredos mantidos fora do repositório.

## Reversão

Reverta pela versão anterior publicada; nunca altere um pacote histórico para simular uma correção. Registre causa, impacto e ação corretiva.
