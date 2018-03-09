import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import CameraFeed
from perception.squareClass.py import getDepth


def run_calibration(cam_feed):
    franka_pos = get_franka_pos
    moves = generate_cube(franka_pos)
    marker_coordinates = np.zeros((9, 3))
    franka_coordinates = np.zeros((9, 3))

    for i in range(len(moves)): # not lengths number of rowes needs to be fixed

        complete_trajectory = generate_trajectory(moves[i], moves[i+1])

        execute_trajectory(complete_trajectory)

        franka_x, franka_y, franka_z = get_franka_pos()
        franka_coordinates[i, 0] = franka_x
        franka_coordinates[i, 1] = franka_y
        franka_coordinates[i, 2] = franka_z

        rgb, depth = cam_feed.get_frames()
        # current_marker_pos = find_cross(current_frame)

        marker_x, marker_y = find_cross(rgb) #not very robust
        marker_z = getDepth(current_frame)
        marker_coordinates[i, 0] = marker_x
        marker_coordinates[i, 1] = marker_y
        marker_coordinates[i, 2] = marker_z

    return marker_coordinates, franka_coordinates


def get_franka_pos():
    """Function that interfaces with ROS code to retreive franka end effector position in franka's reference frame"""
    return franka_pos


def generate_cube(centre_point):
    """function generates an array of 8 x,y,z coordinates for calibration based on an end-effector (1x3) input position"""

    x, y, z = centre_point[0], centre_point[1], centre_point[2]
    # Initial Cube
    p_cube = np.array(
        [[-0.1, -0.1, -0.1], [-0.1, 0.1, -0.1], [-0.1, 0.1, 0.1], [-0.1, -0.1, 0.1], [0.1, -0.1, -0.1],
         [0.1, 0.1, -0.1], [0.1, -0.1, 0.1], [0.1, 0.1, 0.1]])

    # print(p_cube)

    p_cube_x = []
    p_cube_y = []
    p_cube_z = []
    p_cube_x_rxyz = []
    p_cube_y_rxyz = []
    p_cube_z_rxyz = []

    cube_output = np.zeros((9, 3))
    cube_output_x = []
    cube_output_y = []
    cube_output_z = []

    cube_output[0, 0] = x
    cube_output[0, 1] = y
    cube_output[0, 2] = z

    # Transformation matrices
    theta = np.radians(30)
    cos = np.cos(theta)
    sin = np.sin(theta)
    rot_x = np.array([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])
    rot_y = np.array([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])
    rot_z = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

    # Multiplying Initial Cube by Transformation matrices in X, Y & Z
    p_cube_rot_x = p_cube.dot(rot_x)
    p_cube_rot_xy = p_cube_rot_x.dot(rot_y)
    p_cube_rot_xyz = p_cube_rot_xy.dot(rot_z)

    for i in range(len(p_cube)):
        x_tr = x + p_cube_rot_xyz[i, 0]
        y_tr = y + p_cube_rot_xyz[i, 1]
        z_tr = z + p_cube_rot_xyz[i, 2]
        cube_output[i+1, 0] = x_tr
        cube_output[i+1, 1] = y_tr
        cube_output[i+1, 2] = z_tr
        cube_output_x.append([x_tr])
        cube_output_y.append([y_tr])
        cube_output_z.append([z_tr])

    # Separating X, Y, Z coordinates into separate lists for 3D Plot
    for i in range(len(p_cube)):
        x_1 = p_cube[i, 0]
        p_cube_x.append(x_1)
        y_1 = p_cube[i, 1]
        p_cube_y.append(y_1)
        z_1 = p_cube[i, 2]
        p_cube_z.append(z_1)

    for i in range(len(p_cube)):
        x_rx = p_cube_rot_xyz[i, 0]
        p_cube_x_rxyz.append(x_rx)
        y_rx = p_cube_rot_xyz[i, 1]
        p_cube_y_rxyz.append(y_rx)
        z_rx = p_cube_rot_xyz[i, 2]
        p_cube_z_rxyz.append(z_rx)

    # 3D Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(p_cube_x, p_cube_y, p_cube_z)
    # ax.scatter(p_cube_x_rxyz, p_cube_y_rxyz, p_cube_z_rxyz)
    ax.scatter(x, y, z)
    ax.scatter(cube_output_x, cube_output_y, cube_output_z)

    plt.show()

    # print(cube_output)

    return cube_output  # 9x3 array

# if __name__ == '__main__':
#     c = calibrate_cube((1, 1, 1))
#     print('output positions =', c)

    # return moves # list of moves to complete


def generate_trajectory(start, goal):
    """function that calls motion code on new start and goal positions"""

    return # detailed trajectory


def execute_trajectory(trajectory):
    """Function that interfaces with ROS code to feed franka target positions"""
    return # update status: motion finished


def detect(c):
    """Function used by find_cross function to detect the edges and vertices of possible polygons in an image"""
    peri = cv2.arcLength(c, True)
    area = cv2.contourArea(c)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    return (len(approx), peri, area)


def find_cross(frame):
    """function that uses open CV2 to detect a red cross in a photo. This function applies a red mask, finds contours,
    finds the nuber of vertexes in polygons, and selects the shape with the appropriate number of vertices, area and perimeter.
    It then finds the centre of the cross and returns its coordinates"""

    markers = []
    while (1):
        imgsized = frame # frame should be tring of file name
        # imgsized = imutils.resize(img, width=640) try without resizing
        imghsv = cv2.cvtColor(imgsized, cv2.COLOR_BGR2HSV)

        cv2.imshow('frameb', imgsized)

        lower_red1 = np.array([170, 70, 50])
        upper_red1 = np.array([180, 255, 255])
        lower_red2 = np.array([0, 70, 50])
        upper_red2 = np.array([10, 255, 255])

        mask1 = cv2.inRange(imghsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(imghsv, lower_red2, upper_red2)
        mask = mask1 | mask2

        cv2.imshow('mask', mask)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        for c in cnts:

            shape = detect(c)

            if 14 > shape[0] > 10 and 200 > shape[1] > 50 and 820 > shape[2] > 100: # change these values to match geometry of cross
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                cv2.circle(imgsized, (cX, cY), 3, (0, 255, 255), -1)
                markers.append((cX,cY))

                cv2.drawContours(imgsized, [c], -1, (0, 255, 0), 2)
                cv2.putText(imgsized, str(shape[0]), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                cv2.imshow("Image", imgsized)

        print(markers)
        # pts = np.array(markers)
        # cv2.polylines(imgsized, [pts], True, (255, 0, 255), 3)
        # cv2.imshow("Image", imgsized)

        cv2.waitKey(0)
        break

    return markers

    # k = cv2.waitKey(5) & 0xFF
    # if k == 27:
    #     break


# def find_depth(marker, current_frame):
#
#     depth = current_frame[marker[1], marker[0]]
#
#     coordinates = marker[0], marker[1], depth[0]
#
#     return coordinates


cv2.destroyAllWindows()

run_calibration()
