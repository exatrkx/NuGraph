#!/bin/bash
#SBATCH --job-name=fermi2
#SBATCH --output=/net/projects/fermi-2/logs/%A_%a.out
#SBATCH --error=/net/projects/fermi-2/logs/%A_%a.err
#SBATCH --time=12:00:00
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --constraint=a100
#SBATCH --mem-per-cpu=64G



# call this script in command line with:
# sbatch scripts/train_batch_dsi.sh

# or to run interactively, request session with:
# srun -p general -t "12:00:00" --mem "64G" --cpus-per-task 2 --gres gpu:1 --constraint a100 --pty /bin/bash



################ CHANGE ################
# mlp features
vtx_mlp_features=128

# aggregator
vtx_aggr="lstm"

# lstm features
vtx_lstm_features=8

# set variables
epochs=80 

# don't forget to also update the arguments of the python script call below: it should contain with (--logdir & --name) OR (--resume)
# ckpt="epoch=57-step=272194.ckpt"
#########################################


# make logdir under username
username=$USER
logdir="/net/projects/fermi-2/logs/${username}"
mkdir -p "$logdir"
echo $logdir


# set log_name with specified parameters
log_name="log_aggr_${vtx_aggr}_mlpfeats_${vtx_mlp_features}_lstmfeats_${vtx_lstm_features}"


# run training
srun python scripts/train.py \
                 --data-path /net/projects/fermi-2/CHEP2023.gnn.h5 \
                 --version ${log_name} \
                 --semantic \
                 --filter \
                 --vertex \
                 --vertex-aggr ${vtx_aggr} \
                 --vertex-lstm-feats ${vtx_lstm_features} \
                 --vertex-mlp-feats ${vtx_mlp_features} \
                 --epochs ${epochs} \
                 --logdir ${logdir} \
                 --name  "Vertex_Decoder_Search"\
                #  --resume "${logdir}/Vertex_Decoder_Search/${log_name}/checkpoints/${ckpt}" \
                #  --limit_train_batches ${lim_train_batches}\
                #  --limit_val_batches ${lim_val_batches}\
                #  --num_nodes 4 \
