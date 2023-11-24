#!/bin/bash


# srun -p general -t "12:00:00" --mem "64G" --cpus-per-task 2 --gres gpu:1 --constraint a100 --pty /bin/bash
# srun -p general -t "12:00:00" --mem "64G" --cpus-per-task 4 --gres gpu:2 --constraint a100 --pty /bin/bash
# scontrol update jobid=<job_id> TimeLimit=+<new_timelimit>


# source ~/miniconda3/etc/profile.d/conda.sh
# conda activate NuGraph

# source ~/miniconda3/bin/activate


# make logdir under username
username=$USER
logdir="../../../../net/projects/fermi-2/logs/$username"
mkdir -p "$logdir"
echo $logdir


# aggregator
vtx_aggr="lstm"

# mlp features
vtx_mlp_features=2

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
                 --resume "${logdir}/Vertex_Decoder_Search/${log_name}/checkpoints/epoch=27-step=131404.ckpt" \
                 --version ${log_name} \
                 --semantic \
                 --filter \
                 --vertex \
                 --vertex-aggr ${vtx_aggr} \
                 --vertex-lstm-feats ${vtx_lstm_features} \
                 --vertex-mlp-feats ${vtx_mlp_features} \
                 --epochs ${epochs} 
                #  --logdir ${logdir} \
                #  --name  "Vertex_Decoder_Search"      
                #  --limit_train_batches ${lim_train_batches}\
                #  --limit_val_batches ${lim_val_batches}\
                #  --num_nodes 4 \

