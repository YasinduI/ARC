'''
* robot-main.py
* This script acts as the control hub to run the robot
'''

import importlib
map_generator = importlib.import_module("map-graph-generator")
pure_pursuit = importlib.import_module("pure-pursuit")
gps_grid_generator = importlib.import_module("GPS-grid-generator")

def main() :

    # Gets list of waypoints from map-graph-generator.py, given a black and white image of walkable paths
    map_generator.set_map_param(map_ref_path = r"C:\\Users\\User\\Desktop\\ARC\\ARC\\test-image.png",
                               cost_output_path = r"C:\\Users\\User\\Desktop\\ARC\\ARC\\nav-map-costs.csv",
                                  start_node = ['FB', 185],
                                    end_node = ['AKZ', 309])
    waypoints = map_generator.get_waypoints()

    # Gets cost matrix
    cost_matrix = map_generator.get_cost_matrix()

    # Gets GPS coordinate matrix
   # gps_matrix = gps_grid_generator.compile_gps_matrix(cost_matrix = cost_matrix, 
    #                                                     pixel_len = 1.2, 
     #                                               landmark_coord = (69, 69),
      #                                          landmark_gps_coord = (34.0000000, 24.0000000, 'NW'))

    # Uses waypoints list to tell the robot where to move (simulation)
    pure_pursuit.input_waypoints(waypoints)
    pure_pursuit.traverse_path()

if __name__ == '__main__':
    main()
