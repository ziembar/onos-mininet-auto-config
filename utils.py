import re
import networkx as nx
import json
import flow_rule_template as frt
import onos_request as request
import graph_operation

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
        G.add_edge(node1, node2, delay=delay, bw=bw, current_bw=bw, active_tcp=0, active_udp=0,
                   tcp_score=graph_operation.calculate_tcp_score(delay, bw, 0, 0),
                   udp_score=graph_operation.calculate_udp_score(delay, bw, 0, 0))

    return net,G
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

    success = 0

    for i in range(1, len(path) -1):
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
        if nodeFrontPort == 0 or nodeBackPort == 0:
            raise Exception(f"Could not find right ports for node {path[i]}")
        
        protocolId = 1
        if(user_request.type == "TCP"):
            protocolId = 6
        elif(user_request.type == "UDP"):
            protocolId = 17
        elif(user_request.type == "ICMP"):
            protocolId = 1
        
        flow_rule_front = frt.create_flow_rule(node['deviceId'], nodeFrontPort, srcIp, dstIp, protocolId)
        flow_rule_back = frt.create_flow_rule(node['deviceId'], nodeBackPort, dstIp, srcIp, protocolId)
        
        flow_rules.append(flow_rule_front)
        flow_rules.append(flow_rule_back)

        try:
            request.setSwitch(flow_rule_front, node['deviceId'])
            success += 1
        except Exception as err:
            raise Exception(err)

        try:
            request.setSwitch(flow_rule_back, node['deviceId'])
            success += 1
        except Exception as err:
            raise Exception(err)

    return f"[INFO] Successfully added {success} flows to switches."
    
        