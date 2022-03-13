import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  ## FIXME
from FileProcessor import FileProcessor


class BAMProcessor(FileProcessor):
    """Class for supporting functions processing BAM format file

    Parameters
    ----------
    FileProcessor : FileProcessor
        Parent class
    """
    
    def __init__(self):
        pass
    