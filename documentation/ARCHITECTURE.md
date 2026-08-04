# Arquitetura do ecossistema Humanati

## Visão geral

Este repositório reúne a identidade, o Design System, o website e os materiais de comunicação da organização Humanati. Os pacotes históricos PF1, PF2 e PF3 permanecem preservados em `archives/source-packages/`; as pastas de produto representam a versão consolidada e utilizável.

## Camadas

- `branding/`: fontes canônicas de identidade e painéis de referência.
- `design-system/`: tokens, componentes, padrões e recursos compartilhados.
- `ui-kit/`, `glass-ui/`, `backgrounds/`, `icons/` e `dashboard-library/`: bibliotecas de experiência e composição visual.
- `website/`: implementação institucional e pacote consolidado do site.
- `marketing/` e `social-media/`: estratégia, campanhas, apresentações e peças.
- `documentation/`: decisões, inventários, manuais e processos.
- `devops/`: automação de validação, empacotamento e publicação.

## Fluxo de dependência

Branding alimenta tokens e padrões do Design System. O Design System alimenta UI Kit, bibliotecas visuais e website. Marketing e social media reutilizam os mesmos fundamentos, preservando consistência entre produto e comunicação.

## Fonte canônica

O website consolidado está em `website/master-package/`. Os arquivos incrementais adjacentes são preservados como evidência histórica. Novas alterações devem ocorrer nas fontes consolidadas e nunca dentro dos ZIPs em `archives/source-packages/`.

## Integridade

O inventário em `documentation/artifact-inventory.csv` registra caminho, tamanho e SHA-256. A validação automatizada confere estrutura obrigatória, referências essenciais e arquivos vazios antes de uma entrega.
