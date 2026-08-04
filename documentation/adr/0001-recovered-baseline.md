# ADR 0001: preservar pacotes históricos e consolidar fontes utilizáveis

- Estado: aceito
- Data: 2026-08-03

## Contexto

O projeto foi recuperado de 32 pacotes incrementais PF1, PF2 e PF3. Alguns caminhos se repetem entre lotes e podem representar evolução ou alternativas.

## Decisão

Preservar os ZIPs originais sem alteração em `archives/source-packages/` e organizar cópias consolidadas por domínio. Quando arquivos compartilham caminho, mas diferem em conteúdo, preservar as variantes com identificação do lote. O website em `website/master-package/` é a fonte canônica consolidada.

## Consequências

O histórico permanece auditável e reversível. O repositório ocupa mais espaço, porém evita perda de decisões anteriores e permite reconstrução por hashes.
