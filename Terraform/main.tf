
# # Set up the EKS module
module "eks" {
  source = "./modules/eks"
  region = var.region


  # depends_on = [module.vpc]
}



# # Set up the IAM OIDC module
# module "iam" {
#   source               = "../modules/iam-oidc"
#   eks_oidc_issuer_url = module.eks.eks_oidc_issuer_url
# }
