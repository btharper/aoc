#!/bin/bash

for day in "$@"
do
    mkdir -p ${day}
    if [ ! -e ${day}/${day}.py ]
    then
        sed "s/dXXX/${day}/" ../templates/template.py > ${day}/${day}.py
    fi
done
