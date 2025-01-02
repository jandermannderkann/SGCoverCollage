import csv
import isbn as isbnlib
from dataclasses import dataclass

@dataclass
class Book():
    isbn: str
    author: str
    title: str
    read_status: str
    read_count: str
    star_rating: str
    owned: str

class sgCsvParser:
    '''
    Parses a CSV downloaded from StoryGraph. 
    Mainly extracts ISBN (or ASNI) of books
    '''

    
    
    filepath: str = ""
    books: list[Book] = []

    def __init__(self, filepath:str):
        '''
        filepath: Csv file to parse
        '''
        self. filepath = filepath

    def validate_header(self, header:str):
        '''
        Check if the CSV Header-row, is what we expect
        '''
        expected_header = "Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,Content Warning Description,Tags,Owned?"
        header=header.strip()
        return header==expected_header
    
    def books(self):
        if len(self.books) == 0:
            self.parse()
        return self.books
    
    # Headers: 
    # Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,
    # 10: Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,
    # 15: Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,
    # 20: Content Warning Description,Tags,Owned?      
    def book_from_csvRecord(self,record: list[str]):
        '''Creates book object from csv record'''
        title = record[0]
        autor = record[1]
        isbn = record[3]
        read_status=record[5]
        read_count=record[9]
        star_rating = record[18]
        owned =record[22]
        book = Book(
            isbn=isbn,
            author=autor,
            title=title,
            read_count=read_count,
            read_status=read_status,
            owned=owned,
            star_rating=star_rating,
            )
        

    def isbns(self):
        if len(self.books) == 0:
            self.parse()

        return [b.isbn for b in self.books if b.isbn != '' and isbnlib.isIsbn(b.isbn)]

    def parse(self):
        '''
        Parse the file, generating Book objects from them
        '''
        path = self.filepath

        with open(path) as file:
            _header = file.readline()
            reader = csv.reader(file)
            data = [x for x in reader]
            records = data[1:]
            if not self.validate_header(_header):
                exit("Invalid csv format")

            for record in data:
                book = self.book_from_csvRecord(record)
                
                self.books.append(book)
                
                
