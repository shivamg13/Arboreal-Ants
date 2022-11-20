This repository contains the code for the paper:

**Distributed Algorithms from Arboreal Ants  for the Shortest Path Problem** <br>
*Shivam Garg\*, Kirankumar Shiragur\*, Deborah M. Gordon, Moses Charikar* <br>



## Getting started
You can start by cloning our repository and following the steps below.

1. Install the dependencies for the code.

    ```
    conda create --name ants-are-awesome python=3.9
    conda activate ants-are-awesome
    pip install -r requirements.txt
    ```

2. An example of how to run the simulation for the linear decision rule with the Gnp graph with locality constraint.

    ```
    cd src
    python main.py --config conf/linear/gnp-local_inc-flow.yaml
    
    ```
    
    To run for other graph types or decision rules, change the config file above. For each graph type and decision rule, there is a yaml config file in `src/conf`. To change graph parameters (e.g., n and p in the Gnp graph), edit the corresponding config file.
    

