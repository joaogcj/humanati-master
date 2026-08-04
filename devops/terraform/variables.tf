variable "aws_region" {
  description = "Região AWS para os recursos do site."
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Nome globalmente único do bucket de artefatos."
  type        = string
}

variable "tags" {
  description = "Tags adicionais para governança."
  type        = map(string)
  default     = {}
}
