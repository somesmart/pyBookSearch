#!/usr/bin/env python3

STR_ISBN = "ISBN"
STR_TITLE = "Title"
STR_AUTHOR = "Author"

class Book(object):
    def __init__(self, isbn, title=None, author=None):
        ''' Converts all inputs to unicode, and stores them.
        '''
        try:
            # The ISBN
            self.u_isbn = isbn.strip()

            # The Title
            if title != None:
                self.u_title = title.strip()

            # The Author
            if author != None:
                self.u_author = author.strip()

        except AttributeError:
            print("### Could not set book fields.")

    def set_isbn(self, isbn):
        try:
            self.u_isbn = isbn.strip()
        except AttributeError:
            print("### Could not set ISBN")
            self.u_isbn = "AttributeError"

    def get_isbn(self):
        return self.u_isbn

    def set_title(self, title):
        try:
            self.u_title = title.strip()
        except AttributeError:
            print("### Could not set title")
            self.u_title = "AttributeError"

    def get_title(self):
        return self.u_title

    def set_author(self, author):
        try:
            self.u_author = author.strip()
        except AttributeError:
            print("### Could not set author")
            self.u_author = "AttributeError"

    def get_author(self):
        return self.u_author

    def __repr__(self):
        return 'crwBook.Book("' + self.u_isbn + \
               '", "' + self.u_title + \
               '", "' + self.u_author + \
               '")'

    def __str__(self):
        return "ISBN:" + self.u_isbn + \
               ", Title:" + self.u_title + \
               ", Author:" + self.u_author

if __name__ == "__main__":
    book = Book(" 0586039899 ", " The Fabulous Riverboat", "  Philip Jos\u00e9 Farmer")
    print(book)
