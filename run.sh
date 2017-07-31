#!/bin/bash

if [ "$#" -eq 0 ] || [ "-h" = "$1" ] || [ "--help" = "$1" ]; then
    echo "Usage : run script_file arg1 arg2 ..."
    exit 0
fi

script_file=$1
shift

if [ ! -x ${script_file} ] ; then
    chmod u+x ${script_file}
fi

if [ '/' == ${script_file:0:1} ] ; then
    ${script_file} $@
else
    ./${script_file} $@
fi

