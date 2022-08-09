# Script to convert csv files to fasta files
#
import csv

def separate_seq(sequence:str) -> str:
    """ Separate sequence in 60-characters chunks
         and append new line to each chunk except remaing one

    Args:
        sequence : protein sequence from csv file

    Returns:
        fs: separated sequence for fasta file
    """
    # Initialize new sequence
    fs = ""
    # Count number of full chunks
    chunk = 60
    d = len(sequence) // chunk
    r = len(sequence) % chunk
    new_line = '\n'
    # Iterate hrough chunks and append new line char - \n
    for i in range(d):
        low = i * chunk
        high = (i + 1) * chunk
    # If the last line is full chunk, no new line char
        if r == 0 and i == d - 1:
            new_line = ""
        fs += f"{sequence[low : high]}{new_line}"
    # Append remainder
    fs += f"{sequence[d * chunk :]}"
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
        # For files without PBD codes (usually in 1st column)
        if len(fnames) <= 2 and 'sequenc' in PBD_Code.lower():
            Sequence = fnames[0]
            # Create list of sequential protein "names"
            PBD_Code_l = []
            for i in range(1, n_lines+1):
                PBD_Code_l.append(f"Protein_seq_{i:04d}")
 
            j = 0
            for row in reader:
                # Read sequences from the file and combine with previously created keys
                key = PBD_Code_l[j]
                Seq[key] = row[Sequence]
                j += 1
        # Files with PBD Code in the first column (this should be normal)
        else:
            # Iterate through every row and create key-value pairs
            for row in reader:
                Seq[row[PBD_Code]] = row[Sequence]

    # Write to fasta file
    with open(fasta_file, 'w') as fout:
        for code, sequence in Seq.items():
            # Separate sequence in 60-characters chunks
            sequence = separate_seq(sequence)
            # Write code in one line and the sequence below in one or more lines
            fout.write(f">{code}\n{sequence}\n")
