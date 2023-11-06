from mininet.net import Mininet
from mininet.node import OVSController, RemoteController
from mininet.link import TCLink
from mininet.clean import Cleanup
from inetmap import Project
import re

import networkx as nx


# Tworzenie instancji sieci Mininet                controller=RemoteController, , autoStaticArp=True
try:
    net = Mininet(topo=Project(), link=TCLink, autoStaticArp=True)

    net.start()
    G = nx.Graph()

    for host in net.hosts:
        G.add_node(host.name)

    for link in net.links:
        node1 = link.intf1.node.name
        node2 = link.intf2.node.name

        if "delay" in link.intf1.params:
            delay = int(link.intf1.params["delay"][:-2])
        else:
            delay = 0

        if "bw" in link.intf1.params:
            bw = int(link.intf1.params["bw"])
        else:
            bw = 1000
        
        G.add_edge(node1, node2, delay = delay, bw = bw)


    def calculate_path(source_node, destination_node):

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

    best_path = calculate_path("Ateny", "Madryt")[0][0]
    wzorzec = r'^s([1-9]|[1-9][0-9])$'
    for node in best_path:
        full_node = net.get(node)
        print(f"name:  {full_node.name}")
        if re.match(wzorzec, full_node.name):
            print(f"deviceId:  {'%016x' %int(full_node.name.lstrip('s'))}")
        else: 
            print("deviceId: none")


    net.stop()

except Exception as ex:
    Cleanup.cleanup()
    print('Cleanup caused by: ', ex)
