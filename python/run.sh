#! /bin/sh

now=`date +"%Y-%m-%d %H:%M:%S"`
echo "${now} Web-spider start" >> log/stdout.log
nohup python web-spider.py 2>&1 >> log/stdout.log &

