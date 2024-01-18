These instructions are specifically for students working on the NuGraph(2) project via the Data Science Institute, in which case Fermilab setup processes are not directly applicable.


# Environmental Setup

Make sure that you have set up 1, 2, 3, and 6 under the [computer setup guide](https://github.com/dsi-clinic/coding-standards/blob/main/docs/tutorials/clinic-computer-setup.md).
One thing to note is how [Github manages personal tokens](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) during the setup.

Next, follow the [SLURM instructions](https://github.com/dsi-clinic/coding-standards/blob/main/docs/tutorials/slurm.md) through part VI. It may very well be the case that the `miniconda` installation in part VI may not work. In this case, one should use `curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"`, followed by `bash Miniforge3-$(uname)-$(uname -m).sh` verbatim.

At this point, it would be advantageus to set up a `CUDA` environment with the necessary dependencies. The `README` for the repository provides instructions using `mamba`. However, for reasons unbeknownst to us, it seems that using `mamba` on the DSI cluster prevents the model training scripts from running properly on the interactive nodes. It often prevents the `i` and `j` nodes from being accessed, so the `bash` scripts will run in the login node. Even if it reaches an interactive node, i.e. a `g` node, reading the `.err` files for the trained model shows `GPU available: false, used: False`, so the node seems unable to reach an accessible GPU. Remarkably, using a `conda` environment does not encounter these issues. In this folder, there is a `YAML` file with the environmental setup. Run `conda env create -f environment.yml`. This will create a `NuGraph` environment, which can be activated with `conda activate NuGraph`.

Note: The CUDA version of different DSI cluster nodes may change from time to time. If you are sure that the job has been successfully submitted to a computing node with available GPU resources and that there is no error in the code (errors in the code may result in the job intended for a computing node to be pushed back to the login node, so check where your jobs are running by typing `squeue -u [USERNAME]` in command line – if it is running on the computing node, you should see the job listed in the outputs; if it is running on the login node, however, you will not see your job listed in the outputs, and the automatically generated `events.out.tfevents.[...]` file will contain the name of the login node, e.g., `fe01`), but keep getting `GPU available: False, used: False` in the `.err` log and extremely long estimated training time in the `.out` log (e.g., 80 hours per epoch), it is likely that a CUDA version incompatibility between the computing node and the NuGraph module disabled the use of GPU. In that case, try submitting the job again by explicitly specifying another computing node with `#SBATCH --nodelist=[NODENAME]` in the bash script. If the script is correctly running on GPU, you are supposed to get `GPU available: True (cuda), used: True` in the `.err` log.


# Where Things Are

- Data and DSI specific information stored in `~/net/projects/fermi-2`
- Fermi specific model and code stored in `~/NuGraph` (which you will be cloning from GitHub into your home folder)


# Interacting with SLURM

Transferring files in an out of the cluster/local computer
- Open Terminal on local computer
- Run: `scp local/path/to/file remote_host:path/to/remote/folder`
    - Switch folder order if transferring from remote to local
    - Example: `scp ~/Desktop/filename.csv fe01.ds.uchicago.edu:/net/projects/fermi-2`
- If you wish to transport directories, use `scp -r`


# Running Hyperparameter Search

- Start from the login node (`fe01`)
- Activate environment (`conda activate NuGraph`)
- cd to `~/NuGraph`
- Modify params in `train_batch_dsi.sh` as needed
- In command line, run: `sbatch scripts/train_batch_dsi.sh`
- Record your job number and check that the job is running correctly (e.g., you are seeing the process bars in the `.out` log). In cases where the job is resumed from a checkpoint file, it may take several minutes on the GPU cluster for the loading process to be completed.
- To cancel runs in the middle: `scancel [job number]`


# TensorBoard

- In command line: `tensorboard --port [XXXX] --bind_all --logdir /net/projects/fermi-2/logs --samples_per_plugin 'images=200'` -- insert random numbers for `[XXXX]` which you think no one else will use.
- Copy and paste the created link into a web browser to view results.



