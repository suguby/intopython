#!/bin/bash



uwsgi_pids() {
    PIDS=`ps -ef | grep 'uwsgi' | grep '/home/design' | grep -v grep | grep -v '.sh' | awk '{print($2)}'`
}


action_stop() {
    uwsgi_pids
    if [ -n "${PIDS}" ] ; then
        kill -9 ${PIDS}
        echo Uwsgi at ${PIDS} killed...
    fi
}

action_start() {
    source ~/python_enviroments/intopython_env/bin/activate
    uwsgi --ini ~/intopython/extra/uwsgi.ini
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
	touch ~/intopython/extra/uwsgi.reload
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
