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
    *VCFProcessor
    
    Candidates
    ----------
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
    """

    @abstractmethod
    def sanity_check(self) -> bool:
        """Check integrity of file"""
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
    # def readline(self, skip_header: bool) -> str:
    def reader(self, skip_header: bool) -> str:
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
