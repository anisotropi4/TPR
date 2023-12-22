#!/usr/bin/env python

import argparse
import re
from os import path, walk
from pathlib import Path

import pandas as pd

pd.set_option('display.max_columns', None)

def string_in_file(string, filepath, rline=False):
    with open(filepath, "r", encoding="utf-8") as file_in:
        for i, line in enumerate(file_in):
            if string in line.lower().strip():
                if rline:
                    return (filepath, line.strip())
                return filepath
            if i > 128:
                return None
    return None

def list_string_file(filepath, text):
    files = ()
    for d, _, filenames in walk(filepath):
        files = files + tuple(f"{d}/{f}" for f in filenames if text in f)
    return sorted(files)

def get_files(string, this_path):
    files = ()
    for d, _, filenames in walk(this_path):
        for filename in filenames:
            filepath = string_in_file(string.lower(), d + "/" + filename)
            if filepath:
                files += (filepath,)
    return sorted(files)

def get_files2(filepath, route, string):
    r = ()
    for filename in list_string_file(filepath, route):
        s = string_in_file(string.lower(), f"{filename}")
        if s:
            r += (s,)
    return sorted(r)

def get_filelist(route):
    fpath = "txt"
    start_file = get_files2(fpath, route, "5.4 platform lengths")
    if not start_file:
        return []
    start_file = start_file.pop()
    end_file = get_files2(fpath, route, "5.4.1 loop lengths")
    if not end_file:
        return []
    end_file = end_file.pop()
    filelist = list_string_file(fpath, route)
    filelist = sorted([i for i in filelist if i >= start_file and i <= end_file])
    return filelist


PARSER = argparse.ArgumentParser(description="Scrape platform data from TSVs")

def write_xlsx(df):
    filepath = "platform-length.xlsx"
    with pd.ExcelWriter(
        filepath
    ) as writer:  # pylint: disable=abstract-class-instantiated
        df.to_excel(writer, "platform_length", index=False)

def main():
    output = []
    for route in ["AR", "EM", "KT", "LNE", "NAT", "NWC", "SC", "SX", "WW", "WX",]:
        filelist = [i.replace("txt", "lattice", 1).replace("txt", "tsv") for i in get_filelist(route)]
        for filepath in filelist:
            if path.getsize(filepath) == 0:
                continue
            try:
                r = pd.read_csv(filepath, sep="\t", header=None)
            except pd.errors.ParserError as err_msg:
                match_err = re.compile(r"Error tokenizing data. C error: Expected (\d+) fields in line (\d+), saw (\d+)")
                _, n, _ = map(int, match_err.search(str(err_msg)).groups())
                r = pd.read_csv(filepath, sep="\t", header=None, nrows=n-1, dtype=object)            
            r = r.dropna(how="all")
            r[0] = r[0].ffill()
            r = r.replace(r"\r", " ", regex=True)
            text = r.iloc[:, 2].astype(str).str.lower()
            if (text.str.find("length slu") > 0).any():
                continue
            try:
                r.columns = ["station", "platform", "usable length [m]", "notes"]
            except ValueError:
                continue
            page = filepath.split("-").pop().split(".").pop(0)
            ix = r["station"].str.lower() == "station"
            r = r[~ix]
            text = r["station"].astype(str).str.lower()
            ix = text.str.find(" routes") > -1
            if ix.any():
                r = r[~ix]
            text = r["usable length [m]"].astype(str).str.lower()
            ix = text.str.find("in metres") > -1
            if ix.any():
                r = r[~ix]
            ix = text.str.find(" platform ") > -1
            if ix.any():
                r[ix] = r[ix].values[:, [0, 3, 1, 2]]
            r[["route", "page"]] = [route, page]
            r = r.fillna("")
            column = ["route", "page", "station", "platform", "usable length [m]", "notes"]
            output.append(r[column])
    df = pd.concat(output).reset_index(drop=True)
    df.to_csv("platform-length.tsv", sep="\t", index=False)
    write_xlsx(df)

if __name__ == "__main__":
    main()
