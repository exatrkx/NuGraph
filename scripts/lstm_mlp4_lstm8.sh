#!/bin/bash

# srun -p general -t "12:00:00" --mem "64G" --cpus-per-task 2 --gres gpu:1 --constraint a100 --pty /bin/bash


# make logdir under username
username=$USER
logdir="../../../../net/projects/fermi-2/logs/$username"
mkdir -p "$logdir"
echo $logdir


# aggregator
vtx_aggr="lstm"

# mlp features
vtx_mlp_features=4

# lstm features
vtx_lstm_features=8
log_name="log_aggr_${vtx_aggr}_mlpfeats_${vtx_mlp_features}_lstmfeats_${vtx_lstm_features}"


# set variables
epochs=80 #CHANGE


# set directory
cd "$(dirname "$0")"


# run training
python train.py \
                 --data-path /net/projects/fermi-2/CHEP2023.gnn.h5 \
                 --resume "${logdir}/Vertex_Decoder_Search/${log_name}/checkpoints/epoch=14-step=70395.ckpt" \
                 --version ${log_name} \
                 --semantic \
                 --filter \
                 --vertex \
                 --vertex-aggr ${vtx_aggr} \
                 --vertex-lstm-feats ${vtx_lstm_features} \
                 --vertex-mlp-feats ${vtx_mlp_features} \
                 --epochs ${epochs}
                #  --logdir ${logdir} \
                #  --name  "Vertex_Decoder_Search"\
                #  --limit_train_batches 500
                #  --limit_val_batches 2\
                #  --num_nodes 4 \

