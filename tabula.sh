#!/bin/sh
TABULA=1.0.5
TABULAFILE=tabula-${TABULA}-jar-with-dependencies.jar

if [ ! -f ${TABULAFILE} ]; then
    echo downloading ${TABULAFILE}
    curl -L https://github.com/tabulapdf/tabula-java/releases/download/v${TABULA}/${TABULAFILE} -o ${TABULAFILE} 
fi

ROUTE=$1
cd ${ROUTE}

if [ ! -d pdf ]; then
    echo No pdf directory
    exit 1
fi

for FILESTUB in $(cd pdf; ls *.pdf | sed 's/.pdf//')
do
    OUTFILE=$(echo ${ROUTE}-${FILESTUB}.tsv | sed 's/pg_//')
    echo ${OUTFILE}
    #if [ ! -s stream/${FILE}.tsv ]; then
    #    java -Dfile.encoding=utf-8 -Xms256M -Xmx2048M -jar ../${TABULAFILE} -t -f TSV -o ../stream/${OUTFILE} pdf/${FILE}.pdf
    #fi
    if [ ! -f ../lattice/${OUTFILE} ]; then
        java -Dfile.encoding=utf-8 -Xms256M -Xmx2048M -jar ../${TABULAFILE} -l -f TSV -o ../lattice/${OUTFILE} pdf/${FILESTUB}.pdf
        if [ ! -s ../lattice/${OUTFILE} ]; then
            echo WARNING: processing lattice "pdf ${OUTFILE}.pdf" with page cut
            java -Dfile.encoding=utf-8 -Xms256M -Xmx2048M -jar ../${TABULAFILE} -l --area 100,0,3500,2500 -f TSV -o ../lattice/${OUTFILE} pdf/${FILESTUB}.pdf
        fi
    fi
done
