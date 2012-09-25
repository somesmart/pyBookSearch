#!/usr/bin/env /usr/bin/python

SAVE_FILE = "auto_library.csv"

try:
    import gtk
    import crwGTKScannerEntry
    import crwGTKLibrary
    HAVE_GTK = True
except ImportError:
    print "### No GTK"
    import crwLibrary
    HAVE_GTK = False
import crwISBNSearch

if HAVE_GTK:
    library = crwGTKLibrary.GTKLibrary(SAVE_FILE)
else:
    library = crwLibrary.Library(SAVE_FILE)

isbnSearchOrg = crwISBNSearch.ISBNSearchOrg()

if HAVE_GTK:
    scanPage = crwGTKScannerEntry.GTKScannerEntry()
    scanPage.add_library_page(library)
    scanPage.add_web_searcher(isbnSearchOrg)
    gtk.main()
else:
    library.read_from_file()
    isbn = raw_input("Enter ISBN:")
    while isbn != "0":
        if isbn == "save":
            library.save_to_file()
        else:
            exists, book = library.isbn_exists(isbn)
            if exists:
                print book
                add_again = raw_input("### Book exists, do you want to search again?")
                if add_again == "y":
                    book = isbnSearchOrg.search(isbn)
                    library.add_book(book)
                    print book
            else:
                book = isbnSearchOrg.search(isbn)
                library.add_book(book)
                print book
        isbn = raw_input("Enter ISBN:")

    # Save before exiting
    library.save_to_file()
