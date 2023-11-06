import re
import networkx as nx
import json

G = nx.Graph()
file = open('inetmap.json')
net = json.load(file)
file.close()

def find_device_by_name(name):
    """Finds device by name in the net dictionary.
    -------
    Parameters:
    name: string (name of the device)
    -------
    Returns:
    device: dictionary/json object
    """
    for device in net['devices']:
        if device['name'] == name:
            return device
        

def bootstrap():
    """Reads the inetmap.json file and creates a networkx graph.
    -------
    Returns:
    net: dictionary/array json object
    G: networkx graph
    """

    for device in net['devices']:
        G.add_node(device['name'])


    for link in net['links']:
        node1 = next((x['name'] for x in net['devices'] if x['name'] == link['node1']), None)
        node2 = next((x['name'] for x in net['devices'] if x['name'] == link['node2']), None)

        delay = link['delay']
        bw = link['bw']
        G.add_edge(node1, node2, delay = delay, bw = bw)

    return net,G


def calculate_paths(source_node, destination_node):
    """Calculates all paths between source and destination node.
    -------
    Parameters:
    source_node: string (name of the source node)
    destination_node: string (name of the destination node)
    -------
    Returns:
    sorted_paths: list of tuples (path, path_length, path_bw)
    """
    all_paths = nx.all_simple_paths(G, source=source_node, target=destination_node)

    min_bw_path = None
    min_bw = float('inf')  # Inicjalizacja wartości najmniejszego BW jako nieskończoność

    sorted_paths = []
    for path in all_paths:
        path_length = sum(G[path[i]][path[i + 1]]['delay'] for i in range(len(path) - 1))
        
        # Znajdź najmniejszą przepustowość na ścieżce
        path_bw = min(G[path[i]][path[i + 1]]['bw'] for i in range(len(path) - 1))
        
        if path_bw < min_bw:
            min_bw = path_bw
            min_bw_path = path
        
        sorted_paths.append((path, path_length, path_bw))
    sorted_paths = sorted(sorted_paths, key=lambda rekord: rekord[1])
    return sorted_paths