#! /bin/bash

# Force Quit the app
ps aux | grep "$4" | grep -v "grep" | awk '{print $2}' | xargs kill -15