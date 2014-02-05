#!/usr/bin/env /usr/bin/python


import sys
import os
from optparse import OptionParser

try:
    from gi.repository import Gtk
    import crwGTKLibrary
    HAVE_GTK = True
except ImportError:
    print "### No GTK - reverting to text mode"
    HAVE_GTK = False

import crwLibrary
import crwISBNSearch

# ==========================

__all__ = []
__version__ = 0.1
__date__ = '2014-01-30'
__updated__ = '2014-01-30'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def main(argv=None):
    '''Command line options.'''
    
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%1.2f" % __version__
    program_build_date = "%s" % __updated__
 
    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    program_longdesc = '''Search for ISBN and add to library file.'''
    program_license = "Copyright 2013 Chris Willoughby (Home)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"
 
    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-l", "--library", dest="libfile", help="set library file path [default: %default]", metavar="FILE")
        parser.add_option("-t", "--text", action="store_true", dest="textmode", default=False, help="use text mode [default: %default]")
        
        # set defaults
        parser.set_defaults(libfile="./auto_library.csv")
        
        # process options
        (opts, args) = parser.parse_args(argv)
        
        if opts.libfile:
            print("libfile = %s" % opts.libfile)

        print "Text mode", opts.textmode
        if opts.textmode:
            HAVE_GTK = False

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
            
    isbnSearchOrg = crwISBNSearch.ISBNSearchOrg()
        
    if HAVE_GTK:
        library = crwGTKLibrary.GTKLibrary(filename=opts.libfile, searcher=isbnSearchOrg)
        Gtk.main()
    else:
        library = crwLibrary.Library(opts.libfile)
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
