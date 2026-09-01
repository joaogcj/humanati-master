# Regras para sessões trabalhando neste repositório

## Checkpoints - registrar em `CHECKPOINTS.md`

Toda sessão que trabalha neste repositório registra um **checkpoint** em
[`CHECKPOINTS.md`](CHECKPOINTS.md) sempre que:

- **finalizar uma tarefa** (feature, fix ou refactor que fecha);
- **pausar o trabalho** com algo pendente ou movido para o backlog
  (`TODO.md`, `BACKLOG.md` ou issues);
- **aplicar ou preparar** uma alteração em **ambiente real** (deploy,
  configuração de servidor, segredo, migração de banco, DNS);
- fazer uma **alteração relevante** de arquitetura, dependência ou contrato.

Cada entrada leva data + hora (fuso `America/Sao_Paulo`), o que foi feito,
o(s) commit(s), o estado em que ficou (concluído | pausado - o que falta |
preparado - aguardando execução) e como foi validado. Entrada mais recente
no fim do arquivo. O cabeçalho de `CHECKPOINTS.md` tem o formato completo.
Isso é adicional ao `CHANGELOG.md` / `TODO.md`, não os substitui.
