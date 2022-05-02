#!/usr/bin/env python3
import functools
import json
import pathlib, pandas, math, sys,  re, logging, numpy,csv
import warnings
pandas.options.mode.chained_assignment = None
# from pandas.core.algorithms import isin
from tbtamr.CustomLog import logger

class Inferrence(object):

    """
    a base class for collation of tbprofiler results.
    """
    
    def __init__(self,args):

        self.isolates = args
        self.drugs = self._get_drugs()

    def _get_drugs(self):

        drugs = {
            "rifampicin":"Rifampicin",
            "isoniazid":"Isoniazid",
            "pyrazinamide":"Pyrazinamide",
            "ethambutol":"Ethambutol",
            "moxifloxacin":"Moxifloxacin",
            "amikacin":"Amikacin",
            "cycloserine":"Cycloserine",
            "ethionamide":"Ethionamide",
            "para-aminosalicylic_acid":"Para-aminosalicylic acid",
            "clofazimine":"Clofazimine",
            "delamanid":"Delamanid",
            "bedaquiline":"Bedaquiline",
            "linezolid":"Linezolid"
        }

        return drugs
   
    def _get_funcs(self):
        funcs= {
                'rifampicin':self._rifampicin,
                'isoniazid': self._isoniazid,
                'pyrazinamide': self._pyrazinamide,
                'ethambutol':self._ethambutol,
                'moxifloxacin':self._other_drugs,
                'ofloxacin':self._other_drugs,
                'amikacin':self._other_drugs,
                'capreomycin':self._other_drugs,
                'kanamycin':self._other_drugs,
                'ethionamide':self._other_drugs,
                'streptomycin':self._other_drugs,
                'cycloserine':self._other_drugs,
                'para-aminosalicylic_acid': self._other_drugs,
                'clofazimine': self._other_drugs,
                'delamanid':self._other_drugs,
                'bedaquiline':self._other_drugs,
                'linezolid':self._other_drugs
                }

        return funcs

    def _open_json(self, path):

        try:
            with open(f"{path}", 'r') as f:
                results = json.load(f)
                return results
        except Exception as err:
            logger.critical(f"There seems to have been an error opening {path}. The following error was reported {err}")
    
    def _save_json(self, _data, _path):

        logger.info(f"Saving file: {_path}.json")
        with open(f"{_path}.json", 'w') as f:
            json.dump(_data,f)

    def _save_csv(self, _data, _path):
        
        logger.info(f"Saving file: {_path}.csv")

        header = [
            "Seq_ID",
            "Species",
            "Phylogenetic lineage",
            'Predicted drug resistance',
            "Rifampicin",
            "Isoniazid",
            "Pyrazinamide",
            "Ethambutol",
            "Moxifloxacin",
            "Amikacin",
            "Cycloserine",
            "Ethionamide",
            "Para-aminosalicylic acid",
            "Clofazimine",
            "Delamanid",
            "Bedaquiline",
            "Linezolid",
            "Database version"
         ]

        
        df = pandas.DataFrame(_data)
        df = df[header]
        
        df.to_csv(f"{_path}.csv", index = False)

    def _save_data(self, _data, prefix):

        self._save_csv(_data,prefix)
        self._save_json(_data,prefix)


    def _rifampicin(self, res):
        rif_to_remove = [
            'rpoB_p.Ala286Val',
            'rpoB_p.Arg552Cys',
            'rpoB_p.Glu423Ala',
            'rpoB_p.Glu460Gly',
            'rpoB_p.Glu592Asp',
            'rpoB_p.Glu761Asp',
            'rpoB_p.Gly981Asp',
            'rpoB_p.Ile480Thr',
            'rpoB_p.Ile480Val',
            'rpoB_p.Leu490Val',
            'rpoB_p.Phe424Leu',
            'rpoB_p.Phe424Val',
            'rpoB_p.Pro454Arg',
            'rpoB_p.Pro454His',
            'rpoB_p.Pro454Leu',
            'rpoB_p.Pro454Ser',
            'rpoB_p.Pro483Leu',
            'rpoB_p.Ser493Leu',
            'rpoB_p.Thr400Ala',
            'rpoB_p.Gly332Arg'
            ]
        rif_borderline = ["rpoB_p.Leu430Pro","rpoB_p.His445Asn"]
#     print(x)
        if res == '-':
            return 'No mechanism identified'
        elif res in ["*-","-*"]:
            return 'No mechanism identified^'
        else:
            inds = [i.strip() for i in res.split(',')]
