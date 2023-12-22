#!/usr/bin/env python

import argparse
import os
import re
from collections import defaultdict
from itertools import pairwise, tee
from os import walk

import pandas as pd

pd.set_option("display.max_columns", None)

PARSER = argparse.ArgumentParser(description="Extract data from PDFs")
PARSER.add_argument(
    "route", type=str, nargs="?", default="Kent-Sussex-Wessex", help="name of route"
)

ARGS, _ = PARSER.parse_known_args()
ROUTE = ARGS.route


def list_files(filepath):
    files = ()
    for d, _, filenames in walk(filepath):
        files = files + tuple("{}/{}".format(d, f) for f in filenames)
    return files


def get_page(filepath):
    p = re.compile("[._]")
    return p.split(filepath)[-2]


def prune_link(filepath):
    filestub = filepath.split("/")[1:]
    return "/".join(filestub)


def get_md(paths):
    return ["[{}]({})".format(get_page(p), prune_link(p)) for p in paths]


def get_md(file):
    _, route, page, _ = re.split(r"\W", file)
    return (route, page, file)


def write_md(filename, header, filedata, M=11):
    output = defaultdict(list)
    for j, *k in [get_md(i) for i in filedata]:
        output[j].append(k)
    with open(filename, "w", encoding="utf-8") as fout:
        fout.write(header)
        fout.write(f'|route|{"|".join(["page"] * M)}|\n')
        fout.write(f'|{"|".join(["----"] * (M+1))}|\n')
        for route, data in output.items():
            for k in [data[i:j] for i, j in pairwise(range(0, len(data) + M, M))]:
                text = "|".join([f"[{p}]({q})" for p, q in k])
                fout.write(f"|{route}|{text}|\n")


txtfile = sorted(list_files("txt"))
write_md("TPR-text.md", "# Unformatted text extracted from TPR PDFs\n\n", txtfile)
tsvfile = [i for i in sorted(list_files("lattice")) if os.path.getsize(i) > 0]
for tsv in tsvfile:
    try:
        df = pd.read_csv(tsv, sep="\t", dtype=object, header=None)
    except pd.errors.ParserError as err_msg:
        match_err = re.compile(r"Error tokenizing data. C error: Expected (\d+) fields in line (\d+), saw (\d+)")
        _, n, _ = map(int, match_err.search(str(err_msg)).groups())
        df = pd.read_csv(tsv, sep="\t", nrows=n-2, dtype=object, header=None)
    if df.empty:
        df = pd.read_fwf(tsv, dtype=object, header=None)
    df = df.dropna(how="all")
    df = df.dropna(how="all", axis=1)
    df = df.fillna("")
    df = df.replace(r"\s", " ")
    df.columns = [""] * df.shape[1] 
    if not df.empty:
        df.to_markdown(tsv.replace("lattice", "tsv"), index=False)

tsvfile = sorted(list_files("tsv"))
write_md("TPR-tsv.md", "# Formatted TSV extracted from TPR PDFs\n\n", tsvfile)
