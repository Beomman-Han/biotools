import os
from tkinter import *
from tkinter import filedialog

class File:
    """ [summary]
    A class that contains the overall information of a file received as an input.

    Methods
    -----------
    set_filepath(filepath)
    get_filepath() 
    file_stat() 
    Load()

    """
    def __init__(self, filepath :str) -> None:
        """__init__ [summary]

        initailaize object

        Parameters
        ----------
        filepath : str
            [description]
        """

        self.set_filepath(filepath) 
        self.file_stat()
        self._fileformat = os.path.splitext(self._filepath)[1]

    def set_filepath(self, filepath: str) -> None:
        """set_filepath [summary]
        
        Set the filepath attribute of the object.

        Parameters
        ----------
        filepath : str
            [description]
        """
        self._filepath = (os.path.abspath(filepath))
        #print(self._filepath)

    def get_filepath(self) -> str: 
        return self._filepath

    def get_fileformat(self) -> str:
        return self._fileformat

    def file_stat(self) -> None :
        """file_stat [summary]

        Find the stat of the file and check if the file is of the correct format.

        Raises
        ------
        Exception
            [description]

                Exception occurs when the file size is 0.
        """

        self._fileinfo = os.stat(self._filepath)
        
        if self._fileinfo.st_size == 0 :
            raise Exception(f'file size is 0 : {self._filepath}')
        


    def Load(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                            filetypes=(("fasta files", "*.fasta"),
                                            ("all files", "*.*")))
        #print(filename)

    