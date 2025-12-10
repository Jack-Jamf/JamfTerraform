#!/bin/bash
set -x

## Get the logged in user's name to edit ~/Library related files
currentUser=$(/usr/bin/stat -f%Su /dev/console)

# Ensure that AnyConnect is disconnected and closed.
/opt/cisco/anyconnect/bin/vpn disconnect

# wait for it to disconnect
sleep 1

pkill -f "Cisco AnyConnect Secure Mobility Client.app"

# Wait for it to quit
sleep 5

# Uninstall Cisco AnyConnect ISE Compliance if it exists
/opt/cisco/anyconnect/bin/isecompliance_uninstall.sh

# wait for that to finish
sleep 10

# Uninstall Cisco AnyConnect ISEPosture if it exists
/opt/cisco/anyconnect/bin/iseposture_uninstall.sh

# wait for that to finish
sleep 10

# Uninstall Cisco Posture if it exists
/opt/cisco/hostscan/bin64/posture_uninstall.sh

# wait for that to finish
sleep 10

# delete any remaining folders that are created with AnyConnect install
rm -rf /opt/cisco/anyconnect
rm -rf /opt/cisco/hostscan
rm -rf /opt/cisco/vpn
rm -rf /Applications/Cisco/Cisco\ AnyConnect\ Secure\ Mobility\ Client.app
rm -rf /Applications/Cisco/Cisco\ AnyConnect\ Socket\ Filter.app
rm -rf /Applications/Cisco/Cisco\ AnyConnect\ DART.app
rm -rf /Applications/Cisco/Uninstall\ AnyConnect\ DART.app
rm -rf /Applications/Cisco/Uninstall\ AnyConnect.app
rm -rf /Applications/Cisco/*
rm -rf /Applications/Cisco

# wait for that to finsih
sleep 10

# remove any lingering files of the installer
pkgutil --forget com.cisco.pkg.anyconnect.vpn

# wait for that to finish
sleep 10

# remove any user specific items
rm -rf /Users/$currentUser/Library/Preferences/com.cisco.anyconnect.gui.plist
rm -rf /Users/$currentUser/.anyconnect

# wait for that to finish
sleep 10

echo "work complete"

exit 0