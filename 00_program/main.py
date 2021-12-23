#!/usr/bin/env python3
import sys, os, shutil, time, pandas as pd
from multiprocess import Pool
from utils import get_file_paths_from_dir, copy_files_to_folder, make_dirs
from seq_utils import fasta_to_dict, dict_to_fasta
#---------------------------------------------------------------------------
def add_gblocks_marker_to_alns(aln_dir, 
                               out_dir,
                               max_len_for_uncon_block, 
                               min_seq_for_flank, 
                               min_seq_for_cons, 
                               min_block_len, 
                               gap_block_stat = 'n', 
                               seq_type = 'c', 
                               ext = '.aln',
                               threads = 4, 
                               dataset_name = 'gblocks_out',
                               verbose = 1): 
    """"""
    gblocks_out_path = make_dirs(out_dir, dataset_name)
    log_file_path    = os.path.join(out_dir, 'log.txt') 
    
    with open(log_file_path, 'w') as file: 
        file.write('add_gblocks_marker_to_alns\n')
        file.write('--------------------------\n')
        file.write('start time              : {}\n'.format(time.ctime()))
        file.write('aln dir                 : {}\n'.format(aln_dir))
        file.write('suffix of aln files     : {}\n'.format(ext))
        file.write('out dir                 : {}\n'.format(out_dir))
        file.write('dataset name            : {}\n'.format(dataset_name))
        file.write('max_len_for_uncon_block : {}\n'.format(max_len_for_uncon_block))
        file.write('min_seq_for_flank       : {}\n'.format(min_seq_for_flank))
        file.write('min_seq_for_cons        : {}\n'.format(min_seq_for_cons))
        file.write('min_block_len           : {}\n'.format(min_block_len))
        file.write('gap_block_stat          : {}\n'.format(gap_block_stat))
        file.write('seq_type                : {}\n'.format(seq_type))
        file.write('threads                 : {}\n'.format(threads))
        file.write('verbose                 : {}\n'.format(verbose))
        file.write('---------processing-------\n')
    
        # create arguments 
        aln_paths = get_file_paths_from_dir(aln_dir, ext = [ext])
        file.write('number of alignments: {}\n'.format(len(aln_paths)))
        if verbose == 1:
            print('creating arguments for multiproc run')
        
        args = [[os.path.relpath(aln_path), gblocks_out_path,
                             max_len_for_uncon_block, min_seq_for_flank, 
                             min_seq_for_cons, min_block_len, 
                             gap_block_stat, seq_type, verbose] for aln_path in aln_paths]
        
        with Pool(processes = threads) as p: 
            p.map(wrap_add_gblocks_marker_to_aln, args)
        
        file.write('endtime: {}'.format(time.ctime()))
    print('Done. check: {}'.format(gblocks_out_path))
#---------------------------------------------------------------------------
def wrap_add_gblocks_marker_to_aln(args): 
    
    return add_gblocks_marker_to_aln(aln_path               = args[0], 
                                    out_dir                 = args[1],
                                    max_len_for_uncon_block = args[2],
                                    min_seq_for_flank       = args[3],
                                    min_seq_for_cons        = args[4],
                                    min_block_len           = args[5],
                                    gap_block_stat          = args[6],
                                    seq_type                = args[7],
                                    verbose                 = args[8])
