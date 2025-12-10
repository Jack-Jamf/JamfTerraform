#!/bin/bash

#This script writes a file that will trigger an EA in Jamf Pro to join a Smart Group

#Writing the file that is watched by the EA

mkdir /Library/.tje
rm /Library/.tje/block_usb
touch /Library/.tje/read_only_usb

jamf recon

sleep 4

#Quitting Self Service to refresh

osascript -e 'quit application "Self Service"'

osascript -e 'display dialog "Your Mac can mount USB drives in read-only mode. Run the Block All USB policy in Self Service to block access." buttons {"OK"} with icon caution' &

sleep 10

open -a Self\ Service.app

exit 0