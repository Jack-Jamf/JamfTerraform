resource "jamfpro_policy" "restart_daily_at_5pm" {
  name    = "Restart Daily at 5PM"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "safari_update" {
  name    = "Safari Update"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "update_inventory" {
  name    = "Update Inventory"
  enabled = true
  category_id = jamfpro_category.maintenance.id
  frequency = "Once every day"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "device_compliance_registration" {
  name    = "Device Compliance Registration"
  enabled = true
  category_id = jamfpro_category.microsoft_o365.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "eraseinstall_cache_latest_os" {
  name    = "EraseInstall: Cache Latest OS"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "install_swift_dialog" {
  name    = "Install Swift Dialog"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "update_all_installomator_apps" {
  name    = "Update All Installomator Apps"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "all_office_printers" {
  name    = "All Office Printers"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "hp_laserjet" {
  name    = "HP LaserJet"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "marketing_mfp" {
  name    = "Marketing MFP"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "unmap_all_printers" {
  name    = "Unmap All Printers"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "on_demand_check_in" {
  name    = "On Demand Check-in"
  enabled = true
  category_id = jamfpro_category.udacity.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "on_demand_inventory_update" {
  name    = "On Demand Inventory Update"
  enabled = true
  category_id = jamfpro_category.udacity.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }
}

resource "jamfpro_policy" "depnotify_cleanup" {
  name    = "DEPNotify Cleanup"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }
}

resource "jamfpro_policy" "app_auto_patch___self_service" {
  name    = "App Auto Patch - Self Service"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once every day"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.app_auto_patch.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "app_auto_patch_activator" {
  name    = "App Auto Patch Activator"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once every day"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.app_auto_patch_activator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "dlp_block_all_usb_protect_plan" {
  name    = "DLP-Block All USB Protect Plan"
  enabled = true
  category_id = jamfpro_category.compliance.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.block_all_usb.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "jamf_protect_behavioral_detection_bundlore" {
  name    = "Jamf Protect: Behavioral Detection (Bundlore)"
  enabled = true
  category_id = jamfpro_category.jamf_protect.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.bundlore_adware___protect_behavioral_detection.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "jamf_protect_behavioral_remediation" {
  name    = "Jamf Protect: Behavioral Remediation"
  enabled = true
  category_id = jamfpro_category.jamf_protect.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.bundlore_adware___remediate_behavioral_detection.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cisco_anyconnect" {
  name    = "Cisco Anyconnect"
  enabled = true
  category_id = jamfpro_category.anyconnect.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.cisco_any_connect_uninstall_unwanted_modules.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "crowdstrike_uninstall" {
  name    = "CrowdStrike Uninstall"
  enabled = true
  category_id = jamfpro_category.crowdstrike.id
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.crowdstrike_uninstall_.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "dep_notify___prestage" {
  name    = "DEP Notify - Prestage"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.dep_notify___auto_enrollment.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "homebrew_and_xcode_command_line_tools_install" {
  name    = "HomeBrew and Xcode Command Line Tools Install"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.homebrew.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "firefox" {
  name    = "Firefox"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "google_chrome_enterprise" {
  name    = "Google Chrome Enterprise"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "google_drive" {
  name    = "Google Drive"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "google_drive_backup_sync" {
  name    = "Google Drive Backup Sync"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "google_filestream" {
  name    = "Google Filestream"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "google_software_update" {
  name    = "Google Software Update"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator___windows_defender" {
  name    = "Installomator - Windows Defender"
  enabled = true
  category_id = jamfpro_category.windows_defender.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_adobe_creative_cloud_desktop" {
  name    = "Installomator: Adobe Creative Cloud Desktop"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_adobe_reader" {
  name    = "Installomator: Adobe Reader"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_company_portal" {
  name    = "Installomator: Company Portal"
  enabled = true
  category_id = jamfpro_category.microsoft_o365.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_edge" {
  name    = "Installomator: Edge"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_jamf_connect_install" {
  name    = "Installomator: Jamf Connect Install"
  enabled = true
  category_id = jamfpro_category.jamf_apps.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_microsoftazuredatastudio" {
  name    = "Installomator: microsoftazuredatastudio"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "installomator_microsoftonedrive" {
  name    = "Installomator: microsoftonedrive"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "macadmins_python" {
  name    = "MacAdmins Python"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_edge" {
  name    = "Microsoft Edge"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_one_note" {
  name    = "Microsoft One Note"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_onedrive" {
  name    = "Microsoft OneDrive"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_outlook" {
  name    = "Microsoft Outlook"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_outlook_reset" {
  name    = "Microsoft Outlook Reset"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_power_point" {
  name    = "Microsoft Power Point"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_remote_desktop" {
  name    = "Microsoft Remote Desktop"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_sharepoint_plugin" {
  name    = "Microsoft SharePoint Plugin"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_teams" {
  name    = "Microsoft Teams"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "microsoft_xcel" {
  name    = "Microsoft Xcel"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "nudge" {
  name    = "Nudge"
  enabled = true
  category_id = jamfpro_category.operating_system_updates.id
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "Before"
    }
  }
}

resource "jamfpro_policy" "privileges" {
  name    = "Privileges"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "slack" {
  name    = "Slack"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "slack" {
  name    = "Slack"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "supported_browsers_chrome_enterprise_firefox_edge" {
  name    = "Supported Browsers (Chrome Enterprise, Firefox, Edge)"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "zoom" {
  name    = "Zoom"
  enabled = true
  category_id = jamfpro_category.self_service.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "zoom" {
  name    = "Zoom"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.installomator.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "make_me_an_admin" {
  name    = "Make Me An Admin"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.make_me_an_admin.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "pass_bootstrap_token_to_current_logged_in_user" {
  name    = "Pass Bootstrap Token to Current Logged In User"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.pass_bootstrap_token.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "dlp__read_only_usb_protect_plan" {
  name    = "DLP- Read Only USB Protect Plan"
  enabled = true
  category_id = jamfpro_category.compliance.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.read_only_usb.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "safari_update" {
  name    = "Safari Update"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.safari_update.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "open_webpage_helpdesk_ticket" {
  name    = "Open Webpage: Helpdesk Ticket"
  enabled = true
  category_id = jamfpro_category.help_tools.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.self_service_open_website.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "setup_your_mac" {
  name    = "Setup Your Mac"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.setup_your_mac.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "sophos_install" {
  name    = "Sophos Install"
  enabled = true
  category_id = jamfpro_category.sophos_endpoint.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  payloads {
    scripts {
      id       = jamfpro_script.sophos_central_install_script.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "local_account_to_user_and_location" {
  name    = "Local Account to User and Location"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  payloads {
    scripts {
      id       = jamfpro_script.update_user_and_local___local_account_name.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "install_swift_dialog_and_aftermath" {
  name    = "Install Swift Dialog and Aftermath"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  package {
    id     = jamfpro_package.aftermathpkg.id
    action = "Install"
  }
  package {
    id     = jamfpro_package.dialog_250_4768pkg.id
    action = "Install"
  }
}

resource "jamfpro_policy" "erase_install_cache" {
  name    = "Erase install cache"
  enabled = true
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  package {
    id     = jamfpro_package.erase_install_310pkg.id
    action = "Install"
  }

  payloads {
    scripts {
      id       = jamfpro_script.eraseinstall_launcher_script.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "escrow_buddy_install" {
  name    = "Escrow Buddy Install"
  enabled = true
  category_id = jamfpro_category.escrow_buddy.id
  frequency = "Once per computer"

  scope {
    all_computers = true
  }

  package {
    id     = jamfpro_package.escrowbuddy_100pkg.id
    action = "Install"
  }
}

resource "jamfpro_policy" "jamf_setup_manager" {
  name    = "Jamf Setup Manager"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  package {
    id     = jamfpro_package.jamf_setup_manager_pkg_install.id
    action = "Install"
  }
}

resource "jamfpro_policy" "dep_notify" {
  name    = "DEP Notify"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = true
  }

  package {
    id     = jamfpro_package.depnotify_2pkg.id
    action = "Install"
  }
  package {
    id     = jamfpro_package.logopkg.id
    action = "Install"
  }

  payloads {
    scripts {
      id       = jamfpro_script.dep_notify___auto_enrollment.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "nudge_suite_pkg" {
  name    = "Nudge Suite PKG"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  package {
    id     = jamfpro_package.nudge_suite_111681564pkg.id
    action = "Install"
  }
}

resource "jamfpro_policy" "energy_saver_standard_settings" {
  name    = "Energy Saver Standard Settings"
  enabled = true
  frequency = "Ongoing"

  scope {
    all_computers = false
  }

  package {
    id     = jamfpro_package.powermanagement_plist_dmg.id
    action = "Install"
  }
}

resource "jamfpro_policy" "sentinelone_install" {
  name    = "SentinelOne Install"
  enabled = true
  category_id = jamfpro_category.sentinelone.id
  frequency = "Once per computer"

  scope {
    all_computers = false
  }

  package {
    id     = jamfpro_package.sentinelonepkg.id
    action = "Cache"
  }

  payloads {
    scripts {
      id       = jamfpro_script.sentinelone_pkg_install.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "aftermath_scan_and_analyze" {
  name    = "Aftermath Scan and Analyze"
  enabled = true
  category_id = jamfpro_category.jamf_protect.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.aftermath_trigger.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.aftermath_scan_and_analyze.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_1___sequoia_audit_policy" {
  name    = "CIS Level 1 - Sequoia Audit policy"
  enabled = true
  category_id = jamfpro_category.cis_level_1.id
  frequency = "Once every day"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_1___sequoia.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_687a63d69bb9ee130a3e2693_sequoiash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_1___sonoma_audit_policy" {
  name    = "CIS Level 1 - Sonoma Audit policy"
  enabled = true
  category_id = jamfpro_category.cis_level_1.id
  frequency = "Once every day"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_1___sonoma.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_687a63d69bb9ee130a3e2693_sonomash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_1___ventura_audit_policy" {
  name    = "CIS Level 1 - Ventura Audit policy"
  enabled = true
  category_id = jamfpro_category.cis_level_1.id
  frequency = "Once every day"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_1___ventura.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_687a63d69bb9ee130a3e2693_venturash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_2___sequoia_audit_policy" {
  name    = "CIS Level 2 - Sequoia Audit policy"
  enabled = true
  category_id = jamfpro_category.cis_level_2.id
  frequency = "Once every day"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_2___sequoia.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_68ae161280d9a2e9cd4c37c2_sequoiash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_2___sequoia_remediation_policy" {
  name    = "CIS Level 2 - Sequoia Remediation policy"
  enabled = true
  category_id = jamfpro_category.cis_level_2.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_2___sequoia_non_compliant.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_68ae161280d9a2e9cd4c37c2_sequoiash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_2___sonoma_audit_policy" {
  name    = "CIS Level 2 - Sonoma Audit policy"
  enabled = true
  category_id = jamfpro_category.cis_level_2.id
  frequency = "Once every day"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_2___sonoma.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_68ae161280d9a2e9cd4c37c2_sonomash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_2___sonoma_remediation_policy" {
  name    = "CIS Level 2 - Sonoma Remediation policy"
  enabled = true
  category_id = jamfpro_category.cis_level_2.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_2___sonoma_non_compliant.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_68ae161280d9a2e9cd4c37c2_sonomash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_2___ventura_audit_policy" {
  name    = "CIS Level 2 - Ventura Audit policy"
  enabled = true
  category_id = jamfpro_category.cis_level_2.id
  frequency = "Once every day"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_2___ventura.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_68ae161280d9a2e9cd4c37c2_venturash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "cis_level_2___ventura_remediation_policy" {
  name    = "CIS Level 2 - Ventura Remediation policy"
  enabled = true
  category_id = jamfpro_category.cis_level_2.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.cis_level_2___ventura_non_compliant.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.compliance_benchmark_68ae161280d9a2e9cd4c37c2_venturash.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "crowdstrike_api_script_install" {
  name    = "CrowdStrike API Script Install"
  enabled = true
  category_id = jamfpro_category.crowdstrike.id
  frequency = "Once per computer"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.crowdstrike_settings_profile_installed.id]
  }

  package {
    id     = jamfpro_package.falconpkg.id
    action = "Install"
  }

  payloads {
    scripts {
      id       = jamfpro_script.license_falcon.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "eraseinstall_major_os_upgrade" {
  name    = "EraseInstall: Major OS Upgrade"
  enabled = false
  category_id = jamfpro_category.erase_install.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.eraseinstall_installer_cached.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.eraseinstall_launcher_script.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "eraseinstall_reload_mac_full_wipe_and_reinstall_of_macos" {
  name    = "EraseInstall: Reload Mac (Full Wipe and Reinstall of MacOS)"
  enabled = false
  category_id = jamfpro_category.erase_install.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.eraseinstall_reload_macos.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.eraseinstall_launcher_script.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "eraseinstall_reload_recon" {
  name    = "EraseInstall: Reload Recon"
  enabled = false
  category_id = jamfpro_category.erase_install.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.eraseinstall_reload_macos.id]
  }
}

resource "jamfpro_policy" "eraseinstall_update_to_134_hardcoded_version_number_in_parameter_5" {
  name    = "EraseInstall: Update to 13.4 (hardcoded version number in parameter 5)"
  enabled = false
  category_id = jamfpro_category.erase_install.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.eraseinstall_reload_macos.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.eraseinstall_launcher_script.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "filevault_2_recovery_key_reissue" {
  name    = "FileVault 2 Recovery Key Reissue"
  enabled = true
  category_id = jamfpro_category.compliance.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.filevault_2_key_reissue.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.filevault_2_key_reissue.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "jamf_protect_behavioral_notification_bundlore" {
  name    = "Jamf Protect: Behavioral Notification (Bundlore)"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.protect___bundlore.id]
  }

  payloads {
    scripts {
      id       = jamfpro_script.bundlore_adware___notification.id
      priority = "After"
    }
  }
}

resource "jamfpro_policy" "nudge_fix_parameters" {
  name    = "Nudge: Fix Parameters"
  enabled = true
  category_id = jamfpro_category.research_phase.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.nudge_incorrect_parameters.id]
  }
}

resource "jamfpro_policy" "reissue_key" {
  name    = "Reissue Key"
  enabled = true
  category_id = jamfpro_category.escrow_buddy.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.escrow_buddy___invalid_fv_key.id]
  }
}

resource "jamfpro_policy" "rosetta_2_install" {
  name    = "Rosetta 2 Install"
  enabled = true
  category_id = jamfpro_category.zero_touch.id
  frequency = "Ongoing"

  scope {
    all_computers = false
    computer_group_ids = [jamfpro_computer_group.apple_silicon_macs.id]
  }
}