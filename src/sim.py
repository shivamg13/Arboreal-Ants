import numpy as np
import random
import gen_graph as gg
import helper


#Input
#adj: directed adjacency matrix.
#passage: 1 - leakage at each node. should be (0,1].
#inc_rate: factor by which flow increases at each time step
#decay: factor by which pheromone level gets multiplied each time step.
#opt_path: The path for which we want to print the normalized pheromone level.
#non_linearity: a function that takes as input pher matrix and applies the appropriate non-linear decision rule.
#pher: initial pheromone levels at all edges.
#ff_start: incoming forward flow
#bf_end: incoming backward flow
#thold: convergence threshold
#print_period: period after which convergence is checked and the current normalized pheromone level on opt_path is printed.
#max_iter: maximum number of iterations for which to run the dynamics

#Returns (pher, bool indicating if the dynamics converged, non_lin_params)
def simulate(adj, passage, inc_rate, decay, opt_path, non_linearity, pher, ff_start = 1, bf_end = 1, thold = 0.999, print_period = 1000, convergence_check_period = 1000, max_iter = float('inf'), converge_to_opt = False, non_lin_params = None, log_path = None, print_to_console = True):    
    
    n = np.shape(adj)[0]
    ff = np.zeros((1,n)) #current forward flow at all nodes
    bf = np.zeros((1,n)) #current backward flow at all nodes
    ff[0,0] = ff_start
    bf[0,n-1] = bf_end
    
    iter = 0
    
    while iter < max_iter:
        f_norm_pher = helper.row_normalize(non_linearity(pher, adj, non_lin_params)) 
        b_norm_pher = helper.row_normalize(non_linearity(np.transpose(pher), np.transpose(adj),non_lin_params)) 
        
        if iter%print_period==0 and opt_path is not None:
            helper.log_output(f"Iteration {iter}, {np.min(f_norm_pher[opt_path>0]):.5f},  {np.min(b_norm_pher[np.transpose(opt_path)>0]): .5f}", log_path, print_to_console)
#             print(iter, np.min(f_norm_pher[opt_path>0]), np.min(b_norm_pher[np.transpose(opt_path)>0]))
        
        if converge_to_opt:
            if iter>0 and iter%convergence_check_period==0 and (helper.check_convergence(pher, adj, thold,non_linearity,opt_path, non_lin_params = non_lin_params)):
                break
        else:
            if iter>0 and iter%convergence_check_period==0 and (helper.check_convergence(pher, adj,thold, non_linearity, non_lin_params = non_lin_params)):
                break
        
        ff_new = (ff.dot(f_norm_pher))*passage
        bf_new = (bf.dot(b_norm_pher))*passage   
        ff_new[0,0] = ff_start*inc_rate
        bf_new[0,n-1] = bf_end*inc_rate
        ff_new[0,n-1] = 0
        bf_new[0,0] = 0
        
        pher = pher + (f_norm_pher*np.transpose(ff) + np.transpose(b_norm_pher*np.transpose(bf)))
        pher = decay*pher
        ff = ff_new/inc_rate
        bf = bf_new/inc_rate
        pher = pher/inc_rate
        if non_lin_params is not None and 'k' in non_lin_params:
            non_lin_params['k'] = non_lin_params['k']/inc_rate
        
        iter+=1
    if converge_to_opt:
        return (pher, helper.check_convergence(pher, adj, thold, non_linearity, opt_path, non_lin_params=non_lin_params), non_lin_params)
    else:
        return (pher, helper.check_convergence(pher, adj, thold, non_linearity, non_lin_params= non_lin_params), non_lin_params)