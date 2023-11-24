"""
COMMAND: python LAT_updater.py --path "TOP" --head "HEAD"
path: top path
head: file name head to remove. (e.g., "ToBeDelete_")

"""

import os
import argparse

# def update_atime(P_args, in_path, prev_count_suc_file=0, prev_count_suc_folder=0, prev_count_err=0, prev_count_rename=0):
    # # _count_suc
    # _count_suc_file     = 0     # count updated files
    # _count_suc_folder   = 0     # count updated folders
    # _count_err          = 0     # count failures
    # _count_rename       = 0     # count renamed files
    
    # # update input path folder
    # try:
        # os.utime(in_path, None) # update atime to now
        # _count_suc_folder += 1
    
        # # update files and folders inside the input path
        # in_list = os.listdir(in_path)
        # for i_name in in_list:
            # _curr = in_path + "/" + i_name
            
            # if os.path.isfile(_curr):
                # # it is a file
                # try:
                    # os.utime(_curr, None) # update to now
                    # _count_suc_file += 1
                # except:
                    # print("")
                    # print("FAILED UPDATE:", _curr)
                    # print("")
                    # _count_err += 1
                
                # # rename file
                # if P_args.head is not None:
                    # new_name = i_name.lstrip(P_args.head)
                    # if new_name != i_name:
                        # try:
                            # print("\nFile name changed:", i_name, "->", new_name)
                            # print("At:", in_path)
                            # os.rename(in_path + "/"+ i_name, in_path + "/"+ new_name)
                            # _count_rename += 1
                        # except:
                            # print("Rename failed: ", in_path + "/"+ i_name)
                
            # else:
                # # it is not a file
                # _c_suc_file, _c_suc_folder, _c_err = update_atime(P_args
                                                                 # ,_curr
                                                                 # ,_count_suc_file   + prev_count_suc_file
                                                                 # ,_count_suc_folder + prev_count_suc_folder
                                                                 # ,_count_err        + prev_count_err
                                                                 # ,_count_rename     + prev_count_rename
                                                                 # )
                # _count_suc_file     += _c_suc_file
                # _count_suc_folder   += _c_suc_folder
                # _count_err          += _c_err
            
            # print("\rUpdated "
                 # ,prev_count_suc_file   + _count_suc_file,   " files, "
                 # ,prev_count_suc_folder + _count_suc_folder, " folders, with "
                 # ,prev_count_err        + _count_err,        " error."
                 # ,end = "")
        
    # except:
        # print("")
        # print("FAILED UPDATE:", in_path)
        # print("")
        # _count_err += 1
    
    # return _count_suc_file, _count_suc_folder, _count_err



class CounterWithFunc():
    def __init__(self):
        # atime update counts
        self.succ_file      = 0
        self.succ_folder    = 0
        self.fail_atime     = 0
        
        # rename counts
        self.succ_rename    = 0
        self.fail_rename    = 0
    
    def update_atime(self, in_path, in_name=None):
        # in_path: 현재 경로
        # in_name: 선택한 파일 혹은 폴더 이름
        
        if in_name is not None:
            in_path = in_path + "/" + in_name
        
        try:
            os.utime(in_path, None) # update atime to now
            if os.path.isfile(in_path):
                # this is file
                self.succ_file += 1
                return "file"
            else:
                # this is folder
                self.succ_folder += 1
                return "folder"
        except:
            print("")
            print("FAILED UPDATE:", in_path)
            print("")
            self.fail_atime += 1
            return "fail"
    
    def remove_head(self, in_path, in_name, in_head=None, include_folder=True):
        # in_path: 현재 경로
        # in_name: 선택한 파일 혹은 폴더 이름
        # in_head: 삭제할 이름 접두사
        # include_folder: 폴더의 이름도 수정할 것인가?
        if in_head is None:
            pass
        else:
            if os.path.isfile(in_path) or include_folder:
                # 파일에 해당하거나, 폴더도 포함해서 수정하는 경우
                if in_head in in_name:
                    # new_name = in_name.lstrip(in_head)
                    new_name = in_name.replace(in_head, "", 1)
                    if new_name != in_name:
                        try:
                            print("\nFile name changed:", in_name, "->", new_name, "At:", in_path)
                            os.rename(in_path + "/"+ in_name, in_path + "/"+ new_name)
                            self.succ_rename += 1
                        except:
                            print("Rename failed: ", in_path + "/"+ in_name)
                            self.fail_rename += 1

def updater(P_args, CWF, curr_path, next_folder=None):
    if next_folder is not None:
        curr_path = curr_path + "/" + next_folder

    list_name = sorted(os.listdir(curr_path))
    for i_name in list_name:
        _str = CWF.update_atime(curr_path, in_name=i_name)
        if _str == "folder":
            updater(P_args, CWF, curr_path, next_folder=i_name)
        CWF.remove_head(curr_path, i_name, in_head=P_args.head, include_folder=True)
        print("\rUpdated "
             ,CWF.succ_file,   " files, "
             ,CWF.succ_folder, " folders, with "
             ,CWF.fail_atime,        " failure."
             ,end = "")
        




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update last-access-time of file and folder to prevent auto-erase')
    parser.add_argument("--path", type = str, default = None, help = "input path for update last-access-time")
    parser.add_argument("--head", type = str, default = None, help = "input file name head to remove")
    P_args = parser.parse_args()
    
    CWF = CounterWithFunc()
    
    print("---[ Update last-access-time of file and folder started ]---")
    
    if P_args.path is None:
        print("ERROR: You must input a top path!!!")
    else:
        print("Top path:", P_args.path)
        print("")
        CWF.update_atime(P_args.path) # TOP path update
        updater(P_args, CWF, P_args.path)
        
        print("\n\nUpdate result:", CWF.succ_file, "files,", CWF.succ_folder, "folders, with", CWF.fail_atime, "failure.")
        print("Rename result:", CWF.succ_rename, "files and folders are renamed, with", CWF.fail_rename, "failure.")
    
    print("")
    print("---[ Update last-access-time of file and folder finished ]---")