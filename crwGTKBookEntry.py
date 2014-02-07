from gi.repository import Gtk

class GTKBookEntry(Gtk.Window):
    def __init__(self, parent=None):
        """A window to allow full text entry of new books."""
        
        print("Book Entry created")
        
        # create window
        Gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
            self.connect("destroy", parent.destroy)
        except AttributeError:
            self.connect("destroy", self.destroy)

        self.set_title("Books in Library")
        self.set_border_width(5)
        self.set_default_size(500, 250)

        vbox1 = Gtk.VBox(False, 4)
        self.add(vbox1)

# ISBN

        # add a horizontal box
        hbox1 = Gtk.HBox(False, 0)
        vbox1.pack_start(hbox1, expand=False, fill=False, padding=0)
        
        # add a label
        label1 = Gtk.Label("ISBN:")
        hbox1.pack_start(label1, expand=False, fill=False, padding=0)

        # add a text entry field
        self.isbn_entry = Gtk.Entry(max_length=0)
        self.isbn_entry.connect("activate",
            self.isbn_enter_callback, self.isbn_entry)
        hbox1.pack_start(self.isbn_entry, expand=False, fill=False, padding=0)

# TITLE

        # add a horizontal box
        hbox2 = Gtk.HBox(False, 0)
        vbox1.pack_start(hbox2, expand=False, fill=False, padding=0)
        
        # add a label
        label2 = Gtk.Label("Title:")
        hbox2.pack_start(label2, expand=False, fill=False, padding=0)

        # add a text entry field
        self.title_entry = Gtk.Entry(max_length=0)
        self.title_entry.connect("activate",
            self.title_enter_callback, self.title_entry)
        hbox2.pack_start(self.title_entry, expand=False, fill=False, padding=0)

# AUTHORS

        # add a horizontal box
        hbox3 = Gtk.HBox(False, 0)
        vbox1.pack_start(hbox3, expand=False, fill=False, padding=0)
        
        # add a label
        label3 = Gtk.Label("Authors:")
        hbox3.pack_start(label3, expand=False, fill=False, padding=0)

        # add a text entry field
        self.author_entry = Gtk.Entry(max_length=0)
        self.author_entry.connect("activate",
            self.author_enter_callback, self.author_entry)
        hbox3.pack_start(self.author_entry, expand=False, fill=False, padding=0)

# BUTTONS

        # add a horizontal box
        hbox4 = Gtk.HBox(False, 0)
        vbox1.pack_start(hbox4, expand=False, fill=False, padding=0)
        
        # add a query button
        self.add_button = Gtk.Button("Add")
        self.add_button.connect("clicked",
            self.add_callback, None)
        hbox4.pack_start(self.add_button, expand=True, fill=True, padding=0)

        # show stuff
        self.show_all()

    def isbn_enter_callback(self, widget, data=None):
        pass

    def title_enter_callback(self, widget, data=None):
        pass

    def author_enter_callback(self, widget, data=None):
        pass

    def add_callback(self, widget, data=None):
        pass

    def destroy(self, widget, data=None):
        Gtk.main_quit()

