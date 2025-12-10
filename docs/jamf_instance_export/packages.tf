# Package: 1Loginconnect
# NOTE: You must manually place the package file at: support_files/packages/OneLogin-DemoProfile.pkg
resource "jamfpro_package" "r_1loginconnect" {
  package_name        = "1Loginconnect"
  package_file_source = "${path.module}/support_files/packages/OneLogin-DemoProfile.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.jamf_connect.id
}

# Package: Aftermath.pkg
# NOTE: You must manually place the package file at: support_files/packages/Aftermath (2).pkg
resource "jamfpro_package" "aftermathpkg" {
  package_name        = "Aftermath.pkg"
  package_file_source = "${path.module}/support_files/packages/Aftermath (2).pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: DEPNotify (2).pkg
# NOTE: You must manually place the package file at: support_files/packages/DEPNotify (2).pkg
resource "jamfpro_package" "depnotify_2pkg" {
  package_name        = "DEPNotify (2).pkg"
  package_file_source = "${path.module}/support_files/packages/DEPNotify (2).pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: dialog-2.5.0-4768.pkg
# NOTE: You must manually place the package file at: support_files/packages/dialog-2.5.0-4768 (2).pkg
resource "jamfpro_package" "dialog_250_4768pkg" {
  package_name        = "dialog-2.5.0-4768.pkg"
  package_file_source = "${path.module}/support_files/packages/dialog-2.5.0-4768 (2).pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: erase-install-30.2.pkg
# NOTE: You must manually place the package file at: support_files/packages/erase-install-30.2.pkg
resource "jamfpro_package" "erase_install_302pkg" {
  package_name        = "erase-install-30.2.pkg"
  package_file_source = "${path.module}/support_files/packages/erase-install-30.2.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.erase_install.id
}

# Package: erase-install-31.0.pkg
# NOTE: You must manually place the package file at: support_files/packages/erase-install-31.0.pkg
resource "jamfpro_package" "erase_install_310pkg" {
  package_name        = "erase-install-31.0.pkg"
  package_file_source = "${path.module}/support_files/packages/erase-install-31.0.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: Escrow.Buddy-1.0.0.pkg
# NOTE: You must manually place the package file at: support_files/packages/Escrow.Buddy-1.0.0.pkg
resource "jamfpro_package" "escrowbuddy_100pkg" {
  package_name        = "Escrow.Buddy-1.0.0.pkg"
  package_file_source = "${path.module}/support_files/packages/Escrow.Buddy-1.0.0.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.escrow_buddy.id
}

# Package: falcon.pkg
# NOTE: You must manually place the package file at: support_files/packages/falcon.pkg
resource "jamfpro_package" "falconpkg" {
  package_name        = "falcon.pkg"
  package_file_source = "${path.module}/support_files/packages/falcon.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.crowdstrike.id
}

# Package: Jamf Setup Manager PKG Install
# NOTE: You must manually place the package file at: support_files/packages/Setup.Manager.1.0-368 (1).pkg
resource "jamfpro_package" "jamf_setup_manager_pkg_install" {
  package_name        = "Jamf Setup Manager PKG Install"
  package_file_source = "${path.module}/support_files/packages/Setup.Manager.1.0-368 (1).pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.research_phase.id
}

# Package: JamfConnect.pkg
# NOTE: You must manually place the package file at: support_files/packages/JamfConnect.pkg
resource "jamfpro_package" "jamfconnectpkg" {
  package_name        = "JamfConnect.pkg"
  package_file_source = "${path.module}/support_files/packages/JamfConnect.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.jamf_connect.id
}

# Package: JamfConnectMetaPackage.pkg
# NOTE: You must manually place the package file at: support_files/packages/JamfConnectMetaPackage.pkg
resource "jamfpro_package" "jamfconnectmetapackagepkg" {
  package_name        = "JamfConnectMetaPackage.pkg"
  package_file_source = "${path.module}/support_files/packages/JamfConnectMetaPackage.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: logo.pkg
# NOTE: You must manually place the package file at: support_files/packages/logo.pkg
resource "jamfpro_package" "logopkg" {
  package_name        = "logo.pkg"
  package_file_source = "${path.module}/support_files/packages/logo.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: Nudge_Suite-1.1.16.81564.pkg
# NOTE: You must manually place the package file at: support_files/packages/Nudge_Suite-1.1.16.81564.pkg
resource "jamfpro_package" "nudge_suite_111681564pkg" {
  package_name        = "Nudge_Suite-1.1.16.81564.pkg"
  package_file_source = "${path.module}/support_files/packages/Nudge_Suite-1.1.16.81564.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: nudge.err.dmg
# NOTE: You must manually place the package file at: support_files/packages/nudge.err.dmg
resource "jamfpro_package" "nudgeerrdmg" {
  package_name        = "nudge.err.dmg"
  package_file_source = "${path.module}/support_files/packages/nudge.err.dmg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: PowerManagement Plist DMG
# NOTE: You must manually place the package file at: support_files/packages/com.apple.PowerManagement.plist.dmg
resource "jamfpro_package" "powermanagement_plist_dmg" {
  package_name        = "PowerManagement Plist DMG"
  package_file_source = "${path.module}/support_files/packages/com.apple.PowerManagement.plist.dmg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: Self Service Plus
# NOTE: You must manually place the package file at: support_files/packages/SelfService+1.0.0.pkg
resource "jamfpro_package" "self_service_plus" {
  package_name        = "Self Service Plus"
  package_file_source = "${path.module}/support_files/packages/SelfService+1.0.0.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.research_phase.id
}

# Package: SentinelOne.Pkg
# NOTE: You must manually place the package file at: support_files/packages/dialog-2.5.0-4768.pkg
resource "jamfpro_package" "sentinelonepkg" {
  package_name        = "SentinelOne.Pkg"
  package_file_source = "${path.module}/support_files/packages/dialog-2.5.0-4768.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}

# Package: Support.2.5.1.pkg
# NOTE: You must manually place the package file at: support_files/packages/Support.2.5.1.pkg
resource "jamfpro_package" "support251pkg" {
  package_name        = "Support.2.5.1.pkg"
  package_file_source = "${path.module}/support_files/packages/Support.2.5.1.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.research_phase.id
}

# Package: SupportHelper1.0.pkg
# NOTE: You must manually place the package file at: support_files/packages/SupportHelper1.0.pkg
resource "jamfpro_package" "supporthelper10pkg" {
  package_name        = "SupportHelper1.0.pkg"
  package_file_source = "${path.module}/support_files/packages/SupportHelper1.0.pkg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.research_phase.id
}

# Package: wallpaperdmg
# NOTE: You must manually place the package file at: support_files/packages/wallpaper.png.dmg
resource "jamfpro_package" "wallpaperdmg" {
  package_name        = "wallpaperdmg"
  package_file_source = "${path.module}/support_files/packages/wallpaper.png.dmg"
  priority              = 10
  reboot_required       = false
  fill_user_template    = false
  fill_existing_users   = false
  os_install            = false
  suppress_updates      = false
  suppress_from_dock    = false
  suppress_eula         = false
  suppress_registration = false
  category_id = jamfpro_category.no_category_assigned.id
}