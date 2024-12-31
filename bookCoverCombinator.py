from PIL import Image
import math

# 210 x 297 mm
def combineImages(files: list[str], path:str):
    images = [Image.open(x) for x in files ]
    images = [x for x in images if not x.size[0]<100] # Amazon images
    images = [x for x in images if not x.size[1]==248] # Not available images

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

    sqrt = math.sqrt(noImages)
    noRows = math.ceil(sqrt)
    noCols = math.ceil(noImages/noRows)
    assert(noCols*noRows >= noImages)
    print('Target rows/cols: {},{}'.format(noRows, noCols))

    mean_width = sum(widths)/len(widths)
    mean_height = sum(heights)/len(heights)
    print("Mean: {},{}".format(mean_width, mean_height))
    scale_factor_width = (twidth/noCols)/mean_width
    scale_factor_height = (theight/noRows)/mean_height
    print("Mean_Targets {},{}".format((twidth/noCols),theight/noRows))
    print("Scale Factors: {},{}".format(scale_factor_width, scale_factor_height))
    scaled_images = []
    for img in images:
        new_width = math.ceil(img.size[0]*scale_factor_width)
        new_height = math.ceil(img.size[1]*scale_factor_height)
        print("Resizing from {},{} to {},{}".format(img.size[0],img.size[1],new_width, new_height))
        newimg = img.resize((new_width,new_height))
        scaled_images.append(newimg)
    # no_images_width = ratio*math.ceil(math.sqrt(noImages))
    newWidths, newHeights = zip(*(i.size for i in scaled_images))
    print("New dims")
    print(newWidths)
    print(newHeights)

    new_im = Image.new('RGB', (twidth, theight))
    x,y = 0,0
    i = 0
    row = 0
    for row in range(noRows):
        start_row_x = 0
        image_target_width = math.ceil(twidth/noCols)

        print("Drawing row {} with index {} and {} columns".format(row,i,noCols))
        imgs_row = scaled_images[i:i+noCols]
        if len(imgs_row) == 0:
            print("WARN not enough images in row {}".format(row))
            continue
        if len(imgs_row) < noCols:
            missing = noCols-len(imgs_row)
            start_row_x = missing/2*image_target_width
            pass
        row_widths = widths[i:i+noCols]
        row_heights = heights[i:i+noCols]
        # # print("dimensions for row:")
        # # print(row_widths)
        # # print(row_heights)
        # # row_mean_width = sum(row_widths)/len(row_widths)
        # # row_mean_height = sum(row_heights)/len(row_heights)
        
        # print("Row mean: {},{}".format(row_mean_width, row_mean_height))
        # row_scale_factor = (twidth/sum(row_widths))/noCols
        final_images = resize_prop_to_fit_x(imgs_row, image_target_width)
        row_img_heights = [img.size[1] for img in final_images]
        max_height_final_images = math.ceil(sum(row_img_heights)/len(row_img_heights))
        
        for col,img in enumerate(final_images):
            img_x = img.size[0]
            img_y = img.size[1]
            print("Pasting resized image with dim {},{} at {},{}".format(img.size[0],img.size[1],col*image_target_width,y))
            new_im.paste(img,(math.floor(start_row_x+col*image_target_width),y))
        i+=noCols
        y+=max_height_final_images

    print("Saving image")
    new_im.save('test.jpg')

def resize_prop_to_fit_x(imgs: list[Image], twidth):
    resized = []
    for img in imgs:
        img_x = img.size[0]
        img_y = img.size[1]
        scale = twidth/img_x
        new_dim = (math.floor(img_x*scale), math.floor(img_y*scale))
        # print("Resizing Image again to: {},{}".format(new_dim[0],new_dim[1]))
        # print("Total width: {}".format(noCols*new_width))
        new_img = img.resize(new_dim)
        resized.append(new_img)
    return resized
    