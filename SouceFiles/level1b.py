import json
import numpy as np
from python_tsp.heuristics import solve_tsp_simulated_annealing, solve_tsp_local_search

f = open("InputData\\level1b.json")
data = json.load(f)
f.close()

n_neighbourhoods = data["n_neighbourhoods"]
n_restaurants = data["n_restaurants"]

ord_quan = []
dist_matrix = []
dist = [0]
dist.extend(data["restaurants"]["r0"]["neighbourhood_distance"])
dist_matrix.append(dist)

i = 0
for n in data["neighbourhoods"]:
    dist = [data["restaurants"]["r0"]["neighbourhood_distance"][i]]
    dist.extend(data["neighbourhoods"][n]["distances"])
    i += 1
    dist_matrix.append(dist)
    ord_quan.append(data["neighbourhoods"][n]["order_quantity"])

tot_capacity = data["vehicles"]["v0"]["capacity"]
print(ord_quan)
distance_matrix = np.array(dist_matrix)

permutation, distance = solve_tsp_simulated_annealing(distance_matrix)
permutation2, distance2 = solve_tsp_local_search(distance_matrix, x0=permutation, perturbation_scheme="ps3")
permutation2 = permutation2[1:]

delivered = []
curr_capacity = 600
n_delivered = 0
i = 0
start = 0
print(permutation2)
    
while(n_delivered < n_neighbourhoods):
    i = 0
    if curr_capacity <= 0:
        curr_capacity = tot_capacity
    if ord_quan[permutation2[i]-1] < tot_capacity:
        if ord_quan[permutation2[i]-1] <= curr_capacity and str(permutation2[i]-1) not in delivered:
            curr_capacity -= ord_quan[permutation2[i]-1]
            delivered.append(str(permutation2[i]-1))
            n_delivered += 1
            ord_quan[permutation2[i]-1] = 700

for i in range(len(permutation2)):
    if ord_quan[permutation2[i]-1] <= curr_capacity:
        curr_capacity -= ord_quan[permutation2[i]-1]
        delivered.append(str(permutation2[i]-1))
    else:
        curr_capacity = tot_capacity
print(delivered)

opDict = {}
pathDict = {}
path = ["r0"]
for n in permutation:
    if n != 0:
        path.append("n" + str(n-1))
path.append("r0")
pathDict["path"] = path
opDict["v0"] = pathDict

json_object = json.dumps(opDict, indent=4)
with open("Output\\level1b_output.json", "w") as outfile:
    json.dump(opDict, outfile)