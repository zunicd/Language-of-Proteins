import numpy as np
import pandas as pd
import Bio
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
import json

def add_protein_features(df: pd.DataFrame, seq_col_name: str) -> pd.DataFrame:
    df = df.copy()
    
    # Adding length as a feature
    df["length"] = df[seq_col_name].str.len()

    # Make protein analysis object for each sequence
    df["protein_analysis"] = df[seq_col_name].map(ProteinAnalysis)

    # Extract protein features from analysis object column (Note: X, B, O, and U codes are ignored for several of these functions)
    df["amino_acid_count"] = df["protein_analysis"].apply(lambda x: x.count_amino_acids())
    df["amino_acid_percent"] = df["protein_analysis"].apply(lambda x: x.get_amino_acids_percent()) 
    df["aromaticity"] = df["protein_analysis"].apply(lambda x: x.aromaticity())
    df["isoelectric_point"] = df["protein_analysis"].apply(lambda x: x.isoelectric_point())
    df["charge_at_pH"] = df["protein_analysis"].apply(lambda x: x.charge_at_pH(7.4)) # average pH in body

    # The following protein features require us to replace certain non-natural amino acid symbols in the sequence before
    # applying the function

    # Replace X and B
    df["molecular_weight"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.molecular_weight())

    # Replace X, B, U, and O
    df["instability_index"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(lambda x: x.replace('U', '')).map(lambda x: x.replace('O', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.instability_index())

    # Replace X, B, U, and O
    df["flexibility"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(lambda x: x.replace('U', '')).map(lambda x: x.replace('O', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.flexibility())

    # Replace X, B, U, and O
    df["gravy"] = df[seq_col_name].map(lambda x: x.replace('X', '')).map(lambda x: x.replace('B', '')) \
                                            .map(lambda x: x.replace('U', '')).map(lambda x: x.replace('O', '')) \
                                            .map(ProteinAnalysis).map(lambda x: x.gravy())

    # Create three columns for helix, turn, and sheet from secondary structure fraction
    df["helix_frac"] = df["protein_analysis"].apply(lambda x: x.secondary_structure_fraction()[0])
    df["turn_frac"] = df["protein_analysis"].apply(lambda x: x.secondary_structure_fraction()[1])
    df["sheet_frac"] = df["protein_analysis"].apply(lambda x: x.secondary_structure_fraction()[2])

    # Get mean of molar extinction coefficients
    df["molar_extinction_coefficient"] = df["protein_analysis"].apply(lambda x: np.mean(x.molar_extinction_coefficient()))

    # Convert percentages in decimal form to percent form
    df["amino_acid_percent"] = df["amino_acid_percent"].apply(lambda x: {key: 100*val for key, val in x.items()})

    # Convert flexibility arrays into mean flexibility to get a single value, unless empty array, in which case replace with 0
    df["flexibility"] = df["flexibility"].apply(lambda x: np.mean(x) if (x != []) else 0)
    
    # Drop protein analysis object column
    df = df.drop("protein_analysis", axis=1)

    return df

def get_avg_amino_acid_count(df: pd.DataFrame, amino_acids: set or list) -> dict:
    # Initialize amino acid dict for all sequences
    am_acid_dict = dict.fromkeys(amino_acids, 0)

    for am_dict in df.amino_acid_count:
        # This will handle the case in which this function is used after the dataframe has been loaded from a csv,
        # as the dictionaries are converted into strings
        if type(am_dict) == str:
            am_dict = json.loads(am_dict.replace("\'", "\""))
        for key in am_dict.keys():
            # If amino acid present in sequence
            if am_dict[key] != 0:
                am_acid_dict[key] = am_acid_dict.get(key) + am_dict[key]

    for key in am_acid_dict.keys():
        am_acid_dict[key] = am_acid_dict.get(key)/len(df)

    return am_acid_dict

def get_avg_amino_acid_percent(df: pd.DataFrame, amino_acids: set or list) -> dict:
    # Initialize amino acid dict for all sequences
    am_acid_dict = dict.fromkeys(amino_acids, 0)

    for am_dict in df.amino_acid_percent:
        # This will handle the case in which this function is used after the dataframe has been loaded from a csv,
        # as the dictionaries are converted into strings
        if type(am_dict) == str:
            am_dict = json.loads(am_dict.replace("\'", "\""))
        for key in am_dict.keys():
            # If amino acid present in sequence
            if am_dict[key] != 0:
                am_acid_dict[key] = am_acid_dict.get(key) + am_dict[key]

    for key in am_acid_dict.keys():
        am_acid_dict[key] = am_acid_dict.get(key)/float(len(df))

    return am_acid_dict