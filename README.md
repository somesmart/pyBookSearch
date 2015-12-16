# pyBookSearch

A simple terminal or GTK+ based interface to add books to a library file.

Designed to aid entry of books by scanning or typing in their ISBN or LCCN. A
web search then looks up details and the results (including the ISBN, Title,
and Author) are added to a CSV file.

Books may also be added manually in the GTK interface.

The interface is optimised for efficient repeated book entry:

*   pick up book
*   scan ISBN
*   put down book
*   repeat

Some ancilliary routines for post-processing are also included.

The main program is called my_library.py, use the --help option to get current
command line options. At this time the two main options are:

*   -l FILE or --library=FILE
    Specify the file to use for the CSV output.
*   -t or --text
    Use text mode (not the GTK interface)
*	-d DELIMITER or --delimit=DELIMITER
	Specify the delimiter to use in the CSV file (default: |)
*   -f or --fill
    Fill all book fields from as many sources as is needed
*   -r or --requery
    Not yet implemented. Re-query all books in the library
*   -n or --no-questions
    Don't ask any questions, useful for redirected input

## Dependencies

*   bs4 (BeautifulSoup, SoupStrainer)
*   (optional) gi.repository (Gtk, GObject)
*   (optional) fuzzywuzzy
*   various stuff from the standard library
