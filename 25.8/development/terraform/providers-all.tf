variable "base_url" {
  default = "https://eda-demo.test.io:9443"
}

variable "eda_client_secret" {
  default = "your_client_secret"
}

variable "eda_username" {
  default = "your_username"
}

variable "eda_password" {
  default = "your_password"
}

terraform {
  required_providers {
    interfaces-v1alpha1 = {
      source = "nokia-eda/interfaces-v1alpha1"
    }
    fabrics-v1alpha1 = {
      source = "nokia-eda/fabrics-v1alpha1"
    }
    # add more providers here
  }
}

provider "interfaces-v1alpha1" {
  base_url          = var.base_url
  eda_client_secret = var.eda_client_secret
  eda_username      = var.eda_username
  eda_password      = var.eda_password
}

provider "fabrics-v1alpha1" {
  base_url          = var.base_url
  eda_client_secret = var.eda_client_secret
  eda_username      = var.eda_username
  eda_password      = var.eda_password
}

# add more providers configs here if needed
