#!/bin/bash

source `dirname $0`/set_enviroment.sh

if [ -z "$1" ]; then
    fab list
elif [ "$1" = "help" ]; then
    fab --help
else
    fab $*
fi
