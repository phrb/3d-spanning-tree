Spanning Trees in a Cube
------

This python script generates a tree that tries to reach
every node of a cube exactly once, i.e., makes a 3d maze.

The tree obey certain rules, or "walking modes", defined
by functions in the script:

Random Walk: Chooses a new direction for each point,
with no other heuristic than the random number generator.

Weighted Walk: Has a propension to favor a point's previous
direction in new extensions.

Depth Walk: Extends in a single direction until it finds
an occupied cell or the end of the cube.

Shell Walk: Extends until it can, then change direction and 
continue extending, making same-colored paths that span the
"shell" of the cube.

Usage:

    $ python span_tree.py [<random|weighted|depth|shell> <cube_size>]

