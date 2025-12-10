#!/bin/bash
mkdir /private/var/tmp/sophos
cd /private/var/tmp/sophos

# Installing Sophos
curl -L -O "$4"
unzip SophosInstall.zip
chmod a+x /private/var/tmp/sophos/Sophos\ Installer.app/Contents/MacOS/Sophos\ Installer
chmod a+x /private/var/tmp/sophos/Sophos\ Installer.app/Contents/MacOS/tools/com.sophos.bootstrap.helper
sudo /private/var/tmp/sophos/Sophos\ Installer.app/Contents/MacOS/Sophos\ Installer --install;
/bin/rm -rf /private/var/tmp/sophos;
exit 0      ## Success
exit 1      ## Failure