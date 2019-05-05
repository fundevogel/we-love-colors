#!/bin/bash

# Setting up virtualenv & installing dependencies from `requirements.txt`
virtualenv -p python3 .env && source .env/bin/activate && pip install -r requirements.txt
