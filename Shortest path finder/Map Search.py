import folium
import webbrowser
import osmnx as ox
import tkinter as tk
import networkx as nx
from ctypes import windll
import matplotlib.pyplot as plt
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


if windll.shcore:
    windll.shcore.SetProcessDpiAwareness(1)

# Function to fetch graph data using OSMnx
def fetch_graph(city_name):
    # Fetching the map of the city
    G = ox.graph_from_place(city_name, network_type='drive')
    return G

# Function to plot the graph using OSMnx
def plot_graph(G, path=None):
    # Plotting the graph
    fig, ax = ox.plot_graph(G, show=False, figsize=(40, 40), bgcolor="lightgreen",close=False, 
                            node_color='white',edge_color='gray',node_size=15, edge_linewidth=3)
    if path:
        # If a path is provided, plot it on the graph
        fig, ax = ox.plot_graph_route(G, path, route_color='r', edge_linewidth=3, bgcolor="lightgreen",
                                      route_linewidth=6, edge_color='gray', node_size=2, show=False)
    return (fig, ax)

# Function to find the shortest path using A* algorithm
def shortest_path_astar(G, source, destination):
    # Finding the shortest path using A* algorithm
    path = nx.astar_path(G, source, destination, weight='length')
    return path

def open_folium_map():
    # Create a folium map
    m = folium.Map(location=[0, 0], zoom_start=12)
    # Plot the route on the map
    ox.plot_route_folium(G, path, route_map=m)
    # Save the map as HTML file
    m.save("map.html")
    # Open the HTML file in the web browser
    webbrowser.open("map.html")



if __name__ =='__main__':
    
    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Map Route Finder")
    root.attributes('-fullscreen', True)
    def exit_full_screen(event):
        root.attributes('-fullscreen', False)
    root.bind('<Escape>', exit_full_screen)
    root.lift()  # Bring the window to the front
    
    try :
        
        # Get city from the user
        city_input = simpledialog.askstring("Input", "Enter the city name:", parent=root)
        
        if city_input:
            # Display a notification message if the city is entered
            messagebox.showinfo("Notification", f"You entered: {city_input}\nOnce the graph is fetched, choose your source and target nodes.")
        
        # Fetch the graph data
        G = fetch_graph(city_input)

        # Tkinter plot
        fig = plot_graph(G)[0]
        ax = plot_graph(G)[1]
    
        # Get source node from user and mark it with red...
        xy = plt.ginput(n=1, timeout=30)[0]
        source_node = ox.nearest_nodes(G, *xy)
        ax.scatter(*xy ,s=50, c='red', zorder=5)
        plt.draw()
        
        # Get target node from user and mark it with red...
        xy = plt.ginput(n=1, timeout=30)[0]
        target_node = ox.nearest_nodes(G, *xy)
        ax.scatter(*xy ,s=50, c='red', zorder=5)
        plt.draw()
        
        messagebox.showinfo("Nodes Chosen", f"Source Node: {source_node}\nTarget Node: {target_node}")
        
        plt.close()
        
        # Find the shortest path between source and target nodes
        path = shortest_path_astar(G,source_node,target_node)
        
        # Plot the graph with the shortest path
        fig = plot_graph(G, path)[0]
        
        # Display the graph in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH)

        # Add button to show the folium map
        button_map = tk.Button(root, text="Show Map", command=open_folium_map)
        button_map.pack()
        
        # Add button to exit the program
        exit_button = tk.Button(root, text="Exit", command=exit)
        exit_button.pack()
        
        tk.mainloop()
        
    except ValueError:
        messagebox.showinfo("Alert!","You haven't entered any city or city unfound, click okay to leave.")
        exit(0)
      
