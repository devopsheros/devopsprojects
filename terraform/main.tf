// k8s cluster
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.cluster_location_config["regional"] == true ? var.cluster_location_config["regional_location"] : var.cluster_location_config["zonal_location"]
  node_locations = var.cluster_location_config["nodes_location"]

  remove_default_node_pool = true
  initial_node_count       = 1

  maintenance_policy {
    recurring_window {
      end_time = timeadd(timestamp(), "25h" )
      recurrence = "FREQ=WEEKLY;BYDAY=MO"
      start_time = timeadd(timestamp(),"1h" )
    }
  }
  cluster_autoscaling {
    enabled = var.cluster_autoscaler["enabled"]
    resource_limits {
      resource_type = "cpu"
      maximum = var.cluster_autoscaler["max_cpu"]
      minimum = var.cluster_autoscaler["min_cpu"]
    }
    resource_limits {
      resource_type = "memory"
      maximum = var.cluster_autoscaler["max_mem"]
      minimum = var.cluster_autoscaler["min_mem"]
    }
  }
}

// k8s node pool
resource "google_container_node_pool" "node_pool" {
  name       = var.node_pool_name
  cluster    = google_container_cluster.primary.name
  location   = var.cluster_location_config["zonal_location"]

  autoscaling {
    max_node_count = var.cluster_autoscaler["enabled"] == true ? var.autosacling_max_node_count["max_count"] : null
    min_node_count = var.cluster_autoscaler["enabled"] == true ? var.autosacling_max_node_count["min_count"] : null
  }

  management {
    auto_repair  = var.auto_repair
    auto_upgrade = var.auto_upgrade
  }

  upgrade_settings {
    max_surge = var.max_surge
    max_unavailable = var.max_unavailable
  }

  node_config {
    machine_type = var.node_config["machine_type"]
    image_type = var.node_config["image_type"]
    disk_size_gb = var.node_config["disk_size_gb"]
    disk_type = var.node_config["disk_type"]
  }
}

// static ip address
resource "google_compute_address" "static-ip" {
  name          = var.static_ip_name
  address_type  = "EXTERNAL"
  region        = "us-central1"
}

// cloud dns

resource "google_dns_managed_zone" "my_dns_zone" {
  name        = var.domain_name
  description = "Flight App DNS Zone"
  dns_name    = var.domain_host
}

resource "google_dns_record_set" "a_record_domain" {
  name    = var.domain_host
  type    = "A"
  ttl     = 300
  managed_zone = google_dns_managed_zone.my_dns_zone.name
  rrdatas = [
    var.domain_address
  ]
}

resource "google_dns_record_set" "a_record_subdomain" {
  name    = var.subdomain_host
  type    = "A"
  ttl     = 300
  managed_zone = google_dns_managed_zone.my_dns_zone.name
  rrdatas = [
    google_compute_address.static-ip.address
  ]
}

resource "google_dns_record_set" "cname_record_domain" {
  name    = var.cname_domain
  type    = "CNAME"
  ttl     = 300
  managed_zone = google_dns_managed_zone.my_dns_zone.name
  rrdatas = [
    var.domain_host
  ]
}

resource "google_dns_record_set" "cname_record_2" {
  name    = var.cname_subdomain
  type    = "CNAME"
  ttl     = 300
  managed_zone = google_dns_managed_zone.my_dns_zone.name
  rrdatas = [
    var.subdomain_host
  ]
}

