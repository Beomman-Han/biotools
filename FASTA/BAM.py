import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  ## FIXME
from FileProcessor import FileProcessor


class BAMProcessor(FileProcessor):
    """Class for supporting functions processing BAM format file

    Parameters
    ----------
    FileProcessor : FileProcessor
        Parent class
    
    Interfaces
    ----------
    sanity_check()
    open()
    close()
    readline()
    write()
    import_from_json()
    export_to_json()
    """
    
    def __init__(self):
        pass    
    def sanity_check(self):
        pass
    def open(self):
        pass
    def close(self):
        pass
    def readline(self):
        pass
    def write(self):
        pass
    def import_from_json(self):
        pass
    def export_to_json(self,):
        pass