from pathlib import Path
import submitit
import subprocess


# your actual code will have more and longer functions than this sample
def run_vertex_decoder_search(script_path = "scripts/full_vertex_param_search.sh"):

    print('run_vertex_decoder_search called')
    
    # call bash script

    # with open('scripts/full_vertex_param_search.sh', 'r') as file:
    #     script = file.read()
    # subprocess.call(script, shell=True)

    # use /bin/bash shell interpreter, so that our sh script does not bug
    # need to make sh script executable before running (chmod +x SCRIPT_PATH)
    subprocess.call(['chmod', '+x', script_path])
    subprocess.call(script_path)  

    print('bash script run')


if __name__ == "__main__":

    import argparse
    import json

    # set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query", help="path to json file containing query", default='scripts/slurm.JSON'
    )
    args = parser.parse_args()
    
    # read in query
    if Path(args.query).resolve().exists():
        query_path = Path(args.query).resolve()
    else:
        # throw
        raise ValueError(
            f"Could not locate {args.query} in query directory or as absolute path"
        )
    
    # load queried arguments from JSON
    with open(query_path) as f:
        query = json.load(f)

    # instantiate executor & update params
    executor = submitit.AutoExecutor(folder='../../../../net/projects/fermi-2/logs/')
    executor.update_parameters(**query.get("slurm", {}))

    # if submitit is true in our query json, we'll use submitit
    if query.get("submitit", True):
        print("submitit true")
        executor.submit(
            run_vertex_decoder_search()
        )
    # otherwise, call function directly
    else:
        print("submitit false")
        run_vertex_decoder_search()
    