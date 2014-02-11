#!/usr/bin/env python
import csv

input_file = open("auto_library.csv", "rb")
output_file = open("auto_library_utf8.csv", "wb")

headings = ("ISBN", "Title", "Author")

reader = csv.DictReader(input_file, headings)
writer = csv.DictWriter(output_file, headings)

for book in reader:
    isbn = book["ISBN"].decode("iso-8859-1")
    title = book["Title"].decode("iso-8859-1")
    author = book["Author"].decode("iso-8859-1")

    book["ISBN"] = isbn.encode("utf-8")
    book["Title"] = title.encode("utf-8")
    book["Author"] = author.encode("utf-8")

    writer.writerow(book)

input_file.close()
output_file.close()
