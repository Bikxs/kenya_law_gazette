#!/bin/bash

# Function to set up Python virtual environment
make_lambda() {
    # Create virtual environment
    python3.10 -m venv $1
    source $1/bin/activate
    pip install -r $1/requirements.txt
    rm -r $1/bin
    rm -r $1/include
    rm -r $1/lib64
    rm -r $1/pyvenv.cfg
    mkdir $1/python
    mv $1/lib $1/python/
    echo "Created lambda layer $1"
}

# List of packages
#packages=("lambda-power-tools-layer" "web3-layer" "requests-layer" "gremlin-layer" "gurobi-layer")
# packages=("firebase-admin-layer" "lambda-power-tools-layer" "requests-layer")
packages=("web_layer")
# Loop through each package and set up virtual environment
for package in "${packages[@]}"; do
    make_lambda "$package"
done
