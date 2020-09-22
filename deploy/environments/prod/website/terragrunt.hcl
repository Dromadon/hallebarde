include {
  path = find_in_parent_folders()
}

terraform {
  source = "${get_parent_terragrunt_dir()}/..//modules/website"
}

dependencies {
  paths = ["../api-gateway", "../domain"]
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  env = local.env_vars.locals.env
}

inputs = {
  env                   = "${local.env}"
  path_to_website_build = "${get_parent_terragrunt_dir()}/../../hallebarde-frontend/build"
}