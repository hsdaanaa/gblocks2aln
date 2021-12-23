import sys, os
#----------------------------------------
def fasta_to_dict(input_path):
    """takes an input path to a fasta file and delimiters between 
    an identifier, creates a dictionary with identifier: sequence"""
    
    cds_seq_dict = {}

    with open(input_path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                cds_name = line[1:]
                cds_name = cds_name.rstrip('\n')
                key = line[1:].rstrip('\n')
                cds_seq_dict[cds_name] = ''
            else:
                cds_seq_dict[cds_name] += line.rstrip('\n')
        
    return cds_seq_dict
#------------------------------------------------------------------------
def dict_to_fasta(dict_var, path_to_output_file, output_file_name):
    """outputs a dictionary to a fasta formatted file. cds names should be
    keys and values should be sequences"""

    # make file name
    file_name = os.path.join(path_to_output_file, output_file_name)
    # open file 
    file_obj = open(file_name, 'w')
     # loop over dictionary keys and writes cds_name/sequence lines.
    for cds_name in dict_var.keys():
            seq = ''.join(dict_var[cds_name]) # gets cds_sequence from dictionary of cds
            # writes data into file
            cds_name = cds_name.rstrip('\n')
            file_obj.write('>{}\n{}\n'.format(cds_name, seq))
            
    file_obj.close() 
#------------------------------------------------------------------------ 
