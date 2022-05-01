#!/usr/bin/env python3
import json
import pathlib, pandas, math, sys,  re, logging, numpy
import warnings
pandas.options.mode.chained_assignment = None
# from pandas.core.algorithms import isin
from tbtamr.CustomLog import logger

class Inferrence(object):

    """
    a base class for collation of tbprofiler results.
    """
    
    def __init__(self,args):

        self.isolates = args.output_data
        self.drugs = self._get_drugs()

    def _get_drugs(self):

        drugs = {
            "rifampicin":"Rifampicin",
            "isoniazid":"Isoniazid",
            "pyrazinamide":"Pyrazinamide",
            "ethambutol":"Ethambutol",
            "moxifloxacin":"Moxifloxacin",
            "amikacin":"Amikacin",
            "Cycloserine":"Cycloserine",
            "Ethionamide":"Ethionamide",
            "para-aminosalicylic_acid":"Para-aminosalicylic acid",
            "clofazimine":"Clofazimine",
            "delamanid":"Delamanid",
            "bedaquiline":"Bedaquiline",
            "linezolid":"Linezolid"
        }

        return drugs

    def _open_json(self, path):

        try:
            with open(path, 'r') as f:
                results = json.load(f)
                return results
        except Exception as err:
            logger.critical(f"There seems to have been an error opening {path}. The following error was reported {err}")

    def _rifampicin(self):
        pass

    def _isoniazid(self):
        pass

    def _ethambutol(self):
        pass
    
    def _remove_who(self):
        pass

    def _pyrazinamide(self):
        pass

    def _other_drugs(self):
        pass

    def _species(self):
        pass


    def infer(self):
        
        logger.info(f"Now inferring resistance profiles")

        for isolate in self.isolates:
            logger.info(f"Working on {isolate}")
            tbp_result = self._open_json(path = self.isolates[isolate]['collate'])
            


#  headers for output Seq_ID, 
# Identification (WGS), Phylogenetic lineage,Predicted drug resist. summary:, Rifampicin,Isoniazid,Pyrazinamide,Ethambutol,Moxifloxacin,Amikacin,Cycloserine,Ethionamide,Para-aminosalicylic acid,Clofazimine,Delamanid,Bedaquiline,Linezolid,Database