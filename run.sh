#!/bin/bash

IFS=$'\012'

export TPRDIR=${PWD}
export PATH=${PATH}:${NESADIR}

if [ ! -d venv ]; then
    echo Set up python3 virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
else
    source venv/bin/activate
fi

if [ ! -s section-list.json ]; then
    for FILEPATH in $(ls download/*.pdf)
    do
        FILENAME=$(basename ${FILEPATH})
        ROUTE=$(echo ${FILENAME} | sed 's/.*TPR 2024 [^ ]* \([^ ]*\).pdf/\1/')
        echo "{"\"${ROUTE}\": \"${FILENAME}\""}"
    done | jq -cs '.' > section-list.json
fi

for i in txt lattice
do
    if [ ! -d ${i} ]; then
        mkdir -p ${i}
    fi
done

for ROUTE in $(jq -r '.[] | keys[]' section-list.json)
do
    echo Processing ${ROUTE}
    for i in pdf images tsv 
    do
        if [ ! -d ${ROUTE}/${i} ]; then
            mkdir -p ${ROUTE}/${i}
        fi
    done
    ./pdf-separate.sh ${ROUTE}
    echo Process ${ROUTE} PDF pages
    ./generate-txt.sh ${ROUTE}
    ./tabula.sh ${ROUTE}
    find lattice -type f -size 0 -name \*.tsv -exec rm {} \;
done


