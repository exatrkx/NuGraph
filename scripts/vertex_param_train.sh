echo "woo!"

# print working directory
pwd

# Request space on the SLURM
# srun -p general -t 60:00 --mem 10  --pty /bin/bash
# srun -p general --gres=gpu:1 --pty --mem 1000 -t 90:00 /bin/bash
srun --pty  --partition=general --mem=16G --time=2:00:00 /bin/bash
# source activate NuGraph
echo "soo!"

# set variables
vtx_aggr=“lstm”
vtx_lstm_features=8
vtx_mlp_features=8
lim_train_batches=8
lim_val_batches=2

# set file name
log_name=“log_aggr_${vtx_aggr}_lstmfeats_${vtx_lstm_features}_mlpfeats_${vtx_mlp_features}”

# set directory
cd "$(dirname "$0")"
# pwd
echo "boo!"

# run training
# data-path directory should be relative to H5DataModule.py
python train.py \
                 --data-path /net/projects/fermi-2/CHEP2023.gnn.h5 \
                 --logdir ../../../../net/projects/fermi-2/logs/ --name ${log_name} \
                 --version semantic-filter-vertex \
                 --semantic --filter --vertex \
                 --limit_train_batches ${lim_train_batches}\
                 --limit_val_batches ${lim_val_batches}\
                 --vertex-aggr ${vtx_aggr} \
                 --vertex-lstm-feats ${vtx_lstm_features} \
                 --vertex-mlp-feats ${vtx_mlp_features}

echo "foo!"
