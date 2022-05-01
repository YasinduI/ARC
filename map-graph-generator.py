# This script takes a black and white image as input, maps it onto an NxN grid,
# and assigns infinite costs to all impossible paths (white squares)

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image

def grid_image (filePath, dpi, tick_interval) :
    
    """overlays gridlines onto given map or image"""

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

    # save the image
    img_gridlined_path = 'C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image-with-grid.png'
    fig.savefig(img_gridlined_path, dpi = set_dpi)

    # return file path of gridlined image
    return img_gridlined_path


grid_image('C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image.png', 50, 5)


