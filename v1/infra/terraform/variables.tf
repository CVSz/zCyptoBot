variable "node_count" {
  type        = number
  default     = 3
  description = "Total VM count for compact profile."
}

variable "vm_name_prefix" {
  type    = string
  default = "zcypto"
}

variable "vm_cpu" {
  type    = number
  default = 4
}

variable "vm_memory_mb" {
  type    = number
  default = 8192
}

variable "vm_disk_gb" {
  type    = number
  default = 80
}

variable "vsphere_user" { type = string }
variable "vsphere_password" { type = string, sensitive = true }
variable "vsphere_server" { type = string }
variable "allow_unverified_ssl" { type = bool, default = true }

variable "datacenter" { type = string }
variable "cluster" { type = string }
variable "datastore" { type = string }
variable "network" { type = string }
variable "template" { type = string }
