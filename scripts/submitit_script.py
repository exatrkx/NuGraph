from pathlib import Path
import submitit
import subprocess


# your actual code will have more and longer functions than this sample
def run_vertex_decoder_search():

    print('run_vertex_decoder_search called')
    
    # call bash script
    # with open('scripts/full_vertex_param_search.sh', 'r') as file:
    #     script = file.read()
    # subprocess.call(script, shell=True)

    subprocess.call("scripts/full_vertex_param_search.sh")

    print('bash script run')


if __name__ == "__main__":

    import argparse
    import json

    # set up command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query", help="path to json file containing query", default=None
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
    with open(query_path) as f:
        query = json.load(f)

    # instantiate executor
    executor = submitit.AutoExecutor(folder='../../../../net/projects/fermi-2/logs/')
    executor.update_parameters(**query.get("slurm", {}))

    # if submitit is true in our query json, we'll use submitit
    if query.get("submitit", True):
        print("submitit true")
        executor.submit(
            run_vertex_decoder_search()
        )
    else:
        print("submitit false")
        run_vertex_decoder_search()
    