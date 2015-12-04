# pyBookSearch

A simple terminal or GTK+ based interface to add books to a library file.

Designed to aid entry of books by scanning or typing in their ISBN. A web
search then looks up details and the ISBN, Title, and Author are added to a CSV
file.

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
    Use text mode (not the GTK inteface)

## Dependencies

*   bs4 (BeautifulSoup, SoupStrainer)
*   collections
*   csv
*   (optional) gi.repository (Gtk, GObject)
*   html (entities)
*   json
*   optparse (OptionParser)
*   urllib (request, error, parse)
