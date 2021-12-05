#!/bin/bash

for day in "$@"
do
    mkdir -p ${day}
    if [ ! -e ${day}/${day}.py ]
    then
        sed "s/dXXX/${day}/" template.py > ${day}/${day}.py
    fi
done
