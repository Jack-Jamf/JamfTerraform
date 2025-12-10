# Jamf App Catalog: Microsoft Edge
resource "jamfpro_app_installer" "microsoft_edge" {
  name            = "Microsoft Edge"
  enabled         = true
  deployment_type = "SELF_SERVICE"
  update_behavior = "AUTOMATIC"
  category_id     = "-1"
  site_id         = "-1"
  smart_group_id  = "1"  # All Managed Clients
}

# Jamf App Catalog: Jamf Connect
resource "jamfpro_app_installer" "jamf_connect" {
  name            = "Jamf Connect"
  enabled         = true
  deployment_type = "SELF_SERVICE"
  update_behavior = "AUTOMATIC"
  category_id     = "-1"
  site_id         = "-1"
  smart_group_id  = "1"  # All Managed Clients
}

# Jamf App Catalog: Microsoft Intune Company Portal
resource "jamfpro_app_installer" "microsoft_intune_company_portal" {
  name            = "Microsoft Intune Company Portal"
  enabled         = true
  deployment_type = "SELF_SERVICE"
  update_behavior = "AUTOMATIC"
  category_id     = "-1"
  site_id         = "-1"
  smart_group_id  = "1"  # All Managed Clients
}