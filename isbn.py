
def isIsbn(str:str):
    return len(str)==13 or len(str)==10 # there are 2 isbn variants: isbn10 and isbn13

def isASIN(str:str):
    return len(str)==10 
    