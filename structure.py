class Node:
    def __init__(self, value, index):
        self.value = value
        self.index= index
        self.edges = []

class Graph:
    def __init__(self, data):
        self.nodes = self.create_nodes(data)
        self.hash_value=None
    
    def create_nodes(self, data):
        """
        Creating nodes from the data. Each data unit becomes a node.
        """
        nodes=[]
        lyst=list(data)
        for i, j in enumerate(lyst):
            if j==' ':
                raise ValueError("Hyperlink Corrupted - Space Found")
            nodes.append(Node(j, i))
        for i, j in enumerate(nodes):
            if i!=len(nodes)-1:
                self.add_edge(j,nodes[i+1])
        
        return nodes
        

    def add_edge(self, node1, node2):
        """
        Adding an edge between two nodes.
        """
        node1.edges.append(node2)

    def remove_edge(self, node1, node2):
        if node2 in node1.edges:
            node1.edges.remove(node2)
    
    def __str__(self):
        result = ""
        for node in self.nodes:
            neighbors = [neighbor.value for neighbor in node.edges] if node.edges else []
            result += f"Node {node.value} (Index {node.index}): {neighbors}\n"
        return result

#print(Graph("https://www.cricbuzz.com/"))