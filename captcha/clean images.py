from PIL import Image, ImageOps, ImageEnhance
from natsort import natsorted
from os import  listdir
from re import sub

def cleanImage( image ):
    proportion = {}
    pixdata = image.load()
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            if pixdata[x,y] not in proportion: proportion[pixdata[x,y]] = 1
            else: proportion[pixdata[x,y]] += 1

    Lproportions = sorted(proportion.items(), key=lambda x: x[1], reverse=True)

    for y in range(image.size[1]):
        for x in range(image.size[0]):
            # if pixdata[x,y]!= Lproportions[1][0]:     # care about opacity
            if pixdata[x,y][0] != Lproportions[1][0][0] and pixdata[x,y][1] != Lproportions[1][0][1] and pixdata[x,y][2] != Lproportions[1][0][2]: # don't care about opacity
                pixdata[x,y] = (255, 255, 255, 255)     # others will be white 
                # pixdata[x,y] = (0, 0, 0, 255)         # others will be black 
            else:
                # pixdata[x,y] = (255, 255, 255, 255)   # the pixels of the numbers will be white 
                pixdata[x,y] = (0, 0, 0, 255)           # the pixels of the numbers will be black
    
    return image


images = natsorted(listdir('./images'))
for image in images:
    CleanImage = cleanImage( Image.open(f'./images/{ image }') )
    CleanImage.save(f'./cleaned/{ image }')
