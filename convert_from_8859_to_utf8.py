#!/usr/bin/env python3
import argparse
import csv

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Read in a file as iso-8859, write to an output file as utf-8')

parser.add_argument(
    dest="inputfile",
    default=None,
    help="The iso-8859 input file (default: %(default)s)",
    metavar="inputfile")

parser.add_argument(
    dest="outputfile",
    default=None,
    help="The utf-8 output file (default: %(default)s)",
    metavar="outputfile")

# process options
args = parser.parse_args()

input_file = open(args.inputfile, "rt")
output_file = open(args.outputfile, "wt")

# headings = ("ISBN", "Title", "Author")

reader = csv.DictReader(input_file)
print(reader.fieldnames)
writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)

for book in reader:
    for f in reader.fieldnames:
        book[f] = book[f].decode("iso-8859-1").encode("utf-8")
    writer.writerow(book)

input_file.close()
output_file.close()
