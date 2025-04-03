#!/usr/bin/env sh

# The name of the repo that the pages will be generated and hosted in
REPO_NAME="static_site_generator"

# Run static site generater script
python3 ./src/main.py "/$REPO_NAME/"
