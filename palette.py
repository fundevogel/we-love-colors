#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Imports
# For more information, see https://www.python.org/dev/peps/pep-0008/#imports
##

import os
import json


class Palette:
    def __init__(self):
        os.makedirs(self.json_path, exist_ok=True)


    ##
    # Dumps fetched colors as JSON
    ##
    def save(self, output_filename=''):
        if output_filename == '':
            output_filename = self.identifier

        json_path = self.json_path + '/' + output_filename + '.json'

        with open(json_path, 'w') as file:
            file.write(json.dumps(self.sets, indent=4))

        print('Saving "' + json_path + '" .. done')


    ##
    # Creates JSON files for each color set
    ##
    def create_json(self, input_filename=''):
        if input_filename == '':
            input_filename = self.identifier

        with open(self.json_path + '/' + input_filename + '.json', 'r') as file:
            data = json.load(file)

        for set, colors in data.items():
            if len(colors) == 0:
                break

            # Creating subdirectory
            file_path = self.json_path + '/sets'
            os.makedirs(file_path, exist_ok=True)

            json_path = file_path + '/' + set + '_' + str(len(colors)) + '-colors.json'

            # Dumps color sets as JSON
            with open(json_path, 'w') as file:
                file.write(json.dumps(colors, indent=4))

            print('%s has been created.' % json_path)
