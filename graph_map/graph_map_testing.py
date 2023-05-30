'''
Testing bfs, dfs and topo sort on graph map
'''
from graph import *

def read_file(path: str) -> Graph:
    '''
    Reads from file and transform data into graph
    '''
    graph = Graph()
    vertices = {} # need for tracking already present nodes in graph and not to create another objects with same node name
    with open(path) as file:
        next(file)
        for line in file.readlines():
            node_data = line.split()
            node_label = node_data[0]
            if node_label not in vertices:
                node = graph.insert_vertex(node_label)
                vertices[node_label] = node
            else:
                node = vertices[node_label]
            adjacent_nodes = str(node_data[1:])[3:-3].replace(',', '').replace("'", '').split()
            for adj_node_label in adjacent_nodes:
                if adj_node_label != 'none':
                    if adj_node_label not in vertices:
                        adj_node = graph.insert_vertex(adj_node_label)
                        vertices[adj_node_label] = adj_node
                    else:
                        adj_node = vertices[adj_node_label]
                    existing_edge = None
                    for edge in graph.incident_edges(node):
                        if edge.opposite(node) == adj_node:
                            existing_edge = edge
                            break
                    if existing_edge is None:
                        graph.insert_edge(node, adj_node)
    return graph

def dfs_test(graph: Graph) -> dict:
    '''
    Perform DFS for entire graph and return forest (with labels) as a dictionary.
    Result maps each vertex v to the edge (tuple of labels) that was used to discover it.
    (Vertices that are roots of a DFS tree are mapped to None.)
    '''
    forest = {}
    discovered = {}

    def DFS(u: Graph.Vertex, edge: Graph.Edge) -> None:
        '''
        Perform DFS of the undiscovered portion of Graph g starting at Vertex u.
        discovered is a dictionary mapping each vertex to the edge that was used to
        discover it during the DFS. (u should be "discovered" prior to the call.)
        Newly discovered vertices will be added to the dictionary as a result.
        '''
        if u not in discovered:
            if edge is not None:
                forest[u.element()] = edge.endpoints()[0].element(), edge.endpoints()[1].element()
            else:
                forest[u.element()] = edge
            discovered[u] = edge
            for e in graph.incident_edges(u):
                v = e.opposite(u)
                DFS(v, e)

    for vertex in graph.vertices():
        if vertex not in forest:
            DFS(vertex, None)
    return forest

def bfs_test(graph: Graph) -> dict:
    '''
    Perform BFS for entire graph and return forest (with labels) as a dictionary.
    Result maps each vertex v to the edge that was used to discover it (tuple of labels).
    (vertices that are roots of a BFS tree are mapped to None).
    '''
    forest = {}
    
    def BFS(graph: Graph, s: Graph.Vertex, discovered: dict) -> None:
        '''
        Perform BFS of the undiscovered portion of Graph g starting at Vertex s.
        discovered is a dictionary mapping each vertex to the edge that was used to
        discover it during the BFS (s should be mapped to None prior to the call).
        Newly discovered vertices will be added to the dictionary as a result.
        '''
        level = [s]
        while len(level) > 0:
            next_level = []
            for u in level:
                for e in graph.incident_edges(u):
                    v = e.opposite(u)
                    if v not in discovered:
                        discovered[v] = e
                        next_level.append(v)
            level = next_level

    for u in graph.vertices():
        if u not in forest:
            forest[u] = None
            BFS(graph, u, forest)

    for key in list(forest.keys()):
        val = forest.pop(key)
        if val is not None:
            val = val.endpoints()[0].element(), val.endpoints()[1].element()
        key = key.element()
        forest[key] = val
    return forest

def run() -> None:
    '''
    Running all testing functions
    '''
    graph = read_file('data/stanford_cs.txt')
    dfs = dfs_test(graph)
    bfs = bfs_test(graph)
    return dfs, bfs

if __name__ == '__main__':
    dfs, bfs = run()
    print(f'DFS Result: {dfs}\nBFS Result: {bfs}')
