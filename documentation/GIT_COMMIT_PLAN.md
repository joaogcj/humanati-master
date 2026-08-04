# Plano de commits

O repositório foi recuperado sem histórico local de commits e não possui nome ou e-mail de autoria configurados. Para evitar atribuição artificial, os commits devem ser criados após a configuração da identidade do responsável.

## Sequência recomendada

1. `chore(recovery): preserva os 32 pacotes originais`
   - `archives/`, `documentation/RECOVERY_STATUS.md` e inventário inicial.
2. `feat(brand): consolida identidade e fontes canônicas`
   - `branding/` e documentação de marca.
3. `feat(design-system): consolida tokens componentes e storybook`
   - `design-system/`, `ui-kit/`, `stories/`, `.storybook/` e bibliotecas visuais.
4. `feat(website): consolida pacote institucional`
   - `website/`.
5. `feat(marketing): adiciona campanhas conteúdo e apresentação`
   - `marketing/` e `social-media/`.
6. `docs(governance): documenta arquitetura processos e segurança`
   - documentação, `README.md`, `CONTRIBUTING.md` e `SECURITY.md`.
7. `ci(devops): adiciona qualidade contêiner e infraestrutura`
   - `.github/`, `devops/`, `Dockerfile`, `.dockerignore` e `compose.yaml`.

## Fechamento

Após configurar `user.name` e `user.email`, revise o escopo com `git status`, execute os testes e crie os commits na ordem acima. A branch principal deve se chamar `main`. Nenhum push ou publicação deve ocorrer sem repositório remoto e autorização explícita.
