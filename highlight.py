import json
from datetime import date
import random
import logging

# class for storing highlights as highlights
class Highlight:

    def __init__(self, text, color, note) -> None:
        """Constructor

        :param string text: contains the text of the highlight itself
        :param string color: contains the color of higlight used
        :param string note: contains any notes associtated with the text
        """
        self.text = text
        self.color = color
        self.note = note
    
    def __str__(self):
        """returns string representation of Highlight object for display

        :return string: string representation of Highlight object
        """
        if self.note == "":
            return self.text
        return f"{self.text} - {self.note}"

    def toJSON(self):
        """convert Highlight to dict for serialization

        :return dictrionary: dict representation of Highlight object
        """
        return {'text': self.text, 'color': self.color, 'note': self.note}


# class for storing all highlights from a particular book
# TODO support for multiple authors
# TODO support for subtitles
class Book:
    def __init__(self, title, author) -> None:
        """Constructor

        :param string title: contains the title of the book
        :param string author: contains the author of the book
        :param date lastAccessed: the date the book was last accessed on kindle
        """
        self.title = title
        self.author = author
        self.highlights = []
    
    def __str__(self):
        """returns string representation of Book object for display

        :return string: string representation of Book object
        """
        return f"{self.title} \nBy: {self.author}"
    

    def toJSON(self):
        """convert Book to dict for serialization

        :return dictionary: dict representation of Book object
        """
        retval = {'title': self.title, 'author':self.author}
        retval['highlights'] = [highlight.toJSON() for highlight in self.highlights]
        return retval
    
    def addHighlight(self, q):
        """Add a highlight to the book

        :param Highlight q: Highlight object to be appended to self.highlights
        """
        self.highlights.append(q)


# class to contain a collection of books and helper methods 

class BookList:

    # Filename where data should be stored and read from
    # TODO if there are multipule BookList's this may break
    FILENAME = 'notebookData.json'

    def __init__(self):
        """Constructor
        """
        # a list of Book objects with all the books synced
        self.books = []
        # set last synced to min data so all data will be synced
        self.lastSuccessfulSync = date.min
    
    def findBook(self, bookTitle):
        """Seach this BookList for a book with matching title

        :param string bookTitle: The title of the book to find
        :return Book: The Book object whose title matches the input param or None if not found
        """
        for book in self.books:
            if book.title == bookTitle:
                return book
        # if not found      
        return None
    
    def addBook(self, b):
        """Add a Book object to this BookList

        :param Book b: Book to be added to this BookList object
        """
        self.books.append(b)
    
    def removeBook(self, b):
        """Remove a Book object from this Booklist 

        :param Book b: Book object to be removed from BookList
        """
        self.books.remove(b)

    def randomHighlight(self):
        """Get a random highlight from all the highlights in all the books in this list

        :return tuple (Highlight, Book): a tuple containing the randomly selected highlight object and the book the highlight came from
        """

        # Create a list of weights for each book, where the weight is the number of highlights
        weights = [len(book.highlights) for book in self.books]

        # Use the weights to get the index a random book
        b = random.choices(range(len(self.books)), weights=weights)[0]

        # Select a random highlight from the selected book
        q = random.choice(self.books[b].highlights)
        
        return (q, self.books[b])

    def save(self):
        """serialize object to JSON and write to file
        """
        with open(self.FILENAME, "w") as jsonFile:
            jsonFile.write(json.dumps(self.toJSON()))

    def load(self):
        """attempt to load JSON data from file
        """
        try:
            # open file and load data
            with open(self.FILENAME) as jsonFile:
                data = json.load(jsonFile)
                self.lastSuccessfulSync = date.fromisoformat(data["lastSuccessfulSync"])
                # for each book in file create book object
                for item in data["books"]:
                    b = Book(item['title'], item['author'])
                    # for each highlight in book create a highlight object
                    for q in item['highlights']:
                        b.addHighlight(Highlight(q['text'], q['color'], q['note']))
                    self.addBook(b)
        except Exception as e:
            logging.exception(e)

    def toJSON(self):
        """convert BookList to dict for serialization

        :return dictionary: dict representation of BookList object
        """
        retval = {'lastSuccessfulSync': self.lastSuccessfulSync.isoformat()}
        retval['books'] = [book.toJSON() for book in self.books]
        return retval

#test code

# q1 = Highlight('text here', 'yellow', 'heading')
# q2 = Highlight('text here again', 'purple', 'heading2')
# q3 = Highlight('text here now', 'orange', 'heading3')
# q4 = Highlight('text not there', 'pink', 'heading4')
# q5 = Highlight('text here as well', 'orange', 'heading5')

# b1 = Book("the book", 'some idiot')
# b1.addHighlight(q1)
# b1.addHighlight(q2)
# b2 = Book("the next book", 'same idiot')
# b2.addHighlight(q3)
# b2.addHighlight(q4)
# b3 = Book("the last book", 'another idiot')
# b3.addHighlight(q5)

# bl = BookList()
# bl.addBook(b1)
# bl.addBook(b2)
# bl.addBook(b3)
# print(bl.toJSON())
# print(type(bl))

# print(json.dumps(bl.toJSON()))

# test code for loadHighlights

# bl.load()
# print(bl.toJSON())
