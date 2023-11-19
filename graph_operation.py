import networkx as nx

delay_constant_tcp = 20
bw_constant_tcp = 1/20

delay_constant_udp = 1
bw_constant_udp = 1/10

# % of BW that need to stay empty
reserve_constant = 0.2

def fit_into_requirements(user_request, G):
    subgraph = nx.Graph()

    for u, v, data in G.edges(data=True):
        if data['current_bw']*(1-reserve_constant) >= user_request.bw:
            subgraph.add_edge(u, v, **data)
    return subgraph

def best_path_helper(user_request, subgraph):
    if (user_request.type == "TCP" or user_request.type == "ICMP"):
        try:
            path = nx.shortest_path(subgraph, source=user_request.source, target=user_request.destination,
                                    weight="tcp_score", method="dijkstra")
            length = nx.shortest_path_length(subgraph, source=user_request.source, target=user_request.destination,
                                             weight="tcp_score", method="dijkstra")
            return path, length
        except nx.NetworkXNoPath:
            return None, float("inf")
    elif (user_request.type == "UDP"):
        try:
            path = nx.shortest_path(subgraph, source=user_request.source, target=user_request.destination, weight="udp_score",
                                    method="dijkstra")
            length = nx.shortest_path_length(subgraph, source=user_request.source, target=user_request.destination, weight="udp_score",
                                             method="dijkstra")
            return path, length
        except nx.NetworkXNoPath:
            return None, float("inf")

def calculate_delay(path, G):
    delay_sum = 0

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        data = G.get_edge_data(u, v)
        delay_sum = delay_sum + data['delay']
    return delay_sum

def update_score(nodes, user_request,G):
    for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]
        data = G.get_edge_data(u, v)
        if (user_request.type == 'TCP' or user_request.type == 'ICMP'):
            new_tcp_score = calculate_tcp_score(data['delay'], data['bw'] - user_request.bw,
                                                data['active_tcp'] + 1, data['active_udp'])
            new_udp_score = calculate_udp_score(data['delay'], data['bw'] - user_request.bw,
                                                data['active_tcp'] + 1, data['active_udp'])
            G[u][v]['current_bw'] = data['current_bw'] - user_request.bw
            G[u][v]['active_tcp'] = data['active_tcp'] + 1
            G[u][v]['tcp_score'] = new_tcp_score
            G[u][v]['udp_score'] = new_udp_score

        elif (user_request.type == 'UDP'):
            new_tcp_score = calculate_tcp_score(data['delay'], data['bw'] - user_request.bw, data['active_tcp'],
                                                data['active_udp'] + 1)
            new_udp_score = calculate_udp_score(data['delay'], data['bw'] - user_request.bw, data['active_tcp'],
                                                data['active_udp'] + 1)
            G[u][v]['current_bw'] = data['current_bw'] - user_request.bw
            G[u][v]['active_udp'] = data['active_udp'] + 1
            G[u][v]['tcp_score'] = new_tcp_score
            G[u][v]['udp_score'] = new_udp_score

def calculate_tcp_score(delay, current_bw, active_tcp, active_udp):
    """
    assuming that:
    -avg BW is around 100
    -avg delay 5 and median 4 (!)
    hard to say how many TCP/UDP transmisions we will have to service and this may alos affect transmision
    """

    delay_fun = (25/3)*delay-25
    if(active_tcp==0):
        bw_fun = (-5/8)*current_bw +50
    else:
        bw_fun = (-5/8)*(current_bw/active_tcp)+50

    score = delay_fun + bw_fun
    return score

def calculate_udp_score(delay, current_bw, active_tcp, active_udp):
    delay_fun = (5/3)*delay-5
    bw_fun = (-9/8) * current_bw + 90
    score = 100 + delay_fun+bw_fun
    return score

def find_narrow_throat(path, G):
    exceeded_delay = 0
    exceeded_bw = float("inf")

    for i in range(1, len(path) - 2):
        u = path[i]
        v = path[i + 1]
        edge = G.get_edge_data(u, v)
        exceeded_delay = exceeded_delay + edge['delay']
        if (edge['current_bw'] < exceeded_bw):
            exceeded_bw = edge['current_bw']
    return exceeded_bw, exceeded_delay

def find_best_path(user_request,G):
    #Filtr po BW
    subgraph = fit_into_requirements(user_request,G)

    #Optymalna sciezka
    path = best_path_helper(user_request, subgraph)

    #Sprawdzanie delay
    if (path[0] != None):
        delay_sum = calculate_delay(path[0], G)


    if (path[0] == None or delay_sum > user_request.delay):

        #Sciezka na calym grafie
        path_sub_optimal = best_path_helper(user_request, G)

        #Pewnie mozna by to wykorzystac do sortowania w zależności od potrzeb
        #dopa = calculate_paths(source_node,destination_node,G)
        exceeded_bw, exceeded_delay = find_narrow_throat(path_sub_optimal[0], G)

        if (path_sub_optimal[0] == None or exceeded_delay > user_request.delay or exceeded_bw<user_request.bw):
            print(f"Not able to provide connection with given parameters from {user_request.source} to {user_request.destination}.")

            print("Setting best possible connection instead:")
            print(f"Total delay: {exceeded_delay}, minimum throughput: {exceeded_bw}")

        path = path_sub_optimal
    update_score(path[0], user_request,G)

    return path[0]


def calculate_paths(source_node, destination_node,G):
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
        path_bw = min(G[path[i]][path[i + 1]]['current_bw'] for i in range(len(path) - 1))

        if path_bw < min_bw:
            min_bw = path_bw
            min_bw_path = path

        sorted_paths.append((path, path_length, path_bw))
    sorted_paths = sorted(sorted_paths, key=lambda rekord: rekord[1])
    return sorted_paths

