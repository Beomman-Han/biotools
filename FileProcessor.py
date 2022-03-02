from abc import ABC, abstractmethod
import io

class FileProcessor(ABC):
    """Abstract class for processing file
    
    FASTA - 
    VCF - 
    GTF *
    GFF *
    """

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