//Use gcloud command since it cannot be changed in the editor role.

/*resource "google_secret_manager_secret_iam_member" "secret_iam_binding" {
  secret_id = "django_settings"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:-compute@developer.gserviceaccount.com"
}

resource "google_secret_manager_secret_iam_binding" "cloudbuild_settingsecret_accessor" {
  secret_id = "django_settings"
  role      = "roles/secretmanager.secretAccessor"

  members    = [
    "serviceAccount:951466943894@cloudbuild.gserviceaccount.com"
  ]
}

resource "google_secret_manager_secret_iam_binding" "cloudbuild_passwdsecret_accessor" {
  secret_id = "superuser_password"
  role      = "roles/secretmanager.secretAccessor"

  members    = [
    "serviceAccount:951466943894@cloudbuild.gserviceaccount.com"
  ]
}

resource "google_project_iam_member" "cloudsql_client" {
  project = var.project
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:951466943894@cloudbuild.gserviceaccount.com"
}*/