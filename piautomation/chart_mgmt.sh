#!/bin/bash

d=`date +%m-%d-%Y`

cd /home/pi/Documents/automation/awtybot
mkdir /home/pi/Documents/automation/awtybot/stockcharts/${d}
echo "moving all .png and .csv files"
mv *.png /home/pi/Documents/automation/awtybot/stockcharts/${d}
mv *.csv /home/pi/Documents/automation/awtybot/stockcharts/${d} 
echo "files moved"
echo "running moneycall.py"
python3 /home/pi/Documents/automation/awtybot/moneycall.py
