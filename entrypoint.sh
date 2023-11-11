#!/bin/bash

if [ ! -f /mnt/config_weibo.ini ]; then
  echo 'Error: /mnt/config_weibo.ini file not found. Please mount the /mnt/config_weibo.ini file and try again.'
  exit 1
fi

cp -f /mnt/config_weibo.ini /app/config_weibo.ini
python -u main.py
