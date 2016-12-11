#!/bin/sh
echo `ifconfig |grep tap | wc -l`
