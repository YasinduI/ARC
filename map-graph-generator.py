# This script takes a black and white image as input, maps it onto an NxN grid,
# and assigns infinite costs to all impossible paths (white squares)

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


def get_image (filePath) :
    image = plt.imread(filePath)
    plt.show(image)

get_image('C:\\Users\\User\\Desktop\\ARC\\test-image.png')

