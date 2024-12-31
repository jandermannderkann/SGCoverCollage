import csv
import isbn as isbnlib

class sgCsvParser:
    '''
    Parses a CSV downloaded from StoryGraph. 
    Mainly extracts ISBN (or ASNI) of books
    '''

    # Headers: 
    # Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,
    # 10: Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,
    # 15: Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,
    # 20: Content Warning Description,Tags,Owned?      
    
    filepath = ""

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
    
    def isbns(self):
        return [x for x in self.get_isbn_fields() if x != '' and isbnlib.isIsbn(x)]

    def get_isbn_fields(self):
        '''
        Get all isbns
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
                title = record[0]
                autor = record[1]
                isbn = record[3]
                yield isbn
                
                
