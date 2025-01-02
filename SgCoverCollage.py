from sg_csv_parser import sgCsvParser
import argparse
from isbnDB import isbnDbDownloader
import os
from bookCoverCombinator import CollageGenerator
import isbn as isbnlib
from tkinter import *
from PIL import ImageTk, Image
from PIL.Image import Image as ImageObj
import os
import math

class PicturePool():
    '''
    A pool of images stored in a certain directory
    '''
    path: str = "~/Pictures" # sensible default
    files: list[str] = []

    def index(self):
        self.files = os.listdir(self.path)
        print("indexed:")
        print(self.files)

    def __init__(self, path:str):
        if os.path.exists(path):
            self.path = path
        else: 
            exit("Error, Download folder:{} doesnt exist".format(path))
        self.index()

    def missing_images(self, list: list[str]):
        missing = []
        for x in list:
            if not self.has_image(x):
                missing.append(x)
        return missing

    

    def has_image(self, isbn:str):
        if isbn in self.files:
            return True

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
        files = []
        for isbn in isbns:
            if self.has_image(isbn):
                files.append(self.image_location(isbn))
            else: 
                pass
        return files

def downloadAllPicturesToPool(isbns: list[str], pool:PicturePool, downloader: isbnDbDownloader):
    missing = pool.missing_images(isbns)
    print("Pool has {} covers, is missing {}.".format(len(pool.image_files(isbns)),len(missing)))
    
    if isbns == []: # avoid division by zero
        return

    fails = 0
    for isbn in missing:
        url = downloader.get_cover_image_url(isbn)
        if url != None and url != "":
            downloader.downloadImage(url, pool.image_location(isbn))
        else:
            fails += 1
            print("Error no Url found")
    print("Error downloading {} out of {} images ({:<.2}%).".format(fails, len(isbns), fails/len(isbns)))
        

class Gui():
    collage: ImageObj = None
    src_images: list[ImageObj] = []
    args = None
    files: list[str]

    def __init__(self, args):
        self.args = args

    def regenerateCollage(self):
        if len(self.src_images) == 0:
            parser = sgCsvParser(self.args.csvFile)
            downloader = isbnDbDownloader("isbndb.key")
            pool = PicturePool(self.args.tempDir)
            # get images
            if not self.args.skipDownload:

                downloadAllPicturesToPool(parser.isbns(), pool, downloader)
            self.files = pool.image_files(parser.isbns())
        
        generator = CollageGenerator(self.files)
        collage = generator.getCollage()
        self.collage = collage
    
    # def generateCollageBtn(self):
    #     self.regenerateCollage()
    #     img = ImageTk.PhotoImage(img)


    def start(self):    
        root = Tk()
        geometry = (500,500)
        gemoetry_str = "{}x{}".format(geometry[0],geometry[1])
        root.geometry(gemoetry_str)
        self.regenerateCollage()
        
        img = self.collage
        scale = 0.2
        img = img.resize((math.ceil(img.size[0]*scale), math.ceil(img.size[1]*scale)))
        timg = ImageTk.PhotoImage(img)
        panel = Label(root, image = timg)
        panel.pack(side = "bottom")
        root.resizable(width=True, height=True)
        
        gen_btn = Button(root, text='Generate', command=self.regenerateCollage).pack()

        root.mainloop()


def generatePicture(args):
    parser = sgCsvParser(args.csvFile)
    downloader = isbnDbDownloader("isbndb.key")
    pool = PicturePool(args.tempDir)
    #parse csv

    isbns = parser.isbns()
    stats = parser.isbnstats()
    print("Found {:<4} isbns".format(stats['isbn']))

    # get images
    if not args.skipDownload:
        downloadAllPicturesToPool(isbns, pool, downloader)
    files = pool.image_files(parser.isbns())


    generator = CollageGenerator(files)
    collage = generator.getCollage()

    print("Saving image to {}".format(args.outputFile))
    collage.save(args.outputFile)
    

def main():
    parser = argparse.ArgumentParser(
        prog='SgCoverCollage',
        description='Generates nice collage of all your books cover-page',
        epilog='')    

    parser.add_argument('csvFile')           # positional argument
    parser.add_argument('-d', '--tempDir', default='/tmp/SgCoverCollage/')
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