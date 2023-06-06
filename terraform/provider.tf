terraform {
  backend "gcs" {
    bucket = "flight-app-bucket"
    prefix = "state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.66.0"
    }
  }
}

provider "google" {
  credentials = var.key_path
  //credentials = file(var.key_path)
  project     = var.gcp_project
}