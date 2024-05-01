data "aws_availability_zones" "available" {}

module "vpc" {
  source = "../vpc"
  region = var.region
}

module "eks" {
  # source  = "terraform-aws-modules/eks/aws"
  # version = "20.8.5"
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-eks.git?ref=afadb14e44d1cdbd852dbae815be377c4034e82a"

  cluster_name                   = var.cluster_name
  cluster_endpoint_public_access = true
  enable_cluster_creator_admin_permissions = true
  authentication_mode = "API_AND_CONFIG_MAP"

  subnet_ids = module.vpc.private_subnets
  vpc_id = module.vpc.vpc_id

  enable_irsa = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  eks_managed_node_groups = {
    my-cluster = {
      min_size     = 2
      max_size     = 2
      desired_size = 2

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      iam_role_additional_policies = {
        AmazonEBSCSIDriverPolicy = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
      }

      tags = {
        ExtraTag = "my-cluster"
      }
    }
  }

  tags = {
    Example    = var.cluster_name
    GithubRepo = "terraform-aws-eks"
    GithubOrg  = "terraform-aws-modules"
  }
  depends_on = [ module.vpc ]
}



# https://github.com/terraform-aws-modules/terraform-aws-eks/issues/2009
data "aws_eks_cluster" "default" {
  name = var.cluster_name

  depends_on = [module.eks]
}

provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.default.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.default.id]
      command     = "aws"
    }
  }
}



# provider "helm" {
#   kubernetes {
#     config_path = "~/.kube/config"
#   }
# }

module "aws_load_balancer_controller_irsa_role" {
  # source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  # version = "~> 5.0"
  source = "git::https://github.com/terraform-aws-modules/terraform-aws-iam.git//modules/iam-role-for-service-accounts-eks?ref=39e42e1f847afe5fd1c1c98c64871817e37e33ca"

  role_name = "aws-load-balancer-controller"

  attach_load_balancer_controller_policy = true

  oidc_providers = {
    ex = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["kube-system:aws-load-balancer-controller"]
    }
  }

  depends_on = [module.eks]
}


resource "helm_release" "aws_load_balancer_controller" {
  name = "aws-load-balancer-controller"

  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  namespace  = "kube-system"
  version    = "1.7.2"

  set {
    name  = "replicaCount"
    value = "2"  #default is 2
  }

  set {
    name  = "clusterName"
    value = var.cluster_name
  }

  set {
    name  = "serviceAccount.name"
    value = "aws-load-balancer-controller"
  }

  set {
    name  = "serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"
    value = module.aws_load_balancer_controller_irsa_role.iam_role_arn
  }

  depends_on = [module.eks, module.aws_load_balancer_controller_irsa_role]
}


resource "helm_release" "argocd" {
  depends_on = [ module.eks, module.eks-external-dns, module.aws_load_balancer_controller_irsa_role ]

  name       = "argocd"
  repository = "https://argoproj.github.io/argo-helm"
  chart      = "argo-cd"
  namespace = var.kubernetes_argocd_namespace
  create_namespace = true
  version    = "6.7.18"  # Replace with the desired version of ArgoCD
  timeout    = "1200"
  values     = [templatefile("modules/eks/argocd/values.yaml", {})]

  # You can add more `set` blocks to customize ArgoCD configuration
}

resource "aws_iam_policy" "external_dns_policy" {
  depends_on = [module.eks]
  name        = "external-dns-route53-policy"
  description = "Policy for ExternalDNS to manage Route 53 resources"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["route53:ChangeResourceRecordSets"]
        Resource = ["arn:aws:route53:::hostedzone/${var.route_53_zone_id}"]  # Replace var.route_53_zone_id with the actual hosted zone ID
      },
      {
        Effect   = "Allow"
        Action   = ["route53:ListHostedZones", "route53:ListResourceRecordSets"]
        Resource = ["arn:aws:route53:::hostedzone/${var.route_53_zone_id}"]  # Replace var.route_53_zone_id with the actual hosted zone ID
      }
    ]
  })
}


module "eks-external-dns" {
    # source  = "lablabs/eks-external-dns/aws"
    # version = "1.2.0"
    source = "git::https://github.com/lablabs/terraform-aws-eks-external-dns.git?ref=c3381f9ce801c4663656cadf605adade954f7fa7"
    helm_chart_version = "7.2.1"
    cluster_identity_oidc_issuer =  module.eks.cluster_oidc_issuer_url
    cluster_identity_oidc_issuer_arn = module.eks.oidc_provider_arn
    policy_allowed_zone_ids = [
        var.route_53_zone_id  # zone id of your hosted zone
    ]
    settings = {
    "policy" = "sync" # syncs DNS records with ingress and services currently on the cluster.
  }
  irsa_additional_policies = {
      external_dns_policy = aws_iam_policy.external_dns_policy.arn
  }
  depends_on = [module.eks, helm_release.aws_load_balancer_controller]
}

