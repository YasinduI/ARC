# This script takes a black and white image as input, maps it onto an NxN grid,
# and assigns infinite costs to all impossible paths (white squares)

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
import csv

def grid_image (filePath, dpi, tick_interval) :
    
    """overlays gridlines onto given map or image. probably not needed"""

    # open image
    image = Image.open(filePath)

    # set dpi; smaller = thinner gridlines. 50 is good-ish
    set_dpi = dpi

    # image size
    width = image.size[0]/set_dpi
    height = image.size[1]/set_dpi

    fig = plt.figure(figsize = (width, height), dpi = set_dpi)
    axis = fig.add_subplot(1,1,1)

    # removes whitespace from image
    fig.subplots_adjust(left  = 0, right = 1, bottom = 0, top = 1)

    # space between ticks
    grid_interval = tick_interval
    location = plticker.MultipleLocator(base = grid_interval)

    # set major ticks
    axis.xaxis.set_major_locator(location)
    axis.yaxis.set_major_locator(location)

    # add grid
    axis.grid(which = 'major', axis = 'both', linestyle = '-')

    # add the image
    axis.imshow(image)
    plt.imshow(image)

    # axes and ticks
    #plt.show()

    # save the image
    img_gridlined_path = 'C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image-with-grid.png'
    fig.savefig(img_gridlined_path, dpi = set_dpi)

    # return file path of gridlined image
    return img_gridlined_path

def get_map (filePath) :

    """second attempt at algo to get a .csv "map" from image"""

    # load in image
    image = Image.open(filePath)
    pixel = image.load()

    # get dimensions
    width = image.size[0]
    height = image.size[1]

    # path cost matrix with default value of 999
    cost_matrix = [[999 for i in range(width)] for j in range(height)]

    for x in range (width) :
        for y in range (height) :
            if (pixel[x, y] != (255, 255, 255)) :
                cost_matrix[x][y] = 1

# main()

 #grid_image('C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image.png', 50, 5)

get_map('C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image.png')



