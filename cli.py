import utils
from connection_request import connection_request
import graph_operation
import argparse

# Create a parser
parser = argparse.ArgumentParser(description='Process some variables.')
parser.add_argument('-f', '--file', help='Input file containing connection requests')

# Parse the arguments
args = parser.parse_args()


user_requests = []
# Open the file and read each line
with open(args.file, 'r') as f:
    i = 0
    for line in f:
        try:
        # Split the line into its components
            source, destination, connection_type, min_bandwidth, max_delay = line.split()
            
            # Convert min_bandwidth and max_delay to integers
            min_bandwidth = int(min_bandwidth)
            max_delay = int(max_delay)
            
            # Call the connection_request function
            user_requests.append(connection_request(i, source, destination, connection_type, min_bandwidth, max_delay))
            i += 1
        except:
            print("Invalid input. Please check the input file.")
            exit()

# Continue with the rest of the program
net, G =  utils.bootstrap()
for request in user_requests:
    best_path = graph_operation.find_best_path(request, G)
    print(best_path)