// bucket
bucket_config = {
  bucket       = "flight-app-bucket"
  prefix       = "state"
  credentials  = "C:\\Users\\Alon\\PycharmProjects\\project1\\venv\\flight-app\\key.json"
}

// gcp
key_path = "C:\\Users\\Alon\\PycharmProjects\\project1\\venv\\flight-app\\key.json"
gcp_project = "devops-project-387209"

// k8s cluster
cluster_name = "flight-app-cluster"

cluster_location_config = {
  regional          = false
  regional_location = "us-central1"
  nodes_location    = ["us-central1-b"]
  zonal_location    = "us-central1-a"
}



cluster_autoscaler = {
  enabled = true
  max_cpu = 16
  min_cpu = 1
  max_mem = 20
  min_mem = 1

}


// k8s node pool
node_pool_name = "flight-app-node-pool"

autosacling_max_node_count = {
  max_count = 5
  min_count = 0
}

auto_repair  = true
auto_upgrade = true

max_surge       = 1
max_unavailable = 1

node_config = {
  disk_type    = "pd-standard"
  disk_size_gb = 100
  image_type   = "cos_containerd"
  machine_type = "e2-medium"
}


// cloud dns

domain_name       = "flight-app-zone"
domain_host       = "devopsheros.com."
domain_address    = "35.52.108.109"
subdomain_host    = "flight-app.devopsheros.com."
cname_domain      = "www.devopsheros.com."
cname_subdomain   = "www.flight-app.devopsheros.com."

// static ip
static_ip_name = "k8s-lb"