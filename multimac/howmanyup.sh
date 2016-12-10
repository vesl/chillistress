#!/bin/sh
echo `ip addr sh |grep tap|awk '{print $2}' |wc -l` 2>/dev/null
exit 0
