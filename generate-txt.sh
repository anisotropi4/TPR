#!/usr/bin/env bash

ROUTE=$1

for i in ${ROUTE}/pdf/*.pdf
do
    FILESTUB=$(basename ${i} | sed 's/.pdf//' | sed 's/^pg_//')
    PDFPATH=${i}
    TXTPATH=./txt/${ROUTE}-${FILESTUB}.txt
    if [ ! -f ${TXTPATH} ]; then
        pdftotext -layout -nopgbrk ${PDFPATH} ${TXTPATH}
    fi
done
