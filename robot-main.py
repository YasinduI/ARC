import importlib
map_generator = importlib.import_module("map-graph-generator")
pure_pursuit = importlib.import_module("pure-pursuit")

def main() :

    # Gets list of waypoints from map-graph-generator.py, given a black and white image of walkable paths
    waypoints = map_generator.get_waypoints()


    # Uses waypoints list to tell the robot where to move
    pure_pursuit.set_waypoints(waypoints)
    pure_pursuit.traverse_path()

if __name__ == '__main__':
    main()
