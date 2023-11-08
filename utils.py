import re
import networkx as nx
import json
import flow_rule_template as frt
import onos_request as request

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
        bw_factor = (-1)*current_bw*bw_constant_tcp
    else:
        bw_factor = (-1)*(current_bw/active_tcp)*bw_constant_tcp
    score = 50 + delay_factor+bw_factor
    return score

def calculate_udp_score(delay,current_bw,active_tcp,active_udp):
    delay_factor = delay*delay_constant_udp
    bw_factor = (-1)*current_bw*bw_constant_udp
    score = 100 + delay_factor+bw_factor
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
#TODO: handle no path in subgrapg so we can give user another path that does not fit requirements
def find_best_path(source_node, destination_node,user_request):
    subgraph = fit_into_requirements(user_request)
    path = best_path_helper(source_node,destination_node,user_request,subgraph)
    if(path[0]==None):
        print("Nie jestesmy w stanine znalezc zadnej sciezki spelniajacej twoje wymagania")
        path = best_path_helper(source_node,destination_node,user_request,G)
        exceeded_bw, exceeded_delay = find_narrow_throat(path[0],user_request)

    return path

def best_path_helper(source_node, destination_node,user_request,subgraph):
    if (user_request.get_type() == "TCP"):
        try:
            path = nx.shortest_path(subgraph, source=source_node, target=destination_node, weight="tcp_score",
                                    method="dijkstra")
            length = nx.shortest_path_length(subgraph, source=source_node, target=destination_node, weight="tcp_score",
                                             method="dijkstra")
            update_score(path, user_request)
            return path, length
        except nx.NetworkXNoPath:
            return None, float("inf")
    elif (user_request.get_type() == "UDP"):
        try:
            path = nx.shortest_path(subgraph, source=source_node, target=destination_node, weight="udp_score",
                                    method="dijkstra")
            length = nx.shortest_path_length(subgraph, source=source_node, target=destination_node, weight="udp_score",
                                             method="dijkstra")
            update_score(path, user_request)
            return path, length
        except nx.NetworkXNoPath:
            return None, float("inf")
def find_narrow_throat(path,user_request):
    print(path)
    exceeded_delay=[]
    exceeded_bw=[]

    for i in range(1,len(path) - 2):
        u = path[i]
        v = path[i + 1]
        edge = G.get_edge_data(u,v)
        if(edge['delay']>=user_request.get_delay()):
            exceeded_delay.append(edge)
        if(edge['current_bw']<=user_request.get_bw()):
            exceeded_bw.append(edge)

    print(exceeded_bw)
    print(exceeded_delay)

    return exceeded_bw,exceeded_delay
def update_score(nodes,user_request):
    for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]
        data = G.get_edge_data(u,v)
        if(user_request.get_type()=='TCP'):
            new_tcp_score = calculate_tcp_score(data['delay'], data['bw'] - user_request.get_bw(),data['active_tcp']+1,data['active_udp'])
            new_udp_score = calculate_udp_score(data['delay'], data['bw'] - user_request.get_bw(),data['active_tcp']+1,data['active_udp'])
            G[u][v]['current_bw'] = data['bw'] -user_request.get_bw()
            G[u][v]['active_tcp'] = data['active_tcp']+1
            G[u][v]['tcp_score'] = new_tcp_score
            G[u][v]['udp_score'] = new_udp_score

        elif(user_request.get_type()=='UDP'):
            new_tcp_score = calculate_tcp_score(data['delay'], data['bw'] - user_request.get_bw(),data['active_tcp'],data['active_udp']+1)
            new_udp_score = calculate_udp_score(data['delay'], data['bw'] - user_request.get_bw(),data['active_tcp'],data['active_udp']+1)
            G[u][v]['current_bw'] = data['bw'] -user_request.get_bw()
            G[u][v]['active_udp'] =data['active_udp']+1
            G[u][v]['tcp_score'] = new_tcp_score
            G[u][v]['udp_score'] = new_udp_score
def fit_into_requirements(user_request):
    subgraph = nx.Graph()

    #To na lambdy pozniej
    for u, v, data in G.edges(data=True):
        if data['current_bw'] >= user_request.get_bw() and data['delay'] < user_request.get_delay():
            subgraph.add_edge(u, v, **data)
    return subgraph

def create_and_send_flow_rules(path, user_request):
    """Creates and sends to localhost onos controller flow rules for a given path.
    -------
    Parameters:
    path: list of strings (path between source and destination node)
    user_request: connection_request object
    -------
    Returns:
    flow_rules: list of strings (flow rules in JSON format)
    """
    flow_rules = []
    srcIp = find_device_by_name(path[0])['ip']
    dstIp = find_device_by_name(path[-1])['ip']

    for i in range(1, len(path) - 2):
        node = find_device_by_name(path[i])
        frontNode = find_device_by_name(path[i + 1])
        backNode = find_device_by_name(path[i - 1])

        nodeFrontPort = 0
        nodeBackPort = 0
        
        for link in node['links']:
            if nodeFrontPort == 0:
                for frontLink in frontNode['links']:
                    if link['linkId'] == frontLink['linkId']:
                        nodeFrontPort = link['port']
                        break
            if nodeBackPort == 0:
                for backLink in backNode['links']:
                    if link['linkId'] == backLink['linkId']:
                        nodeBackPort = link['port']
                        break
            if nodeFrontPort != 0 and nodeBackPort != 0:
                break


        flow_rule_front = frt.create_flow_rule(node['deviceId'], nodeFrontPort, srcIp, dstIp)
        flow_rule_back = frt.create_flow_rule(node['deviceId'], nodeBackPort, dstIp, srcIp)


        flow_rules.append(flow_rule_front)
        flow_rules.append(flow_rule_back)

        request.setSwitch(flow_rule_front, node['deviceId'])
        request.setSwitch(flow_rule_back, node['deviceId'])

    return flow_rules