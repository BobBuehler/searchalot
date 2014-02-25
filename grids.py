import math

def _random_ease_in_out(min, max, power, random):
    if min == max:
        return min
    t = math.pow(random.random(), power) / 2
    if (random.random() > .5):
        t = 1 - t
    v = (max - min + 1) * t + min
    v = int(v)
    if v > max: v = max # the teeniest bias away from exact mid and toward exact max
    #print t, v
    return v

def generate(width, height, minCost, maxCost, random):
    return [[_random_ease_in_out(minCost, maxCost, 2, random) for x in xrange(width)] for y in xrange(height)]

def neighbor_nodes(grid, node):
    maxY = len(grid) - 1
    maxX = len(grid[0]) - 1
    
    neighbors = []
    if node[0] > 0:
        neighbors.append((node[0]-1, node[1]))
    if node[0] < maxY:
        neighbors.append((node[0]+1, node[1]))
    if node[1] > 0:
        neighbors.append((node[0], node[1]-1))
    if node[1] < maxX:
        neighbors.append((node[0], node[1]+1))
    return neighbors

def set_row(grid, row, value):
    for col in xrange(len(grid[row])):
        grid[row][col] = value
        
def set_col(grid, col, value):
    for row in xrange(len(grid)):
        grid[row][col] = value
        