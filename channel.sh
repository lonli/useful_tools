#!/bin/bash

## change this setting for your need
REMOTE_HOST="127.0.0.1"   
REMOTE_PORT="22"
REMOTE_USER="lonli"
REMOTE_KEY_FILE="/home/lonli/.ssh/id_rsa"

p_id=`pgrep -f '127.0.0.1:7070'`
[ -n "$p_id" ] && kill $d
ssh  -CfNg -D 127.0.0.1:7070 -p ${REMOTE_PORT} -i ${REMOTE_KEY_FILE} ${REMOTE_USER}@${REMOTE_HOST}
