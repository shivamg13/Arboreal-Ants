import numpy as np


def quad(pher,adj):
    return adj*(pher**2)

def slight(pher,adj):
    return adj*(pher**1.1)

def deneubourg(pher,adj,k=1):
    return adj*((pher+k)**2)
    

def rank_edge(pher, adj, p_val = 0.01):

    rank_edge_probs = np.zeros(pher.shape)
    for i in range(pher.shape[0]):
        rank_edge_probs[i,:] = find_rank_edge_probs(pher[i,:], p_val)
        
    return rank_edge_probs
    
    
def find_rank_edge_probs(edges, p_exp):
    
    sorted_edges, inverse_edges, counts_edges = np.unique(edges, return_inverse=True, return_counts=True)
    size_unique = sorted_edges.shape[0]
    
    prob_array = (1-p_exp)*(p_exp**np.flip(np.arange(size_unique), 0))
    zero_present = (sorted_edges[0]==0)
    
    if (zero_present):
        prob_array[0] = 0
        if size_unique>1:
            prob_array[1] = 1 - np.sum(prob_array[2:])
    else:
        prob_array[0] = 1 - np.sum(prob_array[1:])
    
    prob_array_normalized = prob_array/counts_edges
    rank_edge_probs = prob_array_normalized[inverse_edges]
    
    return rank_edge_probs
    
            
    
    

