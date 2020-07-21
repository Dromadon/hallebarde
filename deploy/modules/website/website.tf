resource "aws_s3_bucket_object" "website" {
  for_each = module.template_files.files

  bucket = aws_s3_bucket.website.id
  key    = each.key
  source = each.value.source_path

  etag = each.value.digests.md5

  content_type = each.value.content_type

  acl = "public-read"
}

module "template_files" {
  source = "hashicorp/dir/template"

  base_dir = var.path_to_website_build
}