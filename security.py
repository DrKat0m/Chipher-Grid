import hashlib
import random
import networkx as nx
from structure import Graph
from utils import check_planarity

def apply_hashing(graph):
    """
    Applying hashing to secure the graph structure.
    """
    hash_value = hashlib.sha256(graph.encode()).hexdigest()
    return hash_value

def apply_random_connections(graph, hash_value):
    """
    Randomly connecting nodes in the graph to add security.
    """
    num_nodes = len(graph.nodes)
    if num_nodes < 10 and num_nodes > 100:
        raise ValueError("Less than 10 characters or more than 100 characters")  
    hash_segments = [int(hash_value[i:i+8], 16) for i in range(0, len(hash_value), 8)]
    
    def is_non_crossing(node1, node2):
        for node in graph.nodes:
            for neighbor in node.edges:
                if (node == node1 and neighbor == node2) or (node == node2 and neighbor == node1):
                    return False
        return True
    
    for i, segment in enumerate(hash_segments):
        source_node_index = i % num_nodes 
        target_node_index = (segment % (num_nodes - 8)) + 8    


        #target_node_index = (segment % (num_nodes - 1)) + 1 

        if (-(source_node_index - target_node_index)) == 1 or source_node_index == target_node_index:
            continue
        source_node = graph.nodes[source_node_index]
        target_node = graph.nodes[target_node_index]
        print(source_node.value, target_node.value, source_node_index, target_node_index)
        if is_non_crossing(source_node, target_node) and target_node not in source_node.edges:
            graph.add_edge(source_node, target_node)
            
            if not check_planarity(graph)[0][0]:
                #print(source_node.value, target_node.value)
                graph.remove_edge(source_node, target_node)
            
            
    graph.hash_value = hash_value
    new_graph= check_planarity(graph)[1]
    labels=check_planarity(graph)[2]
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'brown']
    color1=random.choice(colors)
    for u, v in new_graph.edges():
        new_graph[u][v]['color'] = color1
    print(nx.adjacency_matrix(new_graph).todense())
    new_edge_colors = random.sample([c for c in colors if c != color1], 2)
    nodes = list(new_graph.nodes())
    new_edges = []
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                a, b = nodes[i], nodes[j]
                if not new_graph.has_edge(a, b) and not new_graph.has_edge(b, a):
                    # Check if adding this edge maintains planarity
                    temp_G = new_graph.copy()
                    temp_G.add_edge(a, b)
                    if nx.check_planarity(temp_G.to_undirected())[0]:
                        new_graph.add_edge(a, b, color=random.choice(new_edge_colors))
                        new_edges.append((a[0], b[0]))
    print(new_edges)
    print(len(new_edges))
    result = ""
    for node in graph.nodes:
        neighbors = [neighbor.value for neighbor in node.edges] if node.edges else []
        result += f"Node {node.value}: {neighbors}\n"
    print(result)
    return [new_graph, labels, colors.index(color1), colors.index(new_edge_colors[0]), colors.index(new_edge_colors[1]), colors]

#print(apply_hashing('https://open.spotify.com/'))
#print(apply_hashing('https://open.spotify.com/.'))
#print(apply_hashing('www.linkedin.com/in/drkat0m'))
#print(apply_hashing('www.linkedin.com/in/drkatm'))
