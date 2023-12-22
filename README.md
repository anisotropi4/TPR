# TPR
A scrape of the Network Rail Timetable Planning Rules (TPR)

## The Rail Timetable Planning Rules (TPR) for the British rail network
The Network Rail [Timetable Planning Rules](https://www.networkrail.co.uk/industry-and-commercial/information-for-operators/operational-rules/) are used to regulate the standard timings between stations and junctions together with other matters enabling trains to be scheduled into the working timetable for the various parts of the main rail network. However, as this consists of ~10 PDF file for each calendar yeary, their use is significantly restricted.

This respository uses scripts in `shell`, `python` and the [`Tabula`](https://github.com/tabulapdf) project to liberate data and tables trapped inside these PDF files for a given year.

With all data extracted to unstructured text files and the tabular data into Tab Seperated Variable (TSV) files.

## Data Extract
To extract the data

1. download the set of TPR PDF files for the year of interest.
2. execute the bundled data extract scripts:

```{bash}
$ ./run.sh
```

This creates unstructure text files named `<route code>-<page number>.txt` in the `txt` directory, and TSV files named `<route code>-<page number>.tsv`in the `lattice` directory.

## Data

A link to the raw text is [here]("TPR-txt.md"), and a markdown representation of the TSV files is [here]("TPR-tsv.md")


## Acknowledgment
The data is copyright © 2023 Network Rail, and used with thanks to Network Rail for making this data available.
