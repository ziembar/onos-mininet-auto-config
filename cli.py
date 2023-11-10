import utils
from connection_request import connection_request

user_request = connection_request(1,"A","B","TCP",1,100)
user_request2 = connection_request(2,"A","B","TCP",1,100)
user_request3 = connection_request(3,"A","B","TCP",1,100)
user_request_UDP = connection_request(1,"A","B","UDP",40,16)
user_request_UDP2 = connection_request(2,"A","B","UDP",80,90)

net, G =  utils.bootstrap()

best_path = utils.find_best_path("Ateny","Madryt",user_request)
print(best_path)
second = utils.find_best_path("Ateny","Madryt",user_request2)
print(second)
third = utils.find_best_path("Ateny","Madryt",user_request)
print(third)
forth = utils.find_best_path("Ateny","Madryt",user_request_UDP)
print(forth)
fifth =  utils.find_best_path("Ateny","Madryt",user_request_UDP)
print(fifth)

# subgraph = utils.fit_into_requirements(user_request)
# print(subgraph)
