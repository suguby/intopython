#!/bin/bash

cd `dirname $0` # this script in <PROJECT_PATH>/bin
cd ..
export PROJECT_PATH=`pwd`
cd `dirname $0`/..

PROFILE=${PROJECT_PATH}/bin/profile
source ${PROFILE}

if [ -n "${PYENV}" ]; then
    source ${WORKON_HOME}/${PYENV}/bin/activate
else
    if [ -f ${PROJECT_PATH}/env/bin/activate ]; then
        source ${PROJECT_PATH}/env/bin/activate
    else
        echo No PYENV in bin/profile or ${PROJECT_PATH}/env/ !
        exit 1
    fi
fi

source ${PROJECT_PATH}/bin/utils.sh

mkdir -p ${PROJECT_PATH}/extra

export MANAGE_SH=${PROJECT_PATH}/bin/manage.sh
export FAB_SH=${PROJECT_PATH}/bin/fab.sh


