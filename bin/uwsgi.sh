#!/bin/bash

source `dirname $0`/set_enviroment.sh

uwsgi_pids() {
    PIDS=`ps -ef | grep 'uwsgi' | grep ${PROJECT_PATH} | grep -v grep | grep -v '.sh' | awk '{print($2)}'`
}


action_stop() {
    uwsgi_pids
    if [ -n "${PIDS}" ] ; then
        kill -9 ${PIDS}
        echo Uwsgi at ${PIDS} killed...
    fi
}

action_start() {
    uwsgi --ini ${PROJECT_PATH}/extra/uwsgi.ini
}

case "$1" in
  start)
	action_start
        ;;
  stop)
	action_stop
	echo Uwsgi stopped
        ;;
  reload)
	touch ${PROJECT_PATH}/extra/uwsgi.reload
        ;;
  restart)
	action_stop
	action_start
        ;;
  respawn)
	uwsgi_pids
	if [ -z "${PIDS}" ]; then
		action_start
		echo `date`, uwsgi respawned
	fi
        ;;
  *)
	echo "Usage: {start|stop|restart|reload|respawn}" >&2
	exit 3
        ;;
esac
