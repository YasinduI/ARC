'''
* robot-main.py
* map-graph-generator.py
* This script takes a black and white image as input, maps it onto an NxN pixel grid,
* and assigns cost 1 to all non-walkable paths (white squares)
'''

from PIL import Image
import csv

map_ref_file = r""
cost_output_file = r""
cost_matrix = [[]]
start = []
end = []
# set as indices of .csv file. (e.g. AB123 is list [AB, 123])


def set_map_param (map_ref_path, cost_output_path, start_node, end_node) :

    global map_ref_file, cost_output_file, start, end

    map_ref_file = map_ref_path
    cost_output_file = cost_output_path
    start = start_node
    end = end_node


def get_map (csvPath) :

    global map_ref_file, cost_output_file, cost_matrix
    """gets a .csv path cost map "cost_matrix" from a given image"""

    # open .csv file to write cost matrix, and create writer object
    costCSV = open(cost_output_file, 'w', newline = '')
    writer = csv.writer(costCSV)

    # load in image
    image = Image.open(csvPath)
    pixel = image.load()

    # get dimensions
    width = image.size[0]
    height = image.size[1]
    
    # create cost matrix
    # initialize with infinite costs
    # 0 is walkable, 999 is not walkable
    cost_matrix = [[999 for i in range(width)] for j in range(height)]

    # export .csv map of paths costs
    # loop through image and write cost matrix
    img = Image.open(map_ref_file)
    img = img.convert('RGB')

    for y in range (height) :
        for x in range (width) :

            # if pixel is white, assign cost of 999
            # if pixel is black, assign cost of 0
            colors = img.getpixel((x, y))
            colors = (int(colors[0]), int(colors[1]), int(colors[2]))

            if ((colors) != (255, 255, 255)) : # pixels referenced as column, row: x, y
                cost_matrix[y][x] = 0

        writer.writerow(cost_matrix[y]) 

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
    column = 0

    # shift column number -1 because list starts index at 0
    letters = index_list[0]
    lenLetters = len(letters)
    for i in range(lenLetters) :
        column = column + (ord(letters[i])-64) * (26**(lenLetters-i-1))

    # return matrix indices in tuple (row, column)
    return (int(row), int(column))
     

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

def get_cost_matrix():
    global cost_matrix
    return cost_matrix


def get_waypoints():

    global map_ref_file, cost_output_file, start, end

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

    maze = get_map(map_ref_file)

    print('START:', find_map_index(start), 'END:', find_map_index(end), '\n')

    path = astar(maze, (find_map_index(start)), find_map_index(end))
    print(path)

    return(path)

if __name__ == '__main__':
    get_waypoints()