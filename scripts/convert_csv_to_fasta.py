# Script to convert csv files to fasta files
#
import csv
import os

def separate_seq(sequence:str) -> str:
    """ 1. Separate sequence into 60-character segments
           and append new line to each segment except the last one
        2. Create a fasta header in the format:
           >{index}|{sequence_id}|{label}

    Args:
        sequence : protein sequence from csv file

    Returns:
        fs: separated sequence for fasta file
    """
    # Initialize new sequence
    fs = ""
    # Count number of full segments
    segment = 60
    d = len(sequence) // segment
    r = len(sequence) % segment
    new_line = '\n'
    # Iterate through segments and append new line character - \n
    for i in range(d):
        low = i * segment
        high = (i + 1) * segment
    # If the last line is a full segment, no new line character
        if r == 0 and i == d - 1:
            new_line = ""
        fs += f"{sequence[low : high]}{new_line}"
    # Append remainder
    fs += f"{sequence[d * segment :]}"
    return fs


def csv_to_fasta(csv_file, fasta_file):
    """ Convert csv files to fasta files

    Args:
        csv_file: csv formatted file
        fasta_file: fasta file name to write to;
                    no such file needs to exist before running this function

    Returns:
        fasta_file : fasta formatted file
    """
    # Initialize dictionary
    Seq = {}
    
    # Read csv file 
    with open(csv_file) as fin:
        reader = csv.DictReader(fin)
        # Create fieldnames variables - input files have different field names
        fnames = reader.fieldnames
        n_lines = len(list(reader))
        PBD_Code = fnames[0]
        Sequence = fnames[1]
        # Go to the top of the file (due to list(reader))
        fin.seek(0)
        next(fin)
        # Initialize index
        idx = 0
        # For files without PBD codes (usually in 1st column)
        if len(fnames) <= 2 and 'sequenc' in PBD_Code.lower():
            Sequence = fnames[0]
            Label = fnames[1]
            # Create list of sequential protein "names"
            # For 'test_data' dataset add string 'ts' before 4 digit number at the end
            t = ""
            if 'test_data' in os.path.split(csv_file)[1]:
                t = 'ts'
            PBD_Code_l = []
            for i in range(1, n_lines+1):
                PBD_Code_l.append(f"Protein_seq_{t}{i:04d}")
 
            j = 0
            for row in reader:
                # Read sequences from the file and combine with previously created keys
                header = f'{j}|{PBD_Code_l[j]}|{row[Label]}'
                Seq[header] = row[Sequence]
                j += 1
        # Files with PBD Code in the first column (this should be normal)
        else:
            # Iterate through every row and create key-value pairs
            for row in reader:
                Label = fnames[2]
                header = f'{idx}|{row[PBD_Code]}|{row[Label]}'
                Seq[header] = row[Sequence]
                idx += 1
                
    # Write to fasta file
    with open(fasta_file, 'w') as fout:
        for header, sequence in Seq.items():
            # Separate sequence into 60-characters segments
            sequence = separate_seq(sequence)
            # Write code in one line and the sequence below in one or more lines
            fout.write(f">{header}\n{sequence}\n")
