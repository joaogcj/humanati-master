# DevOps Humanati

- `Dockerfile` e `compose.yaml`: build e execução local na porta 8080.
- `.github/workflows/quality.yml`: validação, testes, build, Storybook e imagem de contêiner.
- `swarm/stack.yaml`: implantação replicada com atualização gradual e rollback.
- `ansible/deploy.yml`: publicação idempotente da stack em um gerente Swarm.
- `terraform/`: bucket S3 privado, versionado e criptografado, servido por CloudFront.

Antes de produção, defina um registro de imagens, domínio, certificado, região e canal de segredos aprovados pela organização. Não utilize o inventário de exemplo sem substituir endereço e usuário.
