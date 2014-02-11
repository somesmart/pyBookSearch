
from gi.repository import Gtk

class GTKBookEntry(Gtk.Dialog):
    def __init__(self, parent):
        """A dialog to allow full text entry of new books."""
        
        print("Book Entry created")
        
        # create dialog
        Gtk.Dialog.__init__(self,
            title="Add book",
            parent=parent,
            flags=Gtk.DialogFlags.DESTROY_WITH_PARENT,
            buttons=(Gtk.STOCK_ADD, Gtk.ResponseType.YES, Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE))

        self.connect("delete-event", self.on_delete_event)
        self.add_button = self.action_area.get_children()[1]
        self.add_button.connect("clicked", self.add_callback)
        self.close_button = self.action_area.get_children()[0]
        self.close_button.connect("clicked", self.close_callback)

#        try:
#            self.set_screen(parent.get_screen())
#            self.connect("destroy", parent.destroy)
#        except AttributeError:
#            self.connect("destroy", self.destroy)

#        self.set_title("Books in Library")
        self.set_border_width(5)
#        self.set_default_size(500, 250)

        box = self.get_content_area()
#        vbox1 = Gtk.VBox(False, 4)
#        self.add(vbox1)

# ISBN

        # add a horizontal box
        hbox1 = Gtk.HBox(False, 0)
        box.pack_start(hbox1, expand=False, fill=False, padding=0)
        
        # add a label
        label1 = Gtk.Label("ISBN:")
        hbox1.pack_start(label1, expand=False, fill=False, padding=0)

        # add a text entry field
        self.isbn_entry = Gtk.Entry(max_length=0)
        self.isbn_entry.connect("activate", self.isbn_enter_callback, self.isbn_entry)
        hbox1.pack_start(self.isbn_entry, expand=True, fill=True, padding=0)

# TITLE

        # add a horizontal box
        hbox2 = Gtk.HBox(False, 0)
        box.pack_start(hbox2, expand=False, fill=False, padding=0)
        
        # add a label
        label2 = Gtk.Label("Title:")
        hbox2.pack_start(label2, expand=False, fill=False, padding=0)

        # add a text entry field
        self.title_entry = Gtk.Entry(max_length=0)
        self.title_entry.connect("activate", self.title_enter_callback, self.title_entry)
        hbox2.pack_start(self.title_entry, expand=True, fill=True, padding=0)

# AUTHORS

        # add a horizontal box
        hbox3 = Gtk.HBox(False, 0)
        box.pack_start(hbox3, expand=False, fill=False, padding=0)
        
        # add a label
        label3 = Gtk.Label("Authors:")
        hbox3.pack_start(label3, expand=False, fill=False, padding=0)

        # add a text entry field
        self.author_entry = Gtk.Entry(max_length=0)
        self.author_entry.connect("activate", self.author_enter_callback, self.author_entry)
        hbox3.pack_start(self.author_entry, expand=True, fill=True, padding=0)

# BUTTONS

        # add a horizontal box
#        hbox4 = Gtk.HBox(False, 0)
#        box.pack_start(hbox4, expand=False, fill=False, padding=0)
        
        # add an Add button
#        self.add_button = Gtk.Button("Add")
#        self.add_button.connect("clicked",
#            self.add_callback, None)
#        hbox4.pack_start(self.add_button, expand=True, fill=True, padding=0)

        # show stuff
        self.show_all()

    def isbn_enter_callback(self, widget, data=None):
        self.title_entry.grab_focus()

    def title_enter_callback(self, widget, data=None):
        self.author_entry.grab_focus()

    def author_enter_callback(self, widget, data=None):
        self.add_button.grab_focus()

    def add_callback(self, widget, data=None):
        print ("Add")
        self.isbn_entry.grab_focus()

    def close_callback(self, widget, data=None):
        print ("Close")
        self.hide()

    def on_delete_event(self, widget, data=None):
        return self.hide_on_delete()

    def destroy(self, widget, data=None):
        Gtk.main_quit()

