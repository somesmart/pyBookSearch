#!/usr/bin/env python
import csv

input_file = open("auto_library.csv", "rb")
output_file = open("library.xml", "wb")

csv_reader = csv.DictReader(input_file)

output_file.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
output_file.write("<library>\n")

for line in csv_reader:
    output_file.write("<book><isbn>" +
                      line["ISBN"].decode("iso-8859-1").encode("utf-8") +
                      "</isbn><title>" +
                      line["Title"].decode("iso-8859-1").encode("utf-8") +
                      "</title><author>" +
                      line["Author"].decode("iso-8859-1").encode("utf-8") +
                      "</author></book>\n")

output_file.write("</library>\n")
