# Humanati

Repositório recuperado e consolidado a partir dos pacotes PF1, PF2 e PF3 produzidos no projeto Humanati.

## Conteúdo recuperado

- `branding/`: identidade oficial em SVG, PNG, PDF, ICO e documentação de origem.
- `website/`: arquivos incrementais dos lotes PF2 e o pacote final em `website/master-package/`.
- `design-system/`: componentes, tokens, ícones, exemplos, templates e notas dos 24 lotes PF3.
- `documentation/`: versões históricas dos manifestos e inventário verificável por SHA-256.
- `archives/source-packages/`: os 32 ZIPs originais, preservados sem alterações.

## Fonte canônica

Para o website, `website/master-package/` é a entrega consolidada mais recente. Os demais arquivos em `website/` preservam o material incremental dos lotes.

O Design System foi consolidado por categoria. Quando dois lotes continham o mesmo caminho com conteúdo diferente, ambos foram preservados com o número do lote no nome. É o caso de `charts.json`.

## Integridade

`documentation/artifact-inventory.csv` registra caminho, tamanho e SHA-256 de cada arquivo consolidado. Os pacotes originais permanecem disponíveis em `archives/source-packages/` para auditoria e reconstrução.

## Estado

A sequência recuperada está completa: PF1, PF2 lotes 001–006, PF2 Final v1 e PF3 lotes 001–024. Consulte `documentation/RECOVERY_STATUS.md` para limitações e próximos passos.

## Documentação

- [Arquitetura](documentation/ARCHITECTURE.md)
- [Manual de marca](documentation/BRAND_MANUAL.md)
- [Guia de desenvolvimento](documentation/DEVELOPMENT_GUIDE.md)
- [Governança do Design System](documentation/DESIGN_SYSTEM_GOVERNANCE.md)
- [Processo de entrega](documentation/RELEASE_PROCESS.md)
- [DevOps](devops/README.md)
- [Contribuição](CONTRIBUTING.md)
- [Segurança](SECURITY.md)

## Qualidade

Execute `npm run validate`, `npm test` e `npm run build` antes de uma entrega. O Storybook pode ser revisado localmente com `npm run storybook` e compilado com `npm run build-storybook`.
