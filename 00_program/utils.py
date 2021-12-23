import sys, os, shutil
#-------------------
def get_mod_fname_from_path(path_to_file, mod):
    
    path_without_file_ext = os.path.splitext(path_to_file)[0]
    name = os.path.split(path_without_file_ext)[1]
    ext = os.path.splitext(path_to_file)[1]
    file_name = "{0}{1}{2}".format(name, mod, ext)
    
    return file_name
#-------------------
def copy_files_to_folder(list_of_paths, output_folder):
    """takes an input list of paths and a path to
    an output folder, copies files to folder"""
    
    try:
        os.path.isdir == True
    except AssertionError:
        print('your input dir path was not a directory')    
 
    for path in list_of_paths:
        file_name = os.path.basename(path)
        new_file_path = os.path.join(output_folder, file_name)
        shutil.copy(path, new_file_path)
        
    #print('Done\n')
#-------------------
def make_dirs(path_to_dir, dir_name, overwrite_dirs = False, verbose = 0):
    """takes an input path and a name of 
    dir to make. create dir in the input path
    
    process
    -------
    - checks for user invalid inputs
    - concatenates dir_name to path
    - creates dir in path 
    - if dir exists, creates dir_name_1 or overwrites dir (depending on overwrite_dir input)
    - returns path to dir. 
    
    parameters
    ----------
    path_to_dir: str
        path to create the dir
    dir_name: str
        name of dir to create
    overwrite_dirs: bool
        if True, if the dirname already exists, it is overwritten,
        else an error is raised.
 
    returns 
    -------
    str"""
        
    try:
        assert os.path.isdir(path_to_dir) == True
    except AssertionError:
        print('your input dir path was not a valid dir path: {}'.format(path_to_dir))
    
    dir_path = os.path.join(path_to_dir, dir_name)
    name_copy_number = 1
    
    if (overwrite_dirs == False) or (overwrite_dirs == 'False'): 
        while os.path.exists(dir_path):
            new_dir_name = "{}_{}".format(dir_name, name_copy_number)
            dir_path = os.path.join(path_to_dir, new_dir_name)
            name_copy_number += 1
                
    os.makedirs(dir_path, exist_ok = overwrite_dirs)
        
    return dir_path
#--------------------------------------------------------------------
def get_file_paths_from_dir(dir_path, ext = None, verbose = 0):
    """takes an input directory and returns
    a list of files in that directory. given
    an input file extension, only files with
    that ext. are included in the list.
    
    parameters
    ----------
    input_cwd: str
       path to directory
    ext: None
       extension to use to filter for file types
    verbose: 0,1
        set to 1 for debugging
    
    returns
    -------
    list"""
    
    # checks if input type is valid
    #check_input_type(str,'your input was not a valid type', dir_path)
    
    # get files and folder in cwd
    dir_path = os.path.abspath(dir_path)
    files_folders_in_cwd = os.listdir(dir_path)
    list_of_files = []
    
    # loops over file_folder list and appends file
    # names to list, if ext is specified by the user,
    # only files with the .ext are appended to the list.
    # otherwise, all files are appended to the list.
    for item in files_folders_in_cwd:
        path_to_item = os.path.join(dir_path, item) # allows returning full path of file
        
        if os.path.isfile(path_to_item) == True: 
            if ext != None:    # this allows filtering for files with specific exts.
                
                if type(ext) == list: # this allows fetching files with different .exts
                    for extension in ext:
                        if item.endswith(extension):
                            list_of_files.append(path_to_item)
                else:
                    item.endswith(ext)
                    list_of_files.append(path_to_item)
            else:
                list_of_files.append(path_to_item)
                
    return list_of_files
#------------------------------------
def conv_nested_list_to_list(nlist_var, verbose = 0, none_if_error = True): 
    """takes an input list of lists (nested list). and 
    extracts all 'inner' list elements into the main list,
    making a 1 dimensional list.
    
    strategy
    --------
    -loops list and appends list items to a new list var.
    when the item is a list(inner list), the inner list is
    also looped and its items are appended to the new list. 
    
    parameters
    ----------
    nlist_var: list of list
        nested list to process
    verbose: 0,1
        optional parameter for debugging

    returns
    -------
    list"""

    # prints error message for invalid input
    try:
        assert isinstance(nlist_var, list)
    except:
        if none_if_error == True:
            return None
        else:
            print('your input was not a list')
    #check_input_type(list,'your input was not a list', nlist_var)
    
    new_list = [] # this allows appending items of list and inner list 
    
    
    # loops list and checks if each item is a list
    # if true, loops inner list and appends its elements to the new list
    # else, appends the items to the new list
    for item in nlist_var: 
        if is_list(item) == True:
            items = conv_nested_list_to_list(item)
            new_list.extend(items)
        else:
            new_list.append(item)
            
        if verbose == 1: 
            print("current list item: {0}".format(item))
            
    if verbose == 1: 
        print('created list: {}'.format(new_list))

    return new_list