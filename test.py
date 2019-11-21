# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
#from foma import *

import yaml

DEFAULT_CONFIG_FILENAME = "sample_config.yaml"

def open_config(config_filename=DEFAULT_CONFIG_FILENAME):
    with open(config_filename, "r", encoding="utf-8") as fin: 
        config_options = yaml.safe_load(fin)
        return config_options

def make_fst(config):

    FST.define("a|e|i|o|u", "V")
    FST.define("m|n", "N")

    FST.define("N|P|L", "C")

    ...

    FST.define('~$[ "[" C C "]O" ]', "NoComplexOnsets")

    if not config["complex_onsets_allowed"]:
        FST.define("GEN .O. NoComplexOnsets", "GEN")


    
    if not config["codas_allowed"]:

        make_me_a_constraint(' "]C" ')
        FST.define('~$[ "]C" ]', "NoCodas")
        FST.define("GEN .O. NoCodas", "GEN")
        for i in range(1,5):
            FST.define('~$[ "]C" ]>' + str(i), "NoCodas")
            FST.define("GEN .O. NoCodas", "GEN")



if __name__ == "__main__":
    config = open_config()
    print(config)
    

