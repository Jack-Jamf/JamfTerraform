resource "jamfpro_macos_configuration_profile_plist" "macos_dlp_restrictions" {
  name                = "Macos DLP Restrictions"
  description         = "Turning off iCloud Keychain, iCloud Drive, Local Device Wipe, Airdrop"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/macos_dlp_restrictions.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "fv2" {
  name                = "FV2"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/fv2.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_entraid_233" {
  name                = "Jamf Connect EntraID 2.33"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_entraid_2.33.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "restrict_apple_ids" {
  name                = "Restrict Apple ID's"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/restrict_apple_id_s.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "wipe" {
  name                = "Wipe"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/wipe.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "onedrive_settings" {
  name                = "OneDrive Settings"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/onedrive_settings.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "san_fransisco_pro_" {
  name                = "San Fransisco Pro "
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/san_fransisco_pro.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_preconfigured_trial_settings___okta" {
  name                = "Jamf Connect Preconfigured Trial Settings - Okta"
  description         = "The Jamf Connect preconfigured trial leverages Jamf curated IDP's to demonstrate Jamf Connects local account management and login window authentication works. The IDP credentials are not publicly available. Please reach out to your Jamf Sales team to obtain the current administrator and standard account credentials."
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_preconfigured_trial_settings_-_okta.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_preconfigured_trial_settings___entra_id" {
  name                = "Jamf Connect Preconfigured Trial Settings - Entra ID"
  description         = "The Jamf Connect preconfigured trial leverages Jamf curated IDP's to demonstrate Jamf Connects local account management and login window authentication works. The IDP credentials are not publicly available. Please reach out to your Jamf Sales team to obtain the current administrator and standard account credentials."
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_preconfigured_trial_settings_-_entra_id.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamfcheck___managed_login_item" {
  name                = "JamfCheck - Managed Login Item"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/jamfcheck_-_managed_login_item.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_setup_manager_json" {
  name                = "Jamf Setup Manager JSON"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/jamf_setup_manager_json.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "block_all_usb_plan___jamf_protect_configuration" {
  name                = "Block All USB Plan - Jamf Protect Configuration"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/block_all_usb_plan_-_jamf_protect_configuration.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "read_only_usb_plan___jamf_protect_configuration" {
  name                = "Read Only USB Plan - Jamf Protect Configuration"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/read_only_usb_plan_-_jamf_protect_configuration.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "filevault_2_enforcement" {
  name                = "Filevault 2 Enforcement"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/filevault_2_enforcement.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "filevault_2_enforcement" {
  name                = "Filevault 2 Enforcement"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/filevault_2_enforcement.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "windows_defender_standard_permissions" {
  name                = "Windows Defender Standard Permissions"
  description         = "Source: https://learn.microsoft.com/en-us/defender-endpoint/mac-install-with-jamf\nOnboarding plist and Defender endpoint settings still required: https://learn.microsoft.com/en-us/defender-endpoint/mac-jamfpro-policies#step-1-get-the-microsoft-defender-for-endpoint-onboarding-package"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/windows_defender_standard_permissions.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "defender_auto_update" {
  name                = "Defender Auto Update"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/defender_auto_update.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "apple_intelligence_disable_writing_tools" {
  name                = "Apple Intelligence Disable Writing Tools"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/apple_intelligence_disable_writing_tools.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_preconfigured_trial___onelogin" {
  name                = "Jamf Connect Preconfigured Trial - OneLogin"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_preconfigured_trial_-_onelogin.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "video_reactions_management" {
  name                = "Video Reactions Management"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/video_reactions_management.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sadsadasd" {
  name                = "sadsadasd"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/sadsadasd.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cisco_umbrella_pppc_profile" {
  name                = "Cisco Umbrella PPPC Profile"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  payloads            = file("${path.module}/support_files/profiles/cisco_umbrella_pppc_profile.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "anyconnect_pppc_system_extension_and_content_filter" {
  name                = "AnyConnect PPPC, System Extension, and Content Filter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.anyconnect.id
  payloads            = file("${path.module}/support_files/profiles/anyconnect_pppc_system_extension_and_content_filter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "terminal_pppc" {
  name                = "Terminal PPPC"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.automation.id
  payloads            = file("${path.module}/support_files/profiles/terminal_pppc.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplemcx" {
  name                = "CIS Level 2 - Ventura com.apple.MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplesafari" {
  name                = "CIS Level 2 - Ventura com.apple.Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplesiri" {
  name                = "CIS Level 2 - Ventura com.apple.Siri"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.siri.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplesoftwareupdate" {
  name                = "CIS Level 2 - Ventura com.apple.SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplesubmitdiaginfo" {
  name                = "CIS Level 2 - Ventura com.apple.SubmitDiagInfo"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.submitdiaginfo.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comappleterminal" {
  name                = "CIS Level 2 - Ventura com.apple.Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comappletimemachine" {
  name                = "CIS Level 2 - Ventura com.apple.TimeMachine"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.timemachine.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comappleapplicationaccess" {
  name                = "CIS Level 2 - Ventura com.apple.applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplecontrolcenter" {
  name                = "CIS Level 2 - Ventura com.apple.controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comappleloginwindow" {
  name                = "CIS Level 2 - Ventura com.apple.loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplemdnsresponder" {
  name                = "CIS Level 2 - Ventura com.apple.mDNSResponder"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.mdnsresponder.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplemobiledevicepasswordpolicy" {
  name                = "CIS Level 2 - Ventura com.apple.mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplepreferencessharingsharingprefsextension" {
  name                = "CIS Level 2 - Ventura com.apple.preferences.sharing.SharingPrefsExtension"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.preferences.sharing.sharingprefsextension.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplescreensaver" {
  name                = "CIS Level 2 - Ventura com.apple.screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplesecurityfirewall" {
  name                = "CIS Level 2 - Ventura com.apple.security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comapplesystempolicycontrol" {
  name                = "CIS Level 2 - Ventura com.apple.systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___ventura_comappletimed" {
  name                = "CIS Level 2 - Ventura com.apple.timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_ventura_com.apple.timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplemcx" {
  name                = "CIS Level 2 - Sonoma com.apple.MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplesafari" {
  name                = "CIS Level 2 - Sonoma com.apple.Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplesiri" {
  name                = "CIS Level 2 - Sonoma com.apple.Siri"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.siri.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplesoftwareupdate" {
  name                = "CIS Level 2 - Sonoma com.apple.SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplesubmitdiaginfo" {
  name                = "CIS Level 2 - Sonoma com.apple.SubmitDiagInfo"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.submitdiaginfo.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comappleterminal" {
  name                = "CIS Level 2 - Sonoma com.apple.Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comappletimemachine" {
  name                = "CIS Level 2 - Sonoma com.apple.TimeMachine"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.timemachine.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comappleapplicationaccess" {
  name                = "CIS Level 2 - Sonoma com.apple.applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comappleassistantsupport" {
  name                = "CIS Level 2 - Sonoma com.apple.assistant.support"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.assistant.support.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplecontrolcenter" {
  name                = "CIS Level 2 - Sonoma com.apple.controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comappleloginwindow" {
  name                = "CIS Level 2 - Sonoma com.apple.loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplemdnsresponder" {
  name                = "CIS Level 2 - Sonoma com.apple.mDNSResponder"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.mdnsresponder.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplemobiledevicepasswordpolicy" {
  name                = "CIS Level 2 - Sonoma com.apple.mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplepreferencessharingsharingprefsextension" {
  name                = "CIS Level 2 - Sonoma com.apple.preferences.sharing.SharingPrefsExtension"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.preferences.sharing.sharingprefsextension.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplescreensaver" {
  name                = "CIS Level 2 - Sonoma com.apple.screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplesecurityfirewall" {
  name                = "CIS Level 2 - Sonoma com.apple.security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comapplesystempolicycontrol" {
  name                = "CIS Level 2 - Sonoma com.apple.systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sonoma_comappletimed" {
  name                = "CIS Level 2 - Sonoma com.apple.timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sonoma_com.apple.timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappleaccessibility" {
  name                = "CIS Level 2 - Sequoia com.apple.Accessibility"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.accessibility.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplemcx" {
  name                = "CIS Level 2 - Sequoia com.apple.MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplesafari" {
  name                = "CIS Level 2 - Sequoia com.apple.Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplesoftwareupdate" {
  name                = "CIS Level 2 - Sequoia com.apple.SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplesubmitdiaginfo" {
  name                = "CIS Level 2 - Sequoia com.apple.SubmitDiagInfo"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.submitdiaginfo.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappleterminal" {
  name                = "CIS Level 2 - Sequoia com.apple.Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappletimemachine" {
  name                = "CIS Level 2 - Sequoia com.apple.TimeMachine"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.timemachine.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappleapplicationaccess" {
  name                = "CIS Level 2 - Sequoia com.apple.applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappleassistantsupport" {
  name                = "CIS Level 2 - Sequoia com.apple.assistant.support"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.assistant.support.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplecontrolcenter" {
  name                = "CIS Level 2 - Sequoia com.apple.controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappleloginwindow" {
  name                = "CIS Level 2 - Sequoia com.apple.loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplemdnsresponder" {
  name                = "CIS Level 2 - Sequoia com.apple.mDNSResponder"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.mdnsresponder.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplemobiledevicepasswordpolicy" {
  name                = "CIS Level 2 - Sequoia com.apple.mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplescreensaver" {
  name                = "CIS Level 2 - Sequoia com.apple.screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplesecurityfirewall" {
  name                = "CIS Level 2 - Sequoia com.apple.security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comapplesystempolicycontrol" {
  name                = "CIS Level 2 - Sequoia com.apple.systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "cis_level_2___sequoia_comappletimed" {
  name                = "CIS Level 2 - Sequoia com.apple.timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.cis_level_2.id
  payloads            = file("${path.module}/support_files/profiles/cis_level_2_-_sequoia_com.apple.timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_screensaver" {
  name                = "Monterey_cis_lvl1-screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_softwareupdate" {
  name                = "Monterey_cis_lvl1-SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_timed" {
  name                = "Monterey_cis_lvl1-timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_safari" {
  name                = "Monterey_cis_lvl1-Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_loginwindow" {
  name                = "Monterey_cis_lvl1-loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_controlcenter" {
  name                = "Monterey_cis_lvl1-controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_terminal" {
  name                = "Monterey_cis_lvl1-Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_mcx" {
  name                = "Monterey_cis_lvl1-MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_applicationaccess" {
  name                = "Monterey_cis_lvl1-applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_mobiledevicepasswordpolicy" {
  name                = "Monterey_cis_lvl1-mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_securityfirewall" {
  name                = "Monterey_cis_lvl1-security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "monterey_cis_lvl1_systempolicycontrol" {
  name                = "Monterey_cis_lvl1-systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_monterey_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/monterey_cis_lvl1-systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_screensaver" {
  name                = "Ventura_cis_lvl1-screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_softwareupdate" {
  name                = "Ventura_cis_lvl1-SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_timed" {
  name                = "Ventura_cis_lvl1-timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_safari" {
  name                = "Ventura_cis_lvl1-Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_loginwindow" {
  name                = "Ventura_cis_lvl1-loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_controlcenter" {
  name                = "Ventura_cis_lvl1-controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_terminal" {
  name                = "Ventura_cis_lvl1-Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_mcx" {
  name                = "Ventura_cis_lvl1-MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_applicationaccess" {
  name                = "Ventura_cis_lvl1-applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_mobiledevicepasswordpolicy" {
  name                = "Ventura_cis_lvl1-mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_securityfirewall" {
  name                = "Ventura_cis_lvl1-security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "ventura_cis_lvl1_systempolicycontrol" {
  name                = "Ventura_cis_lvl1-systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.compliance_editor_ventura_cis_level_1.id
  payloads            = file("${path.module}/support_files/profiles/ventura_cis_lvl1-systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "crowdstrike_settings" {
  name                = "CrowdStrike Settings"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.crowdstrike.id
  payloads            = file("${path.module}/support_files/profiles/crowdstrike_settings.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "google_chrome_base_plist" {
  name                = "Google Chrome Base Plist"
  description         = "plist key reference: https://chromeenterprise.google/policies/"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.google_enterprise.id
  payloads            = file("${path.module}/support_files/profiles/google_chrome_base_plist.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_login_okta_classic" {
  name                = "Jamf Connect Login: Okta Classic"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.jamf_connect.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_login_okta_classic.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_menu_bar_and_agent_settings_okta_classic" {
  name                = "Jamf Connect Menu Bar and Agent Settings: Okta Classic"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.jamf_connect.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_menu_bar_and_agent_settings_okta_classic.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_login_azure_ad" {
  name                = "Jamf Connect Login: Azure AD"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.jamf_connect.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_login_azure_ad.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_menu_bar_and_settings_azure_ad" {
  name                = "Jamf Connect Menu Bar and Settings: Azure AD"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.jamf_connect.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_menu_bar_and_settings_azure_ad.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_trust" {
  name                = "Jamf Trust"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.jamf_protect.id
  payloads            = file("${path.module}/support_files/profiles/jamf_trust.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = true
  }
}

resource "jamfpro_macos_configuration_profile_plist" "microsoft_edge_base_plist" {
  name                = "Microsoft Edge Base Plist"
  description         = "Source: https://learn.microsoft.com/en-us/deployedge/configure-microsoft-edge-on-mac"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.microsoft_o365.id
  payloads            = file("${path.module}/support_files/profiles/microsoft_edge_base_plist.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "microsoft_edge_autoupdater" {
  name                = "Microsoft Edge AutoUpdater"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.microsoft_o365.id
  payloads            = file("${path.module}/support_files/profiles/microsoft_edge_autoupdater.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "support_app_json_configuration" {
  name                = "Support App JSON Configuration"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.research_phase.id
  payloads            = file("${path.module}/support_files/profiles/support_app_json_configuration.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "filevault_2_encryption_policy" {
  name                = "FileVault 2 Encryption Policy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.security.id
  payloads            = file("${path.module}/support_files/profiles/filevault_2_encryption_policy.mobileconfig")

  scope {
    all_computers = true
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sentinelone_settings" {
  name                = "SentinelOne Settings"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sentinelone.id
  payloads            = file("${path.module}/support_files/profiles/sentinelone_settings.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_screensaver" {
  name                = "Sequoia_cis_lvl1-screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_accessibility" {
  name                = "Sequoia_cis_lvl1-Accessibility"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-accessibility.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_softwareupdate" {
  name                = "Sequoia_cis_lvl1-SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_timed" {
  name                = "Sequoia_cis_lvl1-timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_safari" {
  name                = "Sequoia_cis_lvl1-Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_assistantsupport" {
  name                = "Sequoia_cis_lvl1-assistant.support"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-assistant.support.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_siri" {
  name                = "Sequoia_cis_lvl1-Siri"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-siri.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_loginwindow" {
  name                = "Sequoia_cis_lvl1-loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_controlcenter" {
  name                = "Sequoia_cis_lvl1-controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_terminal" {
  name                = "Sequoia_cis_lvl1-Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_mcx" {
  name                = "Sequoia_cis_lvl1-MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_applicationaccess" {
  name                = "Sequoia_cis_lvl1-applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_mobiledevicepasswordpolicy" {
  name                = "Sequoia_cis_lvl1-mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_securityfirewall" {
  name                = "Sequoia_cis_lvl1-security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_submitdiaginfo" {
  name                = "Sequoia_cis_lvl1-SubmitDiagInfo"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-submitdiaginfo.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sequoia_cis_lvl1_systempolicycontrol" {
  name                = "Sequoia_cis_lvl1-systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sequoia_cis_lvl1.id
  payloads            = file("${path.module}/support_files/profiles/sequoia_cis_lvl1-systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "disable_auto_logout" {
  name                = "Disable Auto Logout"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/disable_auto_logout.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_screensaver" {
  name                = "Sonoma_800-171-screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_timed" {
  name                = "Sonoma_800-171-timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_mcxbluetooth" {
  name                = "Sonoma_800-171-MCXBluetooth"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-mcxbluetooth.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_systempreferences" {
  name                = "Sonoma_800-171-systempreferences"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-systempreferences.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_dock" {
  name                = "Sonoma_800-171-dock"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-dock.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_icloudmanaged" {
  name                = "Sonoma_800-171-icloud.managed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-icloud.managed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_assistantsupport" {
  name                = "Sonoma_800-171-assistant.support"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-assistant.support.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_mdnsresponder" {
  name                = "Sonoma_800-171-mDNSResponder"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-mdnsresponder.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_security" {
  name                = "Sonoma_800-171-security"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-security.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_loginwindow" {
  name                = "Sonoma_800-171-loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_preferencessharingsharingprefsextension" {
  name                = "Sonoma_800-171-preferences.sharing.SharingPrefsExtension"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-preferences.sharing.sharingprefsextension.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_setupassistantmanaged" {
  name                = "Sonoma_800-171-SetupAssistant.managed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-setupassistant.managed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_mcx" {
  name                = "Sonoma_800-171-MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_driverappleircontroller" {
  name                = "Sonoma_800-171-driver.AppleIRController"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-driver.appleircontroller.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_applicationaccess" {
  name                = "Sonoma_800-171-applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_mobiledevicepasswordpolicy" {
  name                = "Sonoma_800-171-mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_securityfirewall" {
  name                = "Sonoma_800-171-security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_securitysmartcard" {
  name                = "Sonoma_800-171-security.smartcard"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-security.smartcard.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_submitdiaginfo" {
  name                = "Sonoma_800-171-SubmitDiagInfo"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-submitdiaginfo.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_systempolicycontrol" {
  name                = "Sonoma_800-171-systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_800_171_systempolicymanaged" {
  name                = "Sonoma_800-171-systempolicy.managed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_800_171.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_800-171-systempolicy.managed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_screensaver" {
  name                = "Sonoma_Jackboarder-screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_softwareupdate" {
  name                = "Sonoma_Jackboarder-SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_timed" {
  name                = "Sonoma_Jackboarder-timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_safari" {
  name                = "Sonoma_Jackboarder-Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_loginwindow" {
  name                = "Sonoma_Jackboarder-loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_controlcenter" {
  name                = "Sonoma_Jackboarder-controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_terminal" {
  name                = "Sonoma_Jackboarder-Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_mcx" {
  name                = "Sonoma_Jackboarder-MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_applicationaccess" {
  name                = "Sonoma_Jackboarder-applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_mobiledevicepasswordpolicy" {
  name                = "Sonoma_Jackboarder-mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_securityfirewall" {
  name                = "Sonoma_Jackboarder-security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_jackboarder_systempolicycontrol" {
  name                = "Sonoma_Jackboarder-systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_jackboarder.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_jackboarder-systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_screensaver" {
  name                = "Sonoma_KTT-screensaver"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-screensaver.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_softwareupdate" {
  name                = "Sonoma_KTT-SoftwareUpdate"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-softwareupdate.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_timed" {
  name                = "Sonoma_KTT-timed"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-timed.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_safari" {
  name                = "Sonoma_KTT-Safari"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-safari.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_loginwindow" {
  name                = "Sonoma_KTT-loginwindow"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-loginwindow.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_controlcenter" {
  name                = "Sonoma_KTT-controlcenter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-controlcenter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_terminal" {
  name                = "Sonoma_KTT-Terminal"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-terminal.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_mcx" {
  name                = "Sonoma_KTT-MCX"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-mcx.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_applicationaccess" {
  name                = "Sonoma_KTT-applicationaccess"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-applicationaccess.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_mobiledevicepasswordpolicy" {
  name                = "Sonoma_KTT-mobiledevice.passwordpolicy"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-mobiledevice.passwordpolicy.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_securityfirewall" {
  name                = "Sonoma_KTT-security.firewall"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-security.firewall.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sonoma_ktt_systempolicycontrol" {
  name                = "Sonoma_KTT-systempolicy.control"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sonoma_ktt.id
  payloads            = file("${path.module}/support_files/profiles/sonoma_ktt-systempolicy.control.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "sophos_pppc" {
  name                = "Sophos PPPC"
  description         = "https://community.sophos.com/intercept-x-endpoint/f/recommended-reads/116397/sophos-mac-endpoint-how-to-configure-jamf-privacy-preferences-for-10-15-compatibility#mcetoc_1enrp05174"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.sophos_endpoint.id
  payloads            = file("${path.module}/support_files/profiles/sophos_pppc.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "mdatp_mdav_configuration_settings" {
  name                = "MDATP MDAV Configuration Settings"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.windows_defender.id
  payloads            = file("${path.module}/support_files/profiles/mdatp_mdav_configuration_settings.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "mdatp_mdav_auto_update_settings" {
  name                = "MDATP MDAV Auto Update Settings"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.windows_defender.id
  payloads            = file("${path.module}/support_files/profiles/mdatp_mdav_auto_update_settings.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "mdatp_mdav___full_disk_system_extension_and_content_filter" {
  name                = "MDATP MDAV - Full Disk, System Extension and Content Filter"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.windows_defender.id
  payloads            = file("${path.module}/support_files/profiles/mdatp_mdav_-_full_disk_system_extension_and_content_filter.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_login_enrollment_only" {
  name                = "Jamf Connect Login: Enrollment Only"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.zero_touch.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_login_enrollment_only.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect_login__zero_touch__okta" {
  name                = "Jamf Connect Login | Zero Touch | Okta"
  description         = "Exported from Jamf Pro"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.zero_touch.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_login_zero_touch_okta.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}

resource "jamfpro_macos_configuration_profile_plist" "jamf_connect__zero_touch__okta" {
  name                = "Jamf Connect | Zero Touch | Okta"
  description         = "Jamf Connect Settings"
  distribution_method = "Install Automatically"
  level               = "System"
  redeploy_on_update  = "Newly Assigned"
  user_removable      = false
  category_id         = jamfpro_category.zero_touch.id
  payloads            = file("${path.module}/support_files/profiles/jamf_connect_zero_touch_okta.mobileconfig")

  scope {
    all_computers = false
    all_jss_users = false
  }
}