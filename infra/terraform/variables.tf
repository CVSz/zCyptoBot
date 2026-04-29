variable "vsphere_user" {
  description = "vSphere username"
  type        = string
}

variable "vsphere_password" {
  description = "vSphere password"
  type        = string
  sensitive   = true
}

variable "vsphere_server" {
  description = "vSphere server address"
  type        = string
}

variable "allow_unverified_ssl" {
  description = "Allow self-signed vSphere certificates"
  type        = bool
  default     = true
}

variable "datacenter" {
  type = string
}

variable "cluster" {
  type = string
}

variable "datastore" {
  type = string
}

variable "network" {
  type = string
}

variable "template_name" {
  description = "Existing Ubuntu template"
  type        = string
}

variable "vm_count" {
  type    = number
  default = 3
}
