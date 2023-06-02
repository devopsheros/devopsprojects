terraform {
  backend "gcs" {
    bucket = var.bucket_config["bucket"]
    prefix = var.bucket_config["prefix"]
    credentials = file(var.bucket_config["credentials"])
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.66.0"
    }
  }
}

provider "google" {
  credentials = file(var.key_path)
  project     = var.gcp_project
}