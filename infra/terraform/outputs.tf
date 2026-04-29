output "k8s_node_names" {
  value = vsphere_virtual_machine.k8s_nodes[*].name
}
