import random
import numpy as np


def find_two_smallest(numbers):
    if len(numbers) < 2:
        return None
    if numbers[0] < numbers[1]:
        min1, min2 = numbers[0], numbers[1]
    else:
        min1, min2 = numbers[1], numbers[0]

    for num in numbers[2:]:
        if num < min1:
            min2 = min1
            min1 = num
        elif num < min2:
            min2 = num

    return min1, min2


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = []

    def add_edge(self, origin, destiny, value=0):
        if origin in self.nodes and destiny in self.nodes:
            self.nodes[origin].append([destiny, value])
            self.nodes[destiny].append([origin, value])

    def change_edge_value(self, origin, destiny, value):
        if origin in self.nodes and destiny in self.nodes:
            for node in self.nodes[origin]:
                if node[0] == destiny:
                    node[1] = value
            for node in self.nodes[destiny]:
                if node[0] == origin:
                    node[1] = value

class LLRCoder:
    def __init__(self, n, dv, dc):

        if n * dv % dc == 0:
            self.m = (int) (n * dv / dc)
        else:
            print("m must be an integer")
            return

        self.n = n
        self.dv = dv
        self.dc = dc

        self.graph = self.generate_graph()

    def generate_graph(self):
        graph = Graph()

        done = False
        while not done:
            done = True

            for i in range(self.n + self.m):
                graph.add_node(i)

            c_nodes = [self.n + i for i in range(self.m)]
            c_nodes_count = {node: 0 for node in c_nodes}

            for v_node in range(self.n):
                if not c_nodes:
                    break
                c_nodes_aux = c_nodes.copy()

                for _ in range(self.dv):
                    if len(c_nodes_aux) == 0:
                        done = False
                        break
                    index = random.randint(0, len(c_nodes_aux) - 1)
                    current_c_node = c_nodes_aux[index]
                    graph.add_edge(v_node, current_c_node)
                    c_nodes_aux.pop(index)

                    c_nodes_count[current_c_node] += 1
                    if c_nodes_count[current_c_node] == self.dc:
                        c_nodes.remove(current_c_node)
                        c_nodes_count.pop(current_c_node)

        return graph

    def decode(self, received_llrs, max_iter=10):
        for v_node in range(self.n):
            for edge in self.graph.nodes[v_node]:
                self.graph.change_edge_value(v_node, edge[0], 0)

        decoded_llrs = received_llrs.copy()

        for _ in range(max_iter):
            for v_node in range(self.n):
                consent_message = received_llrs[v_node] + sum([edge[1] for edge in self.graph.nodes[v_node]])
                for edge in self.graph.nodes[v_node]:
                    self.graph.change_edge_value(v_node, edge[0], consent_message - edge[1])

            stop_condition = False

            for c_node in range(self.n, self.n + self.m):
                sign = 1
                for edge in self.graph.nodes[c_node]:
                    sign *= np.sign(edge[1])

                if sign == -1:
                    stop_condition = True
                    break

            if not stop_condition:
                break

            for c_node in range(self.n, self.n + self.m):
                sign = 1
                for edge in self.graph.nodes[c_node]:
                    sign *= np.sign(edge[1])

                (min1, min2) = find_two_smallest([abs(edge[1]) for edge in self.graph.nodes[c_node]])

                for edge in self.graph.nodes[c_node]:
                    actual_sign = sign * np.sign(edge[1])

                    if edge[1] == min1:
                        self.graph.change_edge_value(c_node, edge[0], actual_sign * min2)
                    else:
                        self.graph.change_edge_value(c_node, edge[0], actual_sign * min1)
                        
        for v_node in range(self.n):
            decoded_llrs[v_node] += sum([edge[1] for edge in self.graph.nodes[v_node]])

        decoded = np.empty((1, self.n), dtype=int)
        for i in range(self.n):
            decoded[i] = 0 if decoded_llrs[i] >= 0 else 1

        return decoded






