provider "google" {
  project = "gid-project"
  region  = "us-central1"
}

resource "google_container_cluster" "main" {
  name = "gid-gcp"
}
