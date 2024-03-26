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
import sys

import pytrec_eval as pytrec

# Fixes import issues where inference.py couldn't import tools.py in the TILDE directory
sys.path.append(os.path.join(os.path.dirname(__file__),'TILDE'))

from TILDE.inference import inference
from TILDE.tools import load_queries, load_run

def build_run_name(alpha, is_long, run_path="TILDE/data/"):
    return run_path+"runs/alpha{0}_{1}.txt".format(alpha, "Long" if is_long else "Short")

def evaluate(run_file_path, qrel_path, metrics):
    with open(run_file_path) as f_run:
        run = pytrec.parse_run(f_run)

    with open(qrel_path) as f_qrels:
        qrels = pytrec.parse_qrel(f_qrels)

    evaluator = pytrec.RelevanceEvaluator(qrels, metrics)

    return evaluator.evaluate(run)

# Run inference with given dependent variables
#   alpha:     alpha value to use in range [0,1]
#   queries:   set of queries to use
def perform_inference(queries, run, alpha, is_long):
    inference(queries, run, alpha, save_path=build_run_name(alpha, is_long))

def main(args):

    queries = load_queries(args.run_path+"queries/DL2019-queries.tsv")

    long_queries = {k: v for k, v in queries.items() if len(v.split()) > args.n}
    short_queries = {k: v for k, v in queries.items() if len(v.split()) <= args.n}

    run = load_run(args.run_path+"runs/run.trec2019-bm25.res")

    perform_inference(short_queries, run, args.alpha, False)

    eval = evaluate(run_file_path = build_run_name(args.alpha, False),
             qrel_path =     args.run_path+"qrels/2019qrels-pass.txt", 
             metrics =       {'map_cut.10', 'ndcg_cut.10'}).values()

    short_df = pd.DataFrame(list(eval))
    print("Short Queries:")
    print(short_df.describe())

    perform_inference(long_queries, run, (1-args.alpha), True)

    eval = evaluate(run_file_path = build_run_name((1-args.alpha), True),
             qrel_path =     args.run_path+"qrels/2019qrels-pass.txt", 
             metrics =       {'map_cut.10', 'ndcg_cut.10'}).values()

    long_df = pd.DataFrame(list(eval))
    print("Long Queries:")
    print(long_df.describe())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_path", type=str, default="TILDE/data/")
    parser.add_argument("--verbose", type=bool, default=False)
    parser.add_argument("--alpha", type=float, default=0.4)
    parser.add_argument("--n", type=int, default=5) 
    args = parser.parse_args()

    main(args)