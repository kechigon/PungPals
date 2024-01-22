resource "google_sql_database_instance" "instance" {
  name             = "postgres-instance"
  database_version = "POSTGRES_13"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name     = "postgres-database"
  instance = google_sql_database_instance.instance.name
}

resource "google_sql_user" "posgres-user" {
  name     = "postgres-user"
  instance = google_sql_database_instance.instance.name
  password = var.postgres_passwd
}