#!/usr/bin/env python

import gtk
import crwBook
import crwGTKLibrary

class GTKScannerEntry(gtk.Window):

    def __init__(self, parent=None):
        # create window
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect("destroy", self.destroy)

        self.set_title("Enter ISBN")
        self.set_border_width(5)

        self.web_searcher_list = []
        self.library_page = None

        # add a vertical box
        vbox1 = gtk.VBox(False, 4)
        self.add(vbox1)

        # add a label
        label1 = gtk.Label("Enter ISBN:")
        vbox1.pack_start(label1,
            expand=False, fill=False, padding=0)

        # add a text entry field
        self.isbn_entry = gtk.Entry(max=0)
        self.isbn_entry.connect("activate",
            self.isbn_enter_callback, self.isbn_entry)
        vbox1.pack_start(self.isbn_entry,
            expand=False, fill=False, padding=0)

        # add a quit button
        self.quit_button = gtk.Button("Quit")
        self.quit_button.connect_object("clicked",
            gtk.Widget.destroy, self)
        vbox1.pack_start(self.quit_button,
            expand=False, fill=False, padding=0)

        # show stuff
        self.show_all()

    def destroy(self, widget, data=None):
        print "Saving...",
        if self.library_page != None:
            self.library_page.save_to_file()
        gtk.main_quit()

    def isbn_enter_callback(self, widget, entry):
        isbn_text = entry.get_text()

        if self.library_page != None:
            print "ISBN exists:", self.library_page.isbn_exists(isbn_text)
            if len(self.web_searcher_list) > 0:
                for web_searcher in self.web_searcher_list:
                    book_description = web_searcher.search(isbn_text)
                self.library_page.add_book(book_description)
            else:
                self.library_page.add_book(crwBook.Book(isbn_text, "Unknown", "Unknown"))

        entry.set_text("")

    def add_library_page(self, library_page):
        self.library_page = library_page

    def add_web_searcher(self, web_searcher):
        self.web_searcher_list.append(web_searcher)

if __name__ == "__main__":
    libraryPage = crwGTKLibrary.GTKLibrary("library.csv")
    #isbnSearchOrg = ISBNSearchOrg()
    scanPage = GTKScannerEntry()
    scanPage.add_library_page(libraryPage)
    #scanPage.add_web_searcher(isbnSearchOrg)
    gtk.main()
