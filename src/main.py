import numpy as np
import random
import gen_graph as gg
import helper
import sim
import plot
import decision_rules
from schema import schema
from quinine import QuinineArgumentParser
import uuid
import os
import yaml


def main(args):

    num_instances = args.num_instances
    start_seed = args.start_seed
    

    #value of path length/leakage with non-linear decision rule without increaing flow/leakage enforced
    #for leakage we store the -log(1 - path_leakage) for each instance
    path_val_nonlin_wo_array = np.zeros(num_instances)-1
    #whether the forward flow converges to some path and backward flow converged to some path
    converged_nonlin_wo_array = np.zeros(num_instances)-1
    #whether the forward and backward flow converges to the same path
    is_path_nonlin_wo_array = np.zeros(num_instances) - 1
    
    #value of path length/leakage with non-linear decision rule with increaing flow/leakage enforced
    #the descriptions of arrays are same as above
    path_val_nonlin_with_array = np.zeros(num_instances)-1
    converged_nonlin_with_array = np.zeros(num_instances)-1
    is_path_nonlin_with_array = np.zeros(num_instances) - 1
    
    #value of path length/leakage with linear decision rule with increaing flow/leakage enforced
    path_val_lin_with_array = np.zeros(num_instances)-1
    #whether the forward and backward flow converges to the *optimum* path
    converged_lin_with_array = np.zeros(num_instances)-1
    #whether the forward and backward flow converges to the same path.
    is_path_lin_with_array = np.zeros(num_instances) - 1
    
    #optimum path length/leakage
    #for leakage we store the -log(1 - path_leakage) for each instance
    opt_path_val_array = np.zeros(num_instances)-1
    
    
    min_leakage = args.min_leakage #whether we are testing for convergence to minimum leakage path or shortest path
    uniform_init = not args.random_init #initial pheromone level to be initialized uniformly or randomly
    non_lin = args.non_lin
    graph_type = args.graph_type
    
    print_period = args.print_period
    convergence_check_period = args.convergence_check_period
    thold = args.conv_thold
    max_iter = args.max_iter
    decay = args.decay #factor by which pheromone level gets multiplied each time step
    
    log_path = os.path.join(args.out_dir,'log.txt')

    helper.log_output(f"We log the minimum of normalized forward and backward  flows across all edges on the optimum path. Here, by normalized forward (backward) flow at an edge (u,v), we refer to the fraction of forward (backward) flow entering it from the total flow present at vertex u (v). For the linear decision rule, normalized forward and backward flows are same as normalized forward and backward pheromone levels.", log_path, args.print_to_console)
    
    for i in range(num_instances):
        helper.log_output(f"Instance number {i+start_seed}", log_path, args.print_to_console)
