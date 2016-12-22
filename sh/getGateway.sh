#!/bin/bash
GW=`ip r s |grep default`
if [ -z "$GW" ]; then 
	echo "0"
else 
	echo "1"
fi
