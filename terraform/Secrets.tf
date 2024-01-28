//Use the gcloud command since it cannot be changed in the editor role.

/*data "local_file" "env_file" {
  filename = "${path.module}/.env"
}

resource "google_secret_manager_secret" "django_settings" {
  secret_id = "django_settings"

  replication {
    user_managed {
      replicas {
        location = "asia-northeast1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "django_settings_version" {
  secret      = google_secret_manager_secret.django_settings.id
  secret_data = base64encode(data.local_file.env_file.content)
}*/