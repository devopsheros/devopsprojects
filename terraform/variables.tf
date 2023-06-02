// bucket config
variable "bucket_config" {
  type = object({
    bucket      = string
    prefix      = string
    credentials = string
  })
}

// gcp config
variable "key_path" {
  type = string
}

variable "gcp_project" {
  type = string
}



// k8s cluster
variable "cluster_name" {
  type = string
}

variable "cluster_location_config" {
  type = object({
    regional          = bool,
    regional_location = string,
    nodes_location    = list(string),
    zonal_location    = string
  })
}


variable "cluster_autoscaler" {
  type = object({
    enabled = bool,
    max_cpu = number,
    min_cpu = number,
    max_mem = number,
    min_mem = number
  })
}

//k8s node-pool
variable "node_pool_name" {
  type = string
}

variable "autosacling_max_node_count" {
  type = object({
    max_count = number,
    min_count = number
  })
}

variable "auto_repair" {
  type = bool
}

variable "auto_upgrade" {
  type = bool
}

variable "max_surge" {
  type = number
}

variable "max_unavailable" {
  type = number
}

variable "node_config" {
  type = object({
    machine_type = string,
    image_type   = string,
    disk_size_gb = number,
    disk_type    = string
  })
}

// cloud dns

variable "domain_name" {
  type = string
}

variable "domain_host" {
  type = string
}

variable "domain_address" {
  type = string
}

variable "subdomain_host" {
  type = string
}


variable "cname_domain" {
  type = string
}

variable "cname_subdomain" {
  type = string
}
variable "static_ip_name" {
  type = string
}