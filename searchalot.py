import bmp
import grids
import searchers
import random

def main():
    random.seed(44)
    width = 30
    height = 20
    minCost = 10
    maxCost = 40
    highwayCost = 5
    start = (6,8)
    end = (16,20)
    
    g = grids.generate(width, height, minCost, maxCost, random)
    def cost_callback(y, x):
        v = g[y][x]
        v = int(float(v) / maxCost * 127)
        return (v, v, v)
    
    a = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]])
    a.search(start, end)
    def searched_callback(y, x):
        v = cost_callback(y, x)
        if (y,x) in a.path:
            v = (v[0], v[1], v[2] + 127)
        elif (y,x) in a.closed_set:
            v = (v[0], v[1] + 127, v[2])
        elif (y,x) in a.open_set:
            v = (v[0] + 127, v[1], v[2])
        return v
    
    l = searchers.Landmark(g, (0, 0))
    l_h = lambda n, e: max(l.cost_to_l[n] - l.cost_to_l[e], l.cost_from_l[e] - l.cost_from_l[n], 0)
    max_cost_to_l = max(l.cost_to_l.itervalues())
    def landmark_h_callback(y, x):
        n = (y, x)
        h_n = l_h(n, end)
        v = float(h_n) / max_cost_to_l * 255
        return (v, v, v)
    
    a_l = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=l_h)
    a_l.search(start, end)
    def searched_landmark_callback(y, x):
        v = (20,20,20)
        if (y,x) in a_l.path:
            v = (50,50,200)
        elif (y,x) in a_l.closed_set:
            v = (50,200,50)
        elif (y,x) in a_l.open_set:
            v = (200,50,50)
        return v
    
    r = searchers.Reach(g)
    max_reach = max([max([r.value[y][x] for x in xrange(width)]) for y in xrange(height)])
    def reach_callback(y, x):
        v = float(r.value[y][x]) / max_reach * 255
        return (v, v, v)
    
    a_r = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=l_h,
        r=lambda n: r.value[n[0]][n[1]])
    a_r.search(start, end)
    def searched_reach_callback(y, x):
        v = (20,20,20)
        if (y,x) in a_r.path:
            v = (50,50,200)
        elif (y,x) in a_r.closed_set:
            v = (50,200,50)
        elif (y,x) in a_r.open_set:
            v = (200,50,50)
        return v
    
    bmp.write_many('output.bmp', width, height,
        [
            [cost_callback, searched_callback],
            [landmark_h_callback, searched_landmark_callback],
            [reach_callback, searched_reach_callback]
        ])

if __name__ == '__main__':
    main()