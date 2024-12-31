import json
import requests
import os

KEY="58019_e99bca673d8a686231824e3b5d7c4c4c"
AUTH_HEADER = {'Authorization': KEY}
BASE_URL="https://api2.isbndb.com/"
ISBN_SLUG="book/{isbn}"


class isbnDbDownloader:
    '''
    Tries to download pictures for books based on their ISBN from isbndb.com
    '''
    # download_path: str = ""

    # def setDownloadLocation(self, path:str):
    #     self.download_path = path

    def __init__(self):
        pass

    def get_cover_image_url(self, isbn: str):
        '''Queries isbndb.com and retrieves a url to the cover image'''
        url = BASE_URL + ISBN_SLUG.format(isbn=isbn)
        resp = requests.get(url, headers=AUTH_HEADER)
        data = resp.json()
        try:
            image_url = data['book']['image']
        except KeyError:
            print("Error, no image for isbn: {} found".format(isbn))
            return ""
        return image_url
    

    def downloadImage(self, url: str, dest_path: str):
        '''
        Downloads a image from a url and saves it to a file
        url: to download
        dest_path: where to save the image
        '''
        # dest_folder = self.download_path
        # filename = filename

        # if not os.path.exists(dest_folder):
        #     exit("Error, destination folder:{} doesnt exist".format(dest_folder))
        
        # file_path = os.path.join(dest_folder, filename)
        print("Downloading image from url: {} to {}".format(url, dest_path))
        r = requests.get(url, stream=True)
        if r.ok:
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            exit("Download failed: status code {}\n{}".format(r.status_code, r.text))
