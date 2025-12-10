#!/bin/sh

sudo echo $4 > /Library/Application\ Support/JAMF/Waiting\ Room/com.sentinelone.registration-token
sudo /usr/sbin/installer -pkg /Library/Application\ Support/JAMF/Waiting\ Room/SentinelAgent_macos_v21_5_3_5411.pkg -target /