######################
#
# Eval script for IR Project
# Author: Wilson McDade
#
######################

import argparse
import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import random

import pytrec_eval as pytrec

# Fixes import issues where inference.py couldn't import tools.py in the TILDE directory
sys.path.append(os.path.join(os.path.dirname(__file__),'TILDE'))

from TILDE.inference import inference
from TILDE.tools import load_queries, load_run

def build_run_name(alpha, set_name, run_path="TILDE/data/"):
    return run_path+"runs/alpha{0}_{1}.txt".format(alpha, set_name)

def evaluate(run_file_path, qrel_path, metrics):
    with open(run_file_path) as f_run:
        run = pytrec.parse_run(f_run)

    with open(qrel_path) as f_qrels:
        qrels = pytrec.parse_qrel(f_qrels)

    evaluator = pytrec.RelevanceEvaluator(qrels, metrics)

    return evaluator.evaluate(run)

def make_graphs(results):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
    for label, grp in results.groupby('Set'):
        plt.plot(grp['Alpha'], grp['MAP@10'], label=f'Set {label}', marker='o')
    plt.title('Line Graph of MAP@10')
    plt.xlabel('Alpha')
    plt.ylabel('MAP@10')
    plt.legend()

    plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
    for label, grp in results.groupby('Set'):
        plt.plot(grp['Alpha'], grp['NDCG@10'], label=f'Set {label}', marker='o')
    plt.title('Line Graph of NDCG@10')
    plt.xlabel('Alpha')
    plt.ylabel('NDCG@10')
    plt.legend()

    plt.savefig('results.png')

    plt.tight_layout()
    plt.show()

# Run inference with given dependent variables
#   alpha:     alpha value to use in range [0,1]
#   queries:   set of queries to use
def perform_inference(queries, run, alpha, set_name):
    inference(queries, run, alpha, save_path=build_run_name(alpha, set_name))

def main(args):

    df_columns = ["MAP@10", "NDCG@10", "Alpha", "Set"]
    results = pd.DataFrame(columns = df_columns)

    queries = load_queries(args.run_path+"queries/DL2019-queries.tsv")

    # Split queries into named sets
    query_set_a = {k: v for k, v in queries.items() if len(v.split()) <= 4}
    query_set_b = {k: v for k, v in queries.items() if len(v.split()) == 5}
    query_set_c = {k: v for k, v in queries.items() if len(v.split()) == 6}
    query_set_d = {k: v for k, v in queries.items() if len(v.split()) > 6}

    # Pick random query out of set
    rand_query_a = random.choice(list(query_set_a.values()))
    rand_query_b = random.choice(list(query_set_b.values()))
    rand_query_c = random.choice(list(query_set_c.values()))
    rand_query_d = random.choice(list(query_set_d.values()))

    query_sets = [query_set_a, query_set_b, query_set_c, query_set_d]
    query_sets_names = ["A", "B", "C", "D"]

    run = load_run(args.run_path+"runs/run.trec2019-bm25.res")

    i = 0
    for query_set in query_sets:

        for alpha in np.arange(0, 1.1, step=0.1):
            
            perform_inference(query_set, run, alpha, query_sets_names[i])

            eval = evaluate(run_file_path = build_run_name(alpha, query_sets_names[i]),
                    qrel_path =     args.run_path+"qrels/2019qrels-pass.txt", 
                    metrics =       {'map_cut.10', 'ndcg_cut.10'}).values()

            result = pd.DataFrame(list(eval))
            print("Set " + query_sets_names[i] + ":")
            print(result.describe())

            results = pd.concat([pd.DataFrame([[result["map_cut_10"].mean(), 
                                               result["ndcg_cut_10"].mean(), 
                                               alpha, 
                                               query_sets_names[i]]], 
                                               columns=df_columns), results], ignore_index=True)

            print(results.head())

        i += 1

    make_graphs(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_path", type=str, default="TILDE/data/")
    args = parser.parse_args()

    main(args)
