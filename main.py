from sg_csv_parser import sgCsvParser
import argparse
from isbnDB import isbnDbDownloader
import os
from bookCoverCombinator import combineImages
import isbn as isbnlib

class PicturePool():
    path: str 

    def __init__(self, path:str):
        if os.path.exists(path):
            self.path = path
        else: 
            exit("Error, Download folder:{} doesnt exist".format(path))

    # def _has_file(self, filename:str):
    #     return os.path.exists(path)

    def has_image(self, isbn:str):
        path = self.image_location(isbn)
        return os.path.exists(path)
        # # for suffix in ['','.png','.jpg']:
        # if self._has_file(isbn):
        #     return True
        # return False
    
    def image_filename(self, isbn:str):
        return isbn

    def image_location(self, isbn:str):
        filename = self.image_filename(isbn)
        path = os.path.join(self.path, filename)
        return path

    def image_files(self):
        for filename in os.listdir(self.path):
            yield os.path.join(self.path, filename)

class LibraryBook():
    isbn: str
    image_path: str
    
    def __init__(self, isbn:str):
        self.isbn = isbn

def generatePicture(args):
    parser = sgCsvParser(args.csvFile)
    downloader = isbnDbDownloader()
    pool = PicturePool(args.downloadFolder)

    # get images
    for isbn in parser.isbns():
        if not isbnlib.isIsbn(isbn):
            print("Error, not a ISBN: {}".format(isbn))
            continue
        book = LibraryBook(isbn)
        if not pool.has_image(isbn):
            
            url = downloader.get_cover_image_url(isbn)
            if url != None and url != "":
                downloader.downloadImage(url, pool.image_location(isbn))
            else: 
                print("Error no Url found")
        else:
            print("Found Cover for ISBN {}".format(isbn))

    combineImages(pool.image_files(), 'out')
    

def main():
    parser = argparse.ArgumentParser(
        prog='SGPicGenerator',
        description='Generates nice Pictures of your books',
        epilog='')    

    parser.add_argument('csvFile')           # positional argument
    parser.add_argument('downloadFolder', default='tmp/')
    parser.add_argument('-v', '--verbose',
                        action='store_true')  # on/off flag
    args = parser.parse_args()

    generatePicture(args)


if __name__ == "__main__":  
    main()