# Guia de desenvolvimento

## Requisitos

- Node.js 20 ou superior.
- npm compatível com a versão instalada do Node.js.

## Rotina local

1. Instale as dependências com `npm install`.
2. Execute `npm run validate` para conferir a estrutura.
3. Execute `npm test` para validar os contratos automatizados.
4. Execute `npm run build` para gerar o pacote local.
5. Use `npm run storybook` para revisar componentes isoladamente.

## Convenções

- Preserve os pacotes históricos sem edição.
- Reutilize tokens antes de criar valores visuais isolados.
- Use o prefixo `hu-` nas classes compartilhadas do UI Kit.
- Mantenha textos em português do Brasil e arquivos em UTF-8.
- Não adicione credenciais, chaves privadas ou segredos ao repositório.

## Critérios de aceite

Toda alteração deve passar por validação, testes e build. Mudanças visuais exigem revisão responsiva, contraste, navegação por teclado, foco visível e comportamento com movimento reduzido.

## Dependências reproduzíveis

O acervo recuperado não continha um `package-lock.json`, e o ambiente de consolidação não possui acesso ao registro público para gerá-lo com segurança. O primeiro pipeline com acesso controlado à internet deve executar `npm install`, revisar o arquivo gerado e versioná-lo; depois disso, Docker e CI podem migrar de `npm install` para `npm ci`.

Na auditoria de consolidação, validação, testes e build foram executados localmente. O build do Storybook está definido no pipeline, mas sua repetição local depende da instalação das dependências externas declaradas no `package.json`.
