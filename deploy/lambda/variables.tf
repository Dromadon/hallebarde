variable "python_runtime" {
  type = string
  description = "Python runtime, including the version, that will be used by the lambda."
}

variable "path_to_package" {
  type = string
  description = "File path to the zip package containing the python code that will be executed in the lambda"
}