resource "jamfpro_script" "aftermath_scan_and_analyze" {
  name     = "Aftermath Scan and Analyze"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/aftermath_scan_and_analyze.zsh")
}

resource "jamfpro_script" "android_device_manager_install" {
  name     = "Android Device Manager Install"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/android_device_manager_install.sh")
}

resource "jamfpro_script" "app_auto_patch" {
  name     = "App Auto Patch"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/app_auto_patch.zsh")
  info  = "https://github.com/robjschroeder/App-Auto-Patch"
}

resource "jamfpro_script" "app_auto_patch_activator" {
  name     = "App Auto Patch Activator"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/app_auto_patch_activator.zsh")
  info  = "https://github.com/robjschroeder/App-Auto-Patch/wiki/AAP-Activator"
}

resource "jamfpro_script" "block_all_usb" {
  name     = "Block All USB"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/block_all_usb.sh")
}

resource "jamfpro_script" "bundlore_adware___notification" {
  name     = "Bundlore Adware - Notification"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/bundlore_adware_-_notification.zsh")
}

resource "jamfpro_script" "bundlore_adware___protect_behavioral_detection" {
  name     = "Bundlore Adware - Protect Behavioral Detection"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/bundlore_adware_-_protect_behavioral_detection.sh")
}

resource "jamfpro_script" "bundlore_adware___remediate_behavioral_detection" {
  name     = "Bundlore Adware - Remediate Behavioral Detection"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/bundlore_adware_-_remediate_behavioral_detection.zsh")
}

resource "jamfpro_script" "cisco_any_connect_uninstall_unwanted_modules" {
  name     = "Cisco Any-connect Uninstall Unwanted Modules"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/cisco_any-connect_uninstall_unwanted_modules.sh")
  info  = "Default is to uninstall everything except VPN

Source: https://community.jamf.com/t5/jamf-pro/remove-cisco-anyconnect-vpn-tunnels/td-p/278245"
}

resource "jamfpro_script" "compliance_benchmark_687a63d69bb9ee130a3e2693_sequoiash" {
  name     = "compliance_benchmark_687a63d69bb9ee130a3e2693_sequoia.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/compliance_benchmark_687a63d69bb9ee130a3e2693_sequoia.sh.zsh")
  os_requirements = "15.x"
}

resource "jamfpro_script" "compliance_benchmark_687a63d69bb9ee130a3e2693_sonomash" {
  name     = "compliance_benchmark_687a63d69bb9ee130a3e2693_sonoma.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/compliance_benchmark_687a63d69bb9ee130a3e2693_sonoma.sh.zsh")
  os_requirements = "14.x"
}

resource "jamfpro_script" "compliance_benchmark_687a63d69bb9ee130a3e2693_venturash" {
  name     = "compliance_benchmark_687a63d69bb9ee130a3e2693_ventura.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/compliance_benchmark_687a63d69bb9ee130a3e2693_ventura.sh.zsh")
  os_requirements = "13.x"
}

resource "jamfpro_script" "compliance_benchmark_68ae161280d9a2e9cd4c37c2_sequoiash" {
  name     = "compliance_benchmark_68ae161280d9a2e9cd4c37c2_sequoia.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/compliance_benchmark_68ae161280d9a2e9cd4c37c2_sequoia.sh.zsh")
  os_requirements = "15.x"
}

resource "jamfpro_script" "compliance_benchmark_68ae161280d9a2e9cd4c37c2_sonomash" {
  name     = "compliance_benchmark_68ae161280d9a2e9cd4c37c2_sonoma.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/compliance_benchmark_68ae161280d9a2e9cd4c37c2_sonoma.sh.zsh")
  os_requirements = "14.x"
}

resource "jamfpro_script" "compliance_benchmark_68ae161280d9a2e9cd4c37c2_venturash" {
  name     = "compliance_benchmark_68ae161280d9a2e9cd4c37c2_ventura.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/compliance_benchmark_68ae161280d9a2e9cd4c37c2_ventura.sh.zsh")
  os_requirements = "13.x"
}

