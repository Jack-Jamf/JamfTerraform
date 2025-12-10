resource "jamfpro_computer_group_smart" "aftermath_trigger" {
  name = "Aftermath Trigger"
  criteria {
    name = "Aftermath Trigger"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "aftermath"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___sequoia" {
  name = "CIS Level 1 - Sequoia"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "greater than or equal"
    value = "15"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 2
    and_or = "and"
    search_type = "less than"
    value = "16"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___sonoma" {
  name = "CIS Level 1 - Sonoma"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "greater than or equal"
    value = "14"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 2
    and_or = "and"
    search_type = "less than"
    value = "15"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___ventura" {
  name = "CIS Level 1 - Ventura"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "greater than or equal"
    value = "13"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 2
    and_or = "and"
    search_type = "less than"
    value = "14"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___sequoia" {
  name = "CIS Level 2 - Sequoia"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "greater than or equal"
    value = "15"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 2
    and_or = "and"
    search_type = "less than"
    value = "16"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___sequoia_non_compliant" {
  name = "CIS Level 2 - Sequoia Non-compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "CIS Level 2 - Sequoia"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 2 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "matches regex"
    value = "(\b[a-z0-9_\-]+\n?\b)+"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___sonoma" {
  name = "CIS Level 2 - Sonoma"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "greater than or equal"
    value = "14"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 2
    and_or = "and"
    search_type = "less than"
    value = "15"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___sonoma_non_compliant" {
  name = "CIS Level 2 - Sonoma Non-compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "CIS Level 2 - Sonoma"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 2 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "matches regex"
    value = "(\b[a-z0-9_\-]+\n?\b)+"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___ventura" {
  name = "CIS Level 2 - Ventura"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "greater than or equal"
    value = "13"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 2
    and_or = "and"
    search_type = "less than"
    value = "14"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___ventura_non_compliant" {
  name = "CIS Level 2 - Ventura Non-compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "CIS Level 2 - Ventura"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 2 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "matches regex"
    value = "(\b[a-z0-9_\-]+\n?\b)+"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "crowdstrike_settings_profile_installed" {
  name = "CrowdStrike Settings Profile installed"
  criteria {
    name = "Profile Name"
    priority = 0
    and_or = "and"
    search_type = "has"
    value = "CrowdStrike Settings"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "eraseinstall_installer_cached" {
  name = "EraseInstall: Installer Cached"
  criteria {
    name = "EraseInstall: Installer Cached"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "True"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_static" "eraseinstall_reload_macos" {
  name = "EraseInstall: Reload MacOS"
}

resource "jamfpro_computer_group_smart" "filevault_2_key_reissue" {
  name = "FileVault 2 Key Reissue"
  criteria {
    name = "FileVault 2 Individual Key Validation"
    priority = 0
    and_or = "and"
    search_type = "is not"
    value = "Valid"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "FileVault 2 Partition Encryption State"
    priority = 1
    and_or = "and"
    search_type = "is"
    value = "Encrypted"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "protect___bundlore" {
  name = "Protect - Bundlore"
  criteria {
    name = "Jamf Protect - Smart Groups"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "protect-bundlore"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "nudge_incorrect_parameters" {
  name = "Nudge: Incorrect Parameters"
  criteria {
    name = "Nudge: Configuration Profile Update Parameters"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "No Updates Found"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Nudge: Next MacOS Update Available"
    priority = 1
    and_or = "and"
    search_type = "is not"
    value = "No Updates Found"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Nudge: Configuration Profile Update Parameters"
    priority = 2
    and_or = "or"
    search_type = "is"
    value = "requiredInstallationDate="'"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "escrow_buddy___invalid_fv_key" {
  name = "Escrow Buddy - Invalid FV Key"
  criteria {
    name = "Last Check-in"
    priority = 0
    and_or = "and"
    search_type = "less than x days ago"
    value = "30"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Last Enrollment"
    priority = 1
    and_or = "and"
    search_type = "more than x days ago"
    value = "1"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "FileVault 2 Partition Encryption State"
    priority = 2
    and_or = "and"
    search_type = "is"
    value = "Encrypted"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "FileVault 2 Individual Key Validation"
    priority = 3
    and_or = "and"
    search_type = "is not"
    value = "Valid"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "apple_silicon_macs" {
  name = "Apple Silicon Macs"
  criteria {
    name = "Apple Silicon"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Yes"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "abm_enrolled" {
  name = "ABM Enrolled"
  criteria {
    name = "Enrolled via Automated Device Enrollment"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Yes"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "all_computers" {
  name = "All Computers"
  criteria {
    name = "Operating System"
    priority = 0
    and_or = "and"
    search_type = "not like"
    value = "server"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Application Title"
    priority = 1
    and_or = "and"
    search_type = "is not"
    value = "Server.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "all_managed_computers" {
  name = "All Managed Computers"
  criteria {
    name = "Operating System"
    priority = 0
    and_or = "and"
    search_type = "not like"
    value = "server"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Application Title"
    priority = 1
    and_or = "and"
    search_type = "is not"
    value = "Server.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "all_sentinelone_computers" {
  name = "All SentinelOne Computers"
  criteria {
    name = "Operating System"
    priority = 0
    and_or = "and"
    search_type = "not like"
    value = "server"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Application Title"
    priority = 1
    and_or = "and"
    search_type = "is not"
    value = "Server.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "all_site_computers" {
  name = "All Site Computers"
  criteria {
    name = "Operating System"
    priority = 0
    and_or = "and"
    search_type = "not like"
    value = "server"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Application Title"
    priority = 1
    and_or = "and"
    search_type = "is not"
    value = "Server.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "all_users_entra_id" {
  name = "All Users Entra ID"
  criteria {
    name = "memberOf EA"
    priority = 0
    and_or = "and"
    search_type = "like"
    value = "All Users"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "am_test" {
  name = "AM Test"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "has"
    value = "Activity Monitor.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "au" {
  name = "AU"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "AirPort Utility.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "auto_update_microsoft_edge" {
  name = "Auto Update: Microsoft Edge"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "has"
    value = "Microsoft Edge"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "auto_update_microsoft_excel" {
  name = "Auto Update: Microsoft Excel"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Microsoft Excel.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "auto_update_microsoft_excel_365" {
  name = "Auto Update: Microsoft Excel 365"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Microsoft Excel.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "auto_update_microsoft_outlook" {
  name = "Auto Update: Microsoft OutLook"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "does not have"
    value = "Microsoft Outlook"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "auto_update_microsoft_word" {
  name = "Auto Update: Microsoft Word"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "does not have"
    value = "Microsoft Word"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "auto_update_windows_defender" {
  name = "Auto Update: Windows Defender"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "does not have"
    value = "Windows Defender"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___compliant" {
  name = "CIS Level 1 - Compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 1 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "like"
    value = "EMPTY"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___sequoia_non_compliant" {
  name = "CIS Level 1 - Sequoia Non-compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "CIS Level 1 - Sequoia"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 1 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "matches regex"
    value = "(\b[a-z0-9_\-]+\n?\b)+"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___sonoma_non_compliant" {
  name = "CIS Level 1 - Sonoma Non-compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "CIS Level 1 - Sonoma"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 1 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "matches regex"
    value = "(\b[a-z0-9_\-]+\n?\b)+"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_1___ventura_non_compliant" {
  name = "CIS Level 1 - Ventura Non-compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "CIS Level 1 - Ventura"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 1 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "matches regex"
    value = "(\b[a-z0-9_\-]+\n?\b)+"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "cis_level_2___compliant" {
  name = "CIS Level 2 - Compliant"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "All Computers"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "CIS Level 2 - Failed Result List"
    priority = 1
    and_or = "and"
    search_type = "like"
    value = "EMPTY"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "current_user_is_volume_owner" {
  name = "Current User is Volume Owner"
  criteria {
    name = "Volume Owner Status of end user"
    priority = 0
    and_or = "and"
    search_type = "like"
    value = "is the Volume Owner"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "current_user_not_volume_owner" {
  name = "Current User Not Volume Owner"
  criteria {
    name = "Volume Owner Status of end user"
    priority = 0
    and_or = "and"
    search_type = "like"
    value = "is not Volume Owner"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "dlp_block_all_usb_protect_plan_flag" {
  name = "DLP-Block All USB Protect Plan Flag"
  criteria {
    name = "Block All USB Plan Flag"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "block_usb"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "dlp_read_only_usb_protect_plan_flag" {
  name = "DLP-Read Only USB Protect Plan Flag"
  criteria {
    name = "DLP - Read Only USB Plan Flag"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "read_only_usb"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "falcon_not_installed" {
  name = "Falcon Not Installed"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "does not have"
    value = "Falcon.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "filevault_2_enabled" {
  name = "FileVault 2 Enabled"
  criteria {
    name = "FileVault 2 Partition Encryption State"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Encrypted"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "intel_macs" {
  name = "Intel Macs"
  criteria {
    name = "Apple Silicon"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "No"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "jamf_connect_first_run_done" {
  name = "Jamf Connect: First Run Done"
  criteria {
    name = "Jamf Connect - FirstRunDone"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "FirstRunDone"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "jamf_protect_block_all_plan_scoped" {
  name = "Jamf Protect Block All Plan Scoped"
  criteria {
    name = "Profile Name"
    priority = 0
    and_or = "and"
    search_type = "has"
    value = "Block USB  Plan - Jamf Protect Configuration"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "jamf_protect_read_only_plan_scoped" {
  name = "Jamf Protect Read Only Plan Scoped"
  criteria {
    name = "Profile Name"
    priority = 0
    and_or = "and"
    search_type = "has"
    value = "Read Only Plan - Jamf Protect Configuration"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "jamf_routines___redeploy_management_framework" {
  name = "Jamf Routines - Redeploy Management Framework"
  criteria {
    name = "Last Check-in"
    priority = 0
    and_or = "and"
    search_type = "more than x days ago"
    value = "30"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "last_checkin_30" {
  name = "Last Checkin +30"
  criteria {
    name = "Last Check-in"
    priority = 0
    and_or = "and"
    search_type = "more than x days ago"
    value = "30"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "macos_sequoia" {
  name = "MacOS Sequoia"
  criteria {
    name = "Operating System Version"
    priority = 0
    and_or = "and"
    search_type = "greater than or equal"
    value = "15"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "newly_onboarded_macs" {
  name = "Newly Onboarded Macs"
  criteria {
    name = "Last Enrollment"
    priority = 0
    and_or = "and"
    search_type = "less than x days ago"
    value = "1"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "not_macbooks" {
  name = "Not MacBooks"
  criteria {
    name = "Model"
    priority = 0
    and_or = "and"
    search_type = "not like"
    value = "Book"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "nudge_install" {
  name = "Nudge Install"
  criteria {
    name = "Application Title"
    priority = 0
    and_or = "and"
    search_type = "is not"
    value = "Nudge.app"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "nudge_big_sur" {
  name = "Nudge: Big Sur"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "Software Updates Available: Big Sur"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "nudge_monterey" {
  name = "Nudge: Monterey"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "Software Updates Available: Monterey"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "nudge_sonoma" {
  name = "Nudge: Sonoma"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "Software Updates Available: Sonoma"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "nudge_ventura" {
  name = "Nudge: Ventura"
  criteria {
    name = "Computer Group"
    priority = 0
    and_or = "and"
    search_type = "member of"
    value = "Software Updates Available: Ventura"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "security_people_who_are_not_volume_owners" {
  name = "Security People who are not volume owners"
  criteria {
    name = "Department"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Security"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Volume Owner Status of end user"
    priority = 1
    and_or = "and"
    search_type = "is"
    value = "No"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "software_updates_available_big_sur" {
  name = "Software Updates Available: Big Sur"
  criteria {
    name = "Patch Reporting: Apple macOS Big Sur"
    priority = 0
    and_or = "and"
    search_type = "is not"
    value = "Latest Version"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "software_updates_available_monterey" {
  name = "Software Updates Available: Monterey"
  criteria {
    name = "Patch Reporting: Apple macOS Monterey"
    priority = 0
    and_or = "and"
    search_type = "is not"
    value = "Latest Version"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "software_updates_available_sonoma" {
  name = "Software Updates Available: Sonoma"
  criteria {
    name = "Patch Reporting: Apple macOS Sonoma"
    priority = 0
    and_or = "and"
    search_type = "is not"
    value = "Latest Version"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "software_updates_available_ventura" {
  name = "Software Updates Available: Ventura"
  criteria {
    name = "Patch Reporting: Apple macOS Ventura"
    priority = 0
    and_or = "and"
    search_type = "is not"
    value = "Latest Version"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "somona_macs" {
  name = "Somona Mac's"
  criteria {
    name = "Operating System Version"
    priority = 0
    and_or = "and"
    search_type = "greater than or equal"
    value = "14"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "sonoma_macs" {
  name = "Sonoma Macs"
  criteria {
    name = "Operating System Version"
    priority = 0
    and_or = "and"
    search_type = "greater than or equal"
    value = "14"
    opening_paren = false
    closing_paren = false
  }
  criteria {
    name = "Operating System Version"
    priority = 1
    and_or = "and"
    search_type = "less than"
    value = "15"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "ventura" {
  name = "Ventura"
  criteria {
    name = "Operating System Version"
    priority = 0
    and_or = "and"
    search_type = "greater than or equal"
    value = "13"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "windows_defender___onboarding_profile_installed" {
  name = "Windows Defender - Onboarding Profile Installed"
  criteria {
    name = "Profile Name"
    priority = 0
    and_or = "and"
    search_type = "has"
    value = "MDE onboarding for macOS"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_smart" "zero_touch" {
  name = "Zero Touch"
  criteria {
    name = "Enrollment Method: PreStage enrollment"
    priority = 0
    and_or = "and"
    search_type = "is"
    value = "Zero Touch"
    opening_paren = false
    closing_paren = false
  }
}

resource "jamfpro_computer_group_static" "jamf_security" {
  name = "Jamf Security"
}

resource "jamfpro_computer_group_static" "omnifocus" {
  name = "OmniFocus"
}