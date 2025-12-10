#!/bin/zsh

/usr/bin/expect<<EOF
spawn profiles install -type bootstraptoken
expect {
    "Enter the admin user name:" {
        send "$4
"
        exp_continue
    }
    "Enter the password for user 'accountnamehere':" {
        send "$5
"
        exp_continue
    }
}