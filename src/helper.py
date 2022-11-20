import numpy as np
from dijkstar import Graph, find_path
import hashlib
import csv   
import os

def row_normalize(mat):
    deg = np.sum(mat,1).astype('float64')
    deg[deg==0] = 1e-300
    return mat/deg[:,np.newaxis]

def shortest_path(adj, s = 0, d = None):
    n = np.shape(adj)[0]
    graph = Graph()
    for i in range(n):
        for j in range(n):
            if adj[i,j]!=0:
                graph.add_edge(i,j,adj[i,j])
    if d is None:
        d = n-1
    return find_path(graph,s,d)

def min_leakage_path(adj, passage, s=0,d=None):
    weights = -np.log(passage)
    adj_weighted = adj*np.transpose(weights)
    return shortest_path(adj_weighted, s, d)

def shortest_path_adj(adj):
    path_nodes = shortest_path(adj).nodes
    adj_s = np.zeros(adj.shape)
    for i in range(len(path_nodes)-1):
        adj_s[path_nodes[i],path_nodes[i+1]] = 1
    return adj_s

def min_leakage_path_adj(adj, passage):
    path_nodes = min_leakage_path(adj, passage).nodes
    adj_m = np.zeros(adj.shape)
    for i in range(len(path_nodes)-1):
        adj_m[path_nodes[i],path_nodes[i+1]] = 1
    return adj_m

#This function does not check convergence to non-path states
def check_convergence(pher, adj, thold , non_linearity, opt_path = None, non_lin_params = None):
    n = np.shape(pher)[0]
    f_norm_pher = row_normalize(non_linearity(pher, adj, non_lin_params)) 
    b_norm_pher = row_normalize(non_linearity(np.transpose(pher), np.transpose(adj), non_lin_params))
    #check convergence to optimum path. we use this for linear decision rule.
    if opt_path is not None:
        f_min = np.min(f_norm_pher[opt_path>0])
        b_min = np.min(b_norm_pher[np.transpose(opt_path)>0])
        if f_min > thold and b_min > thold:
            return True
        else:
            return False
    else:
        #slightly expensive to check
        #check that converged to some path
        #use this for non-linear decision rules
        cur_node = 0
        cur_set = set([])
        #Check forward path convergence
        while cur_node!=n-1 and cur_node not in cur_set:
            cur_set.add(cur_node)
            if(np.max(f_norm_pher[cur_node,:])==0):
                break
            if(np.max(f_norm_pher[cur_node,:])<thold):
                return False
            cur_node = np.argmax(f_norm_pher[cur_node,:])
            
        
        cur_node = n-1;
        cur_set = set([])
        #Check backward path convergence
        while cur_node!=0 and cur_node not in cur_set:
            cur_set.add(cur_node)
            if(np.max(b_norm_pher[cur_node,:])==0):
                break
            if(np.max(b_norm_pher[cur_node,:])<thold):
                return False
            cur_node = np.argmax(b_norm_pher[cur_node,:])
        return True
            
            

#path of length default_len - k added if no path already present. Otherwise path of length
#k less than the current shortest path length added to the graph.
def add_random_shortest_path(adj, k = 1, default_len = 5):
    n = np.shape(adj)[0]
    try:
        s_path = shortest_path(adj)
        new_path_cost = int(s_path.total_cost - k)
    except:
        new_path_cost = int(default_len - k)
        
    cur_node = 0
    if new_path_cost <= 0:
        return adj
    for co in range(1, new_path_cost):
        cur_cost_f = 0
        cur_cost_b = 0
        while cur_cost_f <= co or cur_cost_b <= new_path_cost  - co:
            next_node = np.random.randint(1,n-1) #random number between 1 and n - 2
            try:
                cur_cost_f = shortest_path(adj,0,next_node).total_cost
            except:
                cur_cost_f = float('inf')
            try:
                cur_cost_b = shortest_path(adj,next_node, n-1).total_cost
            except:
                cur_cost_b = float('inf')
        
        adj[cur_node, next_node] = 1
        cur_node = next_node
    adj[cur_node, n-1] = 1
    
    return adj
                

def update_array(i, pher_final, adj, thold, converged, path_val_array,  is_path_array, converged_array, non_linearity, passage = None, non_lin_params = None):
    if converged:
        f_norm_pher_final = row_normalize(non_linearity(pher_final, adj, non_lin_params))
        b_norm_pher_final = row_normalize(non_linearity(np.transpose(pher_final), np.transpose(adj), non_lin_params))
        n = np.shape(pher_final)[0]
        try:
            if passage is None:
                #find the shortest path
                path_for = shortest_path(f_norm_pher_final >= thold)
                path_back = shortest_path(b_norm_pher_final >= thold,n-1,0)             
            else:
                path_for = min_leakage_path(f_norm_pher_final >= thold, passage)
                path_back = min_leakage_path(b_norm_pher_final >= thold, passage,n-1,0)
            
            if np.array_equal(path_for.nodes, np.flip(path_back.nodes,0)):
                path_val_array[i] = path_for.total_cost
                is_path_array[i] = 1
            else:
                is_path_array[i] = 0
        except:
            is_path_array[i] = 0
        
    converged_array[i] = converged
    
def log_output(output, log_path, print_to_console = False):
    if print_to_console:
        print(output)
    with open(log_path, 'a') as f:
        print(output, file=f) 