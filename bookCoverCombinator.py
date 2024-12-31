from PIL import Image
import math

# 210 x 297 mm
def combineImages(files: list[str], path:str):
    images = [Image.open(x) for x in files]
    noImages = len(images)
    widths, heights = zip(*(i.size for i in images))
    print("widths, heights:")
    print(widths)
    print(heights)
    for h in heights:
        if h != heights[0]:
            print("WARN: pictures dont have equal height")


    # # twidth=1920
    # # theight=1080
    twidth=2100
    theight=2970

    ratio = twidth/theight
    iratio = theight/twidth
    # no_images_width = ratio*math.ceil(math.sqrt(noImages))
    

    new_im = Image.new('RGB', (twidth, theight))
    x,y=0,0
    for img in images:
        img_x = img.size[0]
        img_y = img.size[1]
        if x+img_x > twidth:
            y+=img_y
            x=0
        new_im.paste(img,(x,y))
        x+=img_x
    
    new_im.save('test.jpg')