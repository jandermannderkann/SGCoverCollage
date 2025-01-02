import json
import requests
import os

BASE_URL="https://api2.isbndb.com/"
ISBN_SLUG="book/{isbn}"


class isbnDbDownloader:
    '''
    Tries to download pictures for books based on their ISBN from isbndb.com
    '''
    key: str = "DEFAULT"

    def __init__(self, auth_key: str):
        self.key = auth_key
        if auth_key.endswith(".key"):
            with open(auth_key) as f:
                self.key = f.read().strip()
        

    def header(self):
        return {'Authorization': self.key}

    def get_cover_image_url(self, isbn: str):
        '''Queries isbndb.com and retrieves a url to the cover image'''
        url = BASE_URL + ISBN_SLUG.format(isbn=isbn)
        resp = requests.get(url, headers=self.header())
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
