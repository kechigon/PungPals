resource "google_storage_bucket" "bucket" {
  name     = "${var.service_name}-gcs"
  location = "ASIA-NORTHEAST1"
}

output "bucket_url" {
  value = "gs://${google_storage_bucket.bucket.name}"
}