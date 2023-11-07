import utils
from connection_request import connection_request
#TODO: odzyskiwanie portu z deviceId

user_request = connection_request(1,"A","B","TCP",80,9)
net, G =  utils.bootstrap()

best_path = utils.find_best_path("Ateny","Madryt",user_request)
print(best_path)
utils.update_score(best_path[0],user_request)
second = utils.find_best_path("Ateny","Madryt",user_request)
print(second)

subgraph = utils.fit_into_requirements(user_request)
print(subgraph)
