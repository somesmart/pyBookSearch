#!/usr/bin/env /usr/bin/python3

import sys
import os
import argparse

try:
    from gi.repository import Gtk
    import crwGTKLibrary
    HAVE_GTK = True
except ImportError:
    print("### No GTK - reverting to text mode")
    HAVE_GTK = False

import crwBook
import crwLibrary
from crwISBNSearch import Modes, ISBNSearchOrg, OpenLibraryOrg

# ==========================

__all__ = []
__version__ = 0.2
__date__ = '2015-12-10'
__updated__ = '2015-12-10'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

TEXT_HELP = '''
[h | help]     - show this help
[0 | q | quit] - save and exit
[s | save]     - save
[i | isbn]     - ISBN search mode (default)
[c | lccn]     - LCCN search mode
'''


def main(argv=None):
    '''Command line options.'''

    global HAVE_GTK

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%1.2f" % __version__
    program_build_date = "%s" % __updated__

    program_desc = '''Search for book information by ISBN and add to a library CSV file.'''

    program_epilog = """{} {} ({})
Copyright 2013, 2014, 2015 Chris Willoughby and contributors
Licensed under the Apache License 2.0
http://www.apache.org/licenses/LICENSE-2.0""".format(
        program_name, program_version, program_build_date)

    try:
        # setup argument parser
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=program_epilog,
            description=program_desc)

        parser.add_argument(
            "-l", "--library",
            dest="libfile",
            default='auto_library.csv',
            help="set library file path (default: %(default)s)",
            metavar="FILE")
        parser.add_argument(
            "-t", "--text",
            action="store_true",
            dest="textmode",
            default=False,
            help="use text mode (default: %(default)s)")
        parser.add_argument(
            "-d", "--delimit",
            dest="delimiter",
            default="|",
            help="set the CSV delimiter (default: %(default)s)")
        parser.add_argument(
            "-f", "--fill",
            action="store_true",
            dest="fill",
            default=False,
            help="automatically fill missing details from multiple sources (default: %(default)s)")
        parser.add_argument(
            "-r", "--requery",
            action="store_true",
            dest="requery",
            default=False,
            help="automatically requery the entire library file, filling in missing details (default: %(default)s)")

        # process options
        args = parser.parse_args()

        if args.libfile:
            print("Library File: {}".format(args.libfile))

        print("Text mode:", args.textmode)
        if args.textmode:
            HAVE_GTK = False

        if args.delimiter:
            print("Delimiter: {}".format(args.delimiter))

        print("Fill mode:", args.fill)
        print("Re-query:", args.requery)

    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2

    # Create some searcher objects
    isbnSearchOrg = ISBNSearchOrg()
    openLibraryOrg = OpenLibraryOrg()

    # Put them in lists for ordered processing
    searchers = {
        Modes.ISBN: [isbnSearchOrg, openLibraryOrg],
        Modes.LCCN: [openLibraryOrg]
    }

    if HAVE_GTK:
        library = crwGTKLibrary.GTKLibrary(
            filename=args.libfile,
            searcher=isbnSearchOrg,
            delimiter=args.delimiter)
        Gtk.main()
    else:
        library = crwLibrary.Library(
            filename=args.libfile,
            delimiter=args.delimiter)
        library.read_from_file()
        print('You have {} books in your library.'.format(library.book_count))
        print(TEXT_HELP)

        def find_book(mode, value):

            fill = args.fill
            # Create an empty book
            book = crwBook.Book(isbn=value)

            # Iterate through the searchers for the mode
            for searcher in searchers[mode]:

                print("Checking for the {} at {}... ".format(
                    mode.name, searcher.name))

                # TODO: This doesn't yet cope will fill mode as it
                # will unconditionally overwrite known fields.
                book = searcher.search(
                    isbn=value,
                    mode=mode,
                    book=book,
                    fill=fill)

                if book.has_unknowns:
                    book.display_unknowns()

                if book.author != crwBook.UNKNOWN and not fill:
                    break
                elif book.has_unknowns and fill:
                    print("Attempting to fill unknown values...")
                else:
                    print('\tNot found')

            library.add_book(book)
            print(book)

        mode = Modes.ISBN
        try:
            isbn = input("Enter {}:".format(mode.name))
        except EOFError:
            # When using redirected input, don't bomb out on EOF
            isbn = 'q'

        while (isbn != '0') and (isbn != 'q') and (isbn != 'quit'):
            if isbn == "save" or isbn == 's':
                library.save_to_file()
            elif isbn == 'help' or isbn == 'h':
                print(TEXT_HELP)
            elif isbn == 'isbn' or isbn == 'i':
                mode = Modes.ISBN
                print("Searching by {}".format(mode.name))
            elif isbn == 'lccn' or isbn == 'c':
                mode = Modes.LCCN
                print('Searching by {}'.format(mode.name))
            else:
                exists, book = library.isbn_exists(isbn)
                if exists:
                    print(book)
                    add_again = input("### Book exists, do you want to search again?")
                    if add_again == "y":
                        find_book(mode, isbn)
                else:
                    find_book(mode, isbn)
            try:
                isbn = input("Enter {}:".format(mode.name))
            except EOFError:
                # When using redirected input, don't bomb out on EOF
                isbn = 'q'

        # Save before exiting
        library.save_to_file()

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'show_db_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
