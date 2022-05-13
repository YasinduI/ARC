'''
* robot-main.py
* GPS-grid-generator.py
* This script assigns GPS coordinates to all indices of the corresponding cost matrix
'''

import math

pixel_len = 0.69 # non-zero and arbitrary for now
landmark_gps = (0.0000000, 0.0000000, 'NW')
gps_matrix = [[]]

def compile_gps_grid (cost_matrix, px_len, landmark_coord, landmark_gps_coord) :
    """reads cost_matrix and exports GPS coords from each index into gps_grid"""

    global pixel_len, landmark_gps, gps_matrix
    pixel_len = px_len
    landmark_gps = landmark_gps_coord

    # length in meters of 1 deg longitude = 111319.488*cos(latitude in rad)
    # declare GPS grid with element (latitude, longitude) as (0.0000000, 0.0000000)
    gps_matrix = [[(0.0000000, 0.0000000) for i in range(width)] for j in range(height)]

    width = len(cost_matrix[0])
    height = len(cost_matrix)

    # iterate through cost_matrix to create gps_matrix
    for i in range (height) :
        for j in range (width) :
            current_coord = (i, j)
            gps_matrix [i][j] = get_gps_coord(current_coord, landmark_coord)
    
    return gps_matrix

def get_gps_matrix () :

    global gps_matrix
    return gps_matrix

def get_gps_coord (current_coord, landmark_coord) :
    """gets GPS coordinate (lat, long) given current index in gps_matrix and landmark index in gps_matrix"""

    global pixel_len, landmark_gps

    # NW (north, west)
    # units of meters (m)
    dx = -1.0 * (current_coord[0] - landmark_coord[0]) * pixel_len
    dy = -1.0 * (current_coord[1] - landmark_coord[1]) * pixel_len

    if (landmark_gps[2] == 'NE') : dx = -1.0 * dx
    elif (landmark_gps[2] == 'SW') : dy = -1.0 * dy
    elif (landmark_gps[2] == 'SE') :
        dx = -1.0 * dx
        dy = -1.0 * dy

    # theta refers to deg latitude and deg longitude
    dtheta_x = dx / 111319.488
    dtheta_y = dy / (111319.488 * math.cos(math.radians(landmark_gps[0] + dtheta_x)))

    return (landmark_gps[0] + dtheta_x, landmark_gps[1] + dtheta_y)



    

















    






