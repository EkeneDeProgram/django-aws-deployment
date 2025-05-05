output "kubeconfig" {
  value = aws_eks_cluster.eks_cluster.kubeconfig[0].value
}
