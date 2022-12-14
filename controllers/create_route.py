import numpy as np
import pandas as pd
import heapq  # priority queue
import copy

df = pd.read_excel(
    "models/database/dataset.xlsx", sheet_name="Graph", usecols="A", header=None
)


num_rows = df.shape[0]
num_rows


class Point:
    ID = 0

    def __init__(self, coor):
        # self.street = src['Đường'].split(',')
        # self.name = src['Tên địa điểm']
        self.X = coor[0]
        self.Y = coor[1]
        self.ID = Point.ID
        Point.ID += 1


Points = []
Adjacency = []


def distance(p0, p1):
    return pow(pow((p0.X - p1.X), 2) + pow((p0.Y - p1.Y), 2), 1 / 2)


def find_in_Points(coor):
    if len(Points) == 0:
        return -1
    for idx in range(len(Points)):
        if Points[idx].X == coor[0] and Points[idx].Y == coor[1]:
            return idx
    return -1


for idx in range(num_rows):
    src = df.iloc(0)[idx][0]
    src = src.split(" ", 1)[1]
    src = src[1:-1]
    src = src.split(", ")

    listID = []

    for coor in src:
        coor = coor.split(" ")
        coor = [float(x) for x in coor]

        idx = find_in_Points(coor)
        if idx == -1:
            Points.append(Point(coor))
            Adjacency.append([])
            listID.append(Points[-1].ID)
        else:
            listID.append(Points[idx].ID)
    # print(listID)
    n = len(listID)
    if n >= 2:
        if not listID[1] in Adjacency[listID[0]]:
            Adjacency[listID[0]].append(listID[1])
    for i in range(1, n - 1):
        if not listID[i - 1] in Adjacency[listID[i]]:
            Adjacency[listID[i]].append(listID[i - 1])
        if not listID[i + 1] in Adjacency[listID[i]]:
            Adjacency[listID[i]].append(listID[i + 1])
    if n >= 2:
        if not listID[n - 2] in Adjacency[listID[n - 1]]:
            Adjacency[listID[n - 1]].append(listID[n - 2])
        # print(listID[n - 1])


class Route:
    def __init__(self, src):
        self.v = [src]
        self.len = 0

    def __lt__(self, other):
        return self.len < other.len

    def __le__(self, other):
        return self.len <= other.len

    def add(self, vID, len):
        self.v.append(vID)
        self.len += len

    def get_tail(self):
        return self.v[-1]

    def get_vertices(self):
        return self.v


# print(Points)
# print(Adjacency)

# Python program for Kruskal's algorithm to find
# Minimum Spanning Tree of a given connected,
# undirected and weighted graph

# Class to represent a graph


class Graph:
    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []
        # to store graph

    # function to add an edge to graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # A utility function to find set of an element i
    # (truly uses path compression technique)
    def find(self, parent, i):
        if parent[i] != i:
            # Reassignment of node's parent to root node as
            # path compression requires
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x

        # If ranks are same, then make one as root
        # and increment its rank by one
        else:
            parent[y] = x
            rank[x] += 1

    # The main function to construct MST using Kruskal's
    # algorithm
    def KruskalMST(self):

        result = []  # This will store the resultant MST

        # An index variable, used for sorted edges
        i = 0

        # An index variable, used for result[]
        e = 0

        # Step 1: Sort all the edges in
        # non-decreasing order of their
        # weight. If we are not allowed to change the
        # given graph, we can create a copy of graph
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Number of edges to be taken is equal to V-1
        while e < self.V - 1:

            # Step 2: Pick the smallest edge and increment
            # the index for next iteration
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            # If including this edge doesn't
            # cause cycle, then include it in result
            # and increment the index of result
            # for next edge
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            # Else discard the edge
        print(result)
        # minimumCost = 0
        # print("Edges in the constructed MST")
        # for u, v, weight in result:
        #     minimumCost += weight
        #     print("%d -- %d == %f" % (u, v, weight))
        # print("Minimum Spanning Tree", minimumCost)


# Driver's code
def create_optimized_route():
    g = Graph(len(Points))
    for id, p in enumerate(Adjacency):
        # print(p, id)
        for adj_id in p:
            # print(adj_id)
            if id < adj_id:
                g.addEdge(id, adj_id, distance(Points[id], Points[adj_id]))
    # Function call
    g.KruskalMST()

create_optimized_route()
# This code is contributed by Neelam Yadav
# Improved by James Graça-Jones
