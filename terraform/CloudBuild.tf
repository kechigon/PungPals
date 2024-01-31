/*resource "google_cloud_build_trigger" "django_cloud_migrate_trigger" {
  name     = "django-cloud-migrate-trigger"
  project  = "pungpals"

  filename = "../PungPals/cloudmigrate.yaml"

  substitution {
    _INSTANCE_NAME       = "django-instance"
    _REGION              = var.region
    _SERVICE_NAME        = var.project
    _SECRET_SETTINGS_NAME = "django_settings"
  }

  build {
    tag = "${_LOCATION}-docker.pkg.dev/$PROJECT_ID/${_REPOSITORY}/${_IMAGE}:${formatdate("YYYYMMDDHHMMSS", timestamp())}"
  }
}*/