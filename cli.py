import utils
from connection_request import connection_request

user_request = connection_request(1,"A","B","TCP",80,10)
net, G =  utils.bootstrap()

best_path = utils.find_best_path("Ateny","Madryt","TCP")
print(best_path)
utils.update_score(best_path[0],user_request)
second = utils.find_best_path("Ateny","Madryt","TCP")
print(second)
#TODO: odzyskiwanie portu z deviceId
