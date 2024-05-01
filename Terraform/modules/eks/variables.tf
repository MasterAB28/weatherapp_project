# variable "region" {
#   description = "Region to use in aws"
#   type        = string
#   # default     = var.region
# }

variable "region" {
  description = "Region to use in aws"
  type        = string
  default     = "eu-north-1" 
}

variable "iam_role_name" {
  description = "The name of the IAM role"
  type        = string
  default     = "aws-load-balancer-controller"
}

# variable "name" {
#   description = "module.eks.cluster_id"
#   type        = string
# }

# variable "availability_zone" {
#   description = "AZ to use in aws"
#   type        = string
#   default     = "il-central-1a" 
# }

variable "cluster_name" {
  description = "Cluster name"
  type        = string
  default     = "my-cluster" 
}



variable "kubernetes_argocd_namespace" {
  description = "argoCD namespace"
  type = string
  default = "argocd"
  
}

variable "route_53_zone_id" {
  description = "route 53 hosted zone for external dns"
  type = string
  default = "aviad.click"
}
