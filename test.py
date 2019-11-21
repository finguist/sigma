# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
#from foma import *

import yaml

DEFAULT_CONFIG_FILENAME = "sample_config.yaml"

def open_config(config_filename=DEFAULT_CONFIG_FILENAME):
    with open(config_filename, "r", encoding="utf-8") as fin: 
        config_options = yaml.safe_load(fin)
        return config_options


if __name__ == "__main__":
    config = open_config()
    print(config)
    

