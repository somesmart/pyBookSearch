#!/usr/bin/env python3
import csv

input_file = open("auto_library.csv", "r")
output_file = open("transposed_library.csv", "w")

headings = ("ISBN", "Title", "Author", "Binding", "Publisher", "Published")

reader = csv.DictReader(input_file, headings)
writer = csv.DictWriter(output_file, headings)

for book in reader:
    author = book["Author"]

    # Don't transpose lines with multiple authors.
    # Occasionally a semi-colon is used to separate last_name
    # from first_names, we can't reliably detect this, so
    # don't interfere.
    #
    if author.find(";") == -1:

        # Don't transpose lines that already have a comma.
        # We'll assume, here, that the last_name is already
        # listed first.
        #
        if author.find(",") == -1:
            # Split once, at first whitespace from RHS.
            #
            split_name = author.rsplit(None, 1)

            # Only transpose if we have more than one name.
            #
            if len(split_name) > 1:
                lastname_first = split_name[1] + ", " + split_name[0]
                print ("Converting ({}) -> ({})".format(author, lastname_first))
                book["Author"] = lastname_first

    writer.writerow(book)

input_file.close()
output_file.close()
