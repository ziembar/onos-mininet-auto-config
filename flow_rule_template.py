def create_flow_rule(deviceId, outPort, sourceIp, destinationId, protocolId):
    flow = {
        "priority": 40000,
        "timeout": 100000,
        "isPermanent": False,
        "deviceId": deviceId,
        "treatment": {
            "instructions": [
            {
                "type": "OUTPUT",
                "port": outPort
            }
            ]
        },
        "selector": {
            "criteria": [
            {
                "type": "ETH_TYPE",
                "ethType": "0x0800"
            },
            {
                "type": "IPV4_SRC",
                "ip": "{}/32".format(sourceIp)
            },
            {
                "type": "IPV4_DST",
                "ip": "{}/32".format(destinationId)
            },
            
            ]
        }
    }
    return flow
        
