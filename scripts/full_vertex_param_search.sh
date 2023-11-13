# 
# This file will allow us to loop through the different hyperparameter spaces
# and run the vertex_param_search.sh to optimize
#

# Search spaces
vtx_aggr=(“lstm”)
vtx_lstm_features=(2 4 8 16 32)
vtx_mlp_features=(2 4 8 16 32)

for fxn in ${vtx_aggr[@]}; do
    for mlp_feat in ${vtx_mlp_features[@]}; do
        if [ "$fxn" == "lstm" ]; then
            for lstm_feat in ${vtx_lstm_features[@]}; do
                args=("$fxn" "$mlp_feat" "$lstm_feat")
               
        else
            args=("$fxn" "$mlp_feat")
        fi
            
        ./vertex_param_search "${$args[@]}"
    done
done
