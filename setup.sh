#!/bin/bash

# Setting up & activating virtualenv
virtualenv -p python3 .env
# shellcheck disable=SC1091
source .env/bin/activate

# Installing dependencies
pip install -r requirements.txt

# Creating directory structure
cd palettes || exit

for dir in copic \
           dulux \
           pantone \
           prismacolor \
           ral
do
    mkdir -p "$dir"
done
