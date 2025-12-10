#!/bin/zsh

dialog="/usr/local/bin/dialog"
message="Security investigation complete.\n\nAccess to organizational resources have been restored."
button="Ok"

/bin/rm /Library/LaunchDaemons/com.softwareupdater.fake.plist.plist
/bin/rm /Library/Application\ Support/JamfProtect/groups/*

#Writing the file that is watched by the EA and adding the Aftermath flag for the optional Aftermath workflow

mkdir /Library/.tje
rm /Library/.tje/remediated
rm /Library/.tje/aftermath
touch /Library/.tje/remediated
touch /Library/.tje/aftermath

jamf recon

if [[ ! -f ${dialog} ]] then;
    /usr/local/bin/jamf policy -event installSwiftDialog
fi

runDialog () {
    ${dialog} \
            --title "IT Security Notification" \
            --small \
            --icon 'SF=checkmark.shield.fill,colour=blue' \
            --message ${message} \
            --button1text ${button} \
}

runDialog

# Removing the remediated flag

rm /Library/.tje/remediated

killall -HUP mDNSResponder
killall mDNSResponderHelper
dscacheutil -flushcache

# Calling jamf policy to trigger the optional Aftermath add on

/usr/local/bin/jamf policy

# Opening Jamf Self Service to the Featured category

open "jamfselfservice://content?action=category&id=-2"

sleep 3

exit