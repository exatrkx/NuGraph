# Request space on the SLURM (prior to run)
#srun -p general -t 60:00 --mem 1000  –pty /bin/bash

# pull in passed arguments
args=("$@")
vtx_aggr=${args[0]}
vtx_mlp_features=${args[1]}

if [ ${#args[@]} == 3 ]; then
    vtx_lstm_features=$args[2]
    log_name="log_aggr_${vtx_aggr}_mlpfeats_${vtx_mlp_features}_lstmfeats_${vtx_lstm_features}"

else
    log_name="log_aggr_${vtx_aggr}_mlpfeats_${vtx_mlp_features}"
fi

# set variables
lim_train_batches=8
lim_val_batches=2
epochs=3


# set directory
cd "$(dirname "$0")"

# run training
python train.py \
                 --data-path /net/projects/fermi-2/CHEP2023.gnn.h5 \
                 --logdir ../../../../net/projects/fermi-2/logs/ \
                 --name  "Vertex_Decoder_Search"\
                 --version ${log_name} \
                 --semantic \
                 --filter \
                 --vertex \
                 --limit_train_batches ${lim_train_batches}\
                 --limit_val_batches ${lim_val_batches}\
                 --vertex-aggr ${vtx_aggr} \
                 --vertex-lstm-feats ${vtx_lstm_features} \
                 --vertex-mlp-feats ${vtx_mlp_features} \
                 --num_nodes 4 \
                 --epochs ${epochs}