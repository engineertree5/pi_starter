#!/bin/bash

d=`date +%m-%d-%Y`

cd /home/pi/Documents/automation/awtybot
mkdir /home/pi/Documents/automation/awtybot/stockcharts/${d}
echo "moving all .png files"
mv *.png /home/pi/Documents/automation/awtybot/stockcharts/${d}
echo "files moved"
echo "running moneycall.py"
python3 /home/pi/Documents/automation/awtybot/moneycall.py
