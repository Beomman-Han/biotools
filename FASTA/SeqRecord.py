import typing 
from Seq import Seq

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