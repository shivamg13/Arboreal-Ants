from quinine import (
    tstring,
    tinteger,
    tfloat,
    tboolean,
    stdict,
    tdict,
    default,
    required,
    allowed,
    nullable,
)
from funcy import merge




schema = {
    "num_instances": merge(tinteger, default(200)),
    #number of instances
    
    "start_seed": merge(tinteger, default(0)),
    #seed number from where to start iterating
    
    "min_leakage": merge(tboolean, default(False)),
    #test for convergence with leakage and constant flow. default is increasing flow and no leakage
    
    "random_init": merge(tboolean, default(False)),
    #initialize pheromone levels randomly. default is uniform pheromone level on all edges
    
    "non_lin": merge(tstring, default('none'), allowed(['quad', 'denb', 'rank_edge', 'slight', 'none'])),
    #type of non_linearity. if 'none' is specified, code only runs for linear decision rule.
    
    "k_init": merge(tfloat, default(0)),
    #parameter for denb non-linearity
    
    "p_val": merge(tfloat, default(0.01)),
    #parameter for rankedge non-linearity
    
    "graph_type": merge(tstring, default('gnp_local'), allowed(['grid', 'gnp', 'gnp_local'])),
    #type of graph
    
    "num_nodes": merge(tinteger, default(100)),
    #number of vertices in the graph. should be a perfect square for grid graph
    
    "p_graph": merge(tfloat, default(0.5)),
    #parameter p for gnp and gnp_local graph
    
    "win_size": merge(tinteger, default(10)),
    #window size for gnp_local graph
    
    "with_loop": merge(tboolean, default(False)),
    #allow edges from higher number node to lower number node (only for gnp and gnp_local)
    
    "print_period": merge(tinteger, default(100)),
    #number of iterations after which the normalized pheromone level on the optimum path are printed
    
    "convergence_check_period": merge(tinteger, default(100)),
    #number of iterations after which we check for convergence
    
    "max_iter": merge(tinteger, default(500000000)),
    #maximum number of iterations
    
    "conv_thold": merge(tfloat, default(0.99)),
    #convergence threshold
    
    "decay": merge(tfloat, default(0.9)),
    #pheromone decay parameter
    
    "no_lin": merge(tboolean, default(False)),
    #do not run for the linear rule. specify a non-linear rule in this case. when no_lin is False and a non-linear rule is also specified, then each instance is run with both the linear as well as the speficied non-linear rule
    
    "out_dir": merge(tstring, required),
    #directory where logs and summary of runs in saved
    
    "print_to_console": merge(tboolean, default(True)),
    #whether to print the log in the console
}