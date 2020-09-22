include {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_parent_terragrunt_dir()}/..//modules/api-gateway"
}

dependencies {
  paths = ["../lambda", "../domain", "../cognito"]
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  env = local.env_vars.locals.env
}

inputs = {
  env = "${local.env}"
}