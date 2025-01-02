from sg_csv_parser import sgCsvParser
import argparse
from isbnDB import isbnDbDownloader
import os
from bookCoverCombinator import getCollage, saveCollage
import isbn as isbnlib
from tkinter import *
from PIL import ImageTk, Image
from PIL.Image import Image as ImageObj
import os

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

    def image_files(self, isbns: list[str]):
        for isbn in isbns:
            if self.has_image(isbn):
                yield self.image_location(isbn)
            else: 
                continue

class LibraryBook():
    isbn: str
    image_path: str
    
    def __init__(self, isbn:str):
        self.isbn = isbn

def downloadAllPicturesToPool(isbns: list[str], pool:PicturePool, downloader: isbnDbDownloader):
    for isbn in isbns:
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
class Gui():

    collage: ImageObj = None
    src_images: list[ImageObj] = []
    args = None

    def __init__(self, args):
        self.args = args

    def regenerateCollage(self):
        if len(self.src_images) == 0:
            parser = sgCsvParser(self.args.csvFile)
            downloader = isbnDbDownloader()
            pool = PicturePool(self.args.tempDir)
            # get images
            if not self.args.skipDownload:

                downloadAllPicturesToPool(parser.isbns(), pool, downloader)
            self.images = pool.image_files(parser.isbns())
        collage = getCollage(self.images)
        self.collage = collage
    
    # def generateCollageBtn(self):
    #     self.regenerateCollage()
    #     img = ImageTk.PhotoImage(img)


    def start(self):    
        root = Tk()
        geometry = (500,500)
        gemoetry_str = geometry[0]+"x"+geometry[1]
        root.geometry(gemoetry_str)
        self.regenerateCollage()
        
        img = self.collage
        # scale = 
        img = img.resize((img.size[0]*scale, img.size[1]*scale))
        timg = ImageTk.PhotoImage(img)
        panel = Label(root, image = timg)
        panel.pack(side = "bottom")
        root.resizable(width=True, height=True)
        
        gen_btn = Button(root, text='Generate', command=self.regenerateCollage).pack()

        root.mainloop()


def generatePicture(args):
    parser = sgCsvParser(args.csvFile)
    downloader = isbnDbDownloader()
    pool = PicturePool(args.tempDir)
    # get images
    if not args.skipDownload:
        downloadAllPicturesToPool(parser.isbns(), pool, downloader)
    images = pool.image_files(parser.isbns())
    collage = getCollage(images)

    print("Saving image to {}".format(args.outputFile))
    collage.save(args.outputFile)
    

def main():
    parser = argparse.ArgumentParser(
        prog='SgCoverCollage',
        description='Generates nice collage of all your books cover-page',
        epilog='')    

    parser.add_argument('csvFile')           # positional argument
    parser.add_argument('-d', '--tempDir', default='tmp/')
    parser.add_argument('outputFile', default="collage.jpg")
    parser.add_argument('--skipDownload',
                       action='store_true')  # on/off flag
    parser.add_argument('-g', '--gui',
                        action='store_true')  # on/off flag
    parser.add_argument('-v', '--verbose',
                        action='store_true')  # on/off flag
    args = parser.parse_args()
  
  
    if args.gui:
        gui = Gui(args)
        gui.start()
    else:    
        generatePicture(args)


if __name__ == "__main__":  
    main()