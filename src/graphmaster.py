#!/usr/bin/env python3
# AUTHOR: Bachri Laroussi
# DATE: 2025-11-26
# M1 BBS - S7 Graphs
"""Graphmaster module: a simple graph class and related functions."""
import math
from collections import deque
from pprint import pprint

class Graph:
    """Graph class representing a directed or undirected graph with optional weighted edges."""
    def __init__(self, directed=True, weighted=False, weight_attribute=None):
        self.nodes = {} # node_id (str) -> objet Node
        self.edges = {} # node_id (str) -> { target_id (str) -> objet Edge }
        self.directed = directed
        self.weighted = weighted
        self.weight_attribute = weight_attribute

    def copy(self):
        """Create a deep copy of the graph."""
        g_copy = Graph(self.directed, self.weighted, self.weight_attribute)
        for n, node in self.nodes.items():
            g_copy.add_node(n, node.attributes.copy())
        for u, neigh in self.edges.items():
            for v, e in neigh.items():
                g_copy.add_edge(u, v, e.attributes.copy())
        return g_copy

    @classmethod
    def from_delim(cls, filename, column_separator='\t',
                   directed=True, weighted=False, weight_attribute=None):
        """
        Lit un fichier délimité et retourne une instance de la classe Graph.
        Remplace la fonction read_delim.
        """
        g = cls(directed, weighted, weight_attribute)

        with open(filename, 'r', encoding='utf-8') as f:
            header = f.readline().rstrip()
            if not header:
                return g

            attnames = header.split(column_separator)

            if len(attnames) >= 2:
                attnames.pop(0)
                attnames.pop(0)
            else:
                attnames = []

            # Lecture des lignes de données
            for line in f:
                line = line.rstrip()
                if not line:
                    continue

                vals = line.split(column_separator)
                if len(vals) < 2:
                    continue

                u = vals.pop(0) # Source
                v = vals.pop(0) # Cible

                # Construction du dictionnaire d'attributs pour l'arête
                att = {}
                for i, name in enumerate(attnames):
                    if i < len(vals):
                        att[name] = vals[i]

                # Utilisation de la méthode interne de l'instance g
                g.add_edge(u, v, att)

        return g

    def add_node(self, node_id, attributes=None):
        """Add a node to the graph if it doesn't exist, and return the Node object."""
        if node_id not in self.nodes:
            new_node = Node(node_id, attributes)
            self.nodes[node_id] = new_node
            self.edges[node_id] = {}
        return self.nodes[node_id]

    def add_edge(self, u_id, v_id, attributes=None):
        """Add an edge from u_id to v_id with optional attributes.
          Creates nodes if they don't exist."""

        u_node = self.add_node(u_id)
        v_node = self.add_node(v_id)

        if v_id not in self.edges[u_id]:
            new_edge = Edge(u_node, v_node, attributes)
            self.edges[u_id][v_id] = new_edge

            if not self.directed:

                self.edges[v_id][u_id] = Edge(v_node, u_node, attributes)

        return self.edges[u_id][v_id]

    def neighbors(self, node_id):
        """Return a sorted list of neighbors of a node."""
        return self.edges.get(node_id, {}).keys()

    def node_exists(self, n):
        """Check if a node exists in the graph."""
        return n in self.nodes

    def nb_nodes(self):
        """Return the number of nodes in the graph."""
        return len(self.nodes)

    def get_edges(self):
        """Remplace edges(g)"""
        all_edges = []
        for neighbors_dict in self.edges.values():
            all_edges.extend(neighbors_dict.values())
        return all_edges

    def nb_edges(self):
        """Return the number of edges in the graph"""
        total = sum(len(adj) for adj in self.edges.values())
        return total // (1 if self.directed else 2)

    def edge_exists(self, u, v):
        """Check if an edge from u to v exists."""
        return self.node_exists(u) and v in self.edges[u]

    def in_degree(self, node_id):
        """Return the in-degree of a node (number of incoming edges)."""
        cpt = 0
        for _, adj in self.edges.items():
            if node_id in adj:
                cpt += 1
        return cpt

    def out_degree(self,node_id):
        """Return the out-degree of a node (number of outgoing edges)."""
        return len(self.neighbors(node_id))

    def degree(self,node_id):
        """Return the total degree of a node (in-degree + out-degree)."""
        return (self.in_degree(node_id) + self.out_degree(node_id))

    def select_nodes(self,attribut,attribut_value):
        """Return a list of node identifiers having a given attribute value.

        Parameters
        ----------
        g : dict
            Graph object.
        attribut : str
            Attribute name to test on nodes.
        attribut_value : any
            Value the attribute must have.

        Returns
        -------
        list of hashable
            Node identifiers matching the condition.
            Important point for the other functions that use Select nodes.
        """
        res = []
        for node_obj in self.nodes.values():
            if node_obj.get(attribut) == attribut_value:
                res.append(node_obj.id)
        return res

    def filter_edges(self,attribut , attribut_value):
        """Return a list of edges (u, v) whose attribute matches a given value.

        Parameters
        ----------
        g : dict
            Graph object.
        attribut : str
            Edge attribute name.
        attribut_value : any
            Value the attribute must have.

        Returns
        -------
        set of tuple
            Set of (u, v) edge pairs matching the condition.
        """
        return [e for e in self.get_edges() if e.get(attribut) == attribut_value]

    def relationships(self):
        """Print the number of edges for each relationship type in the graph."""
        liste = ['is a' , 'part of' , 'annotation']
        res = {}
        for el in liste:
            res[el] = len(self.filter_edges('relationship',el))
        return res

    def bfs(self, s):
        """Perform a breadth-first search (BFS) from source node s.

        Parameters
        ----------
        g : dict
            Graph object.
        s : hashable
            Source node identifier.

        Returns
        -------
        tuple
            (state, distance, predecessor) dictionaries:
            - state[u] in {'Unexplored', 'Discovered', 'Finished'}
            - distance[u] is the BFS distance from s (or -inf if unreachable)
            - predecessor[u] is the parent of u in the BFS tree (or None).
        """
        state = {node: 'Unexplored' for node in self.nodes}
        distance = {node: -math.inf for node in self.nodes}
        predecessor = {node: None for node in self.nodes}

        state[s] = 'Discovered'
        distance[s] = 0

        queue = deque([s])

        while queue:
            u = queue.popleft()
            for v in self.neighbors(u):
                if state[v] == 'Unexplored':
                    state[v] = 'Discovered'
                    distance[v] = distance[u] + 1
                    predecessor[v] = u
                    queue.append(v)
            state[u] = 'Finished'

        return state, distance, predecessor

    def path(self,bfs_res, source, target):
        """Reconstruct the shortest path from source to target using BFS results.

        Parameters
        ----------
        bfs_res : tuple
            Result of bfs(g, source): (state, distance, predecessor).
        source : hashable
            Source node identifier.
        target : hashable
            Target node identifier.

        Returns
        -------
        str or None
            A string describing the path and its distance, or None if no path exists.
        """
        _, distance, predecessor = bfs_res

        if source == target:
            return [source]
        route = []
        cur = target
        while cur is not None and cur != source:
            route.append(cur)
            cur = predecessor[cur]

        if cur is None:
            return None

        route.append(source)
        route.reverse()
        return f"{route} \n La distance entre {source} et {target} est de {distance[target]}."

    def dfs_visit(self,u,parcours):
        """Recursive DFS visit from node u, updating the traversal structure.

        Parameters
        ----------
        g : dict
            Graph object.
        u : hashable
            Starting node for this DFS visit.
        parcours : dict
            DFS traversal structure containing state, times and edge classifications.
        """
        parcours['state'][u] = 'Discovered'
        parcours['time'] += 1
        parcours['discovered'][u]= parcours['time']

        for v in self.neighbors(u):
            if parcours['state'][v] == 'Unexplored':
                parcours['predecessor'][v] = u
                parcours['classification'][(u,v)] = 'TREE EDGE'
                self.dfs_visit(v,parcours)
            elif parcours['state'][v] == 'Discovered':
                parcours['classification'][(u,v)] = 'BACK EDGE'
            elif parcours['discovered'][u] > parcours['discovered'][v]:
                parcours['classification'][(u,v) ] = "CROSS EDGE"
            else:
                parcours['classification'][(u,v)] = "FORWARD EDGE"
        parcours['state'][u] = 'Finished'
        parcours['time'] += 1
        parcours['finished'][u] = parcours['time']

    def dfs(self):
        """Perform a depth-first search (DFS) on the whole graph.

        Returns
        -------
        dict
            Traversal information with keys:
            'time', 'state', 'discovered', 'finished',
            'classification', 'predecessor'.
        """
        parcours = {'time' : 0,
            'state' : {},
            'discovered' : {},
            'finished' : {},
            'classification' : {},
            'predecessor' : {},
        }

        for u in self.nodes:
            parcours['state'][u] = 'Unexplored'
            parcours['predecessor'][u] = None


        for v in self.nodes:
            if parcours['state'][v] == 'Unexplored':
                self.dfs_visit(v,parcours)
        return parcours

    def is_acyclic(self):
        """Check whether the graph is acyclic using DFS edge classification.

        Returns
        -------
        str
            A textual message indicating if the graph is a DAG or contains a cycle.
        """

        parcours = self.dfs()
        for el in parcours['classification'].values():
            if el == 'BACK EDGE':
                return False
        return True

    def topological_sort(self):
        """Compute a topological ordering of the nodes of a DAG.

        The graph must be acyclic; otherwise a ValueError is raised.

        Returns
        -------
        list of hashable
            List of node identifiers ordered topologically.
        """
        # Check graph is acyclic.
        if not self.is_acyclic():
            raise ValueError("impossible to sort: DAG.")
        if self.nb_nodes() == 0:
            return False

        parcours = self.dfs()

        fins = parcours['finished']


        sorted_nodes = list(fins.keys())
        sorted_nodes.sort(key=lambda n: fins[n], reverse=True)


        return sorted_nodes

    def transpose(self):
        """Return the transpose of the graph (reverse all edges)."""
        if not self.directed:
            return self.copy()

        gt = Graph(directed=True, weighted=self.weighted, weight_attribute=self.weight_attribute)

        # copy nodes
        for n, node in self.nodes.items():
            gt.add_node(n, node.attributes.copy())

        # reverse edges
        for u, neigh in self.edges.items():
            for v, e in neigh.items():
                gt.add_edge(v, u, e.attributes.copy())

        return gt

    def induced_subgraph(self, induced_nodes):
        """Return the subgraph induced by a given set of nodes."""
        sg = Graph(self.directed, self.weighted, weight_attribute=self.weight_attribute)

        node_set = set(induced_nodes)

        for n in node_set:
            if n in self.nodes:
                sg.add_node(n, self.nodes[n].attributes.copy())

        for u in node_set:
            for v in self.neighbors(u):
                if v in node_set:
                    sg.add_edge(u, v, self.edges[u][v].attributes.copy())

        return sg

class Node:
    """Node class representing a graph node with optional attributes."""
    def __init__(self, node_id, attributes=None):
        self.id = node_id
        self.attributes = attributes if attributes is not None else {}

    def get(self, key, default=None):
        """get node attributes"""
        return self.attributes.get(key, default)

    def __str__(self):
        return f"Node({self.id})"

class Edge:
    """Edge class representing a connection between two nodes with optional attributes."""
    def __init__(self, source, target, attributes=None):
        self.source = source # Objet Node
        self.target = target # Objet Node
        self.attributes = attributes if attributes is not None else {}

    def get(self, key, default=None):
        """get edge attributes"""
        return self.attributes.get(key, default)

    def __str__(self):
        return f"Edge({self.source.id} -> {self.target.id})"

if __name__ == "__main__":
    print("# Graphmaster module")

    pprint(Graph.bfs(Graph.from_delim('data/dressing.tsv'), 'chaussettes'))