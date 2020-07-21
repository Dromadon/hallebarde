include {
  path = find_in_parent_folders()
}

inputs = {
  package_path   = "${get_parent_terragrunt_dir()}/../../app/package/hallebarde.zip"
  python_runtime = "python3.8"
  env            = "${local.env}"
}

terraform {
  source = "${get_parent_terragrunt_dir()}/..//modules/lambda"
}

dependencies {
  paths = ["../iam", "../dynamodb", "../s3"]
}

locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  env = local.env_vars.locals.env
}