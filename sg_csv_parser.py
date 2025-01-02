import csv
import isbn as isbnlib
from dataclasses import dataclass
import argparse

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
    Mainly extracts ISBN (or asin) of books
    '''

    
    
    filepath: str = ""
    library: list[Book] = []

    def __init__(self, filepath:str):
        '''
        filepath: Csv file to parse
        '''
        self. filepath = filepath

    def validate_header(self, header:str) -> bool:
        '''
        Check if the CSV Header-row, is what we expect
        '''
        expected_header = "Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,Content Warning Description,Tags,Owned?"
        header=header.strip()
        return header==expected_header
    
    def books(self) -> list[Book]:
        if len(self.library) == 0:
            self.parse()
        return self.library
    
    # Headers: 
    # Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,
    # 10: Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,
    # 15: Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,
    # 20: Content Warning Description,Tags,Owned?      
    def book_from_csvRecord(self,record: list[str]) -> Book:
        '''Creates book object from csv record'''
        title = record[0]
        autor = record[1]
        isbn = record[3]
        read_status=record[5]
        read_count=record[9]
        star_rating = record[17]
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
        return book

    def isbns(self) -> list[str]:
        if len(self.library) == 0:
            self.parse()

        return [b.isbn for b in self.library if isbnlib.isIsbn(b.isbn) or isbnlib.isASIN(b.isbn)]
    

    def isbnstats(self)->dict[str:int]:
        '''
        Returns 6 values:
        isbn: number of books where isbn was found
        none: number of books without isbn
        other: number of books with some unknwon id
        p_isbn: percentage to `found`
        p_none: percentage to `none`
        p_other: percentage to `other`
        '''
        books = len(self.library)
        isbn = len(self.isbns())
        none = len([b.isbn for b in self.library if b.isbn==''])
        other = len([b.isbn for b in self.library if not isbnlib.isIsbn(b.isbn) and b.isbn != ''])
        
        if books>0:
            p_isbn = isbn/books
            p_none = none/books
            p_other = other/books
               
        return {
            'isbn': isbn,
            'none': none,
            'other': other,
            'p_isbn': p_isbn,
            'p_none': p_none,
            'p_other': p_other,
        }

    def parse(self) -> None:
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
                
                self.library.append(book)

def print_library(books: list[Book]):
    book_line_fmt="{:<13}: {:<80} by {:>10} *{:<2} r#{:<2} {}"
    print(book_line_fmt.format("ISBN","Title", "Author", "rating", "read_count", "owned?"))
    for b in books: 
        if isbnlib.isIsbn(b.isbn):
            continue
        assert(b != None)
        title=b.title
        if len(b.title) > 80:
            title = b.title[:77]+"..."
        print(book_line_fmt.format(b.isbn, title, b.author, b.star_rating, b.read_count, b.owned))

def main():
    parser = argparse.ArgumentParser(
        prog='sgCsvParser',
        description='Parses a Storygraph CSV',
        epilog='')    

    parser.add_argument('csvFile')           # positional argument
    parser.add_argument('--isbn', action='store_true') 
    parser.add_argument('--isbnstats', action='store_true') 
    parser.add_argument('-v', '--verbose', action='store_true')


    args = parser.parse_args()
  
    parser = sgCsvParser(args.csvFile)
    books: list[Book] = parser.books()
    if args.isbn:
        for i in parser.isbns():
            print(i)
    elif args.isbnstats:
        stats = parser.isbnstats()
        print(stats)
    else:
        print_library(books)
   
   

if __name__ == "__main__":  
    main()