#         print(inds)
        if len(inds) == 1 and inds[0] in rif_to_remove:
            return 'No mechanism identified'
        elif len(inds) == 1 and inds[0] in rif_borderline:
            return f'{inds[0]}*'
        else:
            return f";".join(inds)

    def _isoniazid(self,res):
        if res == '-':
            return 'No mechanism identified'
        elif res in ["*-","-*"]:
            return 'No mechanism identified^'
        else:
            inds = [i.strip() for i in res.split(',')]
        if len(inds) == 1 and 'ahpC' in inds[0]:
            return 'No mechanism identified'
        elif len(inds) == 1 and 'fabG' in inds[0]:
            return f'{inds[0]}*' if inds[0] == 'fabG1_c.-15C>T' else 'No mechanism identified'
        else:
            return f";".join(inds)

    def _emb_comp(self, res):
    
        gln497_hc = ['embB_p.Gln497Arg','embB_p.Gln497Lys']
        leu370_us = ['embB_p.Leu370Arg']
    
        if 'embB_p.Gln497' in res and res not in gln497_hc:
            
            return True
        
        elif res in leu370_us:
            
            return True
        
        return False

    def _ethambutol(self,res):
             
        if res == '-':
            return 'No mechanism identified'
        elif res in ["*-","-*"]:
            return 'No mechanism identified^'
        else:
            inds = [i.strip() for i in res.split(',')]
            if len(inds) == 1 and self._emb_comp(inds[0]):
                return 'No mechanism identified'
            elif len(inds) == 1 and inds[0] == 'embA_c.-16C>T':
                return 'No mechanism identified'
            else:
                return f";".join(inds)
    
    def _remove_who(self,res):

        not_reportable = ['PPE35','clpC1','Rv3236c', 'Rv1258c']
        to_remove = []
        muts = set()
        for i in res:
            for r in not_reportable:
                if r in i:
                    to_remove.append('tr')
                else:
                    muts.add(i)
        
        if len(to_remove) == len(res):
            return 'No mechanism identified'
        else:    
            return f";".join(list(muts))

    def _pyrazinamide(self,res):
        
        if res == '-':
            return 'No mechanism identified'
        elif res in ["*-","-*"]:
            return 'No mechanism identified^'
        inds = [i.strip() for i in res.split(',')]
        
        return self._remove_who(inds)

    def _other_drugs(self, res):
        if res == '-':
            return 'No mechanism identified'
        elif res in ["*-","-*"]:
            return 'No mechanism identified^'
        return f";".join(res.split(','))
    
    def _infer_drugs(self, tbp_result, seq_id):

        _d = {'Seq_ID':seq_id}
        funcs = self._get_funcs()
        for drug in self.drugs:
            logger.info(f"Checking {drug}")
            _d[self.drugs[drug]] = funcs[drug](tbp_result[seq_id][drug])
        
        return _d
    
    def _infer_dr_profile(self, res):
        
        fline_a = ['rifampicin','isoniazid']
        fline_b = ['pyrazinamide','ethambutol']
        flq = ['ofloxacin','moxifloxacin','levofloxacin']
        sline = ["amikacin","capreomycin","kanamycin","streptomycin"]
        score = 0
        fline_score = 1
        rif_inh = 3
        flq_score = False
        sline_score = False
        suff = ""
        for drug in self.drugs:
            if 'No mechanism identified' not in res[self.drugs[drug]]:
                if drug in flq:
                    flq_score = True
                elif drug in sline:
                    sline_score = True
                elif drug in fline_a:
                    score = score + rif_inh
                elif drug in fline_b:
                    score = score + fline_score
            if "*" in res[self.drugs[drug]] : #if there are any intermediate resistance mechanims identified add a *
                suff = f"{suff}*"
            elif "^" in res[self.drugs[drug]]: # if there are any missing
                suff = f"{suff}^"
            
        resistance = 'No drug resistance predicted'
        if score == 1 or score == 3: # one first line drug
            resistance = 'Mono-resistance predicted'
        elif score == 2 or score in range(4,6): # more than one first line drug where INH OR RIF can be present
            resistance = 'Poly-resistance predicted'
        elif score in range(6,9): # RIF and INH +/- PZA or EMB
            if flq and sline: # there are mutations in a FLQ and amikacin,capreomycin,kanamycin
                resistance = 'Pre-Extensive drug-resistance predicted'
            else:
                resistance = 'Multi-drug resistance predicted'

        res['Predicted drug resistance'] = f"{resistance}{suff}"

        return res

    def _species(self,res, seq_id):
        # pass
        species = "Mycobacterium tuberculosis"
        if 'La1' in res[seq_id]['main_lin'] and 'BCG' not in res[seq_id]['sublin']:
            species = f"{species} tuberculosis var bovis"
        elif 'La1' in res[seq_id]['main_lin'] and 'BCG' in res[seq_id]['sublin']:
            species = f"{species} tuberculosis var bovis BCG"
        elif 'La3' in res[seq_id]['main_lin']:
            species = f"{species} tuberculosis var orygis"
        elif 'La2' in res[seq_id]['main_lin']:
            species = f"{species} tuberculosis var caprae"
        elif res[seq_id]['main_lin'] == '':
            species = "Not likely M. tuberculosis"
        
        return species

    def _lineage(self,res, seq_id):
        
        if res[seq_id]['main_lin'] == '':
            return "Not typable"
        else:
            return res[seq_id]['main_lin'].replace('lineage', 'Lineage ')

    def _db_version(self, res,seq_id):

        return res[seq_id]['db_version']

    def infer(self):
        
        logger.info(f"Now inferring resistance profiles")
        results = []
        for isolate in self.isolates:
            logger.info(f"Working on {isolate}")
            tbp_result = self._open_json(path = self.isolates[isolate]['collate'])
            _dict = self._infer_drugs(tbp_result = tbp_result,seq_id=isolate)
            _dict = self._infer_dr_profile(res = _dict)
            _dict['Species'] = self._species(res = tbp_result, seq_id=isolate)
            _dict['Phylogenetic lineage'] = self._lineage(res = tbp_result, seq_id=isolate)
            _dict['Database version'] = self._db_version(res = tbp_result, seq_id= isolate)
            self._save_data(_data = [_dict], prefix = f"{isolate}/tbtamr")
            # self._save_csv(_)
            results.append(_dict)
            # break
        
        logger.info(f"Saving collated data.")
        self._save_data(_data = results, prefix = "tbtamr")
        



#  headers for output Seq_ID, 
# Identification (WGS), Phylogenetic lineage,Predicted drug resist. summary:, Rifampicin,Isoniazid,Pyrazinamide,Ethambutol,Moxifloxacin,Amikacin,Cycloserine,Ethionamide,Para-aminosalicylic acid,Clofazimine,Delamanid,Bedaquiline,Linezolid,Database