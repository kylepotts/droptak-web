import sys
import os

def fix_path(root): 
    sys.path.insert(0, os.path.join(root, 'lib'))