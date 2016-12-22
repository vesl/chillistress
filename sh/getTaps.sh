#!/bin/bash
TAPS=`ls /proc/sys/net/ipv4/conf/ |grep tap`
echo $TAPS
