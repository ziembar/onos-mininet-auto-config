import re
import networkx as nx
import json

delay_constant_tcp = 20
bw_constant_tcp = 1/20

delay_constant_udp = 1
bw_constant_udp = 1/10

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
        G.add_edge(node1, node2 ,delay = delay, bw = bw,current_bw=bw,active_tcp=0,active_udp=0, tcp_score=calculate_tcp_score(delay,bw,0,0),udp_score=calculate_udp_score(delay,bw,0,0))

    return net,G
#TODO: add Packet Loss

def calculate_tcp_score(delay,current_bw,active_tcp,active_udp):
    """
    assuming that:
    -avg BW is around 100
    -avg delay 5 and median 4 (!)
    hard to say how many TCP/UDP transmisions we will have to service and this may alos affect transmision
    """
    delay_factor = delay*delay_constant_tcp
    if(active_tcp==0):
        bw_factor = -1*current_bw*bw_constant_tcp
    else:
        bw_factor = -1*(current_bw/active_tcp)*bw_constant_tcp
    score = 50 + delay_factor+bw_factor
    return score
def calculate_udp_score(delay,current_bw,active_tcp,active_udp):
    delay_factor = delay*delay_constant_udp
    bw_factor = -1*current_bw*bw_constant_udp
    score = 50 + delay_factor+bw_factor
    return score
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
def find_best_path(source_node, destination_node,conection_type):
    if(conection_type=="TCP"):
        try:
            path = nx.shortest_path(G, source=source_node, target=destination_node, weight="tcp_score", method="dijkstra")
            length = nx.shortest_path_length(G, source=source_node, target=destination_node, weight="tcp_score", method="dijkstra")
            return path, length
        except nx.NetworkXNoPath:
            return None, float("inf")
    else:
        try:
            path = nx.shortest_path(G, source=source_node, target=destination_node, weight="udp_score",method="dijkstra")
            length = nx.shortest_path_length(G, source=source_node, target=destination_node, weight="udp_score", method="dijkstra")
            return path, length
        except nx.NetworkXNoPath:
            return None, float("inf")
def update_score(nodes,user_request):
    edges = []
    for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]
        data = G.get_edge_data(u,v)
        if(user_request.get_type()=='TCP'):
            new_tcp_score = calculate_tcp_score(data['delay'], data['bw'] - user_request.get_bw(),data['active_tcp']+1,data['active_udp'])
            new_udp_score = calculate_udp_score(data['delay'], data['bw'] - user_request.get_bw(),data['active_tcp']+1,data['active_udp'])
            G[u][v]['current_bw'] = data['bw'] -user_request.bw
            G[u][v]['active_tcp'] = data['active_tcp']+1
            G[u][v]['tcp_score'] = new_tcp_score
            G[u][v]['udp_score'] = new_udp_score

        elif(user_request.get_type=="UDP"):
            new_tcp_score = calculate_tcp_score(data['delay'], data['bw'] - user_request.get_bw,data['active_tcp'],data['active_udp']+1)
            new_udp_score = calculate_udp_score(data['delay'], data['bw'] - user_request.get_bw,data['active_tcp'],data['active_udp']+1)
            G[u][v]['current_bw'] = data['bw'] -user_request.bw
            G[u][v]['active_udp'] =data['active_udp']+1
            G[u][v]['tcp_score'] = new_tcp_score
            G[u][v]['udp_score'] = new_udp_score

