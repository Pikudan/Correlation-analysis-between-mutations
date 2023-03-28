'''
Creat a DataFrame of mutation-predictor and mutation-response pairs that are adjacent in a structure or sequence
Input Data:
    Two DataFrame with mutation-predictor and mutation-response
    predictor, response - names two mutations
    mode - "structure/sequence":
        "structure" uses a contact map to find close pairs.
        "sequence" uses a index mutation to find close pairs
    contact_map - contact map is required when mode="structure"
    environment - environment of inclusion in a pair of muations
    Default: mode = "sequence", contact_map=None, radius=1
Output Data:
    DataFrame of mutation-predictor and mutation-response pairs
'''
import pandas as pd
def creat_merge(df_predictor, df_response, predictor, response, mode="sequence", contact_map=None, environment=[-1, 0, 1]):
    df = df_response.copy(deep=False)
    #Add columns-indicators of mutation response
    df = df.loc[((df['start_amino'] == response[0]) & (df['end_amino'] == response[1]))]
    df = df[["pdb", "ddG", "index", "type_ddG"]]
    #Pairing of all mutations
    result = pd.merge(df, df_predictor,on = ["pdb"], how="left")
    #drop NaN
    result = result.dropna()
    #This strange result merge: converting type from int to float ._.
    result[''.join(("index", predictor))] = result[''.join(("index", predictor))].astype('int')
    if len(result) != 0:
        if mode == "structure":
            contact = result.apply(lambda x: abs(contact_map[x["pdb"]][x["index"] - 1, x[''.join(("index", predictor))] - 1]) < 6, axis=1)
            #result = result.loc[(contact_map[result["pdb"]][result["index"] - 1, result[''.join(("index", predictor))] - 1])]
        else:
            result = result.apply(lambda x: x["index"] - x[''.join(("index", predictor))] in environment, axis=1)
        result = result[contact]
    return result

'''
Input Data:
    DataFrame containing columns: "pdb", "ddG", "type_ddG", "mutation", "index", "start_amino", "end_amino"
    predictor - name mutation-predictor
Output Data:
    DataFrame with predictor containing columns: "pdb", "ddGXX", "indexXX", "type_ddGXX", where XX - name mutation-predictor
    DataFrame with response containing columns: "pdb", "mutation", "ddG", "index", "type_ddG", "start_amino", "end_amino"
'''
def split_at_predictor(data, predictor):
    df = data.copy(deep=False)
    #Add columns-indicators of two mutations: predictor and response
    #df = df.loc[((df['start_amino'] == predictor[0]) & (df['end_amino'] == predictor[1]))]
    #df[predictor] = df.apply(lambda x: x["start_amino"] == predictor[0] and x["end_amino"] == predictor[1], axis = 1)
    #split DataFrame into data with and without mutation-predictor
    select_with_predictor = df.loc[((df['start_amino'] == predictor[0]) & (df['end_amino'] == predictor[1]))]
    select_without_predictor = df.loc[((df['start_amino'] != predictor[0]) | (df['end_amino'] != predictor[1]))]
    select_with_predictor = select_with_predictor[["pdb", "ddG", "index", "type_ddG"]]
    select_without_predictor = select_without_predictor[["pdb", "mutation", "ddG", "index", "type_ddG", "start_amino", "end_amino"]]
    select_with_predictor.columns = ["pdb", ''.join(("ddG", predictor)), ''.join(("index", predictor)), ''.join(("type_ddG", predictor))]
    return select_with_predictor, select_without_predictor
