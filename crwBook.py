#!/usr/bin/env python3

(bkISBN, bkTitle, bkAuthor, bkBinding, bkPublisher, bkPublished) = list(range(6))
bkFields = {
    bkISBN : "ISBN",
    bkTitle : "Title",
    bkAuthor : "Author",
    bkBinding : "Binding",
    bkPublisher : "Publisher",
    bkPublished : "Published"
}

class Book(object):
    def __init__(self, isbn, title=None, author=None):
        self.binding = None
        self.publisher = None
        self.published = None
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
            self.u_isbn = "Unknown ISBN"

    def get_isbn(self):
        return self.u_isbn

    def set_title(self, title):
        try:
            self.u_title = title.strip()
        except AttributeError:
            print("### Could not set title")
            self.u_title = "Unknown Title"

    def get_title(self):
        return self.u_title

    def set_author(self, author):
        try:
            self.u_author = author.strip()
        except AttributeError:
            print("### Could not set author")
            self.u_author = "Unknown Author"

    def get_author(self):
        return self.u_author

    def set_isbn_13(self, isbn13):
        self.isbn_13 = isbn13.strip()

    def get_isbn_13(self):
        return self.isbn_13

    def set_isbn_10(self, isbn10):
        self.isbn_10 = isbn10.strip()

    def get_isbn_10(self):
        return self.isbn_10

    def set_binding(self, binding):
        self.binding = binding.strip()

    def get_binding(self):
        return self.binding

    def set_publisher(self, publisher):
        self.publisher = publisher.strip()

    def get_publisher(self):
        return self.publisher

    def set_published(self, published):
        self.published = published.strip()

    def get_published(self):
        return self.published

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
