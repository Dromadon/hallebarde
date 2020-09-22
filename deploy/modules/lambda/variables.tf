variable "python_runtime" {
  type        = string
  description = "Python runtime, including the version, that will be used by the lambda."
}

variable "env" {}
variable "application_name" {}
variable "package_path" {}
variable "route53_zone_name" {}
