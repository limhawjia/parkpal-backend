#!/bin/bash

printenv | sed 's/^\(.*\)$/export \1/g' > /root/project_env.sh
python -m main.startup

if [ -z "$CRON_FREQUENCY" ]
then
  echo "CRON_FREQUENCY environment variable not set, defaulting to 1 minute."
else
  sed -i "s/\* \* \* \* \*/\*\/$CRON_FREQUENCY \* \* \* \*/g" ./cron
fi

cron -f
