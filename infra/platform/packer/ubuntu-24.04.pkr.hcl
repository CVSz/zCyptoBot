packer {
  required_version = ">= 1.10.0"
}

variable "image_name" {
  type    = string
  default = "zeaz-ubuntu-2404-golden"
}

source "null" "ubuntu_2404_contract" {
  communicator = "none"
}

build {
  name    = var.image_name
  sources = ["source.null.ubuntu_2404_contract"]

  provisioner "shell-local" {
    inline = [
      "echo Golden image contract: Ubuntu 24.04, containerd, Docker, auditd, chrony, apparmor, kubectl, helm, argocd",
      "echo Use scripts/zeaz-os-bootstrap.sh --apply inside provider-specific builders."
    ]
  }
}