#---------------------------------------------------------------------------
def add_gblocks_marker_to_aln(aln_path, out_dir,
                             max_len_for_uncon_block, min_seq_for_flank, 
                             min_seq_for_cons, min_block_len, 
                             gap_block_stat = 'n', seq_type = 'c', 
                             verbose = 0):
    """takes an input path to an alignment and returns an alignment with a 
    gblocks marker that specifies sites that would be retained or will be 
    filtered by gblock
    
    gblocks parameters (taken from Gblocks documentation; see /exe/Gblock_ISX_0.91b.tar.Z): 
    
        - max_len_for_uncon_block : Maximum number of contiguous non conserved positions 
        - min_seq_for_flank       : Minimum number of Sequences for a flank position
        - min_seq_for_cons        : Minimum number of sequences for a conserved position
        - min_block_len           : Minimum length of a block # should be 2 or greater
        - gap_block_stat          : Allowed Gap Positions (None, With Half, All)	n, h, a
        - seq_type                : type of sequence (can be protein (p), DNA (d) or codons (c))

    Other parameters 
    ----------------
    path: str
        path to alignment file
    outpath: str
        path to output folder
    gblocks_path: str
        path to Gblocks exectutable
    verbose: int 0, 1
        set to 1 for debugging output
    
    returns 
    -------
    str"""

    aln_path = os.path.relpath(aln_path)
                 
    command = 'exe/Gblocks {} {} -t={} -e=.gbm -k=y -b3={} -b2={} -b1={} -b4={} -b5={} g'.format(aln_path, out_dir, 
                                                                                                 seq_type, 
                                                                                                 max_len_for_uncon_block, 
                                                                                                 min_seq_for_flank,  
                                                                                                 min_seq_for_cons, 
                                                                                                 min_block_len, 
                                                                                                 gap_block_stat)
    # run gblocks
    if verbose == 1: 
        print('command passing to shell: {}\n'.format(command))
        print('running command\n')
        
    os.system(command)
    if verbose == 1: 
        print('extracting gblocks output file paths\n')

    # find gblocks files
    dir_paths     = get_file_paths_from_dir(os.path.dirname(aln_path))
    gblocks_files = [i for i in dir_paths if os.path.basename(aln_path) + '.gbm' in i]
    if verbose == 1: 
        print('creating marker sequence\n')
    
    # convert blocks to coordinate in sequence
    maskfile = fasta_to_dict(aln_path + '.gbmMask')
    mask_seq = maskfile[[i for i in maskfile if 'Gblocks' in i][0]].replace('#', 'C').replace('.', "N").rstrip('*').replace(' ','') # 
#     dir_paths = [i for i in dir_paths if not i == '00.filelist']trip('*').replace(' ','') # 
    if verbose == 1:
        print('copying gblocks files to output dir\n')
 
    # should move gblock files elsewhere
    copy_files_to_folder(gblocks_files, out_dir)
    
    # deletes gblocks outputs from initial path
    [os.remove(i) for i in gblocks_files]
        
    # make gblocks marker name with param values
    marker_name = 'gbs_{}_{}_{}_{}_marker'.format(max_len_for_uncon_block, min_seq_for_flank, min_seq_for_cons, min_block_len)
        
    # open alignment file 
    aln              = fasta_to_dict(aln_path)
    
    # add gblocks marker to alignment
    aln[marker_name] = mask_seq
    
    dict_to_fasta(aln, out_dir, os.path.basename(aln_path) + '_{}_{}_{}_{}.gbsm.aln'.format(max_len_for_uncon_block, min_seq_for_flank, min_seq_for_cons, min_block_len))
        
    return aln
#-----------------------------
if __name__ == '__main__': 
    aln_dir                 = sys.argv[1]
    out_dir                 = sys.argv[2]
    max_len_for_uncon_block = int(sys.argv[3])
    min_seq_for_flank       = int(sys.argv[4])
    min_seq_for_cons        = int(sys.argv[5])
    min_block_len           = int(sys.argv[6])
    gap_block_stat          = sys.argv[7]
    seq_type                = sys.argv[8]
    ext                     = sys.argv[9]
    threads                 = int(sys.argv[10])
    dataset_name            = sys.argv[11]
    verbose                 = int(sys.argv[12])
    
    add_gblocks_marker_to_alns(aln_dir             = aln_dir,
                           out_dir                 = out_dir,
                           max_len_for_uncon_block = max_len_for_uncon_block,
                           min_seq_for_flank       = min_seq_for_flank,
                           min_seq_for_cons        = min_seq_for_cons,
                           min_block_len           = min_block_len,
                           gap_block_stat          = gap_block_stat,
                           seq_type                = seq_type,
                           ext                     = ext,
                           threads                 = threads,
                           dataset_name            = dataset_name,
                           verbose                 = verbose)