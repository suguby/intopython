#!/bin/bash

source `dirname $0`/set_enviroment.sh

export PYTHONDONTWRITEBYTECODE=x
cd ${PROJECT_PATH}

if [ -z "$*" ]; then
    echo ""
    echo "Run manage.py with DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} settings "
    echo ""
    echo "Usage: $0 <subcommand>"
    echo ""
    ask "Show manage.py help?" 'exit'
    python ${PROJECT_PATH}/manage.py
else
    python ${PROJECT_PATH}/manage.py $*
fi
