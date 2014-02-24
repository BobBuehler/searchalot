import bmp
import grids
import searchers
import random

def main():
    random.seed(45)
    width = 30
    height = 20
    minCost = 10
    maxCost = 40
    start = (6,8)
    end = (16,20)
    
    g = grids.generate(width, height, minCost, maxCost, random)
    #grids.set_row(g, 5, 5)
    #grids.set_col(g, 5, 5)
    #grids.set_col(g, 15, 5)
    def cost_callback(y, x):
        v = g[y][x]
        v = int(float(v) / maxCost * 127)
        return (v, v, v)
    
    e_l = searchers.Landmark(g, end)
    p_h = lambda n, e: e_l.cost_to_l[n]
    max_cost_to_e = max(e_l.cost_to_l.itervalues())
    def perfect_h_callback(y, x):
        v = float(p_h((y,x), None)) / max_cost_to_e * 255
        return (v, v, v)
    a_p = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=p_h)
    a_p.search(start, end)
    def searched_perfect_callback(y, x):
        v = cost_callback(y, x)
        if (y,x) in a_p.path:
            v = (v[0], v[1], v[2] + 127)
        elif (y,x) in a_p.closed_set:
            v = (v[0], v[1] + 127, v[2])
        elif (y,x) in a_p.open_set:
            v = (v[0] + 127, v[1], v[2])
        return v
        
    a_p_endless = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=p_h)
    a_p_endless.search(start, None)
    max_f = max(a_p_endless.f_scores.itervalues())
    def f_callback(y, x):
        v = float(a_p_endless.f_scores[(y,x)]) / max_f * 255
        return (v, v, v)
    
    bmp.write_many('output.bmp', width, height,
        [
            [perfect_h_callback, searched_perfect_callback],
            [f_callback]
        ])

if __name__ == '__main__':
    main()