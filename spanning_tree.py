import sys
import random
#import matplotlib.pyplot as plt
#import mpl_toolkits.mplot3d.axes3d as p3
#import matplotlib.animation as animation


class Point:
    def __init__ (self, coordinates, next_p):
        self.coordinates = coordinates
        self.next_p = next_p

class Path:
    def __init__ (self, head, last):
        self.head = head
        self.last = last
        self.head.next_p = self.last
        self.length = 2
        self.dead = False

def reset (path):
    new_last = path.head.next_p

    while (is_valid (path) == False and 
            new_last != None):
        path.last = new_last
        new_last = new_last.next_p

    if (is_valid(path) == False):
        path.dead = True
        
def add_point (path, new_coord, painted):
    cube[new_coord[0]][new_coord[1]][new_coord[2]] = 1
    connections.append ([list(path.last.coordinates), 
                         list(new_coord)])
    point = Point (new_coord, None)
    path.last.next_p = point
    path.last = point
    path.length += 1
    painted += 1

    return painted

def fork (path, new_coord, painted):
    cube[new_coord[0]][new_coord[1]][new_coord[2]] = 1
    point = Point (new_coord, None)

    path_list.append (
            Path (Point (path.last.coordinates, point), point))

    connections.append ([list(path.last.coordinates), 
                         list(new_coord)])
    painted += 1
    
    return painted

def find (path, direction):
    new_coord = [0,0,0]
    for i in range (len (path.last.coordinates)):
        new_coord[i] = path.last.coordinates[i]

    if direction == 0:
        new_coord[0] += 1 
    elif direction == 1:
        new_coord[1] += 1
    elif direction == 2:
        new_coord[2] += 1        
    elif direction == 3:
        new_coord[0] -= 1
    elif direction == 4:
        new_coord[1] -= 1
    elif direction == 5:
        new_coord[2] -= 1

    if (new_coord[0] > n - 1 or new_coord[0] < 0 or
        new_coord[1] > n - 1 or new_coord[1] < 0 or
        new_coord[2] > n - 1 or new_coord[2] < 0 or
        cube[new_coord[0]]
            [new_coord[1]]
            [new_coord[2]] == 1):
        return None

    return list (new_coord)

def is_valid (path):
    coord = path.last.coordinates
    if (coord[0] < n - 1 and 
        cube[coord[0] + 1]
            [coord[1]]
            [coord[2]] == 0):
        return True
    elif (coord[0] > 0 and
        cube[coord[0] - 1]
            [coord[1]]
            [coord[2]] == 0):
        return True 
    elif (coord[1] < n - 1 and
        cube[coord[0]]
            [coord[1] + 1]
            [coord[2]] == 0):
        return True
    elif (coord[1] > 0 and
        cube[coord[0]]
            [coord[1] - 1]
            [coord[2]] == 0):
        return True
    elif (coord[2] < n - 1 and
        cube[coord[0]]
            [coord[1]]
            [coord[2] + 1] == 0):
        return True
    elif (coord[2] > 0 and
        cube[coord[0]]
            [coord[1]]
            [coord[2] - 1] == 0):
        return True

    return False

def walk (max_path_length):
    painted = 2
    has_live_paths = True
    print ("Walking...")
    while (painted < n*n*n):
        has_live_paths = False
        for path in path_list:
            if (path.dead == False):
                has_live_paths = True
                direction = random.randrange (0, 6)
                new_coord = find (path, direction)
                valid = is_valid (path)
                if (valid):
                    if (path.length >= max_path_length and
                            new_coord != None):
                        painted = fork (path, new_coord, painted)
                    elif (new_coord != None):
                        painted = add_point (path, new_coord, painted)
                else:
                    reset (path)
        if (has_live_paths == False):
            print ("All paths died.")
            break

    print ("Done!")
    print ("Painted: ", painted)

#def animate (i):
#    connection = connections[i]
#    p1 = connection[0]
#    p2 = connection[1]
#    lines.append (space.plot (
#        [p1[0], p2[0]],
#        [p1[1], p2[1]],
#        [p1[2], p2[2]],
#        antialiased = True))

#    space.view_init (11, azim=2.5 * i)
#    return lines

if (len(sys.argv) == 2):
    print ("""Usage:
    $ python spanning_tree.py [<cube_size> <max_path_length>]
            """)
    sys.exit()
elif (len(sys.argv) > 2):
    max_path_length = int (sys.argv[2])
    n = int (sys.argv[1])
else:
    max_path_length = 1 
    n = 10 

#figure = plt.figure ()
#space = figure.add_axes ([0, 0, 1, 1], projection='3d')
#space.axis ('off')

#space.set_xlim3d ([0, n])
#space.set_ylim3d ([0, n])
#space.set_zlim3d ([0, n])

cube = [[[
    0 
    for k in range (n)] 
    for j in range (n)] 
    for i in range (n)]

path_list = []
lines = []
connections = []

p1 = Point ([n//2, n//2, (n//2) + 1], None)
p0 = Point ([n//2, n//2, n//2], p1)
path_list.append (Path (p0, p1))
connections.append ([list(p0.coordinates), 
                     list(p1.coordinates)])

walk (max_path_length)

print ("Paths: ", len(path_list))

#anim = animation.FuncAnimation (
#        figure, 
#        animate,
#        frames = len(connections),
#        interval=2, 
#        blit=False,
#        repeat=True
#        )
#plt.show()
