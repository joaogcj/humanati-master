# Checkpoints

Registro cronológico (data + hora, fuso `America/Sao_Paulo`) dos marcos de
trabalho neste repositório. Uma sessão registra um checkpoint sempre que:

- **finaliza uma tarefa** (feature, correção ou refatoração que fecha);
- **pausa o trabalho** deixando algo pendente ou movido para o backlog
  (`TODO.md`, `BACKLOG.md` ou issues);
- **aplica ou prepara uma alteração em ambiente real** (deploy, configuração
  de servidor, segredo rotacionado, migração de banco, DNS, etc.);
- faz uma **alteração relevante** de arquitetura, dependência ou contrato que
  outra sessão precise saber que aconteceu.

Não substitui `CHANGELOG.md`, `TODO.md` nem `BACKLOG.md`: o checkpoint é o
"o que esta sessão fez e em que estado ficou", com ponteiros para o detalhe.
Mudança pequena e isolada não precisa de checkpoint próprio; o fechamento da
tarefa que a contém, sim.

## Formato de cada entrada

    ## AAAA-MM-DD - título curto do marco

    - **HH:MM** - o que foi feito. Commit(s): `abc1234`.
      Estado: concluído | pausado (o que falta) | preparado (aguardando
      quem tem acesso real). Validação: testes / build / verificação
      manual, ou "não validado" e por quê.

Fuso `America/Sao_Paulo` em todas as datas e horas. Entrada mais recente no
fim do arquivo.

---

## 2026-09-01 - convenção de checkpoints adicionada ao repositório

- **20:49** - criados `CHECKPOINTS.md` (este arquivo) e a seção "Checkpoints"
  em `CLAUDE.md`, padronizando o registro de marcos de trabalho nos projetos
  ativos. Estado: concluído. Validação: mudança só de documentação, sem
  efeito em código ou ambiente.
