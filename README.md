# pyBookSearch

A simple terminal or GTK+ based interface to add books to a library file.

Designed to aid entry of books by scanning or typing in their ISBN. A web search then looks up details
and the ISBN, Title, and Author are added to a CSV file.

Books may also be added manually.

The interface is optimised for efficient repeated book entry.

Some ancilliary routines for post-processing are also included.

## Dependencies

*   bs4 (BeautifulSoup, SoupStrainer)
*   collections
*   csv
*   gi.repository (Gtk, GObject)
*   html (entities)
*   json
*   optparse (OptionParser)
*   urllib (request, error, parse)
