# Governança do Design System

## Princípios

O Humanati Design System é a referência compartilhada para interfaces e comunicação digital. Seus fundamentos devem ser previsíveis, acessíveis, reutilizáveis e rastreáveis.

## Ciclo de mudança

1. Identificar uma necessidade recorrente e documentar o caso de uso.
2. Verificar se tokens ou componentes existentes atendem à necessidade.
3. Propor a menor extensão compatível com o sistema atual.
4. Implementar estados, acessibilidade, exemplos e testes.
5. Revisar no Storybook e registrar impacto de migração.
6. Publicar segundo versionamento semântico.

## Níveis de estabilidade

- Experimental: sujeito a mudanças e não recomendado para fluxos críticos.
- Estável: documentado, testado e indicado para produção.
- Descontinuado: mantido temporariamente com alternativa e prazo de retirada.

## Responsabilidades

Design mantém linguagem, tokens e critérios visuais. Engenharia mantém API, qualidade e compatibilidade. Produto valida utilidade e prioridade. Comunicação assegura coerência da marca. Mudanças estruturais exigem decisão registrada em `documentation/adr/`.

## Acessibilidade

Componentes estáveis devem atender WCAG 2.2 nível AA quando aplicável, incluindo contraste, semântica, teclado, foco, nomes acessíveis, mensagens de erro e redução de movimento.
