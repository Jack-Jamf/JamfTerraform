terraform {
  required_providers {
    jamfpro = {
      source  = "deploymenttheory/jamfpro"
      version = "~> 0.5.0"
    }
  }
}

provider "jamfpro" {
  jamfpro_instance_fqdn = "kickthetires.jamfcloud.com"
  # Authentication - configure via environment variables:
  # export JAMFPRO_BASIC_AUTH_USERNAME="your-username"
  # export JAMFPRO_BASIC_AUTH_PASSWORD="your-password"
  # Or use client credentials:
  # export JAMFPRO_CLIENT_ID="your-client-id"
  # export JAMFPRO_CLIENT_SECRET="your-client-secret"
}
