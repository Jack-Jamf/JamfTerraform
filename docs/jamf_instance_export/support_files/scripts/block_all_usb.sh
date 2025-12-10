#!/bin/bash

#This script writes a file that will trigger an EA in Jamf Pro to join a Smart Group

#Writing the file that is watched by the EA

mkdir /Library/.tje
rm /Library/.tje/read_only_usb
touch /Library/.tje/block_usb

jamf recon

sleep 4

#Quitting Self Service to refresh

osascript -e 'quit application "Self Service"'

osascript -e 'display dialog "Your Mac can no longer mount USB drives. Please run the Allow Read-Only USB policy in Self Service to regain access." buttons {"OK"} with icon caution' &

sleep 10

open -a Self\ Service.app

exit 0