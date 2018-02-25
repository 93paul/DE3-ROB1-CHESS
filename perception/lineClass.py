import cv2
import numpy as np


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.dy = self.y2 - self.y1
        self.dx = self.x2 - self.x1
        self.center = ((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)

        if abs(self.dx) > abs(self.dy):
            self.category = 'horizontal'
        else:
            self.category = 'vertical'

        self.c = -(self.x1 * self.y2 - self.x2 * self.y1)

    def draw(self, image, color=(0, 0, 255), thickness=2):
        '''
        Draws line onto image
        :param image:
        :param color:
        :param thickness:
        :return:
        '''
        cv2.line(image, (self.x1, self.y1), (self.x2, self.y2), color, thickness)

    def intersect(self, other):
        '''
        Finds intersections points between two lines
        :param other:
        :return:
        '''

        if self.x * other.b == other.a * self.y:
            raise ValueError("Lines have the same slope.")

        a = np.array ( ( (self.x, self.y), (other.a, other.b) ) )
        b = np.array ( (-self.c, -other.c) )
        x, y = np.linalg.solve(a,b)

        return x,y


def filterClose(lines, horizontal=True, threshold = 40):
    if horizontal:
        item = 1
    else:
        item = 0

    i = 0
    ret = []

    while i < len(lines):
        itmp = i
        while i < len(lines) and (lines[i].center[item] - lines[itmp].center[item] < threshold):
            i += 1
        ret.append(lines[itmp + int((i - itmp) / 2)])
    return ret