#         print("Instance number  %3d" % (i+start_seed))
        rseed = i+start_seed
        random.seed(rseed)
        np.random.seed(rseed)
        
        if graph_type == 'gnp_local':
            n = args.num_nodes #number of nodes
            p = args.p_graph
            has_path = False
            #Keep sampling new graphs until it has at least one path from source to destination
            while not has_path:
                try:
                    adj = gg.g_np_local(n,p,args.win_size, not min_leakage, args.with_loop) #Directed adjacency matrix
                    helper.shortest_path(adj)
                    has_path = True
                except:
                    has_path = False
        elif graph_type == 'gnp':
            n = args.num_nodes #number of nodes
            p = args.p_graph
            adj = gg.g_np(n,p, not min_leakage, args.with_loop) #Directed adjacency matrix
            has_path = False
            #Keep sampling new graphs until it has at least one path from source to destination
            while not has_path:
                try:
                    adj = gg.g_np(n,p, not min_leakage, args.with_loop) #Directed adjacency matrix
                    helper.shortest_path(adj)
                    has_path = True
                except:
                    has_path = False
        else:
            n = args.num_nodes
            adj =  gg.grid(int(np.sqrt(n)), not min_leakage)
        

            
    
        if min_leakage:
            passage = 0.9+0.1*np.random.rand(1,n) #1-leakage at each node. should be (0,1]
            inc_rate = 1 #factor by which flow increases at each time step
            opt_path = helper.min_leakage_path_adj(adj, passage) #The path to which linear dynamics are expected to converge
            opt_path_val_array[i] = helper.min_leakage_path(adj, passage).total_cost
        else:
            passage = 1*np.ones((1,n))  #1-leakage at each node. should be (0,1]
            inc_rate = 1.1 #factor by which flow increases at each time step
            opt_path = helper.shortest_path_adj(adj) #The path to which linear dynamics are expected to converge
            opt_path_val_array[i] = helper.shortest_path(adj).total_cost
        
        if uniform_init:
            pher =  adj.copy() #Pheromone levels
        else:
            pher = np.random.rand(n,n)*adj
            
        passage.flags.writeable = False
        
    
       
        ff_start = 0.5 + np.random.rand()*0.5 #forward flow at start node
        bf_end = 0.5 + np.random.rand()*0.5 #backward flow at end node
        
        k_init = 0
        non_lin_params = {'k':k_init}
        #k only used for denb. Only use this dictionary for nonlinear parameters that change dynamically during simulation. For example, k changes when flow is increasing with time due to the way increasing flow is implemented.
        if non_lin == 'quad':
            non_linearity = lambda pher, adj, non_lin_params: decision_rules.quad(pher, adj) #non-linearity in decision rule
        elif non_lin == 'slight':
            non_linearity = lambda pher, adj, non_lin_params: decision_rules.slight(pher, adj) #non-linearity in decision rule
        elif non_lin == 'rank_edge':
            non_linearity = lambda pher, adj, non_lin_params: decision_rules.rank_edge(pher, adj, p_val = args.p_val)
        elif non_lin == 'denb':
            k_init = args.k_init
            non_lin_params['k'] = k_init
            non_linearity = lambda pher, adj, non_lin_params: decision_rules.deneubourg(pher, adj, k=non_lin_params['k'])
        
        # if a non-linear rule specified
        if not args.no_nonlin:
            # run dynamics with the non-linear rule w/o leakage/increasing flow
            (pher_final_nonlin_wo, converged_nonlin_wo, non_lin_params) = sim.simulate(adj.copy(), 1*np.ones((1,n)), 1, decay, opt_path, non_linearity, pher.copy(), ff_start, bf_end, thold, print_period, convergence_check_period, max_iter, non_lin_params = non_lin_params, log_path = log_path, print_to_console = args.print_to_console)
            if min_leakage:
                helper.update_array(i, pher_final_nonlin_wo,adj, thold, converged_nonlin_wo, path_val_nonlin_wo_array,  is_path_nonlin_wo_array, converged_nonlin_wo_array, non_linearity, passage, non_lin_params = non_lin_params)
            else:
                helper.update_array(i, pher_final_nonlin_wo,adj, thold, converged_nonlin_wo, path_val_nonlin_wo_array,  is_path_nonlin_wo_array, converged_nonlin_wo_array, non_linearity, non_lin_params = non_lin_params)
                    
            # run dynamics with the non-linear rule with leakage/increasing flow
            non_lin_params['k'] = k_init
            (pher_final_nonlin_with, converged_nonlin_with, non_lin_params) = sim.simulate(adj.copy(), passage.copy(), inc_rate, decay, opt_path, non_linearity, pher.copy(), ff_start, bf_end, thold, print_period, convergence_check_period, max_iter, non_lin_params = non_lin_params, log_path = log_path, print_to_console = args.print_to_console)  
            if min_leakage:
                helper.update_array(i, pher_final_nonlin_with,adj, thold, converged_nonlin_with, path_val_nonlin_with_array,  is_path_nonlin_with_array, converged_nonlin_with_array, non_linearity, passage, non_lin_params = non_lin_params)
            else:
                helper.update_array(i, pher_final_nonlin_with,adj, thold, converged_nonlin_with, path_val_nonlin_with_array,  is_path_nonlin_with_array, converged_nonlin_with_array, non_linearity, non_lin_params = non_lin_params)
        
        #in the case of linear decision rule, we check convergence to the optimum path. For other rules, we check convergence to some path.
        if not args.no_lin:
            # run dynamics with the linear rule with leakage/increasing flow
            non_lin_params['k'] = k_init
            (pher_final_lin_with, converged_lin_with, non_lin_params) = sim.simulate(adj.copy(), passage.copy(), inc_rate, decay, opt_path, lambda pher,adj,non_lin_params : pher, pher.copy(), ff_start, bf_end, thold, print_period, convergence_check_period, max_iter,  converge_to_opt = True, non_lin_params = non_lin_params, log_path = log_path, print_to_console = args.print_to_console)  

            if min_leakage:
                helper.update_array(i, pher_final_lin_with,adj, thold, converged_lin_with, path_val_lin_with_array,  is_path_lin_with_array, converged_lin_with_array, lambda pher,adj,non_lin_params : pher, passage, non_lin_params = non_lin_params)
            else:
                helper.update_array(i, pher_final_lin_with,adj, thold, converged_lin_with, path_val_lin_with_array,  is_path_lin_with_array, converged_lin_with_array, lambda pher,adj,non_lin_params : pher, non_lin_params = non_lin_params)
                
    check_array = converged_nonlin_wo_array*converged_nonlin_with_array*(is_path_nonlin_wo_array==1)*(is_path_nonlin_with_array==1)
        
    return path_val_nonlin_wo_array, path_val_nonlin_with_array, path_val_lin_with_array, converged_nonlin_wo_array, converged_nonlin_with_array, converged_lin_with_array, is_path_nonlin_wo_array, is_path_nonlin_with_array, is_path_lin_with_array,  check_array, opt_path_val_array
        


