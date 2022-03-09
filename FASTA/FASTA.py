import os, sys, json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from typing import Dict, TextIO, Tuple, Type, Generator
import io

from Seq import Seq
from FileProcessor import FileProcessor

import re
#from GunHyeong import sanityCheck

class SeqRecord:
    def __init__(
        self,
        seq,
        title: str,
        description: str,
    ):
        """_summary_

        Parameters
        ----------
        seq : str
            _description_
        title : str
            _description_
        description : str
            _description_
        """
        
        self.seq = seq
        self.title = title
        self.description = description

class FASTAProcessor(FileProcessor):
    """Class supports functions that process FASTA format file"""
    
    def __init__(self, path : str) -> None:
        """Initialize FASTAProcessor class

        Parameters
        ----------
        path : str
            path of .fasta file
        """
        
        self.path = path
        self.open_obj = False
        #sanity_check = sanityCheck.SanityCheck(self.path)
        #sanity_check.fastaSanityCheck()
        
        return
    
    def open(self, file_name, mode: str = "r") -> None:
        """_summary_

        Parameters
        ----------
        file_name : str
            The name of the file to open.
        mode : str
            open mode (r, w, ...)
        """
        if self.open_obj:
            print('Current Open Obj is already open')
        else:
            self.open_mode = mode
            self.open_obj = open(file_name, mode)
        
        pass
    
    def close(self: io.BufferedReader or io.BufferedWriter) -> None:
        """_summary_

        Parameters
        ----------
        opened_file : io.BufferedReaderorio.BufferedWriter
            _description_
        """
        self.open_obj.close()
        self.open_obj = False
    
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
    
    def write(self, title: str, sequence: str, desc : str = None) -> None:
        """Write file by line

        Parameters
        ----------
        line: str
            A line for writing file
        """
        
        if 'r' in self.open_mode:
            print('Current Open Obj is "Read" mode')
        
        elif 'w' in self.open_mode:
            fasta_title = f'>{title}'
            if desc: fasta_title += f' {desc}'
            self.open_obj.write(f'{fasta_title}\n')
            for i in range(0, len(sequence), 70):
                self.open_obj.write(sequence[i:i+70]+'\n')
        pass
    
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
    
    def __del__(self):
        if self.open_obj:
            print('close File')
            self.close()

    def sanity_check(self,target_seq :tuple ,mode : str ) -> bool:
        """sanity_check [summary]

        Parameters
        ----------
        mode : str
            [description]
            r,e
            r = respectively
            e = entire
        Returns
        -------
        bool
            [description]

        Raises
        ------
        Exception
            [description]
        """

        fastaElement : list= ['A','T','G','C','N','R','Y','S','W','K','M','B','D','H','V']
        #target_seq = next(fasta_seq)
        print(f'file format is fasta. \nStart the sanity check for {target_seq[0]}')
    
        if mode == "r":
            checkbase = [base in fastaElement for base in target_seq[2].strip()]
            checkbool :bool = all(checkbase)
            true_list =list((filter(lambda x: x, checkbase)))
            if checkbool == False:
                misbaseList = [ (target_seq[2][i],i+1) for i, b in enumerate(checkbase) if b == False]
                #print(misbaseList)
                print(f'Please enter a valid seq : \n(misbase,seq position. : {misbaseList} \n')
            if checkbool == False:
                print("Check the seq")
                return False
            else:
                print("Seq is normal.")
                return True

    def find_seq(self,seq:str) -> None:
        fasta_obj = open(self.path,"r")
        p = re.compile(seq)
        for fasta in self.simple_fasta_parser(fasta_obj):
            matched_iter = p.finditer((fasta[2]))
            for target in matched_iter:
                print(f'find seq in {fasta[0]} ==> start : {target.start()+1}, end : {target.end()+1}')

def export_json(output_name: str, seq_dict: dict):
    """export_json

    Parameters
    ----------
    output_name : str
        Output file name
    seq_dict : dict
        SeqRecord dictionary
    """
    json_dic = {}
    for title in seq_dict:
        record = seq_dict[title]
        json_dic[title] = { 'seq': str(record.seq),
                            'description': record.description
                            }
    json.dump(json_dic, open(output_name, 'w'), indent=4)
    
if __name__ == "__main__":
    
    fasta_fn = 'FASTA/RGS14_cDNA.fasta'
    obj_fasta = FASTAProcessor(fasta_fn)
    
    fasta_dic = obj_fasta.to_dict(open(fasta_fn))
    
    first_id = list(fasta_dic.keys())[0]
    first_fasta = fasta_dic[first_id]
    print(repr(first_fasta.seq))
    print(type(first_fasta.seq))
    
    #obj_fasta.open("first_fasta",mode='w')
    #obj_fasta.write(first_id, str(first_fasta.seq))
    #obj_fasta.close()

    #obj_fasta.open("second_fasta",mode='w')
    #obj_fasta.write(first_id, str(first_fasta.seq))
    # 1) obj_fasta.close()
    # 2) del obj_fasta
    
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
    
    print(len(fasta_dic))
    export_json("test.json", fasta_dic)