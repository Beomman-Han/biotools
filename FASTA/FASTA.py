from typing import Dict, TextIO, Tuple, Type, Generator

from SeqRecord import SeqRecord
from Seq import Seq
# from FileProcessor import FileProcessor

class FASTAProcessor(object):
    """Class supports functions that process FASTA format file"""
    
    def __init__(self, path : str) -> None:
        """Initialize FASTAProcessor class

        Parameters
        ----------
        path : str
            path of .fasta file
        """
        
        self.path = path
        
        return
        
    def simple_fasta_parser(self, handle : TextIO) -> Generator[Tuple[str], None, None]:
        """Generator function parsing fasta format contents

        Parameters
        ----------
        handle : TextIO
            TextIO of fasta file

        Yields
        ------
        Tuple[str]
            tuple of contig name, description, sequence
        """
        
        sequences = []
        for line in handle:
            if line.startswith('>'):
                if len(sequences) != 0:
                    yield(title, desc, ''.join(sequences))
                    
                title = line.strip().split()[0][1:]
                try: desc = ' '.join(line.strip().split()[1:])
                except: desc = ''
                sequences = []
            else:
                sequences.append(line.strip())
        yield title, desc, ''.join(sequences)

    # def iterate(self, handle : Type["SeqRecord"]) -> Type["SeqRecord"]:
    def iterate(self, handle : TextIO) -> Generator[Type['SeqRecord'], None, None]:
        """Generate function yield SeqRecord object from TextIO

        Parameters
        ----------
        handle : TextIO
            TextIO of fasta file


        Yields
        ------
        SeqRecord
            SeqRecord object containing sequence, title, description
        """
        for title, description, seq in self.simple_fasta_parser(handle):
            yield SeqRecord(seq=Seq(seq), title=title, description=description)

    def parse(self, handle : TextIO) -> Generator[Type['SeqRecord'], None, None]:
        """Start parsing fasta file

        Parameters
        ----------
        handle : TextIO
            TextIO of fasta file

        Returns
        -------
        Generator
            self.iterate generator function
        """
        record = self.iterate(handle)
        return record

    def to_dict(self, handle : TextIO) -> Dict[str, Type['SeqRecord']]:
        """Make dict with {title: SeqRecord object} <- FIXME why make it?

        Parameters
        ----------
        handle : TextIO
            TextIO of fasta file

        Returns
        -------
        Dict[str, Type['SeqRecord']]
            dictionary which consists of {title : SeqRecord object}

        Raises
        ------
        ValueError
            Error occurs when duplicate title is in fasta file
        """
        
        record_dict = {}
        for record in self.parse(handle):
            data_id = record.title
            if data_id in record_dict:
                raise ValueError(f"Duplicate key '{data_id}'")
            else:
                record_dict[data_id] = record
        return record_dict

if __name__ == "__main__":
    
    fasta_fn = 'RGS14_cDNA.fasta'
    
    # seq Iterator
    #RGS14_cDNA = Fasta()
    #for i, record in enumerate(RGS14_cDNA.parse(open(fasta_fn)), 1):
        #if i == 10: break
        #print(record.title)
        #print(i, record.title, record.description, '%s...' % record.seq[:10])
        #print(dir(record))
     
    #record = RGS14_cDNA.parse(open(fasta_fn))
    #data1 = next(record) # 1
    #print(data1.title, data1.description, data1.seq[:10])
    #data2 = next(record) # 2
    #print(data2.title, data2.description, data2.seq[:10])
    
    #record_dict = RGS14_cDNA.to_dict(open(fasta_fn))
    #print(list(record_dict.keys())[0])
