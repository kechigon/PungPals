variable "credentials_file" {
  description = "Path to crdential file"
}

variable "project" {
  default = "pungpals"
}

variable "region" {
  default = "asia-northeast1"
}

variable "zone" {
  default = "asia-northeast1-b"
}

variable "service_name" {
  default = "pungpals"
}

variable "postgres_passwd" {
  description = "postgres password"
}