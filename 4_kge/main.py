from pathlib import Path
from pykeen_triples_extractor import extract_triples_from_db
import os

working_dir = Path(__file__).parent

if __name__ == '__main__':
    folder = os.path.join(working_dir, 'triples')
    if os.path.exists(folder):
        print('yes')
    print('main')
