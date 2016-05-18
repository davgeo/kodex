#!/bin/sh
# Synology DSM bootup script for Gunicorn webserver running Ananke
PACKAGE="ananke"
EXEC_DIR="/volume1/scripts/ananke/ananke"

WSGI_EXEC="${PACKAGE}.wsgi"
PID_FILE="/var/run/${PACKAGE}.pid"

GUNICORN_EXEC="/volume1/@appstore/py3k/usr/local/bin/gunicorn"
BIND_IP='0.0.0.0:8000'

start_daemon()
{
  cd ${EXEC_DIR}
  ${GUNICORN_EXEC} ${WSGI_EXEC} -w 2 --bind ${BIND_IP} --pid ${PID_FILE} --reload --daemon
}

stop_daemon()
{
  kill `cat ${PID_FILE}`
  wait_for_status 1 20 || kill -9 `cat ${PID_FILE}`
  rm -f ${PID_FILE}
}

daemon_status ()
{
  if [ -f ${PID_FILE} ] && kill -0 `cat ${PID_FILE}` > /dev/null 2>&1; then
    return
  fi
  rm -f ${PID_FILE}
  return 1
}

wait_for_status ()
{
  counter=$2
  while [ ${counter} -gt 0 ]; do
    daemon_status
    [ $? -eq $1 ] && return
    let counter=counter-1
    sleep 1
  done
  return 1
}

case "$1" in
  start)
    if daemon_status; then
      echo "${PACKAGE} is already running"
    else
      echo "Starting ${PACKAGE} ..."
      start_daemon
    fi
   ;;
  stop)
    if daemon_status; then
      echo "Stopping ${PACKAGE} ..."
      stop_daemon
    else
      echo "${PACKAGE} is not running"
    fi
    ;;
   status)
    if daemon_status; then
      echo "${PACKAGE} is running"
    else
      echo "${PACKAGE} is not running"
      exit 1
    fi
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
    exit 1
esac

exit 0