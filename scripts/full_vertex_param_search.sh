#!/bin/bash


# 
# This file will allow us to loop through the different hyperparameter spaces
# and run the vertex_param_search.sh to optimize
#


# set directory
cd "$(dirname "$0")"


# search spaces
vtx_aggr=("lstm")
vtx_lstm_features=(2 4 8 16 32)
#vtx_mlp_features=(2 4 8 16 32)
vtx_mlp_features=(2 4 16 32)


# loop through parameters in search spaces
for fxn in "${vtx_aggr[@]}"; do

    for mlp_feat in "${vtx_mlp_features[@]}"; do

        if [ "$fxn" == "lstm" ]; then
            for lstm_feat in "${vtx_lstm_features[@]}"; do
                args=("$fxn" "$mlp_feat" "$lstm_feat")
                # Change out script call here
                /bin/bash vertex_param_search.sh "${args[@]}"
                # sbatch vertex_param_search.sh "${args[@]}"
            done
        else
            args=("$fxn" "$mlp_feat")
            # Change out script call here
            /bin/bash vertex_param_search.sh "${args[@]}"
            # sbatch vertex_param_search.sh "${args[@]}"
        fi

    done

done
