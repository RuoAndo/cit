#!/bin/sh

for i in `seq 0 15`
do
    echo "obase=2;ibase=10;$i" | bc | xargs printf %04d
    echo ""
done
