import sys
import random
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

class Point:
    def get_indexes (self, direction):
        if (direction == 0 and self.pos[0] < n - 1):
            return [self.pos[0] + 1,
                    self.pos[1],
                    self.pos[2]]
        elif (direction == 1 and self.pos[0] > 0):
            return [self.pos[0] - 1,
                    self.pos[1],
                    self.pos[2]]
        elif (direction == 2 and self.pos[1] < n - 1):
            return [self.pos[0],
                    self.pos[1] + 1,
                    self.pos[2]]
        elif (direction == 3 and self.pos[1] > 0):
            return [self.pos[0],
                    self.pos[1] - 1,
                    self.pos[2]]
        elif (direction == 4 and self.pos[2] < n - 1):
            return [self.pos[0],
                    self.pos[1],
                    self.pos[2] + 1]
        elif (direction == 5 and self.pos[2] > 0):
            return [self.pos[0],
                    self.pos[1],
                    self.pos[2] - 1]
        else:
            return None

    def __init__ (self, pos, came_from):
        global cube
        self.pos = pos
        self.came_from = came_from
        cube[self.pos[0]][self.pos[1]][self.pos[2]] = 1
        self.prox = [-1, -1, -1, -1, -1, -1]
        for i in range (len (self.prox)):
            npos = self.get_indexes (i)
            if (npos != None):
                self.prox[i] = cube[npos[0]][npos[1]][npos[2]]

    def not_surrounded (self):
        for p in self.prox:
            if (p == 0):
                return True
        return False

    def is_free (self, direction):
        npos = self.get_indexes (direction)
        if (npos != None):
            cvalue = cube[npos[0]][npos[1]][npos[2]]
            self.prox[direction] = cvalue
        if (self.prox[direction] == 0):
            return True
        return False

    def occupy (self, direction):
        self.came_from = direction
        npos = self.get_indexes (direction)
        return npos

if (len(sys.argv) > 2):
    print ("""Usage:
    $ python spanning_tree.py [cube_size]
            """)
    sys.exit()
elif (len(sys.argv) == 2):
    n = int (sys.argv[1])
else:
    n = 6

current_frame = 0
connections = []
current_points = []
cube = [[[ 0 for k in range (n)]
             for j in range (n)]
             for i in range (n)]

def shell_walk ():
    global current_points
    current_points.append (Point ([n - 1, 0, n - 1], 
        random.randrange (0, 6, 1)))
    found = 0
    while (current_points != []):
        working = current_points
        current_points = []
        for p in working:
            direction = random.randrange (0, 6, 1)
            if (p.not_surrounded ()): 
                current_points.append (p)
                if (p.is_free (direction)):
                    npos = p.occupy (direction)
                    newp = Point ([npos[0], 
                        npos[1], 
                        npos[2]], 
                        direction)
                    current_points.append (newp)
                    connections.append ([p.pos, npos])
                    found += 1
                    while (newp.not_surrounded ()):
                        if (newp.is_free (direction)):
                            npos = newp.occupy (direction)
                            current_points.append (Point (
                                [npos[0], npos[1], npos[2]], direction))
                            connections.append ([newp.pos, npos])
                            found += 1
                        else:
                            direction = random.randrange (0, 6, 1)
                        if (newp.not_surrounded):
                            newp = Point ([npos[0], 
                                npos[1], 
                                npos[2]], 
                                direction)
                    connections.append (None)
        connections.append (None)
    print ("Found", found, "points!")

def depth_walk ():
    global current_points
    current_points.append (Point ([n - 1, 0, n - 1], 
        random.randrange (0, 6, 1)))
    found = 0
    while (current_points != []):
        working = current_points
        current_points = []
        for p in working:
            direction = random.randrange (0, 6, 1)
            if (p.not_surrounded ()): 
                current_points.append (p)
                if (p.is_free (direction)):
                    npos = p.occupy (direction)
                    newp = Point ([npos[0], 
                        npos[1], 
                        npos[2]], 
                        direction)
                    current_points.append (newp)
                    connections.append ([p.pos, npos])
                    found += 1
                    while (newp.is_free (direction)):
                        npos = newp.occupy (direction)
                        current_points.append (Point (
                            [npos[0], npos[1], npos[2]], direction))
                        connections.append ([newp.pos, npos])
                        found += 1
                        newp = Point ([npos[0], 
                            npos[1], 
                            npos[2]], 
                            direction)
        connections.append (None)
    print ("Found", found, "points!")

def weighted_walk ():
    global current_points
    current_points.append (Point ([n - 1, 0, n - 1], 
        random.randrange (0, 6, 1)))
    found = 0
    while (current_points != []):
        working = current_points
        current_points = []
        for p in working:
            direction = random.randrange (0, 100, 1)
            if (direction < 60):
                direction = p.came_from
            else:
                direction %= 6
            if (p.not_surrounded ()): 
                current_points.append (p)
                if (p.is_free (direction)):                
                    npos = p.occupy (direction)
                    current_points.append (Point (
                        [npos[0], npos[1], npos[2]], direction))
                    connections.append ([p.pos, npos])
                    found += 1
        connections.append (None)
    print ("Found", found, "points!")

def random_walk ():
    global current_points
    current_points.append (Point ([n - 1, 0, n - 1], 
        random.randrange (0, 6, 1)))
    found = 0
    while (current_points != []):
        working = current_points
        current_points = []
        for p in working:
            direction = random.randrange (0, 6, 1)
            if (p.not_surrounded ()): 
                current_points.append (p)
                if (p.is_free (direction)):                
                    npos = p.occupy (direction)
                    current_points.append (Point (
                        [npos[0], npos[1], npos[2]], direction))
                    connections.append ([p.pos, npos])
                    found += 1
        connections.append (None)
    print ("Found", found, "points!")

def animate ():
    global current_frame
    while (current_frame < len (connections) and
            connections[current_frame] != None):
        p1 = connections[current_frame][0]
        p2 = connections[current_frame][1]
        points = np.vstack (
                            [[p1[0], p2[0]],
                             [p1[1], p2[1]],
                             [p1[2], p2[2]]]
                ).transpose ()
        colors = pg.glColor ((current_frame,n*100))
        plot = gl.GLLinePlotItem (pos=points,
                color = colors,
                width = 3,
                antialias=True)
        window.addItem (plot)
        current_frame += 1
    current_frame += 1

#random_walk ()
#weighted_walk ()
depth_walk ()
#shell_walk ()

app = QtGui.QApplication ([])
window = gl.GLViewWidget ()
window.opts['distance'] = n * 3 
window.show ()
window.setWindowTitle ("SpanTree3d")
current_frame = 0
timer = QtCore.QTimer ()
timer.timeout.connect (animate)
timer.start (0)
QtGui.QApplication.instance ().exec_()    
