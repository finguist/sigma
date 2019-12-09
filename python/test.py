# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import sys

# Load the foma stuff:
sys.path.append('./python')
from foma import *

# This is where the FST is customized
import yaml

DEFAULT_CONFIG_FILENAME = "sample_config.yaml"

def open_config(config_filename=DEFAULT_CONFIG_FILENAME):
    with open(config_filename, "r", encoding="utf-8") as fin: 
        config_options = yaml.safe_load(fin)
        return config_options

### MASTER FST ###

def make_fst(config):

    # Defines vowel #
    FST.define("i|e|ɛ|a", "FrontVowel")
    FST.define("u|o|ʌ|ɑ|ɔ", "BackVowel")
    FST.define("i|e|u|o", "HighVowel")
    FST.define("a|ɛ|ʌ|ɑ|ɔ", "LowVowel")
    FST.define("FrontVowel|BackVowel|ə", "Vowel")
    
    # Defines consonant #
    FST.define("m|n|ŋ", "Nasal")
    FST.define("l|ɹ|j|w", "Approximant")
    FST.define("f|v|s|z|ð|θ|χ|ʁ|ʒ|ʃ", "Fricative")
    FST.define("tɬ|ts|dz|tʃ|dʒ", "Affricate")
    FST.define("p|b|t|d|k|g|ʔ", "Plosive")
    FST.define("Fricative|Affricate|Plosive", "Obstruent")
    FST.define("Nasal|Approximant", "Sonorant")
    FST.define("Nasal|Approximant|Fricative|Affricate|Plosive", "Consonant")

    # Defines phoneme #
    FST.define("Consonant|Vowel", "Phoneme")

## PARSING FUNCTION ##
   
    #Any sequence of phonemes can be parsed as an Onset, Nucleus, or Coda
    FST.define('''
        [Phoneme]* -> "["...["]O"|"]N"|"]C"]
        ''', "Parse")

## SYLLABLE COMPONENTS ##
# ONSET #

    FST.define('"[" Consonant+ "]O"', "Onset")
    # replace "X" with special onset character    
    if config["special_onset"]:
        FST.define("X", "special_onset")
        FST.define('"[" special_onset "]O"', "Onset")

# NUCLEUS #

    FST.define('"[" ([Vowel]) "]N"', "Nucleus")
    if config["nucleus_nasal"]:
        FST.define('"[" ([Vowel|Nasal]) "]N"', "Nucleus")
    if config["nucleus_approximant"]:
        FST.define('"[" ([Vowel|Approximant]) "]N"', "Nucleus")
    if config["nucleus_sonorant"]:
        FST.define('"[" ([Vowel|Sonorant]) "]N"', "Nucleus")
    if config["nucleus_fricative"]:
        FST.define('"[" ([Vowel|Fricative]) "]N"', "Nucleus")
    if config["nucleus_affricate"]:
        FST.define('"[" ([Vowel|Affricate]) "]N"', "Nucleus")
    if config["nucleus_plosive"]:
        FST.define('"[" ([Vowel|Plosive]) "]N"', "Nucleus")
    if config["nucleus_obstruent"]:
        FST.define('"[" ([Vowel|Obstruent]) "]N"', "Nucleus")
    if config["nucleus_consonant"]:
        FST.define('"[" ([Vowel|Consonant]) "]N"', "Nucleus")

    # replace "X" with special nucleus character    
    if config["special_nucleus"]:
        FST.define("X", "special_nucleus")
        FST.define('"[" special_nucleus "]O"', "Nucleus")

# CODA #

    FST.define('"[" [Consonant]* "]C"', "Coda") 
    if config["coda_nasal"]:
        FST.define('"[" ([Nasal]) "]N"', "Coda")
    if config["coda_approximant"]:
        FST.define('"[" ([Approximant]) "]N"', "Coda")
    if config["coda_sonorant"]:
        FST.define('"[" ([Sonorant]) "]N"', "Coda")
    if config["coda_fricative"]:
        FST.define('"[" ([Fricative]) "]N"', "Coda")
    if config["coda_affricate"]:
        FST.define('"[" ([Affricate]) "]N"', "Coda")
    if config["coda_plosive"]:
        FST.define('"[" ([Plosive]) "]N"', "Coda")
    if config["coda_obstruent"]:
        FST.define('"[" ([Obstruent]) "]N"', "Coda")

    # replace "X" with special nucleus character    
    if config["special_coda"]:
        FST.define("X", "special_coda")
        FST.define('"[" special_coda "]O"', "Coda")

## Syllable definitions
    FST.define('(Onset) Nucleus (Coda))', "Syllable") 
    FST.define('Syllable [Syllable]*)', "Syllables")

## Syllabification
    FST.define("GEN .o. Parse", "GEN")
    FST.define("GEN .o. Syllables", "GEN")

##
    fst = FST("GEN")
    return fst
#fst.apply_down("strostrlk")

### Constraints for OT

## Onset Constraints
# OnsetsRequired

# FST.define('$[ Coda Nucleus ]', "OnsetsRequired")
# if config["onsets_required"]:
#     FST.define("GEN .O. OnsetsRequired", "GEN")


# # NoComplexOnsets 

#     FST.define('~$[ Consonant Consonant "]O" ]', "NoComplexOnsets")

#     if not config["complex_onsets"]:
#         FST.define("GEN .O. NoComplexOnsets", "GEN")
#     #TODO: make constraint that outlaws 3+

## NUCLEUS
#TODO: adjustable number of segments 0-3



## CODA
#TODO: adjustable number of segments 0-4

## Coda Constraints
# NoCoda  


        #make_me_a_constraint(' "]C" ') why do we need this?
        # FST.define('~$[ "]C" ]', "NoCodas")
        #     if not config["codas_allowed"]:
        #         FST.define("GEN .O. NoCodas", "GEN")
        #         for i in range(1,5):
        #             FST.define('~$[ "]C" ]>' + str(i), "NoCodas")
        #             FST.define("GEN .O. NoCodas", "GEN")



if __name__ == "__main__":
    config = open_config()
    print(config)
    fst = make_fst(config)
    fst.apply_down("something")

