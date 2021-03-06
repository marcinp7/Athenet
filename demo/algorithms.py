"""
    Runs chosen algorithm on chosen type of network and prints results.
    With -p flag displays results on the plot.
    By default runs simple_neuron_deleter algorithm on LeNet network on one
    configuration case.

    More information with -h option.
"""


import argparse
import sys
from argparse import RawTextHelpFormatter

from config.algorithm import algorithms, get_network, ok,\
    get_file_name
from config.datasets import datasets
from athenet.utils import run_algorithm, plot_2d_results

parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                 description="Runs chosen algorithm on chosen "
                                 "type of network and prints results.")

parser.add_argument("-a", "--algorithm",
                    help="Chooses algorithm of which result will be "
                         "demonstrated. Meaning of shortcuts "
                         "(shortcut: called function):\n"
                         " * sender: simple_neuron_deleter (default)\n"
                         " * sender2: simple_neuron_deleter2\n"
                         " * rat: sparsify_smallest_on_network\n"
                         " * rat2: sparsify_smallest_on_layers\n"
                         " * filters: sharpen_filters\n"
                         " * derest: derest",
                    choices=["sender", "sender2", "rat", "rat2", "filters",
                             "derest"],
                    default="sender")

parser.add_argument("-n", "--network",
                    help="Algorithm will be ran on chosen kind of network. "
                         "Default option is \"lenet\".",
                    choices=["lenet", "alexnet", "googlenet"],
                    default="lenet")

parser.add_argument("-p", "--plot",
                    help="When this option is added results will be displayed"
                         " on the plot.",
                    action="store_true")

parser.add_argument("-l", "--log",
                    help="When this option is added the plot (if chosed) will"
                    " be displayed on logaritmic scale",
                    action="store_true")

parser.add_argument("-d", "--dataset", type=int,
                    help="Number of dataset. Dataset is a set of configs."
                         " Algorithm will run on every config from chosen "
                         "dataset. Datasets are numered from 0. "
                         "Default dataset is 0.\n"
                         "Amount of datasets depends on algorithm:\n"
                         " * simple_neuron_deleter (sender): "
                         + str(len(datasets["sender"])) + "\n"
                         " * simple_neuron_deleter2 (sender2): "
                         + str(len(datasets["sender2"])) + "\n"
                         " * sparsify_smallest_on_network (rat): "
                         + str(len(datasets["rat"])) + "\n"
                         " * sparsify_smallest_on_layers (rat2): "
                         + str(len(datasets["rat2"])) + "\n"
                         " * sharpen_filters (filters): "
                         + str(len(datasets["filters"])) + "\n"
                         " * derest: " + str(len(datasets["derest"])) + "\n",
                    default=0)

parser.add_argument("-f", "--file", type=str,
                    help="Name of file to save results to", default=None)

parser.add_argument("-v", "--val_size", type=int,
                    help="validation size for dataset", default=None)


args = parser.parse_args()


print "parsing arguments..."
datasets_available = len(datasets[args.algorithm])
if args.dataset >= datasets_available or args.dataset < 0:
    sys.exit("Invalid choise of dataset. Please choose the numer between"
             " 0 and " + str(datasets_available - 1))
dataset = datasets[args.algorithm][args.dataset]
algorithm = algorithms[args.algorithm]
ok()

print "loading network..."
network = get_network(args.network, args.val_size)
ok()

file_name = get_file_name(args)

print "generating results..."
results = run_algorithm(network, algorithm, dataset, verbose=True,
                        results_pkl=file_name).get_zeros_fraction()
ok()

for config in dataset:
    print "for config", config
    print "zeroed_fraction:", results[config][0]
    print "error rate:", results[config][1]

if args.plot:
    plot_2d_results(results, file_name, ylog=args.log,
                    title="results of " + args.algorithm + " algorithm")
