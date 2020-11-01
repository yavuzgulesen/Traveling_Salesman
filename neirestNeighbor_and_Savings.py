# -*- coding: utf-8 -*-

def output_msg(tour, origin):
    output = ''
    for i in range(0, len(tour) - 1):
        output += str(tour[i])
        output += " -> "
    output += str(origin)
    return output

def draw_graph(tour, path_lengths):
    import networkx as nx
    print("Path lengths:", path_lengths)
    edges = {(str(tour[0]), str(tour[1]), path_lengths[0])}
    i = 1
    while i <(len(tour)-1):
        edges.add((str(tour[i]), str(tour[i+1]), path_lengths[i]))
        i+=1
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    
    pos = nx.spring_layout(G, scale = 100.)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    
def nearest_neighbor(origin, nodes, d):
    tour = [origin]
    tour_paths = []
    tour_length = 0
    current_node = origin
    while len(tour) < len(nodes):
        nearest_node = None
        dist_nearest_node = max(d[current_node])+1  #max value in the row + 1
        for i in nodes:
            if i not in tour and d[current_node][i] < dist_nearest_node:
                dist_nearest_node = d[current_node][i]
                nearest_node = i
        tour_length += dist_nearest_node
        tour.append(nearest_node)
        tour_paths.append(dist_nearest_node)
        current_node = nearest_node
    tour_length += d[tour[-1]][origin] #return back to home7
    tour_paths.append(d[tour[-1]][origin])
    tour.append(origin)
    tour_length = round(tour_length, 2)
    

    
    print('TSP tour found with nearest neighbor search starting from', origin, 'is:')
    print(output_msg(tour, origin))
    print('with total length of', tour_length)
    #draw_graph(tour, tour_paths)
    
    
def two_opt(tour, tour_length, d):
    current_tour, current_tour_length = tour, tour_length
    best_tour, best_tour_length = current_tour, current_tour_length
    solution_improved = True
    
    while solution_improved:
        solution_improved = False
        
        for i in range(1, len(current_tour)-2):
            for j in range(i+1, len(current_tour)-1):
                diff = round((d[current_tour[i-1]][current_tour[j]]
                                  + d[current_tour[i]][current_tour[j+1]]
                                  - d[current_tour[i-1]][current_tour[i]]
                                  - d[current_tour[j]][current_tour[j+1]]), 2)
                
                if current_tour_length + diff < best_tour_length:
                    print('Found an improving move! Updating the best tour...')
                    
                    best_tour = current_tour[:i] + list(reversed(current_tour[i:j+1])) + current_tour[j+1:]
                    best_tour_length = round(current_tour_length + difference, 2)
                    
                    print('Improved tour is:', best_tour, 'with length',
                          best_tour_length)
                    
                    solution_improved = True
                    
        current_tour, current_tour_length = best_tour, best_tour_length
    
    # Return the resulting tour and its length as a tuple
    return best_tour, best_tour_length  

def savings(origin, nodes, d):
    from pqdict import pqdict
    
    customers = {i for i in nodes if i != origin}
    tours = {(i,i): [origin, i, origin] for i in customers}
    
    savings = {(i, j): round(d[i][origin] + d[origin][j] - d[i][j], 2) 
               for i in customers for j in customers if j != i}
    
    pq = pqdict(savings, reverse = True)
    while len(tours) > 1:
        i,j = pq.pop()
        break_outer = False
        for t1 in tours:
            #i & j should be in different subtours
            for t2 in tours.keys()-{t1}:
                #if i is last node and j is the first node in their corresponding
                #subtours, merge:
                if t1[1] == i and t2[0] == j:
                    tours[(t1[0], t2[1])] = tours[t1][:-1] + tours[t2][1:]
                    del tours[t1], tours[t2]
                    break_outer = True
                    break
            if break_outer:
                break
    # Final tours dictionary (involves a single tour, which is the TSP tour)
    #print(tours)
    
    # Compute tour length
    tour_length = 0
    for tour in tours.values():
        for i in range(len(tour)-1):
            tour_length += d[tour[i]][tour[i+1]]
            
    # Round the result to 2 decimals to avoid floating point representation errors
    tour_length = round(tour_length, 2)
    
    # Print the tour
    print('TSP tour found with savings heuristic starting from', origin, 'is:')
    print(output_msg(tour, origin))
    print('with total length', tour_length)
    
    
def TSP(origin, filename, algo):
    import pandas as pd
    df = pd.read_excel(filename)
    nodes = list(range(df.shape[0]))
    d = [[round(float(df[j][i]), 2) for j in nodes] for i in nodes] 
    
    if algo == 'nn':
        nearest_neighbor(origin, nodes, d)
    elif algo == 'savings':
        savings(origin, nodes, d)
    else:
        print("wrong input")
        
TSP(0, 'real_distances_10customers.xls', 'nn')
print("--------------------------")
TSP(0, 'tsp_data.xls', 'savings')


