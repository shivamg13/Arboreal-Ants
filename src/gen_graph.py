import numpy as np
import helper

#with shortest path to be implemented
def g_np(n,p,with_shortest_path = False, with_loop = True):
    adj = (np.random.rand(n,n) < p)+0 #+0 is to change the type from boolean
    if not with_loop:
        adj = np.triu(adj, k=1)
    if with_shortest_path:
        adj = helper.add_random_shortest_path(adj)
    return adj

#edge between i and j only when |i - j| <= win_size
def g_np_local(n,p,win_size,with_shortest_path = False, with_loop = True):
    adj = g_np(n,p,False,with_loop)

    for i in range(n):
        cur_win_size_f = min(win_size,n-i-1);
        cur_win_size_b = min(win_size, i);
        
        if i+cur_win_size_f+1 <= n-1:
            adj[i, i+cur_win_size_f+1:n] = 0;
    
        if i - cur_win_size_b - 1>= 0:
            adj[i, 0:i - cur_win_size_b - 1] = 0;
    
    #Add a unique shortest path
    if with_shortest_path:
        jump_size = np.random.randint(1, win_size)        
        cur_node = 0;
        while cur_node <= n-2:
            next_node = cur_node+ win_size + jump_size ;
            if next_node >= n - win_size -1:
                next_node = n-1;
            adj[cur_node, next_node] = 1;
            cur_node = next_node;

    
    return adj
    

#l is the length of the grid
def grid(l, with_shortest_path = False):
    n = l**2
    adj = np.zeros((n,n))
    for i in range(l):
        for j in range(l):
            if j < l-1:
                adj[i*l+j,i*l+j+1] = 1
            if i < l-1:
                adj[i*l+j,(i+1)*l+j] = 1
    if with_shortest_path:
        adj = helper.add_random_shortest_path(adj, k = np.random.randint(int(0.9*l),int(1.2*l)))
    return adj
