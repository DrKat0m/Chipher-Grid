from structure import Graph
from PIL import Image, ImageOps
import networkx as nx
import matplotlib.pyplot as plt
import pytesseract
import easyocr
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class Decoder:
    
    def decode(self, qr_code, qr_text):
        """
        Decoding the pixelated QR code back into a graph and retrieve the original data.
        """
        # Converting QR code back to a graph structure
        graph = self.qr_to_graph(qr_code, qr_text)
        hash_value=''.join(graph['hash'])
        adj_matrix=graph['adjacency_matrix']
        color=int(graph['bottom_right'])
        labels=graph['labels']
        
        
        # Step 3: Traverse the graph to reconstruct the original data
        data = self.graph_to_data(hash_value, adj_matrix, color, labels)
        return data
    
    def qr_to_graph(self, qr_code, qr_text):
        """
        Converting the QR code pixel grid back into a graph structure.
        """
        # Implementing conversion from QR code to graph
        '''
        try:
            # Open the image file
            image = Image.open(qr_code)

            # Perform OCR using Tesseract
            extracted_text = pytesseract.image_to_string(image)

            print(extracted_text)
        except Exception as e:
            print(f"An error occurred: {e}")'''
        '''
        reader = easyocr.Reader(['en'])  # 'en' for English
        result = reader.readtext(qr_code, detail=0)  # Extract text
        print("\n".join(result))'''
        lines = qr_text.strip().split("\n")
        
        # Extracting the top row
        top_row = lines[0]
        padding = 5  
        top_left = top_row.strip().split('[[', 1)[1].split(']]')[0]  # Extracting the `[[...]]` value from top-left
        top_right = top_row.strip().rsplit('[[', 1)[-1].split(']]')[0]  # Extracting the `[[...]]` value from top-right
        
        # Extracting labels (the part between top_left and top_right)
        formatted_nodes = top_row.strip().split(f'[[{top_left}]]')[1].split(f'[[{top_right}]]')[0].strip()
        labels = formatted_nodes.split()
        
        # Extracting the bottom row
        bottom_row = lines[-1]
        bottom_left = bottom_row.strip().split('[[', 1)[1].split(']]')[0]
        bottom_right = bottom_row.strip().rsplit('[[', 1)[-1].split(']]')[0]
        
        # Parsing the matrix and hash section
        matrix_lines = lines[1:-1]  # Excluding top and bottom rows
        hash_list = []
        adjacency_matrix = []
        count=0
        for line in matrix_lines:
            count+=1
            parts = line.strip().split()
            if count<=len(labels):
                hash_value = parts[0]
                matrix_row = parts[1:]
                hash_list.append(hash_value)
                adjacency_matrix.append(list(map(int, matrix_row)))
            else:
                # Remaining hash values (not part of the matrix)
                hash_list.extend(parts)
        
        # Combining all hash values
        hash_list = [h for h in hash_list if h != 'x']  # Removing padding 'x' if any
        
        # Converting adjacency matrix to numpy array
        adjacency_matrix = np.array(adjacency_matrix)
        
        # Extracting colors from adjacency matrix
        colors = [f"color_{top_left}",f"color_{top_right}", f"color_{bottom_left}"]  # Reversing map to color indices
    
        # Returning the reconstructed components
        return {
            "hash": hash_list,
            "adjacency_matrix": adjacency_matrix.tolist(),
            "colors": colors,
            "top_left": top_left,
            "top_right": top_right,
            "bottom_left": bottom_left,
            "bottom_right": bottom_right,
            "labels": labels,
        }

    
    def graph_to_data(self, hash_value, adj_matrix, color, labels):
        """
        Traversing the graph to retrieve the original encoded data.
        """
        n = len(adj_matrix)  # Number of nodes in the graph

        #Updating node labels to ensure uniqueness
        label_count = {}
        unique_labels = []
        for label in labels:
            if label not in label_count:
                label_count[label] = 0
                unique_labels.append(label)
            else:
                label_count[label] += 1
                unique_labels.append(f"{label}_{label_count[label]}")

        # Sorting nodes by labels
        sorted_indices = sorted(range(n), key=lambda x: (unique_labels[x], x))
        sorted_matrix = [[adj_matrix[i][j] for j in sorted_indices] for i in sorted_indices]
        sorted_labels = [unique_labels[i] for i in sorted_indices]
        
        # Filtering edges by color (optional, depending on decoding condition)
        filtered_matrix = [[0 if sorted_matrix[i][j] != color + 1 else sorted_matrix[i][j]
                            for j in range(n)] for i in range(n)]
        #print(filtered_matrix)

        # Removing redundant edges
        for i in range(n):
            outgoing_edges = [j for j in range(n) if filtered_matrix[i][j] != 0]
            for v in outgoing_edges:
                for u in outgoing_edges:
                    if v != u and self.has_alternate_path(filtered_matrix, i, v, u):
                        # Remove the edge to u if there's an alternate path from i to u
                        filtered_matrix[i][u] = 0
        #print(filtered_matrix)

        '''
        # Additional check for reachability to `z` from `v` or `u`
        for i in range(n):
            outgoing_edges = [j for j in range(n) if filtered_matrix[i][j] != 0]
            if len(outgoing_edges) == 2:  # Rows with two non-zero entries
                v, u = outgoing_edges
                if self.can_reach(filtered_matrix, v, i):
                    # If `z` is reachable from `v`, remove edge from `z` to `v`
                    filtered_matrix[i][v] = 0
                if self.can_reach(filtered_matrix, u, i):
                    # If `z` is reachable from `u`, remove edge from `z` to `u`
                    filtered_matrix[i][u] = 0
        print(filtered_matrix)
        #print(sorted_labels) 
        '''

        return ''.join(self.reconstruct_linear_graph(filtered_matrix, sorted_labels))

    def reconstruct_linear_graph(self, matrix, labels):
        n = len(matrix)
        
        # Truncating labels longer than 2 characters to their first character
        truncated_labels = [label[0] if len(label) > 2 else label for label in labels]
        
        # Calculating indegree and outdegree for each node
        indegree = [0] * n
        outdegree = [0] * n
        
        for i in range(n):
            for j in range(n):
                if matrix[i][j] != 0:
                    indegree[j] += 1
                    outdegree[i] += 1
        
        # Identifying the starting and ending nodes
        starting_node = None
        ending_node = None
        
        for i in range(n):
            if indegree[i] == 0 and outdegree[i] == 1:
                starting_node = i
            elif indegree[i] == 1 and outdegree[i] == 0:
                ending_node = i
        
        if starting_node is None or ending_node is None:
            raise ValueError("The graph does not have a valid starting or ending node.")
        
        # Reconstructing the linear path using labels
        path = []
        current = starting_node
        while current != ending_node:
            path.append(truncated_labels[current])
            # Finding the next node in the path
            next_node = None
            for j in range(n):
                if matrix[current][j] != 0:
                    next_node = j
                    break
            if next_node is None:
                raise ValueError("The graph is not a valid linear directed graph.")
            current = next_node
        
        # Adding the ending node to the path
        path.append(truncated_labels[ending_node])
        return path


    def can_reach(self, matrix, source, target):
        """
        Checking if there's a path from `source` to `target` in the graph.
        """
        n = len(matrix)
        visited = [False] * n

        def dfs(node):
            if node == target:
                return True
            visited[node] = True
            for neighbor in range(n):
                if not visited[neighbor] and matrix[node][neighbor] != 0:
                    if dfs(neighbor):
                        return True
            return False

        return dfs(source)

    def has_alternate_path(self, matrix, source, exclude_node, target):
        """
        Checking if there's a path from `source` to `target` in the graph
        while ignoring the direct edge from `source` to `exclude_node`.
        """
        n = len(matrix)
        visited = [False] * n

        def dfs(node):
            if node == target:
                return True
            visited[node] = True
            for neighbor in range(n):
                # Skipping the direct edge from `source` to `target`
                if not visited[neighbor] and matrix[node][neighbor] != 0:
                    if dfs(neighbor):
                        return True
            return False

        visited[source] = True
        for neighbor in range(n):
            # Ignoring the direct edge from `source` to `target`
            if matrix[source][neighbor] != 0 and neighbor != target:
                if dfs(neighbor):
                    return True
        return False