import networkx as nx
import matplotlib.pyplot as plt

def check_planarity(graph):
    
    """
    Checking if the graph is planar and modify it to maintain planarity if needed.
    """
    
    nx_graph = nx.DiGraph()
    unique_node_ids = {}
    
    # Adding nodes and edges to the NetworkX graph
    for node in graph.nodes:
        current_node_id = f"{node.value}_{id(node)}"
        unique_node_ids[current_node_id] = node.value  # Keeping track of the original value
        nx_graph.add_node(current_node_id)
        for neighbor in node.edges:
            neighbor_node_id = f"{neighbor.value}_{id(neighbor)}"
            unique_node_ids[neighbor_node_id] = neighbor.value
            nx_graph.add_node(neighbor_node_id)
            nx_graph.add_edge(current_node_id, neighbor_node_id)
    
    # Checking if the underlying undirected graph is planar
    undirected_graph = nx.Graph(nx_graph)  # Convert to undirected for planarity check
    is_planar = nx.check_planarity(undirected_graph)
    print(is_planar)
    labels = {node: unique_node_ids[node] for node in nx_graph.nodes}
    '''
    if is_planar[0]:
        # If planar, use a planar layout
        planar_pos = nx.planar_layout(undirected_graph)
        plt.figure(figsize=(15, 10))
        nx.draw(nx_graph, pos=planar_pos, labels=labels, with_labels=True, arrows=True,
                node_color='skyblue', edge_color='black')
        plt.title("Planar Layout of Directed Graph")
        plt.show()
    else:
        print("The graph is not planar.")
        spacious_pos = nx.spring_layout(nx_graph, k=0.5)
        plt.figure(figsize=(15, 10))
        nx.draw(nx_graph, pos=spacious_pos, labels=labels, with_labels=True, arrows=True, node_color='skyblue', edge_color='black')
        plt.title("Non-Planar Directed Graph")
        plt.show()
    '''
    return [is_planar, nx_graph, labels] 