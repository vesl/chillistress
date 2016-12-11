#!/bin/sh
echo `ifconfig $1 |head -n1 |awk '{print $5}'`
