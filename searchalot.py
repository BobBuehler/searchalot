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

    max_h = 50 * minCost

    manhattan_h = lambda n, e: abs(n[0] - e[0]) + abs(n[1] - e[1])
    def manhattan_h_callback(y, x):
        v = float(manhattan_h((y,x), end)) / max_h * 255
        return (v, v, v)
    a_manhattan = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=manhattan_h)
    a_manhattan.search(start, end)
    def searched_manhattan_callback(y, x):
        v = cost_callback(y, x)
        if (y,x) in a_manhattan.path:
            v = (v[0], v[1], v[2] + 127)
        elif (y,x) in a_manhattan.closed_set:
            v = (v[0], v[1] + 127, v[2])
        elif (y,x) in a_manhattan.open_set:
            v = (v[0] + 127, v[1], v[2])
        return v

    manhattan_c_h = lambda n, e: (abs(n[0] - e[0]) + abs(n[1] - e[1])) * minCost
    def manhattan_c_h_callback(y, x):
        v = float(manhattan_c_h((y,x), end)) / max_h * 255
        return (v, v, v)
    a_manhattan_c = searchers.AStar(
        lambda n: grids.neighbor_nodes(g, n),
        lambda n1, n2: g[n2[0]][n2[1]],
        h=manhattan_c_h)
    a_manhattan_c.search(start, end)
    def searched_manhattan_c_callback(y, x):
        v = cost_callback(y, x)
        if (y,x) in a_manhattan_c.path:
            v = (v[0], v[1], v[2] + 127)
        elif (y,x) in a_manhattan_c.closed_set:
            v = (v[0], v[1] + 127, v[2])
        elif (y,x) in a_manhattan_c.open_set:
            v = (v[0] + 127, v[1], v[2])
        return v

    bmp.write_many('output.bmp', width, height,
        [
            [cost_callback, searched_callback],
            [manhattan_h_callback, searched_manhattan_callback],
            [manhattan_c_h_callback, searched_manhattan_c_callback]
        ])

if __name__ == '__main__':
    main()