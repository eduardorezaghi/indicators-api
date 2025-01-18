variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "region" {}
variable "compartment_id" {}
variable "db_project_db_name" {}
variable "db_password" {}


variable "home_address" {
  default = "192.168.1.1/32"
}

variable "project_name" {
  default = "stone-indicators"
}

variable "containers_name" {
  default = "stone-indicators-api"
}

variable "registry" {
  default = "gru.ocir.io"
}

variable "namespace" {
  default = "grtxhlfqxfde"
}