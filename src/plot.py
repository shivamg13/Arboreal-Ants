import matplotlib.pyplot as plt
import numpy as np



#color = [0, 0.4470, 0.7410]
#color = [0.4660, 0.6740, 0.1880]
#color = [0.9290, 0.6940, 0.1250]

def gen_plot(path_length_array, path_length_inc_array, path_length_lin_array, check_array, min_leakage):
    plt.rcParams['axes.edgecolor']='#333F4B'
    plt.rcParams['axes.linewidth']=0.8
    plt.rcParams['xtick.color']='#333F4B'
    plt.rcParams['ytick.color']='#333F4B'
    plt.rcParams.update({'font.size': 28})
    
    num_instances = 30
    mask = np.where(check_array == 1)[0][0:num_instances]
    
    if not min_leakage:
        l1 = "non-lin. rule const. flow."
        l2 = "non-lin. rule inc. flow."
        l3 = "lin. rule inc. flow."
        l4 = "Path length"
        
        plt.bar(range(0,num_instances),path_length_array[mask], color='#dce6f2', edgecolor='#c3d5e8',  width = 0.95, align='center', label = l1)
        plt.bar(range(0,num_instances),path_length_inc_array[mask], color= '#ffc001', edgecolor='#c3d5e8', width = 0.7, alpha = 0.75, align = 'center', label = l2)
        plt.bar(range(0,num_instances),path_length_lin_array[mask], color = [0.4660, 0.6740, 0.1880] , edgecolor='#c3d5e8', width = 0.3, alpha = 0.75, align = 'center', label = l3)
    
    else:
        l1 = "non-lin. rule w/o leak."
        l2 = "non-lin. rule with leak."
        l3 = "lin. rule with leak."
        l4 = "Path leakage"
        leakage_array = (1-np.exp(-path_length_array))
        leakage_inc_array = (1-np.exp(-path_length_inc_array))
        leakage_lin_array = (1-np.exp(-path_length_lin_array))
        
        plt.bar(range(0,num_instances),leakage_array[mask], color='#dce6f2', edgecolor='#c3d5e8',  width = 0.95, align='center', label = l1)
        plt.bar(range(0,num_instances),leakage_inc_array[mask], color= '#ffc001', edgecolor='#c3d5e8', width = 0.7, alpha = 0.75, align = 'center', label = l2)
        plt.bar(range(0,num_instances),leakage_lin_array[mask], color = [0.4660, 0.6740, 0.1880] , edgecolor='#c3d5e8', width = 0.3, alpha = 0.75, align = 'center', label = l3)
            
    ax = plt.axes()
    ax.set_facecolor("white")
    #if min_leakage:
    #    ax.set_yscale('log')
    
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    
    ax = plt.gca()
    ax.set_xlim([-0.5,num_instances])
    if min_leakage:
        ax.set_ylim([0,1.05*np.max(leakage_array[mask])])
    else:
        ax.set_ylim([0,1.01*np.max(path_length_array[mask])])
    
    plt.xlabel("Graph Instances")
    plt.ylabel(l4)      
    plt.legend(loc='lower right', facecolor = 'white', prop={"size":24})
    plt.margins(0,0)
    plt.show()