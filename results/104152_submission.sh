#!/bin/bash

# Parameters
#SBATCH --error=/home/shangao/NuGraph/results/%j_0_log.err
#SBATCH --gres=gpu:1
#SBATCH --job-name=sample
#SBATCH --mem-per-cpu=16000
#SBATCH --nodes=1
#SBATCH --open-mode=append
#SBATCH --output=/home/shangao/NuGraph/results/%j_0_log.out
#SBATCH --partition=general
#SBATCH --signal=USR2@90
#SBATCH --time=60:00
#SBATCH --wckey=submitit

# command
export SUBMITIT_EXECUTOR=slurm
srun --unbuffered --output /home/shangao/NuGraph/results/%j_%t_log.out --error /home/shangao/NuGraph/results/%j_%t_log.err /home/shangao/miniconda3/envs/NuGraph/bin/python -u -m submitit.core._submit /home/shangao/NuGraph/results
