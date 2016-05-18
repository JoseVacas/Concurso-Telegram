#!/bin/bash
/usr/local/bin/telegram-cli -k /home/pi/.src/tg/tg-server.pub -W -R -D -e "msg $1 $2" > /dev/null
