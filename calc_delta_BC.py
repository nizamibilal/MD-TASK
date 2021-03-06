#!/usr/bin/env python
#
# Calculate the change in the betweenness centrality of each residue over the 
# course of an MD simulation
#
# Script distributed under GNU GPL 3.0
# 
# Author: David Brown
# Date: 17-11-2016


from natsort import natsorted
from datetime import datetime

import numpy as np

from lib.utils import *

import os, sys, argparse, matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt



def calc_delta_BC(reference_file, alternative_files, generate_plots=False):
    reference = np.loadtxt(reference_file)
    num_nodes = reference.shape[0]
    
    delta_BC = np.zeros((num_nodes, num_nodes))
    BC_mutant = np.zeros((num_nodes, num_nodes))
    
    label = "BC"
    
    delta_BC = np.zeros((num_nodes, num_nodes))
    alternatives = natsorted(alternative_files)
    
    log("Calculating delta %s for %d networks...\n" % (label, len(alternatives)))
    
    for i, alternative in enumerate(alternatives):
        log("Calculating delta %s (%d/%d)\r" % (label, i + 1, len(alternatives)))
        
        prefix = ".".join(alternative.split(".")[:-1])
        alternative = np.loadtxt(alternative)
        
        difference = alternative - reference
        
        delta_BC[i,:] = difference
        
        np.savetxt("%s_delta_%s.dat" % (prefix, label), difference)
        
        if generate_plots:
            node_axis = range(1, num_nodes + 1)
            plt.plot(node_axis, difference)
            plt.axhline(0, color='black')
            plt.title("%s $\Delta$ %s" % (prefix, label), fontsize=18)
            plt.xlabel('Residue Numbers', fontsize=16)
            plt.ylabel("$\Delta$ %s" % label, fontsize=16)
            plt.savefig("%s_delta_%s.png" % (prefix, label), dpi=300, bbox_inches='tight')
            plt.close()
    
    log("\n")
    
    return delta_BC


def main(args):
    calc_delta_BC(args.reference, args.alternatives, args.generate_plots)



silent = False
stream = sys.stdout

def log(message):
    global silent
    global stream
    
    if not silent:
        stream.write(message)
        stream.flush()
    

if __name__ == "__main__":
    
    #parse cmd arguments
    parser = argparse.ArgumentParser()
    
    #standard arguments for logging
    parser.add_argument("--silent", help="Turn off logging", action='store_true', default=False)
    parser.add_argument("--log-file", help="Output log file (default: standard output)", default=None)
    
    #custom arguments
    parser.add_argument("--reference", help="The reference BC matrix (.dat)")
    parser.add_argument("--alternatives", help="The alternative BC matrices (.dat)", nargs="*")
    parser.add_argument("--generate-plots", help="Plot results - without setting this flag, no graph will be generated", action='store_true', default=False)
    
    args = parser.parse_args()
    
    #set up logging
    silent = args.silent
    
    if args.log_file:
        stream = open(args.log_file, 'w')
    
    start = datetime.now()
    log("Started at: %s\n" % str(start))
    
    #run script
    main(args)

    end = datetime.now()
    time_taken = format_seconds((end - start).seconds)
    
    log("Completed at: %s\n" % str(end))
    log("- Total time: %s\n" % str(time_taken))
    
    #close logging stream
    stream.close()
    
    
