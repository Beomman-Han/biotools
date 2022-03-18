from abc import ABC, abstractmethod
import io

class File(ABC):
    """Abstract class for child classes which support functions processing file
    containig biological information
    
    Child Class
    -----------
    FASTAProcessor
        Implemented (last at 2022/03/13)
    *BAMProcessor
        On going
    
    Candidates
    ----------
    *VCFProcessor
        (to be implemented)
    *GTFProcessor
        (to be implemented)
    *GFFProcessor
        (to be implemented)
        
    Interface
    ---------
    sanity_check()
    open()
    close()
    readline()
    write()
    import_from_json()
    export_to_json()
    """

    @abstractmethod
    def sanity_check(self) -> bool:
        """Open file"""
        pass
    
    @abstractmethod
    def open(self, mode: str) -> io.BufferedReader or io.BufferedWriter:
        """Open file"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close file"""
        pass

    @abstractmethod
    def readline(self, skip_header: bool) -> str:
        """Read file by line

        Parameters
        ----------
        None

        Returns
        -------
        str
        > line from a line
        """
        pass

    @abstractmethod
    def write(self, line: str) -> None:
        """Write file by line

        Parameters
        ----------
        line: str
            A line for writing file
        """
        pass
    
    @abstractmethod
    def import_from_json(self, json_file: str) -> dict:
        """import json by dictionary 

        Parameters
        ----------
        json_dict : dict
            Dictionary type
        """
        pass
    
    @abstractmethod
    def export_to_json(self, json_dict: dict) -> None:
        """Write json by dictionary 

        Parameters
        ----------
        json_dict : dict
            Dictionary type
        """
        pass
    