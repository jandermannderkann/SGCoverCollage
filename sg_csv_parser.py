
class sgCsvParser:
    # Headers: 
    # Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,
    # 10: Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,
    # 15: Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,
    # 20: Content Warning Description,Tags,Owned?      
    filepath = ""

    def __init__(self, filepath:str):
        self. filepath = filepath

    def validate_header(self, header:str):
        expected_header = "Title,Authors,Contributors,ISBN/UID,Format,Read Status,Date Added,Last Date Read,Dates Read,Read Count,Moods,Pace,Character- or Plot-Driven?,Strong Character Development?,Loveable Characters?,Diverse Characters?,Flawed Characters?,Star Rating,Review,Content Warnings,Content Warning Description,Tags,Owned?"
        header=header.strip()
        return header==expected_header
        
    def isbns(self):
        path = self.filepath

        with open(path) as file:
            _header = file.readline()
            if not self.validate_header(_header):
                exit("Invalid csv format")

            for line in file:
                data = line.split(',')
                title = data[0]
                autor = data[1]
                isbn = data[3]
                yield isbn
                
                
