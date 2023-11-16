#!/bin/bash

#SBATCH --job-name=fermi2
#SBATCH --output=dsi_log/fermi2.out
#SBATCH --error=dsi_log/fermi2.err
#SBATCH --time=12:00:00
#SBATCH --partition=general
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=12
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=ALL  # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=jiheeyou@rcc.uchicago.edu  # mail notification for the job

srun python train.py --data-path /net/projects/fermi-2/CHEP2023.gnn.h5 --logdir /home/jiheeyou/NuGraph/scripts/dsi_log --name fermi2 --version semantic-filter --semantic --filter
