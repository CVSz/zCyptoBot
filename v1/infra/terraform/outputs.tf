output "node_names" {
  value = [for vm in vsphere_virtual_machine.nodes : vm.name]
}

output "node_ips" {
  value = [for vm in vsphere_virtual_machine.nodes : vm.default_ip_address]
}
