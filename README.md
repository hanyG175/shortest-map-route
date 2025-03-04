# Map Route Finder

This project is a Python application that uses `OSMnx`, `NetworkX`, and `Folium` to fetch street network data for a specified city, compute the shortest driving route between two user-selected points using the A* algorithm, and visualize it both in a `Tkinter` GUI and an interactive `Folium` map.

## Features
- Fetches driving network data for any city using OpenStreetMap via `OSMnx`.
- Allows users to select source and target nodes by clicking on a matplotlib graph.
- Calculates the shortest path using the A* algorithm from `NetworkX`.
- Displays the city's street network and route in a `Tkinter` GUI with `matplotlib`.
- Provides an interactive `Folium` map viewable in a web browser.

## Prerequisites
To run this project, you’ll need:
- **Python 3.x** (tested with Python 3.9+)
- **Required Libraries**:
  - `folium` (install with `pip install folium`)
  - `osmnx` (install with `pip install osmnx`)
  - `tkinter` (usually included with Python; if not, install via `sudo apt-get install python3-tk` on Linux)
  - `networkx` (install with `pip install networkx`)
  - `matplotlib` (install with `pip install matplotlib`)
- **Windows-specific**: Uses `ctypes` for high DPI support, optimized for Windows but adaptable to other OSes.

## Installation
1. Clone or download this repository:
   `git clone <repository-url>`
   `cd <repository-folder>`
2. Install the required dependencies:
   `pip install folium osmnx networkx matplotlib`
3. Ensure `tkinter` is available. On Linux, you may need:
   `sudo apt-get install python3-tk`

## Usage
1. Run the script:
   `python map_route_finder.py`
   (Replace `map_route_finder.py` with your script’s filename.)
2. Steps:
   - Enter a city name (e.g., "New York, NY, USA") in the input dialog.
   - Wait for the street network to load, then click on the graph to select a source node (marked in red).
   - Click again to select a target node (marked in red).
   - View the shortest path overlaid on the graph in the `Tkinter` window.
   - Click "Show Map" to open an interactive `Folium` map in your browser.
   - Click "Exit" or press `Escape` to close the application.

## Project Structure
- **`map_route_finder.py`**: Main script containing the route-finding logic and GUI.
  - **Graph Fetching**: Uses `OSMnx` to retrieve street network data.
  - **Path Finding**: Implements A* algorithm via `NetworkX`.
  - **Visualization**: Displays graph in `Tkinter` with `matplotlib` and route in `Folium`.

## Customization
- **City Input**: Modify the `city_input` prompt or hardcode a city in `fetch_graph()`.
- **Graph Style**: Adjust colors, sizes, or linewidths in `plot_graph()` (e.g., `bgcolor`, `node_size`).
- **Algorithm**: Replace `astar_path` with other `NetworkX` algorithms (e.g., Dijkstra via `shortest_path`).

## Example Output
- **GUI**: A fullscreen `Tkinter` window showing the city’s street network (light green background, gray edges) with the shortest path in red.
- **Folium Map**: An HTML file (`map.html`) opens in your browser, displaying an interactive map centered on the city with the route highlighted.

## Limitations
- Requires an internet connection to fetch OpenStreetMap data via `OSMnx`.
- May fail if the city name is invalid or too vague (e.g., "Springfield" without state/country).
- User must click within 30 seconds to select nodes, or the script times out.
- Optimized for Windows DPI; may need adjustments for other OSes.

## Contributing
Submit issues or pull requests to enhance functionality, improve UI, or fix bugs!

## License
This project is open-source under the [MIT License](LICENSE).
