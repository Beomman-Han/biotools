import os, sys
import re
import json

from typing import Dict, TextIO, Tuple, Type, Generator

from File import File
from FASTA.Seq import Seq
from FASTA.Constant import *

__all__ = ('SeqRecord', 'FASTA')

class SeqRecord:
    def __init__(
        self,
        seq,
        title: str,
        description: str,
        ) -> None:
        
        """SeqRecord class for recording sequence info (FASTA)

        Parameters
        ----------
        seq : str
            Sequence information
        title : str
            Title of sequence (ex. '>title')
        description : str
            Description of sequence
        """
        
        self.seq = seq
        self.title = title
        self.description = description
        
        return
    
    def rename_title(self, new_title: str) -> Type['SeqRecord']:
        """Return new SeqRecord instance with new title and same content"""
        
        new_seqrecord = SeqRecord(self.seq, new_title, self.description)        
        return new_seqrecord

    def __str__(self) -> str:
        res_str = ''
        res_str += f'>{self.title} {self.description}\n'
        res_str += f'{self.seq}'
        return res_str

class FASTA(File):
    """Class supports functions that process FASTA format file
    
    Example
    -------
    >>> import sys
    >>> sys.path.appned('/Users/hanbeomman/Documents/project/')
    >>> from biotools.FASTA import FASTA
    >>> fa = FASTA('/Users/hanbeomman/Documents/project/biotools/FASTA/test.fa')
    >>> fa.open()
    >>> fa.close()
    """
    
    def __init__(self, path: str) -> None:
        """Initialize FASTA class

        Parameters
        ----------
        path : str
            Absolute path of .fasta file
        """
        
        self.path = os.path.abspath(path)
        self.open_obj = False
        
        return
    
    def __del__(self):
        if self.open_obj:
            print('close File')
            self.close()
    
    def open(self,
        mode : str = "r"
        ) -> None:
        
        """Open fasta file (self.path) to self.open_obj

        Parameters
        ----------
        mode : str
            Open mode (r, w, ...)
        """
        
        if self.open_obj:
            print('Current open_obj is already opened.')
        else:
            self.open_mode = mode
            self.open_obj = open(self.path, mode)
        
        return
    
    def close(self) -> None:
        """Close self.open_obj attribute"""
        self.open_obj.close()
        self.open_obj = False
        return
    
    def readline(self):
        ...
        
    def reader(self) -> Generator[SeqRecord, None, None]:
        """Generator function parsing fasta format contents

        Yields
        ------
        SeqRecord
            SeqRecord instance with contig name, description, sequence
        """
        
        if not self.open_obj:
            print(f'[ERROR] {self.path} is not opened.')
            return
    
        sequences = []
        for line in self.open_obj:
            if line.startswith('>'):
                if len(sequences) != 0:
                    yield SeqRecord(''.join(sequences), title, desc)
                    
                title = line.strip().split()[0][1:]
                try: desc = ' '.join(line.strip().split()[1:])
                except: desc = ''
                sequences = []
            else:
                sequences.append(line)
        yield SeqRecord(''.join(sequences), title, desc)
    
    def write(self,
        title : str,
        sequence : str,
        desc : str = None
        ) -> None:
        
        """Write file by line

        Parameters
        ----------
        title : str
            Title of sequence
        seqence : str
            Sequence string
        desc : str, optional
            Description of sequence, by default None
        """
        
        if 'r' in self.open_mode:
            print('Current open_obj is "read" mode')
        
        elif 'w' in self.open_mode:
            fasta_title = f'>{title}'
            if desc:
                fasta_title += f' {desc}'
            self.open_obj.write(f'{fasta_title}\n')
            self.open_obj.write(sequence)

        return
    
    def export_to_json(self,
        output_name : str,
        seq_dict : dict = False
        ) -> None:
        
        """Export fasta contents to json format file.
        If 'seq_dict' param is False, then export with self.path fasta info.

        Parameters
        ----------
        output_name : str
            Output file name
        seq_dict : dict, optional
            SeqRecord dictionary, by default False
        """
        
        json_dic = {}
        if not seq_dict:
            for record in self.parse(open(self.path)):
                title = record.title
                json_dic[title] = { 'seq': str(record.seq),
                                    'description': record.description
                                    }
        else:
            for title in seq_dict:
                record = seq_dict[title]
                json_dic[title] = { 'seq': str(record.seq),
                                    'description': record.description
                                    }
        json.dump(json_dic, open(output_name, 'w'), indent=4)
        return
    
    def import_from_json(self, json_file: str = False) -> dict:
        """Data import from json

        Parameters
        ----------
        json_file : str, optional
            _description_, by default False

        Returns
        -------
        dict
            _description_
        """
        
        if not json_file: json_file = self.path
        result_dict = {}
        json_dic = json.load(open(json_file))
        for title in json_dic:
            seq = Seq(json_dic[title]['seq'])
            try: description = json_dic[title]['description']
            except: description = ''
            result_dict[title] = SeqRecord(seq, title, description)
            
        return result_dict
    
    # def iterate(self, handle : Type["SeqRecord"]) -> Type["SeqRecord"]:
    def iterate(self, handle: TextIO) -> Generator[Type['SeqRecord'], None, None]:
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
        for title, description, seq in self.readline(handle):
            check_out = self.sanity_check((title, description, seq), mode="r")
            if not check_out:
                sys.exit(f'\n==// WARNING //==\n- {title} seqeunce sanity check is failure...\n')
            yield SeqRecord(seq=Seq(seq), title=title, description=description)

    def parse(self, handle: TextIO) -> Generator[Type['SeqRecord'], None, None]:
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

    def to_dict(self, handle: TextIO) -> Dict[str, Type['SeqRecord']]:
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

    def sanity_check(self,
        target_seq : Tuple[str],
        mode : str,
        verbose : bool = False
        ) -> bool:
       
        """Check whether input sequence info ('target_seq') is normal format.

        Parameters
        ----------
        target_seq : Tuple[str]
            Sequence info (title, desc, seq)
        mode : str
            Check mode
        verbose : bool
            Print process message
            (True = Print check message,
            False = Silent mode)
            
        Returns
        -------
        bool
            Whether target_seq parameter is normal foramt
        """

        if verbose: print(f'file format is fasta. \nStart the sanity check for {target_seq[0]}')
    
        if mode == "r":
            check_base = [base in BASE_IUPAC for base in target_seq[2].strip()]
            check_bool: bool = all(check_base)
            true_list = list((filter(lambda x: x, check_base)))
            if check_bool == False:
                misbase_list = [ (target_seq[2][i],i+1) for i, b in enumerate(check_base) if b == False]
                if verbose: print(f'Please enter a valid seq : \n(misbase,seq position. : {misbase_list} \n')
            if check_bool == False:
                if verbose: print("Check the seq")
                return False
            else:
                if verbose: print("Seq is normal.")
                return True

    def find_seq(self, seq: str) -> None:
        fasta_obj = open(self.path,"r")
        p = re.compile(seq)
        for fasta in self.readline(fasta_obj):
            matched_iter = p.finditer((fasta[2]))
            for target in matched_iter:
                print(f'find seq in {fasta[0]} ==> start : {target.start()+1}, end : {target.end()+1}')

    def find_title(self,title:str) -> None:
        fasta_obj = open(self.path,"r")
        p = re.compile(title)
        for fasta in self.readline(fasta_obj):
            matched_iter = p.finditer((fasta[0]))
            for target in matched_iter:
                print(f'find title : {fasta[0]}')

    def rename_title(self, convert_file: str, new_file: str) -> None:
        """Rename titles from convert_file and write file with new title
        
        convert_file:
        old_title\tnew_title\n
        """

        titles = dict()
        convert_file = open(convert_file, 'r')
        for line in convert_file:
            cols = line.strip().split('\t')
            titles[cols[0]] = cols[1]
        convert_file.close()
        
        new_fa = FASTA(new_file)
        new_fa.open(mode='w')
        
        for seq in self.reader():
            new_seq = seq.rename_title(titles[seq.title])
            new_fa.write(new_seq.title, new_seq.seq, new_seq.description)
        new_fa.close()
        
        return

def _test():
    import doctest
    
    doctest.testmod()

if __name__ == "__main__":

    # fa = FASTA('/Users/hanbeomman/Documents/project/mg-bio/FASTA/test.fa')
    # fa.open()
    # # for seq in fa.reader():
    # #     print(seq)
    
    # seq = SeqRecord('AAAA', 'chr1', 'chromosome 1')
    # print(seq)
    
    # # fa.rename_title('')
    # fa.rename_title('/Users/hanbeomman/Documents/project/mg-bio/FASTA/test.tsv', '/Users/hanbeomman/Documents/project/mg-bio/FASTA/new_test.fa')
    
    _test()