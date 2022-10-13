#!/bin/sh

while read line; do
    echo $line
done < $1
