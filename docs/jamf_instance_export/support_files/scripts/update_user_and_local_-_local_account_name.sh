#!/bin/bash

# Add currently logged in username to Jamf Pro inventory
# jamf recon -endUsername $3

# Add currently logged in username and Real Name to jamf Pro Inventory

loggedInUser=`/bin/ls -l /dev/console | /usr/bin/awk '{ print $3 }'`

userRealName=`dscl . -read /Users/$loggedInUser | grep RealName: | cut -c11-`
            if [[ -z $userRealName ]]; then
                userRealName=`dscl . -read /Users/$loggedInUser | awk '/^RealName:/,/^RecordName:/' | sed -n 2p | cut -c 2-`
            fi
            
# Get NetworkUser/Email if created with Jamf Connect
useremail=`dscl . -read /Users/$loggedInUser | grep NetworkUser: | cut -c14-`

# Submit Inventory

jamf recon -endUsername "$useremail" -realname "$userRealName" -email "$useremail"