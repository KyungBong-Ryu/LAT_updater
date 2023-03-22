import os
import argparse

def update_atime(in_path, prev_count_suc_file=0, prev_count_suc_folder=0, prev_count_err=0):
    # _count_suc
    _count_suc_file     = 0     # count updated files
    _count_suc_folder   = 0     # count updated folders
    _count_err          = 0     # count failures
    
    # update input path folder
    try:
        os.utime(in_path, None) # update atime to now
        _count_suc_folder += 1
    
        # update files and folders inside the input path
        in_list = os.listdir(in_path)
        for i_name in in_list:
            _curr = in_path + "/" + i_name
            
            if os.path.isfile(_curr):
                # it is a file
                try:
                    os.utime(_curr, None) # update to now
                    _count_suc_file += 1
                except:
                    print("")
                    print("FAILED UPDATE:", _curr)
                    print("")
                    _count_err += 1
                
            else:
                # it is not a file
                _c_suc_file, _c_suc_folder, _c_err = update_atime(_curr
                                                                 ,_count_suc_file
                                                                 ,_count_suc_folder
                                                                 ,_count_err
                                                                 )
                _count_suc_file     += _c_suc_file
                _count_suc_folder   += _c_suc_folder
                _count_err          += _c_err
            
            print("\rUpdated "
                 ,prev_count_suc_file   + _count_suc_file,   " files, "
                 ,prev_count_suc_folder + _count_suc_folder, " folders, with "
                 ,prev_count_err        + _count_err,        " error."
                 ,end = "")
        
    except:
        print("")
        print("FAILED UPDATE:", in_path)
        print("")
        _count_err += 1
    
    return _count_suc_file, _count_suc_folder, _count_err

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update last-access-time of file and folder to prevent auto-erase')
    parser.add_argument("--path", type = str, default = None, help = "input path for update last-access-time")
    args = parser.parse_args()
    
    print("---[ Update last-access-time of file and folder started ]---")
    
    if args.path is None:
        print("ERROR: You must input a top path!!!")
    else:
        print("Top path:", args.path)
        print("")
        count_suc_file, count_suc_folder, count_err = update_atime(args.path)
        print("\n\nUpdate result:", count_suc_file, "files,", count_suc_folder - 1, "+ 1 folders, with", count_err, "error.")
    
    print("")
    print("---[ Update last-access-time of file and folder finished ]---")