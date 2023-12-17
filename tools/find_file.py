import os

def find_file(file_name='', directory=''):
    if not file_name or not directory:
        return None
    # Search for the file in the specified directory
    full_path = os.path.join(directory, file_name)
    if os.path.isfile(full_path):
        return f'The file {file_name} was found at {directory}'
    else:
        return f'The file {file_name} was not found in {directory}'