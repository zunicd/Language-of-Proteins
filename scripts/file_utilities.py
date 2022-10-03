# Collection of file utilities
#    file_paths - prepare paths for files and folders
#    convert_h5_to_pt - convert h5 files to pt files
#    emb_files_stats - prints stats for embedding folders
#    read_embeddings - read embeddings from pt files
#    check_with_df - check our data using DataFrame displaying few rows only

# Import dependencies
import os
import h5py
import torch
import esm
import pandas as pd

# Prepare file paths
def file_paths(ptmodel, task, file_base, model, pool, data_folder = '../../data'):
    """ Prepare paths for files and folders

    Args:
        pt_model: pretrained models repositories - ['esm', 'prose']
        task: protein groups - ['acp', 'amp', 'dna_binding']
        file_base: ['test', 'train', 'all_data']
        model: prose - ['prose_dlm, 'prose_mt']
               esm - ['esm1v_t33_650M_UR90S_1', 'esm1b_t33_650M_UR50S']
        pool: pooling operations
                  prose - ['avg', 'max', 'sum']
                  esm - ['mean']
        data_folder: root of data folder - ['../../data'] default

    Returns:
        path_fa: path to fasta file
        path_h5: path to h5 files (prose only)
        path_pt: path to pt files
    """
    # Initialize path variables for correct return output when there is an error
    path_pt, path_h5, path_fa = '', '', ''
    prose_ptm = ['prose_dlm', 'prose_mt']
    esm_ptm = ['esm1v_t33_650M_UR90S_1', 'esm1b_t33_650M_UR50S']
    
    # Check models
    if ptmodel == 'prose':
        if model in prose_ptm:
            mabr = model.split('_')[1]
        else:
            print('Incorrect model name!')
            return path_pt, path_h5, path_fa
    elif ptmodel == 'esm':
        if model in esm_ptm:
            mabr = model.split('_')[0]
        else:
            print('Incorrect model name!')
            return path_pt, path_h5, path_fa
    else:
        print('Incorrect pretrained model source!')
        return path_pt, path_h5, path_fa

    
    # Update task folder for dbp
    task_folder = task
    if task == 'dbp':
        task_folder = 'dna_binding'
        file_base_m = f'{file_base}_{ptmodel}'
    else:
        file_base_m = file_base
    
    data_path = os.path.join(data_folder, task_folder)
    # find fasta file for train/test/all
    files = os.listdir(data_path)
    for f in files:
        if file_base_m in f and 'fa' in f:
            file_fa = f
    
    # Path for fasta file
    path_fa = os.path.join(data_path, file_fa)
    
    # Subfolder for embeddings (.pt files)
    if task == 'amp':
        sfolder_pt = f'{task}_all_{mabr}_{pool}'
    else:
        sfolder_pt = f'{task}_{file_base}_{mabr}_{pool}'

        
    file_h5 = f'{sfolder_pt}.h5'
    path_emb = os.path.join(data_path, ptmodel, file_base)
    # Psth for h5 files (prose only)
    if ptmodel == 'prose':
        path_h5 = os.path.join(path_emb, file_h5)
    # Path for pt files
    path_pt = os.path.join(path_emb, sfolder_pt)
    
    return path_pt, path_h5, path_fa


# Converts h5 file to pt files, one per each sequence embedding.
def convert_h5_to_pt(path_h5, path_pt, pool):
    """ Convert h5 files to pt files (used for prose only)

    Args:
        path_h5: path to h5 files
        path_pt: path to pt files
        pool: pooling operation

    Returns:
        Saving pt files with embeddings
    """
    os.makedirs(path_pt, exist_ok=True)
    with h5py.File(path_h5, 'r') as hf:
        dd = {}
        for key in hf.keys():
            
            dd['label'] = key
            t = torch.tensor(hf.get(key))
            dd[f'{pool}_representations'] = {'layer': t}
            torch.save(dd, f'{os.path.join(path_pt, key)}.pt')
 
# Prints the total size and number of pt files in embedding folders
def emb_files_stats(path_pt):
    """ Prints stats for embedding folders
    Args:
        path_pt: path to pt files,       

    Returns:
        Prints total size and number of pt files per folder
    """
    base = os.path.split(path_pt)[0]
    j = 0
    # Generate directory tree
    for root, dirs, files in os.walk(base):
        # skip stats for base folder
        if j == 0:
            j += 1
            continue
       # Stats for all subfolders
        tail = os.path.split(root)[1]
        # Calculate the total size of all files in a subfolder
        tail_size = round(sum(os.path.getsize(os.path.join(root, name)) for name in files)/1024/1024, 2)
        
        print(f'{tail} consumes: {tail_size}MB in {len(files)} files')
        j += 1
        

# Extract embeddings, target labels, sequential ids from pt files
def read_embeddings(path_fa, path_pt, pool, emb_layer, print_dims=True):
    """ Read embeddings from pt files
    Args:
        path_fa: path to fasta file 
        path_pt: path to pt files folder
        pool: pooling operations used 
        emb_layer: layer from which embeddings are extracted,
                   for prose we are using string 'layer'
        print_dims: do not print dimms when modelling 

    Returns:
        Xs: an array of embeddings
        ys: our target labels
        seq_id: sequence ids 
        
    """
    # Initialize lists
    ye = []
    Xe = []
    seq_id = []
    
    # Read fasta headers and iterate through them
    for header, _seq in esm.data.read_fasta(path_fa):
        # Extract target label from each entry and append to list
        label = header[-1]
        ye.append(int(label))
        # Extract sequence ids and append to list
        # Below code is used due to existence of an additional "|" 
        #  in fasta header for dna_binding test dataset
        seq_id.append(header.split('|', 1)[-1][:-2])
        # Embeddings are stored with the file name from fasta header
        fn = f'{path_pt}/{header[1:]}.pt'
        # Load the file
        embs = torch.load(fn)
        # Extract embedding tensor and append it to list
        Xe.append(embs[f'{pool}_representations'][emb_layer])
    # Concatenate embeding tensors from the list and convert to an array
    Xe = torch.stack(Xe, dim=0).numpy()
    
    if print_dims:
        print(f'Shape of embeddings: \t\t{Xe.shape}')
        print(f'Length of target label list:\t{len(ye)}')
        print(f'Length of sequential ids list:\t{len(seq_id)}')

    return Xe, ye, seq_id


# Check our data after extraction
def check_with_df(Xs, ys, seq_id, n=2):
    """Check our data using dataframe displaying few rows only 
    Args:
        Xs: an array of embeddings
        ys: our target labels
        seq_id: sequence ids 
        n: number of rows to display as head and tail

    Returns:
        Displays dataframe with first and last 'n' lines  
    """
    # Create datframe from Xs and seq_id first
    df = pd.DataFrame(Xs, index=seq_id ).reset_index().rename(columns={'index':'sequence'})
    # Concatenate it with target labels dataframe
    df = pd.concat([df, pd.DataFrame(ys, columns =['label'])], axis=1)
    # Display a short version of dataframe
    with pd.option_context('display.max_rows', n*2):
        display(df)
