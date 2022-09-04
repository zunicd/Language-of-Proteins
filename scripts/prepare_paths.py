# Prepare file paths
import os
def file_paths(ptmodel, task, file_base, model, pool, data_folder = '../data'):
    """ Convert csv files to fasta files

    Args:
        pt_model: 
        task: 
        file_base:
        model:
        pool:
        data_folder:

    Returns:
        path_fa: path to fasta file
        path_h5: path to h5 files (prose only)
        path_pt: path to pt files
    """
    # Initialize path variables for correct return output when there is an error
    path_pt, path_h5, path_fa = '', '', ''
    prose_ptm = ['prose_dlm', 'prose-mt']
    esm_ptm = ['esm1v_t33_650M_UR90S_1']
    
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