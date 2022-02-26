from typing import Dict, Iterator, TextIO, Tuple, Type

from SeqRecord import SeqRecord
from Seq import Seq

def simple_fasta_parser(handle : TextIO) -> Tuple[str]:
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

def iterate(handle : Type["SeqRecord"]) -> Type["SeqRecord"]:
    """_summary_

    Parameters
    ----------
    handle : SeqRecord
        _description_

    Returns
    -------
    SeqRecord
        _description_

    Yields
    ------
    Iterator[SeqRecord]
        _description_
    """
    
    for title, description, seq in simple_fasta_parser(handle):
        yield SeqRecord(seq=Seq(seq), title=title, description=description)

def parse(handle : TextIO) -> Iterator[str]:
    record = iterate(handle)
    return record

def to_dict(handle : TextIO) -> Dict[str, Iterator[str]]:
    record_dict = {}
    for record in parse(handle):
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
