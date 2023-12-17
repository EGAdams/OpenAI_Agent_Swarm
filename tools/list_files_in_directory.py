import os

def list_files_in_directory(directory_path):
    try:
        print( "creating file list..." )
        file_list = os.listdir(directory_path)
        print( "file_list: ", file_list )
        return file_list
    except Exception as e:
        return str(e)