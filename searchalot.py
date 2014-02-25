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
    start = (6,8)
    end = (16,20)
    
    g = grids.generate(width, height, minCost, maxCost, random)
    def cost_callback(y, x):
        v = g[y][x]
        v = int(float(v) / maxCost * 127)
        return (v, v, v)
    
    l = searchers.Landmark(g, (0, 0))
    l_h = lambda n, e: max(l.cost_from_l[e] - l.cost_from_l[n], l.cost_to_l[n] - l.cost_to_l[e])
    max_cost_from_l = max(l.cost_from_l.itervalues())
    max_cost_to_l = max(l.cost_from_l.itervalues())
    def landmark_h_callback(y, x):
        n = (y, x)
        h_n = l_h(n, end)
        v = float(h_n) / max(max_cost_from_l, max_cost_to_l) * 255
        if v < 0:
            return (256+v, 0, 256+v)
        return (v, v, v)
    
    a_l = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=l_h)
    a_l.search(start, end)
    def searched_landmark_callback(y, x):
        v = cost_callback(y, x)
        if (y,x) in a_l.path:
            v = (v[0], v[1], v[2] + 127)
        elif (y,x) in a_l.closed_set:
            v = (v[0], v[1] + 127, v[2])
        elif (y,x) in a_l.open_set:
            v = (v[0] + 127, v[1], v[2])
        return v
        
    lz_h = lambda n, e: max(l.cost_from_l[e] - l.cost_from_l[n], l.cost_to_l[n] - l.cost_to_l[e], 0)
    def landmarkz_h_callback(y, x):
        n = (y, x)
        h_n = lz_h(n, end)
        v = float(h_n) / max(max_cost_from_l, max_cost_to_l) * 255
        if v < 0:
            return (256+v, 0, 256+v)
        return (v, v, v)
    
    a_lz = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=lz_h)
    a_lz.search(start, end)
    def searched_landmarkz_callback(y, x):
        v = cost_callback(y, x)
        if (y,x) in a_lz.path:
            v = (v[0], v[1], v[2] + 127)
        elif (y,x) in a_lz.closed_set:
            v = (v[0], v[1] + 127, v[2])
        elif (y,x) in a_lz.open_set:
            v = (v[0] + 127, v[1], v[2])
        return v
    
    bmp.write_many('output.bmp', width, height,
        [
            [landmark_h_callback, searched_landmark_callback],
            [landmarkz_h_callback, searched_landmarkz_callback],
        ])

if __name__ == '__main__':
    main()