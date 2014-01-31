#!/usr/bin/env python

import crwBook
import crwLibrary
from gi.repository import Gtk, GObject

(
    COLUMN_ISBN,
    COLUMN_TITLE,
    COLUMN_AUTHOR
) = range(3)

class GTKLibrary(Gtk.Window, crwLibrary.Library):
    def __init__(self, filename, parent=None):
        # create window
        Gtk.Window.__init__(self)

        # create library
        crwLibrary.Library.__init__(self, filename)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect("destroy", self.destroy)

        self.set_title("Books in Library")
        self.set_border_width(5)
        self.set_default_size(500, 250)

        vbox1 = Gtk.VBox(False, 4)
        self.add(vbox1)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox1.pack_start(sw, expand=True, fill=True, padding=0)

        # create book model
        self.book_model = Gtk.ListStore(
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING)

        # fill the model from file
        self.read_from_file()

        # create tree view
        self.tree_view = Gtk.TreeView(self.book_model)
        # hint across rows
        self.tree_view.set_rules_hint(True)
        #
        self.tree_view.set_search_column(COLUMN_ISBN)

        sw.add(self.tree_view)

        # add columns to the tree view
        self.__add_columns()

        # add a horizontal box
        hbox1 = Gtk.HBox(False, 0)
        vbox1.pack_start(hbox1,
            expand=False, fill=False, padding=0)
        
        # add a save button
        self.save_button = Gtk.Button("Save")
        self.save_button.connect("clicked",
            self.save_callback, None)
        hbox1.pack_start(self.save_button,
            expand=True, fill=True, padding=0)

        # add a delete button
        self.delete_button = Gtk.Button("Delete")
        self.delete_button.connect("clicked",
            self.delete_callback, None)
        hbox1.pack_start(self.delete_button,
            expand=True, fill=True, padding=0)

        # show stuff
        self.show_all()

    def __add_columns(self):
        # column for ISBN
        column = Gtk.TreeViewColumn(crwBook.STR_ISBN,
            Gtk.CellRendererText(), text=COLUMN_ISBN)
        column.set_sort_column_id(COLUMN_ISBN)
        column.set_resizable(True)
        self.tree_view.append_column(column)

        # column for title
        column = Gtk.TreeViewColumn(crwBook.STR_TITLE,
            Gtk.CellRendererText(), text=COLUMN_TITLE)
        column.set_sort_column_id(COLUMN_TITLE)
        column.set_resizable(True)
        self.tree_view.append_column(column)

        # column for author
        column = Gtk.TreeViewColumn(crwBook.STR_AUTHOR,
            Gtk.CellRendererText(), text=COLUMN_AUTHOR)
        column.set_sort_column_id(COLUMN_AUTHOR)
        column.set_resizable(True)
        self.tree_view.append_column(column)

    def destroy(self, widget, data=None):
        print "Saving...",
        self.save_to_file()
        Gtk.main_quit()

    def save_callback(self, widget, data=None):
        self.save_to_file()

    def delete_callback(self, widget, data=None):
        ''' The remove_isbn call removes all entries, the model remove only removes one.
            It would also be better if the overloaded remove_isbn function actually did
            the remove from the model.
        '''
        print "Delete - logic wrong"
        selection = self.tree_view.get_selection()
        (model, iter) = selection.get_selected()
        isbn = model.get(iter, 0)[0]
        self.remove_isbn(isbn)
        model.remove(iter)

    def add_book(self, book):
        # Call the super class function
        super(GTKLibrary, self).add_book(book)

        # Add it to the model
        iter = self.book_model.append()
        self.book_model.set(iter,
            COLUMN_ISBN, book.get_isbn(),
            COLUMN_TITLE, book.get_title(),
            COLUMN_AUTHOR, book.get_author())
        self.tree_view.scroll_to_cell(
            path=self.book_model.get_path(iter),
            use_align=True)

    def remove_book(self, book):
        super(GTKLibrary, self).remove_book(book)

    def remove_isbn(self, isbn):
        super(GTKLibrary, self).remove_isbn(isbn)

    def read_from_file(self):
        # Call the super class function
        super(GTKLibrary, self).read_from_file()
        
        for book in self.book_list:
            iter = self.book_model.append()
            self.book_model.set(iter,
                COLUMN_ISBN, book.get_isbn(),
                COLUMN_TITLE, book.get_title(),
                COLUMN_AUTHOR, book.get_author())

if __name__ == "__main__":
    gtkLibrary = GTKLibrary("library.csv")
    gtkLibrary.add_book(crwBook.Book("9876", "9876", "9876"))
    gtk.main()
