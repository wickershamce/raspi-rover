#!/usr/bin/env bash

# check if pigpiod is already running. if it is, pass, if not, start it
if pgrep -x "pigpiod" > /dev/null
then
  echo "pigpiod already running"
else
  echo "pigpiod is not running. starting it..."
  sudo pigpiod      # run gpio daemon
fi

# run main python script
python ~/raspi-rover/python/rover.py
