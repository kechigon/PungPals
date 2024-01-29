//Use gcloud command since it cannot be changed in the editor role.

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
}

resource "random_string" "password" {
  length  = 30
  upper   = true
  lower   = true
  special = false
  number  = false
}

resource "google_secret_manager_secret" "superuser_password_secret" {
  secret_id = "superuser_password"
  
  replication {
    user_managed {
      replicas {
        location = "asia-northeast1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "password_version" {
  secret = google_secret_manager_secret.superuser_password_secret.id
  secret_data = random_string.password.result
}*/