#!/bin/bash
tcpdump -i eth1 -n | grep 'IP.*length [0-9^\n]*' | while read args; do python `pwd`/dbdump.py $args; done;
