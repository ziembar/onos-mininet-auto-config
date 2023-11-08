import utils
from connection_request import connection_request

user_request = connection_request(1,"A","B","TCP",30,9)
user_request_UDP = connection_request(1,"A","B","UDP",40,9)
net, G =  utils.bootstrap()

best_path = utils.find_best_path("Ateny","Madryt",user_request)
print(best_path)
second = utils.find_best_path("Ateny","Madryt",user_request)
print(second)
third = utils.find_best_path("Ateny","Madryt",user_request)
print(third)
forth = utils.find_best_path("Ateny","Madryt",user_request_UDP)
print(forth)
fifth =  utils.find_best_path("Ateny","Madryt",user_request_UDP)
print(fifth)

# subgraph = utils.fit_into_requirements(user_request)
# print(subgraph)

utils.create_and_send_flow_rules(best_path[0], user_request)
