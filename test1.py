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

    # Uruchomienie sieci
    net.start()
    # Tworzenie obiektu grafu NetworkX na podstawie topologii Mininet
    G = nx.Graph()

    # Dodawanie węzłów (hostów i przełączników) do grafu
      # Dodawanie hostów jako wierzchołki do grafu
    for host in net.hosts:
        G.add_node(host.name)

    wzorzec = r'^s([1-9]|[1-9][0-9])$'

    # Dodawanie krawędzi (połączeń) między hostami na podstawie połączeń w Mininet
    for link in net.links:
        node1 = link.intf1.node.name
        node2 = link.intf2.node.name
    
        for innerLink in net.links:
            if innerLink.intf1.node.name == node1 and not re.match(innerLink.intf2.node.name, wzorzec):
                node1 = innerLink.intf2.node.name
            if innerLink.intf2.node.name == node1 and not re.match(innerLink.intf1.node.name, wzorzec):
                node1 = innerLink.intf1.node.name
            if innerLink.intf1.node.name == node2 and not re.match(innerLink.intf2.node.name, wzorzec):
                node2 = innerLink.intf2.node.name
            if innerLink.intf2.node.name == node2 and not re.match(innerLink.intf1.node.name, wzorzec):
                node2 = innerLink.intf1.node.name
            
        if(node1==node2):
            continue
                
        G.add_edge(node1, node2, delay = int(link.intf1.params["delay"][:-2]), bw = link.intf1.params["bw"])




    # Znalezienie wszystkich możliwych ścieżek między dwoma węzłami
    source_node = 'Londyn'  # Zmień na odpowiednią nazwę węzła źródłowego
    destination_node = 'Warszawa'  # Zmień na odpowiednią nazwę węzła docelowego
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
    for path in sorted_paths:
        print(path)



    net.stop()
except Exception as ex:
    Cleanup.cleanup()
    print('Cleanup caused by: ', ex)