if __name__ == "__main__":
    
    parser = QuinineArgumentParser(schema=schema)
    args = parser.parse_quinfig()
    
    args.no_nonlin = args.non_lin == 'none'
    
    run_id = str(uuid.uuid4())
    out_dir = os.path.join(args.out_dir, run_id)
    summary_path = os.path.join(args.out_dir, 'summary.txt')
    args.out_dir = out_dir
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(summary_path):
        helper.log_output(f"run id, num instances, num converged opt lin, linear all converged to opt?, num converged nonlin, fraction same nonlin, fraction improved nonlin, mean change nonlin, mean change opt\n",summary_path, False)
    
    with open(os.path.join(out_dir, "config.yaml"), "w") as yaml_file:
        yaml.dump(args.__dict__, yaml_file, default_flow_style=False)
        
    log_path = os.path.join(out_dir,'log.txt')
    helper.log_output(f"Running with: {args}", log_path, args.print_to_console)
    

        
    path_val_nonlin_wo_array, path_val_nonlin_with_array, path_val_lin_with_array, converged_nonlin_wo_array, converged_nonlin_with_array, converged_lin_with_array, is_path_nonlin_wo_array, is_path_nonlin_with_array, is_path_lin_with_array,  check_array, opt_path_val_array  = main(args)
    
    helper.log_output(f"\nTotal number of instances: {args.num_instances}", log_path, args.print_to_console)
    
    

    
    #if we ran for non-linear rule, compare the paths obtained with and without leakage/increasing flow
    if not args.no_nonlin:
        num_converged_nonlin = np.sum(check_array)
        len_mask = min(len(np.where(check_array == 1)[0]), 100)
        if len_mask < 100:
            helper.log_output("Warning: Less than 100 of the instances ran with non-linear rule satisfy the convergence criterion. Run with more number of instances to get more accurate stats of difference in path found with and w/o leakage/increasing flow.", log_path, args.print_to_console)
        mask = np.where(check_array == 1)[0][0:len_mask]
        f_same = np.mean(path_val_nonlin_wo_array[mask] == path_val_nonlin_with_array[mask])
        f_imp = np.mean(path_val_nonlin_wo_array[mask] > path_val_nonlin_with_array[mask])
        f_worse = np.mean(path_val_nonlin_wo_array[mask] < path_val_nonlin_with_array[mask])
        

        
        
        if args.min_leakage:  
            objective_name = "leakage"
            force_name = "leakage"
            path_leakage_nonlin_wo_array = (1-np.exp(-path_val_nonlin_wo_array[mask]))
            path_leakage_nonlin_with_array = (1-np.exp(-path_val_nonlin_with_array[mask]))
            opt_path_leakage_array = (1-np.exp(-opt_path_val_array[mask]))
            mean_change = np.mean((path_leakage_nonlin_with_array - path_leakage_nonlin_wo_array)/path_leakage_nonlin_wo_array)
            mean_change_opt = np.mean((opt_path_leakage_array - path_leakage_nonlin_wo_array)/path_leakage_nonlin_wo_array)
        else:
            objective_name = "length"
            force_name = "inc. flow"
            mean_change = np.mean((path_val_nonlin_with_array[mask] - path_val_nonlin_wo_array[mask])/path_val_nonlin_wo_array[mask])
            mean_change_opt = np.mean((opt_path_val_array[mask] - path_val_nonlin_wo_array[mask])/path_val_nonlin_wo_array[mask])
        
        helper.log_output(f"Number of instances converging to some path with non-linear rule with and without {force_name}: {num_converged_nonlin}", log_path, args.print_to_console)
        helper.log_output(f"Stats for non-linear rule for the first {len_mask} converged instances.", log_path, args.print_to_console)
        helper.log_output(f"Fraction of instances with improved path {objective_name} in the prescence of {force_name} with non-linear rule: {f_imp: .5f}", log_path, args.print_to_console)
        helper.log_output(f"Fraction of instances with the same path {objective_name} in the prescence of {force_name} with non-linear rule: {f_same: .5f}", log_path, args.print_to_console)
        helper.log_output(f"Fraction of instances with worse path {objective_name} in the prescence of {force_name} with non-linear rule: {f_worse: .5f}", log_path, args.print_to_console)
        helper.log_output(f"Mean change in path {objective_name} for non-linear rule compared to the baseline: {mean_change: .5f}", log_path, args.print_to_console)
        helper.log_output(f"Mean change in path {objective_name} for optimum compared to the baseline: {mean_change_opt: .5f}", log_path, args.print_to_console)
    else:
        f_same = "NA"
        f_imp = "NA"
        f_worse = "NA"
        mean_change  = "NA"
        mean_change_opt = "NA"
        num_converged_nonlin = "NA"
        
    #Check for linear rule that all instances converged to the optimum path.
    if not args.no_lin:   
        lin_opt = np.sum(converged_lin_with_array*is_path_lin_with_array)==args.num_instances
        num_converged_lin = np.sum(converged_lin_with_array*is_path_lin_with_array)
        helper.log_output(f"Number of instances converging to the opt path with linear rule: {num_converged_lin}", log_path, args.print_to_console)
        helper.log_output(f"All instances converged to the optimum path with linear rule? {lin_opt}", log_path, args.print_to_console)
    else:
        lin_opt = "NA"
        num_converged_lin = "NA"
    

    if not args.no_nonlin:
        helper.log_output(f"{run_id}, {args.num_instances}, {num_converged_lin}, {lin_opt}, {num_converged_nonlin}, {f_same: .5f}, {f_imp: .5f}, {mean_change: .5f}, {mean_change_opt: .5f}",summary_path, False)
    else:
        helper.log_output(f"{run_id}, {args.num_instances}, {num_converged_lin}, {lin_opt}, {num_converged_nonlin}, {f_same}, {f_imp}, {mean_change}, {mean_change_opt}",summary_path, False)
       
    
        
#    plot.gen_plot(path_val_nonlin_wo_array, path_val_nonlin_with_array, path_val_lin_with_array, check_array, args.min_leakage)