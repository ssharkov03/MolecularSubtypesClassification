import pandas as pd
import numpy as np

import pickle
from typing import Tuple

from sklearn.preprocessing import MinMaxScaler


def Get_mRNA(miRNA: str, genes_pool : pd.core.frame.DataFrame) -> list:
    tmp = genes_pool.loc[genes_pool['mirna']  == miRNA]
    return list(tmp.mrna)

def Get_miRNA(mRNA: str, genes_pool : pd.core.frame.DataFrame) -> list:
    tmp = genes_pool.loc[genes_pool['mrna']  == mRNA]
    return list(tmp.mirna)

def Get_integration_rate(mRNA: str, miRNA: str, genes_pool : pd.core.frame.DataFrame) -> float:
    tmp = genes_pool.loc[(genes_pool['mrna']  == mRNA) & (genes_pool['mirna'] == miRNA)]
    return list(tmp.int_rate)[0]


def preprocess_miRNA_df(df : pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    scaler = MinMaxScaler()
    scaled_df = pd.DataFrame(scaler.fit_transform(df))
    scaled_df.index = df.index
    scaled_df.columns = df.columns
    return scaled_df



# input_df has miRNAs, df is dataframe used for model training and it has mRNAs
def miRNA_to_mRNA(input_df : pd.core.frame.DataFrame, df : pd.core.frame.DataFrame, genes_pool : pd.core.frame.DataFrame) -> Tuple[pd.core.frame.DataFrame, list]:
    
    df_mRNA_s = list(df.columns)
    pool_mRNA_s = list(set(genes_pool.mrna))
    
    for mRNA in pool_mRNA_s:
        if mRNA not in df_mRNA_s:
            genes_pool = genes_pool.loc[genes_pool['mrna'] != mRNA]
            
    input_df_miRNA_s = list(input_df.columns)
    pool_miRNA_s = list(set(genes_pool.mirna))
    
    for miRNA in pool_miRNA_s:
        if miRNA not in input_df_miRNA_s:
            genes_pool = genes_pool.loc[genes_pool['mirna'] != miRNA]
            
    input_df_scaled = preprocess_miRNA_df(input_df)
    
    pool_mRNA_s_updated = list(set(genes_pool.mrna))
    
    resulting_df = pd.DataFrame()
    class_weights = []
    
    for mRNA in pool_mRNA_s_updated:
        corresponding_miRNA_s = Get_miRNA(mRNA, genes_pool)
        best_miRNA = corresponding_miRNA_s[0]
        for miRNA in corresponding_miRNA_s:
            if Get_integration_rate(mRNA, miRNA, genes_pool) > Get_integration_rate(mRNA, best_miRNA, genes_pool):
                best_miRNA = miRNA
        resulting_df[mRNA] = input_df_scaled[best_miRNA]
        class_weights.append(Get_integration_rate(mRNA, best_miRNA, genes_pool))
        
    return resulting_df, class_weights


if __name__ == '__main__':
    with open('Saved data/X.pickle', 'rb') as input_file:
        df = pickle.load(input_file)
        
    input_file_path = 'input_data.csv'
    input_df = pd.read_csv(input_file_path, index_col=0)
    
    genes_pool = pd.read_csv("modified_genes_pool.csv")
    
    resulting_df, class_weights = miRNA_to_mRNA(input_df, df, genes_pool)
    for feature, weight, in zip(list(resulting_df.columns), class_weights):
        print(f'{feature} : {weight}')
    