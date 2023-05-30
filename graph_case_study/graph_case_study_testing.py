'''
Testing bfs, dfs and topological sort on linked directed graph
'''

from graph import *
from linkedstack import LinkedStack
from collections import deque

def read_file(path: str) -> LinkedDirectedGraph:
    '''
    Reads from file and transform data into directed graph
    Also checks for simillar nodes (doesn't add twice)
    '''
    graph = LinkedDirectedGraph()
    vertices = {}  # Need for tracking already present nodes in the graph
    with open(path) as file:
        next(file) # skips first line
        for line in file.readlines():
            node_data = line.split()
            node_label = node_data[0]
            if node_label not in vertices:
                node = LinkedVertex(node_label)
                vertices[node_label] = node
                graph.addVertex(node_label)
            else:
                node = vertices[node_label]
            adjacent_nodes = str(node_data[1:])[3:-3].replace(',', '').replace("'", '').split() # specical for reading correctly the line with two and more adjacent vertices
            for adj_node_label in adjacent_nodes:
                if adj_node_label != 'none':
                    if adj_node_label not in vertices:
                        adj_node = LinkedVertex(adj_node_label)
                        vertices[adj_node_label] = adj_node
                        graph.addVertex(adj_node_label)
                    else:
                        adj_node = vertices[adj_node_label]
                    if not graph.containsEdge(node_label, adj_node_label):
                        graph.addEdge(node_label, adj_node_label, None)
    return graph

def dfs_test(graph: LinkedDirectedGraph, vertex_position: LinkedVertex):
    '''
    DFS traversal in linked directed graph from given position.
    Marking all vertices on its way (DFS) and return list of marked vertices (path)
    Clears all vertex marks in graph before dfs
    Note: works with unique items in graph (means every node in graph has its unique label)
    On graph with identical labels wasn't tested :)
    '''
    graph.clearVertexMarks()
    stack = LinkedStack()
    path = []
    vertex_position.setMark()
    stack.push(vertex_position)
    while not stack.isEmpty():
        current_vertex = stack.pop()
        path.append(current_vertex.getLabel())
        for vertex in graph.neighboringVertices(current_vertex.getLabel()):
            if not vertex.isMarked():
                vertex.setMark()
                stack.push(vertex)
    return path
    
def bfs_test(graph: LinkedDirectedGraph, vertex_position: LinkedVertex):
    '''
    DFS traversal in linked directed graph from given position.
    Marking all vertices on its way (BFS) and return list of marked vertices (path)
    Clears all vertex marks in graph before bfs
    Note: works with unique items in graph (means every node in graph has its unique label)
    On graph with identical labels wasn't tested :)

    '''
    graph.clearVertexMarks()
    path = []
    queue = deque([vertex_position])
    vertex_position.setMark()
    while queue:
        current_vertex = queue.popleft()
        path.append(current_vertex.getLabel())
        for vertex in graph.neighboringVertices(current_vertex.getLabel()):
            if not vertex.isMarked():
                vertex.setMark()
                queue.append(vertex)
    return path

def topological_sort_test(graph: LinkedDirectedGraph, start_label=None) -> LinkedStack:
    '''
    Makes topological sort on graph and returns stack of vertices on its path
    Starts from start_label if given else start from first in graph
    Clears all vertex marks in graph before bfs
    '''
    graph.clearVertexMarks()
    stack = LinkedStack()

    def helper_dfs(graph: LinkedDirectedGraph, vertex_position: LinkedVertex, stack: LinkedStack) -> None:
        '''
        Helper function for topo sort
        '''
        vertex_position.setMark()
        for vertex in graph.neighboringVertices(vertex_position.getLabel()):
            if not vertex.isMarked():
                helper_dfs(graph, vertex, stack)
        stack.push(vertex_position)

    if start_label is not None:
        start_vertex = graph.getVertex(start_label)
        helper_dfs(graph, start_vertex, stack)
    else:
        for vertex in graph.vertices():
            if not vertex.isMarked():
                helper_dfs(graph, vertex, stack)
    return stack
    
def run() -> None:
    '''
    Runs all tests to get and return results
    '''
    graph = read_file('data/stanford_cs.txt')
    vertex_position = graph.getVertex('CS161') # used to start tests from specific position, can be changed
    dfs = dfs_test(graph, vertex_position)
    bfs = bfs_test(graph, vertex_position)
    topo_sort = topological_sort_test(graph) # can also add start position in str name if need
    return dfs, bfs, topo_sort

if __name__ == '__main__':
    dfs, bfs, topo_sort = run()
    print(f'DFS Result: {dfs}\nBFS Result: {bfs}\nTopological sort: {topo_sort}')
    

