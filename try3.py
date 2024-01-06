import json
import numpy as np
from python_tsp.heuristics import solve_tsp_simulated_annealing, solve_tsp_local_search
import numpy as np
import pandas as pd
import pulp
import itertools
import gmaps
import googlemaps
import matplotlib.pyplot as plt 

f = open("InputData\\level1a.json")
data = json.load(f)
f.close()



n_neighbourhoods = data["n_neighbourhoods"]
n_restaurants = data["n_restaurants"]

customer_count = 20
vehicle_count = 1
vehicle_capacity = 600

# fix random seed
np.random.seed(seed=777)

for vehicle_count in range(1,vehicle_count+1):
    
    # definition of LpProblem instance
    problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

    # definition of variables which are 0/1
    x = [[[pulp.LpVariable("x%s_%s,%s"%(i,j,k), cat="Binary") if i != j else None for k in range(vehicle_count)]for j in range(customer_count)] for i in range(customer_count)]

    # add objective function
    problem += pulp.lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                          for k in range(vehicle_count) 
                          for j in range(customer_count) 
                          for i in range (customer_count))

    # constraints
    # foluma (2)
    for j in range(1, customer_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0 
                              for i in range(customer_count) 
                              for k in range(vehicle_count)) == 1 

    # foluma (3)
    for k in range(vehicle_count):
        problem += pulp.lpSum(x[0][j][k] for j in range(1,customer_count)) == 1
        problem += pulp.lpSum(x[i][0][k] for i in range(1,customer_count)) == 1

    # foluma (4)
    for k in range(vehicle_count):
        for j in range(customer_count):
            problem += pulp.lpSum(x[i][j][k] if i != j else 0 
                                  for i in range(customer_count)) -  pulp.lpSum(x[j][i][k] for i in range(customer_count)) == 0

    #foluma (5)
    for k in range(vehicle_count):
        problem += pulp.lpSum(df.demand[j] * x[i][j][k] if i != j else 0 for i in range(customer_count) for j in range (1,customer_count)) <= vehicle_capacity 


    # fomula (6)
    subtours = []
    for i in range(2,customer_count):
         subtours += itertools.combinations(range(1,customer_count), i)

    for s in subtours:
        problem += pulp.lpSum(x[i][j][k] if i !=j else 0 for i, j in itertools.permutations(s,2) for k in range(vehicle_count)) <= len(s) - 1

    
    # print vehicle_count which needed for solving problem
    # print calculated minimum distance value
    if problem.solve() == 1:
        print('Vehicle Requirements:', vehicle_count)
        print('Moving Distance:', pulp.value(problem.objective))
        break

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

print(ord_quan)
distance_matrix = np.array(dist_matrix)

permutation, distance = solve_tsp_simulated_annealing(distance_matrix)
permutation2, distance2 = solve_tsp_local_search(distance_matrix, x0=permutation, perturbation_scheme="ps3")

#permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
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
with open("Output\\level1a_output.json", "w") as outfile:
    json.dump(opDict, outfile)