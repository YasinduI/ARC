'''
* path_following_algorithms
* pure_pursuit.py
* Copyright (c) 2021, Seunghyun Lim
'''

import numpy as np
import matplotlib.pyplot as plt
import time
import map-graph-generator

global L, wp, vx, theta, w_limit
L = 10 #lookahead distance
wp = 0 
vx = 5 #velocity
theta = 0.5 #angle
w_limit = 0.48 #rad/s
#waypoints = [[0, 8], [5, 8], [5, 0], [12, 0]]
#waypoints = [[0, 8], [5, 8], [6, 10], [5, 0], [12, 0]]
#waypoints = [[0, 8], [5, 8], [5, 5], [3, 3], [5 ,0], [8, 2], [12, 0]]
##waypoints = [[0, 0], [3, 8], [7, 8], [8, 5], [3, 3], [5 ,0], [8, 2], [12, 0]]
waypoints = [(184, 33), (185, 34), (186, 35), (187, 36), (188, 37), (189, 38), (190, 39), (191, 40), (192, 41), (193, 42), (194, 43), (195, 44), (196, 45), (197, 46), (198, 47), (199, 48), (200, 49), (201, 50), (202, 51), (203, 52), (204, 53), (205, 54), (206, 55), (207, 56), (208, 57), (209, 58), (210, 59), (211, 60), (212, 61), (213, 62), (214, 63), (215, 64), (216, 65), (217, 66), (218, 67), (219, 68), (220, 69), (221, 70), (222, 71), (223, 72), (224, 73), (225, 74), (226, 75), (227, 76), (228, 77), (229, 78), (230, 79), (231, 80), (232, 81), (233, 82), (234, 83), (235, 84), (236, 85), (237, 86), (238, 87), (239, 88), (240, 89), (241, 89), (242, 89), (243, 89), (244, 89), (245, 89), (246, 89), (247, 89), (248, 89), (249, 89), (250, 89), (251, 89), (252, 89), (253, 89), (254, 89), (255, 89), (256, 89), (257, 89), (258, 89), (259, 89), (260, 89), (261, 89), (262, 89), (263, 89), (264, 89), (265, 89), (266, 89), (267, 89), (268, 89), (269, 89), (270, 89), (271, 89), (272, 89), (273, 89), (274, 89), (275, 89), (276, 89), (277, 89), (278, 89), (279, 89), (280, 89), (281, 89), (282, 89), (283, 89), (284, 89), (285, 89), (286, 89), (287, 89), (288, 89), (289, 89), (290, 89), (291, 89), (292, 89), (293, 89), (294, 89), (295, 89), (296, 89), (297, 89), (298, 89), (299, 89), (300, 89), (301, 89), (302, 89), (303, 89), (304, 89), (305, 89), (306, 89), (307, 89), (308, 89)]
position = [184, 33]
#def plot_waypoints(waypoints):


def position_vector(vx, w, theta):
    global w_limit
    tmp = np.dot(np.array([[np.cos(theta), 0],[np.sin(theta), 0],[0, 1]]),np.array([[vx],[w]]))
    Xdot = tmp[0][0]
    Ydot = tmp[1][0]
    tdot = tmp[2][0]
    if tdot >= w_limit:
        tdot = w_limit
    elif tdot <= -w_limit:
        tdot = -w_limit
    return Xdot, Ydot, tdot

def pure_pursuit(position, waypoints):
    global L, wp, vx, theta
    X = position[0]
    Y = position[1]
    x_n0 = waypoints[wp][0]
    y_n0 = waypoints[wp][1]
    x_n1 = waypoints[wp+1][0]
    y_n1 = waypoints[wp+1][1]
    up = ((X - x_n0)*(x_n1 - x_n0)+(Y - y_n0)*(y_n1 - y_n0))/((x_n1 - x_n0)**2+(y_n1 - y_n0)**2)
    xo = x_n0 + up*(x_n1 - x_n0)
    yo = y_n0 + up*(y_n1 - y_n0)

    error = np.sqrt((X - xo)**2+(Y - yo)**2)

    if np.sqrt((x_n1 - xo)**2+(y_n1 - yo)**2) <= L:
        if wp<len(waypoints)-2:
            wp=wp+1

    do = np.sqrt((X - xo)**2+(Y - yo)**2)
    if do**2 >= L**2:
        dl = 0
    else:
        dl = np.sqrt(L**2-do**2)

    wpvec = np.array([x_n1 - x_n0, y_n1 - y_n0])
    norm_vec = wpvec/np.linalg.norm(wpvec)

    [xl, yl] = [xo, yo] + dl*norm_vec
    rot_matrix = np.array([[np.cos(-theta), -np.sin(-theta)], [np.sin(-theta), np.cos(-theta)]])
    tmp = np.dot(rot_matrix, np.array([[xl-X],[yl-Y]]))
    yd = tmp[1][0]

    w = 2*yd*vx/(L**2)

    return vx, w, error

x_way = []
y_way = []
for item in waypoints:
    x_way.append(item[0])
    y_way.append(item[1])

w = 0 #rad/s
dt = 0.1 #s
iter = 0 #iteration
fig = plt.subplots()
plt.xlim(0, 500)
plt.ylim(0, 100)
command_list = []
error_list = []
odom_list = [[],[]]

while np.linalg.norm(np.array(position)-waypoints[len(waypoints)-1])>0.1:
    vx, w, error = pure_pursuit(position, waypoints)
    command_list.append([vx, w])
    error_list.append(error)
    Xdot, Ydot, tdot = position_vector(vx, w, theta)
    position[0] = position[0]+dt*Xdot
    position[1] = position[1]+dt*Ydot
    odom_list[0].append(position[0])
    odom_list[1].append(position[1])
    plt.plot(odom_list[0], odom_list[1], 'b')
    theta = theta+dt*tdot
    iter += 1
    plt.plot(x_way, y_way, 'r--')
    plt.arrow(position[0], position[1], Xdot, Ydot, width=0.05)
    plt.scatter(position[0], position[1])
    plt.title("Pure pursuit")
    plt.legend(['odometry','path'])
    plt.xlim(0, 500)
    plt.ylim(0, 100)
    plt.pause(dt*0.01)
    if np.linalg.norm(np.array(position)-waypoints[len(waypoints)-1])>0.1:
        plt.cla()
    else:
        plt.waitforbuttonpress()
        plt.cla()
        plt.axis(option='auto')
        plt.title("Position RMSE (L: {}m)".format(L))
        plt.plot(error_list)
        plt.waitforbuttonpress()
        plt.cla()
        plt.axis(option='auto')
        plt.ylim(-10, 10)
        plt.title("Command input (L: {}m)".format(L))
        plt.plot(command_list)
        plt.legend(['Vx(m/s)','w(rad/s)'])
        plt.show()
print("Average Error: {}".format(np.average(error_list)))