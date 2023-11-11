import utils
from connection_request import connection_request
import graph_operation

user_request = connection_request(1,"A","B","TCP",1,100)
user_request2 = connection_request(2,"A","B","TCP",1,100)
user_request3 = connection_request(3,"A","B","TCP",1,100)
user_request_UDP = connection_request(1,"A","B","UDP",41,160)
user_request_UDP2 = connection_request(2,"A","B","UDP",51,20)
user_request_TCP = connection_request(2,"A","B","UDP",51,20)


net, G =  utils.bootstrap()

best_path = graph_operation.find_best_path("Ateny","Madryt",user_request,G)
print(best_path)
second = graph_operation.find_best_path("Ateny","Madryt",user_request2,G)
print(second)
third = graph_operation.find_best_path("Ateny","Madryt",user_request,G)
print(third)
forth = graph_operation.find_best_path("Ateny","Madryt",user_request_UDP,G)
print(forth)
fifth =  graph_operation.find_best_path("Ateny","Madryt",user_request_UDP2,G)
print(fifth)


# subgraph = utils.fit_into_requirements(user_request)
# print(subgraph)
