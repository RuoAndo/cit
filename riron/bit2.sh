#!/bin/sh

for i in `seq 0 15`
do
    result=`echo "obase=2;ibase=10;$i" | bc | xargs printf %04d`
    result2=`./hamming2 $result`
    echo $result $result2
done
