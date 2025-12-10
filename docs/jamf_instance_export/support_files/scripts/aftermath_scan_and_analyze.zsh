#!/bin/zsh

#Remove remnants of previous Aftermath scans
rm -rf ~/Desktop/Aftermath*

#Set variables for SwiftDialog, download SwiftDialog if not present and pop alert to explain what Aftermath is doing
dialog="/usr/local/bin/dialog"
info_link="https://github.com/jamf/aftermath"
message="A threat has been detected on this Mac. We would like to gather logs to understand the threat in more detail.\n\nThis will take a few minutes.\n\nPlease click OK (or More Info) when you're ready to start the scan."
button="OK"

if [[ ! -f ${dialog} ]] then;
    /usr/local/bin/jamf policy -event installSwiftDialog
fi

runDialog () {
    ${dialog} \
    --title "Aftermath Scan In Progress" \
    --small \
    --ontop \
    --moveable \
    --position topleft \
    --icon 'SF=exclamationmark.shield.fill,colour=red' \
    --message ${message} \
    --messagefont "size=18" \
    --infobuttontext "More Info" \
    --infobuttonaction ${info_link} \
    --button1text ${button} \
}

runDialog

#Run Aftermath and output to /tmp/
sudo aftermath -o /tmp/

#Analyze the Aftermath zip file and output to ~/Desktop/
sudo aftermath --analyze /tmp/Aftermath*.zip -o ~/Desktop/

#Remove the Aftermath tmp file
rm -rf /tmp/Aftermath*

#Unzip the Aftermath file on and copy to ~/Desktop/
ditto -xk ~/Desktop/Aftermath*.zip ~/Desktop/

#Remove the Aftermath zip file from the Desktop
rm -rf ~/Desktop/Aftermath*.zip

#Open the Aftermath folder
open ~/Desktop/Aftermath*

#Display an alert saying the scan is done and explaining what's in the file
dialog2="/usr/local/bin/dialog"
info_link2="https://github.com/jamf/aftermath"
message2="Please look through the contents of the folder for the output of the Aftermath analysis.\n\nThe Storyline file will present the events that happened on this machine in chronological order to aid in the process of investigating threats on your endpoint."
button2="OK"

runDialog () {
    ${dialog2} \
    --title "Aftermath Scan Complete" \
    --small \
    --ontop \
    --moveable \
    --position topleft \
    --icon 'SF=exclamationmark.shield.fill,colour=green' \
    --message ${message2} \
    --messagefont "size=18" \
    --infobuttontext "More Info" \
    --infobuttonaction ${info_link2} \
    --button1text ${button2} \
}

runDialog

#Removing the hidden directory flag that triggers Aftermath
rm /Library/.tje/aftermath

/usr/local/bin/jamf recon

exit