"""
This file will perform a bayesian optimization hyperparameter selection for
the vertex_param_search.sh file. This may avert having to run so may 
hyperparameters and save time. 

Authors: Kate Habich, Rohan Mehta
"""
import numpy as np
import matplotlib.pyplot as plt
from skopt import gp_minimize
from skopt.space import Real, Integer, Categorical
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import subprocess
import os
import glob

def run_bayesian_search():
    '''
    Performs bayesian optimization search for train and validation models.

    Returns (list containing below):
        best_X: optimal set of hyperparameters
        best_y: accuracy achieved with these model hyperparameters
    '''
    parameter_space = [
        Real(0, 10, name = 'vtx_aggr'),
        Real(0, 10, name = 'vtx_lstm_features'),
        Real(0, 10, name = 'vtx_mlp_features')
        ]
    
    # Function model
    model = model_function

    # run optimizer to find optimal parameter set
    decoded_param_space = param_space_decoder(parameter_space)
    
    optimize_model(model, parameter_space)
    single_set_outcome = optimize_model(model,
                   parameter_space)
    (all_X, all_y), (best_X, best_y) = single_set_outcome
    perc_accuracy = all_y * -100

    calls = np.linspace(1, 10, 10)
    best_yet_y = []
    points = [[] for _ in range(10)]

    for i, yi in enumerate(perc_accuracy):
        if best_yet_y:
            if yi > max(best_yet_y):
                best_yet_y.append(yi)
                points[i].append(yi)
            else:
                best_yet_y.append(max(best_yet_y))
                points[i].append(max(best_yet_y))
        else:
            best_yet_y.append(yi)
            points[i].append(yi)

    visualize_optimization(calls, all_y, best_yet_y)
    
    return (best_X, best_y)

# TODO Change this if necessary; matched to submitit_script.py's logdir

def get_bash_username():
    # Get the user's USERNAME
    username = os.environ.get('USER')
    if username is None:
        sys.exit('ERROR: USER variable is not set.')
    return username

username = get_bash_username()
folder = '../../../../net/projects/fermi-gnn/logs/' + username

def find_latest_file(folder):
    '''
    Finds the path to the most recent metric log to deal with
    multiple iterations.
    '''
    files=glob.glob(os.path.join(folder, '*'))
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def extract_vertex_resolution(folder):
    '''
    Extracts the value of vertex_resolution on the test data.
    This can also be modified to include the validation.
    '''
    latest_log = find_latest_file(folder)
    ea = event_accumulator.EventAccumulator(latest_log)
    ea.Reload()
    vertex_resolution = ea.Scalars('vertex_resolution/test')[-1].value
    return vertex_resolution

def model_function(encoded_parameters):
    '''
    Objective function for minimization. Converts decoded parameter space
    to form compatible with bash command and calls the vertex_param_search.sh
    script. Returns -1 * vertex_resolution.
    '''
    decoded_params = param_space_decoder(encoded_parameters)
    # Convert dictionary -> string for bash command
    parameters_str = ' '.join(f" --{key} {value}" for key, value in decoded_params.items())
    # TODO: Change if needed to call a different script
    bash_cmd = f"bash vertex_param_search.sh {parameters_str}"
    subprocess.run(bash_cmd, shell=True)
    metric = extract_vertex_resolution(folder)
    return -metric 


def param_space_decoder(parameters):
    '''
    Turns bayesian parameter space (0-10) into hyperparameter values which 
    are readable to the model, while preserving an evenly spaced selection.

    Inputs:
        parameters (list): 

    Returns (dict): 
    '''
    d = {
            'vtx_aggr': None,
            'vtx_lstm_features': None,
            'vtx_mlp_features': None
        }
    
    vtx_aggr, vtx_lstm_features, vtx_mlp_features = parameters

    # aggregator function 
    # TODO: CHANGE if more aggregation functions added
    if vtx_aggr <= 10:
        d['vtx_aggr'] = "lstm"

    # number of LSTM features
    if vtx_lstm_features < 2:
        d['vtx_lstm_features'] = 2
    elif (vtx_lstm_features >= 2) & (vtx_lstm_features < 4):
        d['vtx_lstm_features'] = 4
    elif (vtx_lstm_features >= 4) & (vtx_lstm_features < 6):
        d['vtx_lstm_features'] = 8
    elif (vtx_lstm_features >= 6) & (vtx_lstm_features < 8):
        d['vtx_lstm_features'] = 16
    else:
        d['vtx_lstm_features'] = 32

    # number of MLP features
    if vtx_mlp_features < 2:
        d['vtx_mlp_features'] = 2
    elif (vtx_mlp_features >= 2) & (vtx_mlp_features < 4):
        d['vtx_mlp_features'] = 4
    elif (vtx_mlp_features >= 4) & (vtx_mlp_features < 6):
        d['vtx_mlp_features'] = 8
    elif (vtx_mlp_features >= 6) & (vtx_mlp_features < 8):
        d['vtx_mlp_features'] = 16
    else:
        d['vtx_mlp_features'] = 32

    return d
    

def optimize_model(model, parameter_space):
    '''
    Chooses model parameters to run next based on bayesian optimizer.

    Inputs:
        model: vertex training and validation runs to retrieve accuracy
        parameter_space (dict): undecoded parameter names keyed to value 0-10

    Return (list containing below): 
        rf_opt.x_iters: parameters chosen
        rf_opt.func_vals: success rate of each parameter set choice
        rf_opt.x: optimal parameter set chosen
        rf_opt.fun: success rate of optimal parameter
    '''
    n_test_points = 0
    n_learning_points = 10
    rf_opt = gp_minimize(
        model,
        dimensions = parameter_space,
        # args=(split),
        # gp_hedge randomly picks from LCB, EI, PI acquisitions at each iteration
        acq_func = "gp_hedge",
        n_calls = n_learning_points + n_test_points,
        n_initial_points = n_test_points,
        random_state = 60615
        )
    
    return ((rf_opt.x_iters, rf_opt.func_vals), (rf_opt.x, rf_opt.fun))


def visualize_optimization(calls, all_accuracies, best_yet_accuracy):
    '''
    Visualize the convergence of the bayesian optimizer

    Inputs:
        calls (list): sequential number of calls made at each accuracy
        all_accuracies (list): accuracy returned at each call
        best_yes_accuracy (list): maximum accuracy yet found by the model
    '''
    perc_accuracy = all_accuracies * -100

    plt.figure(figsize = (5,3))
    plt.plot(calls, best_yet_accuracy)
    plt.plot(calls, perc_accuracy,
            alpha = 0.3,
            color = 'orange')
    # plt.axhline(100, 
    #             linestyle = "--", 
    #             color = "blue")
    plt.axvline(10, 
                linestyle = "--", 
                color = "gray")
    plt.ylim(min(perc_accuracy), 101)
    plt.title(f"Vertex Optimizer Convergence")
    plt.show()
