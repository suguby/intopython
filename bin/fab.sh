#!/bin/bash

cd `dirname $0`
cd ..
export DJANGO_SETTINGS_MODULE="intopython.settings"
export PYTHONWARNINGS=ignore
export PYTHONPATH=${PYTHONPATH}:`pwd`
fab $*
