from pathlib import Path
import submitit
import subprocess

# your actual code will have more and longer functions than this sample
##def get_mean_amount_after_year(path_to_csv: str, earliest_year: int):
##    """ Return mean value of 'amount' column with year > earliest_year """
##    df = pd.read_csv(path_to_csv)
##    df = df[df["year"] > earliest_year]
##    return df["amount"].mean()

def run_vertex_decoder_search():
    subprocess.call(['bash', 'full_vertex_param_search.sh'], shell=True)
        # apparently shell=True can be a security risk if using external
        # inputs, but we are not in this case

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
    # save query parameters to variables. if you want a default, better to put
    # at the outermost call to a function.
    #path_to_data = query.get("path_to_data")
    ##default_earliest_year = 2005
    ##earliest_year = query.get("earliest_year", default_earliest_year)

    output_directory = Path("results").resolve()
    executor = submitit.AutoExecutor(folder=output_directory)
    # here we unpack the query dictionary and pull any slurm commands that 
    # are in 'slurm' key. For more info on the ** syntax, see:
    # https://stackoverflow.com/a/36908. The slurm options here are the same
    # as those you use on the command line but instead of prepending with '--'
    # we prepend with 'slurm_'
    executor.update_parameters(**query.get("slurm", {}))

    # if submitit is true in our query json, we'll use submitit
    # if query.get("submitit", False):
    #     executor.submit(
    #         get_mean_amount_after_year,
    #         path_to_csv,
    #         earliest_year,
    #     )
    # else:
    #     get_mean_amount_after_year(
    #         path_to_csv,
    #         earliest_year,
    #     )

    # Kate code
    if query.get("submitit", False):
        executor.submit(
            run_vertex_decoder_search()
        )
    else:
        run_vertex_decoder_search()
    