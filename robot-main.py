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
    waypoints = map_generator.get_waypoints()

    # Uses waypoints list to tell the robot where to move
    pure_pursuit.input_waypoints(waypoints)
    pure_pursuit.traverse_path()

if __name__ == '__main__':
    main()