resource "jamfpro_script" "crowdstrike_download_and_install" {
  name     = "Crowdstrike Download and Install"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/crowdstrike_download_and_install.zsh")
  info  = "https://github.com/franton/Crowdstrike-API-Scripts/blob/main/install-csf.sh"
  notes = "Falcon download API client:

Clientid = a185f38a13314c2b9ff3426d3c0045ed
Secret = seNux0618mv42nfcTk9JpO5t7GMUFhHqZ3QEzboS
BaseURL = https://api.us-2.crowdstrike.com"
}

resource "jamfpro_script" "crowdstrike_uninstall_" {
  name     = "Crowdstrike Uninstall "
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/crowdstrike_uninstall.zsh")
  info  = "https://github.com/franton/Crowdstrike-API-Scripts/blob/main/uninstall-csf.sh"
}

resource "jamfpro_script" "dep_notify___auto_enrollment" {
  name     = "DEP Notify - Auto Enrollment"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/dep_notify_-_auto_enrollment.sh")
  info  = "Source: https://github.com/jamf/DEPNotify-Starter"
  notes = "Lines 155 to set custom triggers or policy ID. You can modify existing entries or use the format below to add new ones

 \"Installing <Application Name>,<trigger name or policy ID>\""
}

resource "jamfpro_script" "dep_notify_cleanup" {
  name     = "DEP Notify CleanUp"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/dep_notify_cleanup.sh")
  info  = "https://github.com/jamf/DEPNotify-Starter/blob/master/depNotifyReset.sh"
}

resource "jamfpro_script" "depnotify___web_enroll" {
  name     = "DEPnotify - Web Enroll"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/depnotify_-_web_enroll.sh")
}

resource "jamfpro_script" "eraseinstall_launcher_script" {
  name     = "EraseInstall Launcher Script"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/eraseinstall_launcher_script.zsh")
  info  = "Source: https://github.com/grahampugh/erase-install/wiki/6.-Use-in-Jamf-Pro"
  notes = "Workfflows: https://github.com/grahampugh/erase-install/wiki/6.-Use-in-Jamf-Pro#option-2-upload-the-script-and-use-policy-script-parameters"
}

resource "jamfpro_script" "filevault_2_key_reissue" {
  name     = "FileVault 2 Key Reissue"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/filevault_2_key_reissue.sh")
  info  = "Source: https://github.com/jamf/FileVault2_Scripts/blob/master/reissueKey.sh"
}

resource "jamfpro_script" "force_quit" {
  name     = "Force Quit"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/force_quit.sh")
}

resource "jamfpro_script" "homebrew" {
  name     = "Homebrew"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/homebrew.sh")
  info  = "https://github.com/Honestpuck/homebrew.sh/blob/master/homebrew-3.3.sh"
}

resource "jamfpro_script" "installomator" {
  name     = "Installomator"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/installomator.zsh")
  info  = "Source: https://github.com/Installomator/Installomator/
Application Label List: https://github.com/Installomator/Installomator/blob/main/Labels.txt"
  notes = "Guide: https://scriptingosx.com/2020/06/using-installomator-with-jamf-pro/"
}

resource "jamfpro_script" "installomator_new" {
  name     = "Installomator New"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/installomator_new.zsh")
}

resource "jamfpro_script" "license_falcon" {
  name     = "License Falcon"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/license_falcon.sh")
}

resource "jamfpro_script" "make_me_an_admin" {
  name     = "Make me an admin"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/make_me_an_admin.sh")
  info  = "https://github.com/jamf/MakeMeAnAdmin"
}

resource "jamfpro_script" "monterey_cis_lvl1_compliancesh" {
  name     = "Monterey_cis_lvl1_compliance.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/monterey_cis_lvl1_compliance.sh.zsh")
}

