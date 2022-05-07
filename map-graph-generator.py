# This script takes a black and white image as input, maps it onto an NxN grid,
# and assigns infinite costs to all impossible paths (white squares)

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from PIL import Image
import csv

def get_map (filePath) :

    """gets a .csv path cost map "cost_matrix" from a given image"""

    # open .csv file to write cost matrix, and create writer object
    costCSV = open('C:\\Users\\User\\Desktop\\ARC\\ARC\\nav-map-costs.csv', 'w', newline = '')
    writer = csv.writer(costCSV)

    # load in image
    image = Image.open(filePath)
    pixel = image.load()

    # get dimensions
    width = image.size[0]
    height = image.size[1]

    # path cost matrix with default value of 999 for impossible paths
    cost_matrix = [[1 for i in range(width)] for j in range(height)]

    # alter cost matrix to assign possible paths a cost of 1
    # export .csv map of paths costs
    for y in range (height) :
        for x in range (width) :

            zero = int(pixel[x, y][0])   # convert zeroth element in pixel to int
            first = int(pixel[x, y][1]) 
            second = int(pixel[x, y][2]) 
           
            if ((zero, first, second) != (255, 255, 255)) : # pixels referenced as column, row: x, y
                cost_matrix[y][x] = 0

        writer.writerow(cost_matrix[y])
    
    print (cost_matrix[197][42], cost_matrix[192][34])

    # close .csv map file
    costCSV.close()
    
    return cost_matrix

# main()
class Node():
    """A node class for A* pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def find_map_index(index_list) :
    """ finds map index in the cost matrix given .csv location in [AB, 123] form """
    
    # shift row number -1 because list starts index at 0
    row = index_list[1] - 1

    letters = index_list[0]
    # shift column number -1 because list starts index at 0
    column = (26 * (len(letters) - 1)) - 1
    for letter in letters :
        column = column + (ord(letter) - 64) # subtract by 64 to get accurate ASCII value
    
    # return matrix indices in list [row, column]
    return (row, column)
        

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():

    # create maze using external script
    # overlay a NxN grid
    # if square.hasWhite() : cost = 999999. These are impossible paths
    # assign costs to nodes only because paths can have a cost of 1. since impossible paths have a cost of 999
    
    #maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 6, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    maze = get_map('C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image.png')
    
    # depends on classroom locations. set as index in .csv file. (e.g. AB123 is list [AB, 123])
    start =  ['AP', 198]
    end = ['BG', 193]

    # indices in matrix
    startNode = find_map_index(start)
    endNode = find_map_index(end)

    print (startNode, endNode)
    
    path = astar(maze, startNode, endNode)
    print(path)

if __name__ == '__main__':
    main()
  #  get_map('C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image.png')



