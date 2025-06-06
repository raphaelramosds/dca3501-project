terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.39.0"
    }
  }
}

provider "google-beta" {
  project = var.project
  region  = var.region
  zone    = "us-central1-a"
}

data "google_iam_policy" "public_invoker" {
  binding {
    role    = "roles/run.invoker"
    members = ["allUsers"]
  }
}

resource "google_cloudbuild_trigger" "streamlit-app-build" {
  name            = "streamlit-app-build"
  project         = var.project
  location        = var.region
  service_account = "projects/${var.project}/serviceAccounts/cloud-build-service-account@sample-project-460722.iam.gserviceaccount.com"
  filename        = "streamlit/cloudbuild.yaml"

  github {
    owner = "raphaelramosds"
    # NOTE: You MUST connect this repo on GCP console at Cloud Build / Triggers / Connect repository
    name = "dca3501-project"
    push {
      branch = "main"
    }
  }

  approval_config {
    approval_required = true
  }

}

resource "google_cloud_run_service" "streamlit-app" {
  project  = var.project
  name     = "streamlit-app"
  location = var.region

  template {
    spec {
      containers {
        image = "us-central1-docker.pkg.dev/sample-project-460722/sample-project-repository/streamlit-app"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_policy" "public-access" {
  service     = google_cloud_run_service.streamlit-app.name
  location    = google_cloud_run_service.streamlit-app.location
  policy_data = data.google_iam_policy.public_invoker.policy_data
}

# Enable required APIs for this infrastructure
resource "google_project_service" "enable_services" {
  for_each = toset([
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  project = var.project
  service = each.key
}