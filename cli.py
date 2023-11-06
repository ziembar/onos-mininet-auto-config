import utils
net, G =  utils.bootstrap()

best_path = utils.calculate_paths("Ateny", "Madryt")[0][0]


for node in best_path:
    full_node = utils.find_device_by_name(node)
    print(f"name:  {full_node['name']}")
    if 'deviceId' in full_node:
        print(f"deviceId:  {full_node['deviceId']}")
    else: 
        print("deviceId: none")

