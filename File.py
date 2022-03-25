from abc import ABC, abstractmethod
import io
from typing import Generator

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
    reader()
    write()
    """

    @abstractmethod
    def sanity_check(self) -> bool:
        """Check integrity of file"""
        ...
    
    @abstractmethod
    def open(self, mode: str) -> io.BufferedReader or io.BufferedWriter:
        """Open file"""
        ...

    @abstractmethod
    def close(self) -> None:
        """Close file"""
        ...

    @abstractmethod
    def readline(self, skip_header: bool) -> str:
        """Read file by one line"""
        ...
        
    def reader(self) -> Generator:
        """Reader object to read file"""
        ...

    @abstractmethod
    def write(self, line: str) -> None:
        """Write one line at file"""
        ...