resource "jamfpro_script" "mount_network_drive" {
  name     = "Mount Network Drive"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/mount_network_drive.sh")
  notes = "https://github.com/robjschroeder/macOS-shell/blob/main/NetworkDrive-MapNetworkDrive.sh"
}

resource "jamfpro_script" "pass_bootstrap_token" {
  name     = "Pass Bootstrap Token"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/pass_bootstrap_token.zsh")
  info  = "This script will pass the bootstrap token to the end user. This will make the current logged in user a volume owner for OS updates.

Parameters 4 and 5 will need to contain the current secure token holder account name and password. This is not recommended nor secure, but there's no way around it)"
  notes = "Reference: https://support.apple.com/guide/deployment/use-secure-and-bootstrap-tokens-dep24dbdcf9e/web
https://learn.jamf.com/bundle/technical-articles/page/Manually_Leveraging_Apples_Bootstrap_Token_Functionality.html"
}

resource "jamfpro_script" "read_only_usb" {
  name     = "Read Only USB"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/read_only_usb.sh")
}

resource "jamfpro_script" "remove_script" {
  name     = "Remove Script"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/remove_script.sh")
}

resource "jamfpro_script" "safari_update" {
  name     = "Safari update"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/safari_update.sh")
}

resource "jamfpro_script" "self_service_open_website" {
  name     = "Self Service Open Website"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/self_service_open_website.sh")
  info  = "Source: https://macadmins.slack.com/archives/C04QVP86E/p1632881475209900"
}

resource "jamfpro_script" "sentinel_one_full_install" {
  name     = "Sentinel One Full Install"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sentinel_one_full_install.sh")
}

resource "jamfpro_script" "sentinelone_pkg_install" {
  name     = "SentinelOne Pkg Install"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sentinelone_pkg_install.sh")
}

resource "jamfpro_script" "sequoia_cis_lvl1_compliancesh" {
  name     = "Sequoia_cis_lvl1_compliance.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sequoia_cis_lvl1_compliance.sh.zsh")
}

resource "jamfpro_script" "setup_your_mac" {
  name     = "Setup your Mac"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/setup_your_mac.sh")
}

resource "jamfpro_script" "sonoma_800_171_compliancesh" {
  name     = "Sonoma_800-171_compliance.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sonoma_800-171_compliance.sh.zsh")
}

resource "jamfpro_script" "sonoma_jackboarder_compliancesh" {
  name     = "Sonoma_jackboarder_compliance.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sonoma_jackboarder_compliance.sh.zsh")
}

resource "jamfpro_script" "sonoma_ktt_compliancesh" {
  name     = "Sonoma_ktt_compliance.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sonoma_ktt_compliance.sh.zsh")
}

resource "jamfpro_script" "sophos_central_install_script" {
  name     = "Sophos Central Install Script"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/sophos_central_install_script.sh")
  info  = "To obtain download URL: https://docs.sophos.com/central/customer/help/en-us/PeopleAndDevices/ProtectDevices/EndpointProtection/MacDeployment/index.html#download-installer"
}

resource "jamfpro_script" "temp_admin" {
  name     = "Temp Admin"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/temp_admin.sh")
}

resource "jamfpro_script" "update_user_and_local___local_account_name" {
  name     = "Update User and Local - Local Account Name"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/update_user_and_local_-_local_account_name.sh")
}

resource "jamfpro_script" "ventura_cis_lvl1_compliancesh" {
  name     = "Ventura_cis_lvl1_compliance.sh"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/ventura_cis_lvl1_compliance.sh.zsh")
}

resource "jamfpro_script" "xcode_install" {
  name     = "Xcode Install"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/xcode_install.sh")
}

resource "jamfpro_script" "xcode_suppress_eula" {
  name     = "Xcode Suppress EULA"
  priority = "After"
  script_contents = file("${path.module}/support_files/scripts/xcode_suppress_eula.sh")
  info  = "https://macadmins.slack.com/archives/C04QVP86E/p1663678529231119?thread_ts=1663675611.125399&cid=C04QVP86E"
}