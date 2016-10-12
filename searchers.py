import grids

# n(n) calculates the neighbors of n
# g(n1,n2) calculates the cost of going from n1 to n2
# h(n,e) estimates the minimum remaining cost from n to e
# r(n) calculates upper bound on reach
class AStar:
    def __init__(self, n, g, h = None, r = None):
        self.n = n
        self.g = g
        self.h = h if h else lambda n,e: 0
        self.r = r if r else lambda n: float('inf')
    
    def search(self, start, end):
        self.g_scores = {start: 0}
        self.f_scores = {start: self.h(start, end)}
        
        self.closed_set = set()
        self.closed_list = []
        self.open_set = [start]
        self.came_from = {}
        
        while self.open_set and end not in self.closed_set:
            current = min(reversed(self.open_set), key=lambda n: self.f_scores[n])
            self.open_set.remove(current)
            self.closed_set.add(current)
            self.closed_list.append(current)
            
            for neighbor in self.n(current):
                if neighbor in self.closed_set:
                    continue
                tentative_g = self.g_scores[current] + self.g(current, neighbor)
                
                if neighbor not in self.open_set or tentative_g < self.g_scores[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_scores[neighbor] = tentative_g
                    h_value = self.h(neighbor, end)
                    self.f_scores[neighbor] = tentative_g + h_value
                    r_value = self.r(neighbor)
                    if tentative_g <= r_value and h_value <= r_value and neighbor not in self.open_set:
                        self.open_set.append(neighbor)

        self.path = reconstruct_path(self.came_from, end)    
    
class Landmark:
    def __init__(self, grid, position):
        self.grid = grid
        self.position = position
        self.calculate()
        
    def calculate(self):
        a = AStar(
            lambda n: grids.neighbor_nodes(self.grid, n),
            lambda n1, n2: self.grid[n2[0]][n2[1]],
            lambda n, e: 0)
        a.search(self.position, None)
        self.cost_from_l = a.g_scores
        a = AStar(
            lambda n: grids.neighbor_nodes(self.grid, n),
            lambda n1, n2: self.grid[n1[0]][n1[1]],
            lambda n, e: 0)
        a.search(self.position, None)
        self.cost_to_l = a.g_scores

class Reach:
    def __init__(self, grid):
        self.grid = grid
        self.calculate()
        
    def calculate(self):
        height = len(self.grid)
        width = len(self.grid[0])
        self.value = grids.generate(width, height, 0, 0)
        a = AStar(
            lambda n: grids.neighbor_nodes(self.grid, n),
            lambda n1, n2: self.grid[n1[0]][n1[1]],
            lambda n, e: 0)
        for y in xrange(height):
            for x in xrange(width):
                a.search((y,x), None)
                for leaf_node in find_leaf_nodes(a.came_from):
                    path = reconstruct_path(a.came_from, leaf_node)
                    path_distance = sum(self.grid[node[0]][node[1]] for node in path[1:])
                    distance_to = 0
                    for path_node in path[1:]:
                        distance_to += self.grid[path_node[0]][path_node[1]]
                        distance_from = path_distance - distance_to
                        path_reach = min(distance_to, distance_from)
                        if path_reach > self.value[path_node[0]][path_node[1]]:
                            self.value[path_node[0]][path_node[1]] = path_reach

def reconstruct_path(came_from, node):
    path = [node]
    while node in came_from:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path

def find_leaf_nodes(came_from):
    parents = set()
    nodes = set()
    for node in came_from:
        nodes.add(node)
        parents.add(came_from[node])
    return nodes - parents
