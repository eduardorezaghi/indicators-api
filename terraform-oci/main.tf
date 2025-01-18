provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# VCN
resource "oci_core_vcn" "app_vcn" {
  compartment_id = var.compartment_id
  cidr_block     = "10.0.0.0/16"
  display_name   = "${var.project_name}-vcn"
  freeform_tags = {
    "project-name" = "${var.project_name}"
  }
}


# Security List
resource "oci_core_security_list" "app_security_list" {
  compartment_id = var.compartment_id
  vcn_id        = oci_core_vcn.app_vcn.id
  display_name  = "${var.project_name}-security-list"

  ingress_security_rules {
    protocol = "6" # TCP
    source   = "${var.home_address}"
    description = "Allow access to port 80 from my home address"
    
    tcp_options {
      min = 80
      max = 80
    }
  }

  ingress_security_rules {
    protocol = "6"
    source_type = "CIDR_BLOCK"
    source   = "${var.home_address}"
    description = "Allow access to port 7012 from my home address"
    
    tcp_options {
      min = 7012
      max = 7012
    }
  }

  egress_security_rules {
      protocol = "6"
      destination_type = "CIDR_BLOCK"
      destination = "0.0.0.0/0"
      description = "Access to the internet"
      tcp_options {
          min = 80
          max = 80
      }
  }

  egress_security_rules {
    protocol = "17" # UDP
    destination = "0.0.0.0/0"
    description = "DNS over UDP"
    udp_options {
        min = 53
        max = 53
    }
  }

  egress_security_rules {
    protocol         = 6
    destination_type = "CIDR_BLOCK"
    destination      = "0.0.0.0/0"
    description      = "access to container registries via HTTPS"
    tcp_options {
      min = 443
      max = 443
    }
  }
}


# Subnet
resource "oci_core_subnet" "app_subnet" {
  compartment_id    = var.compartment_id
  vcn_id           = oci_core_vcn.app_vcn.id
  cidr_block       = "10.0.1.0/24"
  display_name     = "${var.project_name}-subnet"
  security_list_ids = [
    oci_core_security_list.app_security_list.id
  ]
  prohibit_public_ip_on_vnic = false
  route_table_id    = oci_core_route_table.app_rt.id

  freeform_tags = {
    "project-name" = "${var.project_name}"
  }
}

# Internet Gateway & Route Table
resource "oci_core_internet_gateway" "app_ig" {
  compartment_id = var.compartment_id
  vcn_id        = oci_core_vcn.app_vcn.id
  display_name  = "${var.project_name}-ig"
  enabled       = true
  freeform_tags = {
    "project-name" = "${var.project_name}"
  }
}

resource "oci_core_route_table" "app_rt" {
  compartment_id = var.compartment_id
  vcn_id        = oci_core_vcn.app_vcn.id
  display_name  = "${var.project_name}-rt"

  route_rules {
    network_entity_id = oci_core_internet_gateway.app_ig.id
    destination     = "0.0.0.0/0"
  }
  freeform_tags = {
    "project-name" = "${var.project_name}"
  }
}

# Get a list of Availability Domains
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

output "show-ads" {
  value = data.oci_identity_availability_domains.ads.availability_domains
}

# ------------------------------------------------------------------------------------------------ database instances

# Database
resource "oci_database_autonomous_database" "postgresql" {
  compartment_id           = var.compartment_id
  db_name                 = "PostgreSQL"
  admin_password         = var.db_password
  display_name           = "${var.project_name}-autonomous-database"
  license_model          = "LICENSE_INCLUDED"
  is_free_tier           = true
}

output "postgresql_connection" {
  value = {
    username          = "ADMIN"
    password          = var.db_password
  }
  sensitive = true
}



# ------------------------------------------------------------------------------------------------ containers instances

# Redis container
# resource "oci_container_instances_container_instance" "app_redis" {
#   compartment_id = var.compartment_id
#   availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
#   display_name  = "${var.project_name}-redis"
#   vnics {
#     subnet_id = oci_core_subnet.app_subnet.id
#   }

#   containers {
#     image_url = "redis:latest"
#   }

#   shape = "CI.Standard.E4.Flex"
#   shape_config {
#     memory_in_gbs = 1
#     ocpus = 1
#   }
# }




# Flask API container
# resource "oci_container_instances_container_instance" "app_container" {
#   availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
#   compartment_id = var.compartment_id
#   display_name  = "${var.project_name}-container-instance"
#   container_restart_policy = "ALWAYS"
#   shape = "CI.Standard.E4.Flex"
#   shape_config {
#     memory_in_gbs = 1
#     ocpus = 1
#   }


#   vnics {
#     subnet_id = oci_core_subnet.app_subnet.id
#     display_name = "${var.project_name}-container-instance"
#     is_public_ip_assigned = true
#     nsg_ids = []
#   }

# #   image_pull_secrets {
# #     registry_endpoint = ${var.registry}
# #   }

#   containers {
#     image_url = "${var.registry}/${var.namespace}/${var.containers_name}-web:latest"
#     display_name = "${var.project_name} Flask API container"

#     environment_variables = {
#       "FLASK_APP" = "src.app"
#       "FLASK_ENV" = "production"
#       "SQLALCHEMY_DATABASE_URI" = "$"
#     #   "CELERY_BROKER_URL" = "redis://${oci_redis_instance.app_redis.host}:6379/0"
#     #   "CELERY_RESULT_BACKEND" = "redis://${oci_redis_instance.app_redis.host}:6379/0"
#     }
#   }

# }
