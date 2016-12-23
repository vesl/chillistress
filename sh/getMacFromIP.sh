#!/bin/bash
MAC=`arp -an |grep $1 |awk '{print $4}'`
echo $MAC