def create_flow_rule(deviceId, outPort, sourceIp, destinationId, protocolId):
    priority = 40000
    flow = {
        "priority": priority,
        "timeout": 20000,
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
                "ip": f"{sourceIp}/32"
            },
            {
                "type": "IPV4_DST",
                "ip": f"{destinationId}/32"
            },
             {
                "type": "IP_PROTO",
                "protocol": protocolId
            }
            ]
        }
    }
    return flow
        
