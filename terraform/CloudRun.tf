//Use gcloud command since it cannot be changed in the editor role.
/*resource "google_cloud_run_service" "pungpals_service" {
  name     = "pungpals-service"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project}/${var.project}/${var.project}"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service" "pungpals_service_env" {
  name     = google_cloud_run_service.pungpals_service.name
  location = google_cloud_run_service.pungpals_service.location

  template {
    spec {
      containers {
        image = google_cloud_run_service.pungpals_service.template.0.spec.0.containers.0.image

        env {
          name  = "CLOUDRUN_SERVICE_URL"
          value = google_cloud_run_service.polls_service.status[0].url
        }
      }
    }
  }

  depends_on = [google_cloud_run_service.pungpals_service]

  traffic {
    percent         = 100
    latest_revision = true
  }
}*/