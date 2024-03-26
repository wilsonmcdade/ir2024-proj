# IR 2024 Project

## How to install system
1. `make install` - This initializes the git submodules, installs TILDE requirements and trec_eval
2. 'make get_collection' - Fetches MS Marco from remote

## Using system
1. 'source venv/bin/activate' - Enter virtual environment used for running system
2. 'python eval.py' - Run eval script with default values
    a. 'python eval.py --help' - Use for tips to run evaluation script

## What has been changed?
* eval.py
    * This is our main experimentation program. This uses TILDE and exposes an interface for the "inference" program in the model. Once the program as been run, the resulting inference will be scored using pytrec_eval, which is a evaluation tool that uses trec_eval. 
* TILDE/inference.py
    * This is the main unit being experimented on in TILDE. There have been no changes to the logic of the program but the main inference logic has been moved around so we can run an inference with default values and without running the inference.py file itself.
* Makefile
    * We have a Makefile that can do some predefined tasks like installing the system, running an index using TILDE, training TILDE (unused), and collecting datasets from remote sources.

## Weights and Data
* All necessary weights and data can be acquired with `make install` and `make get_collection`. These steps are both part of the normal installation process.