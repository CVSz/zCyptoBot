provider "google" {
  project = "zeaz"
  region  = "asia-southeast1"
}

resource "google_container_cluster" "gke" {
  name               = "zeaz-gke"
  location           = "asia-southeast1"
  initial_node_count = 3
}
