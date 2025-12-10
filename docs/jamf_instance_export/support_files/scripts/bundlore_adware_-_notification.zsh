#!/bin/zsh

dialog="/usr/local/bin/dialog"
info_link="https://www.virustotal.com/gui/file/003a2e2e5d618af62aef7249eaa51b9ef14b61160f37382bac3748a0dbf0b331/"
message="Malicious activity was detected on your device.\n\nAccess to organizational resources has been suspended until an investigation has been completed.\n\nOnce completed, click OK and your access will be restored."
button="Remove Threat"
button1_link="jamfselfservice://content?entity=policy&id=$4&action=execute"

if [[ ! -f ${dialog} ]] then;
    /usr/local/bin/jamf policy -event @dialog
fi

runDialog () {
    ${dialog} \
            --title "IT Security Notification" \
            --small \
            --ontop \
            --moveable \
            --position topleft \
            --icon 'SF=exclamationmark.shield.fill,colour=blue' \
            --message ${message} \
            --messagefont "size=18" \
            --infobuttontext "More Info" \
            --infobuttonaction ${info_link} \
            --button1text ${button} \
            --button1action ${button1_link}\
}

runDialog

open -R '/Library/LaunchDaemons/com.softwareupdater.fake.plist.plist'