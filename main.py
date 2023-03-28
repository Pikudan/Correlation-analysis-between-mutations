'''
Input Data:
    From script.sh:
        path_input_file - path input csv file of muutations
        path_ouput_file - path creat csv file of analysis Spearmman and Pearson correlations and their  p-values, Chi squared test
    Can be entered by the user further:
        range - separation of mutations by class relattive to ddG
        environment - environment of inclusion in a pair of muations(predictor and any other)
        c - count pair mutations for analysis
        load_pdb - flag load pdb
        predictor, response - names two mutations. Can you use only predictor or both together or nothing(then the program will simpply sort throuugh all possible pairs
        mode_contact_map - how calculate distance between residius:
            'ca' - contact between CA
            'center' = contact between center of mass
        mode - "structure/sequence":
            "structure" uses a contact map to find close pairs.
            "sequence" uses a index mutation to find close pairs.
        print_size - flag printing change useg memory
        
        Default:
            range = [-10, -1.5, -0.5, 0.5, 1.5, 10]
            environment = [-1, 0, 1]
            c = 400;
            load_pdb = False;
            predictor, response = None;
            mode = 'sequence';
            mode_contact_map='center';
            print_size=False;
            
'''
import sys
from load import load
import numpy as np
import pandas as pd
import itertools as it
from analysis import analys
import preparing_data_for_analysis
from preparing_data_for_analysis import split_at_predictor
from preparing_data_for_analysis import creat_merge
import optimize_memory_usage
import contact_map
from contact_map import creat_contact_map
def main(path_input_file=None, path_output_file=None):
    print("Default:\n\trange = [-10, -1, 0, 1, 10];\n\tenvironment = [-1, 0, 1];\n\tc = 400;\n\tload_pdb = False;\n\tpredictor = None, response = None;\n\tmode ='sequence';\n\tmode_contact_map='center';\n\tprint_size=False;")

    change = input("Do you want change default parameters?: (y/n)\t").lower().strip()
    if change == "y":
        range = [float(x) for x in input("Change range in format: x y z").split()]
        
        load_pdb = input("Change load_pdb: False/True").lower().split()
        if load_pdb == "true": load_pdb = True
        else: load_pdb = False
        
        range = [float(x) for x in input("Change range in format: x y z ...").split()]
        
        response, predictor = input("Change name predictor and response mutation in format: XX YY or XX None or None None").upper().split()
        if response == "NONE": response = None
        if predictor == "NONE": predictor = None
        
        mode = input("Change mode 'structure' or 'sequence':\n\t'structure' uses a contact map to find close pairs.\n\t'sequence' uses a index mutation to find close pairs").lower().split()

        if mode == "structure":
            mode_contact_map=input("Change mode_contact_map - how calculate distance between residius:\n\t'ca' - contact between CA\n\t'center' = contact between center of mass").lower().split()
        else:
            environment = [int(i) for i in input("Change environment - environment of inclusion in a pair of muations - in format x y z ...").split()]
        print_size = input("Change print_size: False/True").lower().split()
        if print_size == "true": print_size = True
        else: print_size = False
        
        c = int(input("Change c - count pair mutations for analysis"))
    else:
        range = [-10, -1, 0, 1, 10]
        environment = [-1, 0, 1]
        c = 400
        load_pdb = False
        predictor = None
        response = None
        mode = "sequence"
        mode_contact_map='center'
        print_size=False
 
    
    df = load(path_input_file, range, print_size)
    df['check'] = df["pdb"].apply(lambda x: x in ["1BK2", "1EM7", "1ENH", "1EM7", "1GB4", "1GJS", "1GL5", "1I6C", "1K1V", "1MNH", "1OPS", "1PGA", "1PWT", "1QP2", "1TGO", "1UBQ", "1UCS", "1UFM", "1WCL"])
    df = df[df['check'] == True]
    
    if mode == "structure":
        contact_map = creat_contact_map(df['pdb'].unique(), mode_contact_map, load_pdb)
    else: contact_map = {}
    
    amino_acids = np.array(["A", "R", "N", "D", "C", "E", "Q", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"])
    mutation = ["".join((x,y)) for x, y in it.permutations(amino_acids, 2)]
    
    result = np.array([])
    if predictor is not None:
        df_predictor, df_response = split_at_predictor(df, predictor)
        if response is not None:
            merge = creat_merge(df_predictor, df_response, predictor, response, mode, contact_map, environment)
            result = analys(merge, predictor, response, result)
        else:
            for response in mutation:
                if c == 0: break
                if predictor == response: continue
                merge = creat_merge(df_predictor, df_response, predictor, response, mode, contact_map, environment)
                result = analys(merge, predictor, response, result)
                c -= 1
    else:
        for predictor in mutation:
            if c == 0: break
            df_predictor, df_response = split_at_predictor(df, predictor)
            for response in mutation:
                if c == 0: break
                if predictor == response: continue
                merge = creat_merge(df_predictor, df_response, predictor, response, mode, contact_map, environment)
                result = analys(merge, predictor, response, result)
                c -= 1
    result_pd = pd.DataFrame({"predictor": result[0::10], "response": result[1::10], "len": result[2::10].astype(int), "spearman": result[3::10].astype(float), "p-value-spearman": result[4::10].astype(float), "pearson": result[5::10].astype(float), "p-value-pearson": result[6::10].astype(float), "F-statistic": result[7::10].astype(float), "p-value-chi2": result[8::10].astype(float), "what": result[9::10].astype(float)})
    result_pd.to_csv(path_output_file, index=False) 

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error. Not enough parameters.")
        sys.exit(1)
    if len (sys.argv) > 3:
        print("Error. Too many parameters.")
        sys.exit(1)
    path_input_file = sys.argv[1]
    path_output_file = sys.argv[2]
    main(path_input_file, path_output_file)

