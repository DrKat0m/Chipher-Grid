# encoder.py
import networkx as nx
import os
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from structure import Graph
from security import apply_hashing, apply_random_connections

class Encoder:
    
    def encode(self, data):
        """
        Converting input data into a graph structure, applying security, 
        and converting the graph into a QR code format.
        """

        graph = self.data_to_graph(data)
        hash_val = apply_hashing(data)
        secure_graph = apply_random_connections(graph, hash_val)
        a="\n".join(nx.generate_edgelist(secure_graph[0]))
        print(a)
        print(hash_val)
        print(len(hash_val))
        self.visualize(secure_graph[0],secure_graph[1])
        qr_code, qr_text = self.graph_to_qr(secure_graph, hash_val)
        return [qr_code, qr_text]

    def visualize(self, G, labels):
        edge_color_list = [G[u][v].get('color', 'black') for u, v in G.edges()]
        # Plotting the graph
        pos = nx.planar_layout(G)  # Generate a layout for the graph
        nx.draw(G, pos, labels=labels, with_labels=True, edge_color=edge_color_list, node_color='lightblue', node_size=700)
        plt.show()

    def data_to_graph(self, data):
        """
        Converting data into a graph structure with nodes and edges.
        """
        return Graph(data)
    
    def graph_to_qr(self, graph, hash):
        """
        Converting a planar graph into an ASCII representation.
        """
        matrix = nx.adjacency_matrix(graph[0]).todense()
        padding=5
        hash=list(hash)
        colors=graph[5]
        labels=list(graph[1].values())
        print(labels)
        n = len(matrix)  # Assuming square matrix (n x n)
        last_rows=len(hash)-n
        hash+=(n+1-(last_rows%(n+1)))*['x']

        nodes = list(graph[0].nodes())
        for u, v in graph[0].edges():
            color_index = colors.index(graph[0][u][v]['color'])  # Geting the color index
            u_idx = nodes.index(u)  # Finding row index for `u`
            v_idx = nodes.index(v)  # Finding column index for `v`
            matrix[u_idx, v_idx] = color_index+1 #so that it doesn't become 0 as other entries

        # Creating the top-left and top-right corner nested lists
        top_left = f"[[{graph[2]}]]".ljust(padding)
        top_right = f"[[{graph[3]}]]".rjust(padding + n -len(labels))
        
        # Creating the bottom-left and bottom-right corner nested lists
        bottom_left = f"[[{graph[4]}]]".ljust(padding)
        bottom_right = f"[[{graph[2]}]]".rjust(padding + n+2)
        formatted_nodes="  "
        for value in labels:
            formatted_nodes += value+ " "
        # Formating the top row with padding
        top_row = top_left + formatted_nodes + top_right
        
        # Formating the matrix with padding
        formatted_matrix = ""
        for row in matrix:
            formatted_matrix += " " * (padding) + str(hash.pop(0)) +' '+ " ".join(map(str, row)) + "\n"
        for i in range(0, len(hash), n+1):
            formatted_matrix+=" " * (padding)+' '.join(hash[i:i+n+1])+ '\n'
        bottom_row = bottom_left + " " * n + bottom_right
        result = top_row + "\n" + formatted_matrix + bottom_row
        print(result)
        return [self.text_to_image(result), result]

    def text_to_image(self, result, font_path="Font\Montserrat-Regular.ttf", font_size=30, line_spacing=5, output_file="gradient_terminal_text.png"):
        neon_colors = ['#FF5733', '#33FF57', '#5733FF', '#FF33A1', '#33FFF5', '#FFF533', '#F533FF', '#33A1FF']
        font = ImageFont.load_default()

        # Calculating image dimensions
        lines = result.split("\n")
        max_line_length = max(len(line) for line in lines)
        char_width = font.getbbox("M")[2]  # Width of a single character
        char_height = font.getbbox("M")[3]
        
        image_height = len(lines) * (char_height + line_spacing) + line_spacing
        image_width = image_height+6*char_width

        # Creating a blank image with a black background
        img = Image.new("RGB", (image_width, image_height), "black")
        draw = ImageDraw.Draw(img)

        # Drawing each character with a random neon color
        y_offset = line_spacing
        for line in lines:
            x_offset = 10  
            for char in line:
                color = random.choice(neon_colors)  # Picking a random neon color
                draw.text((x_offset, y_offset), char, fill=color, font=font)
                x_offset += char_width  # Moving to the next character
            y_offset += char_height + line_spacing  # Moving to the next line
        output_folder='Test'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Creating the folder if it doesn't exist
    
        output_path = os.path.join(output_folder, output_file)
        
        # Saving the image
        img.save(output_path)
        print(f"Gradient neon text image saved as '{output_file}'")
        img.show()
        return output_path


#Encoder().encode("http//kls/1234567890/abcdefghijklmn")
#Encoder().encode("http")