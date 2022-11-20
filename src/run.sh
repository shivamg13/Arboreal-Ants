#!/bin/bash

#Linear Rule
python main.py --config conf/linear/gnp-local_inc-flow.yaml --print_to_console False
python main.py --config conf/linear/gnp-local_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/linear/gnp-local_inc-flow.yaml --random_init True --print_to_console False
python main.py --config conf/linear/gnp-local_inc-flow_with_loop.yaml --random_init True --print_to_console False

python main.py --config conf/linear/gnp-local_leakage.yaml --print_to_console False
python main.py --config conf/linear/gnp-local_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/linear/gnp-local_leakage.yaml --random_init True --print_to_console False
python main.py --config conf/linear/gnp-local_leakage_with_loop.yaml --random_init True --print_to_console False

python main.py --config conf/linear/gnp_inc-flow.yaml --print_to_console False
python main.py --config conf/linear/gnp_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/linear/gnp_inc-flow.yaml --random_init True --print_to_console False
python main.py --config conf/linear/gnp_inc-flow_with_loop.yaml --random_init True --print_to_console False

python main.py --config conf/linear/gnp_leakage.yaml --print_to_console False
python main.py --config conf/linear/gnp_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/linear/gnp_leakage.yaml --random_init True --print_to_console False
python main.py --config conf/linear/gnp_leakage_with_loop.yaml --random_init True --print_to_console False

python main.py --config conf/linear/grid_inc-flow.yaml --print_to_console False
python main.py --config conf/linear/grid_inc-flow.yaml --random_init True --print_to_console False

python main.py --config conf/linear/grid_leakage.yaml --print_to_console False
python main.py --config conf/linear/grid_leakage.yaml --random_init True --print_to_console False

#Nonlinear Rule
python main.py --config conf/non-linear/quad/grid_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp-local_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp-local_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp-local_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/quad/gnp-local_inc-flow.yaml --print_to_console False

python main.py --config conf/non-linear/slight/grid_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp-local_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp-local_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp-local_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/slight/gnp-local_inc-flow.yaml --print_to_console False

python main.py --config conf/non-linear/denb/grid_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp-local_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp-local_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp-local_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/denb/gnp-local_inc-flow.yaml --print_to_console False

python main.py --config conf/non-linear/rank_edge/grid_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp_inc-flow.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp-local_leakage_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp-local_leakage.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp-local_inc-flow_with_loop.yaml --print_to_console False
python main.py --config conf/non-linear/rank_edge/gnp-local_inc-flow.yaml --print_to_console False