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

    e_l = searchers.Landmark(g, end)
    p_h = lambda n, e: e_l.cost_to_l[n]
    max_cost_to_e = max(e_l.cost_to_l.itervalues())
    def perfect_h_callback(y, x):
        v = float(p_h((y,x), None)) / max_cost_to_e * 255
        return (v, v, v)
    
    l = searchers.Landmark(g, (0, 0))
    l_h = lambda n, e: max(l.cost_from_l[e] - l.cost_from_l[n], l.cost_to_l[n] - l.cost_to_l[e], 0)
    max_cost_from_l = max(l.cost_from_l.itervalues())
    max_cost_to_l = max(l.cost_from_l.itervalues())
    def landmark_h_callback(y, x):
        n = (y, x)
        h_n = l_h(n, end)
        v = float(h_n) / max(max_cost_from_l, max_cost_to_l) * 255
        return (v, v, v)
        
    def perfect_minus_landmark(y, x):
        pv = p_h((y,x), None)
        lv = l_h((y,x), end)
        v = float(pv - lv) / max_cost_to_e * 255
        return (v, v, v)

    bmp.write_many('output.bmp', width, height,
        [
            [perfect_h_callback, landmark_h_callback],
            [perfect_minus_landmark],
        ])

if __name__ == '__main__':
    main()