def create_flow_rule(deviceId, outPort, sourceIp, destinationId):
    flow = """{{
        "priority": 40000,
        "timeout": 1500,
        "isPermanent": true,
        "deviceId": "of:{0}",
        "treatment": {{
            "instructions": [
            {{
                "type": "OUTPUT",
                "port": "{1}"
            }}
            ]
        }},
        "selector": {{
            "criteria": [
            {{
                "type": "ETH_TYPE",
                "ethType": "0x0800"
            }},
            {{
                "type": "IPV4_SRC",
                "ip": "{2}/32"
            }},
            {{
                "type": "IPV4_DST",
                "ip": "{3}/32"
            }}
            ]
        }}
    }}"""
    return flow.format(deviceId, outPort, sourceIp, destinationId)
        
