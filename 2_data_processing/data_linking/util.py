import os
from pathlib import Path
from os import listdir
from os.path import isfile, join

def get_files_for_folder(folder_path):
    files = []
    working_dir = Path(__file__).parent.parent.parent
    folderPath = os.path.join(working_dir, folder_path)
    for f in listdir(folderPath):
        if isfile(join(folderPath, f)) and not '.DS_Store' in f:
            files.append(join(folderPath, f))
    return files