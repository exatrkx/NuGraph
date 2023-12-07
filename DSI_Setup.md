These instructions are specifically for students working on the NuGraph(2) project via the Data Science Institute, in which case Fermilab setup processes are not directly applicable.

# Environmental Setup

Make sure that you have set up 1, 2, 3, and 6 under the [computer setup guide](https://github.com/dsi-clinic/coding-standards/blob/main/docs/tutorials/clinic-computer-setup.md).
One thing to note is how [Github manages personal tokens](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) during the setup.

Next, follow the [SLURM instructions](https://github.com/dsi-clinic/coding-standards/blob/main/docs/tutorials/slurm.md) through part VI. It may very well be the case that the `miniconda` installation in part VI may not work. In this case, one should use `curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"`, followed by `bash Miniforge3-$(uname)-$(uname -m).sh` verbatim.

At this point, it would be advantageus to set up a `CUDA` environment with the necessary dependencies. The `README` for the repository provides instructions using `mamba`. However, for reasons unbeknownst to us, it seems that using `mamba` on the DSI cluster prevents the model training scripts from running properly on the interactive nodes. It often prevents the `i` and `j` nodes from being accessed, so the `bash` scripts will run in the login node. Even if it reaches an interactive node, i.e. a `g` node, reading the `.err` files for the trained model shows `GPU available: false, used: False`, so the node seems unable to reach an accessible GPU. Remarkably, using a `conda` environment does not encounter these issues. In this folder, there is a `YAML` file with the environmental setup. Run `conda env create -f environment.yml`. This will create a `numl` environment, which can be activated with `conda activate numl`.

# Interacting with SLURM

Ideally, Submitit would be a more sophisticated way to run scripts, but it would often lead to a non-computational node being used. Thus, a script could be initiated from an interactive node and yet run on the login node when queued via Submitit. As such, `sbatch` was used. 

...
