from typing import Type

class Seq:
    def __init__(self,
        type : str,
        data : str
        ) -> None:
        
        """Initializae Seq class with type, sequence.

        Parameters
        ----------
        type : str
            Type of sequence ('DNA' or 'RNA' or 'Protein')
        data : str
            Sequence string
        """
        
        self.type = type
        self.data = data
        
    def __repr__(self) -> str:
        """Represent Seq object by
        printing it's summary sequence data.

        Returns
        -------
        str
            Summary sequence data
        """
        
        if len(self.data) < 60:
            return f"Seq({self.data})"
        else:
            ## it would be better printing 60 char
            start = self.data[:30]
            end = self.data[-30:]
            return f"Seq({start}...{end})"       

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def complement(self) -> Type['Seq']:
        """Make complementary sequence of self.data.
        If Seq type is not DNA or RNA, it returns replicate object.

        Returns
        -------
        Seq
            Seq object which contains complementary sequence
        """
        
        if self.type == 'DNA':
            watson_crick = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
            for base in watson_crick.keys():
                watson_crick[base.lower()] = watson_crick[base].lower()
            return Seq(self.type, "".join(watson_crick[base] for base in self.data))
        elif self.type == 'RNA':
            watson_crick = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
            for base in watson_crick.keys():
                watson_crick[base.lower()] = watson_crick[base].lower()
            return Seq(self.type, "".join(watson_crick[base] for base in self.data))
        else:
            print('[WARNING] Only DNA or RNA sequence can get complement seq.')
            ## return replicate Seq object
            return Seq(self.type, self.data)

    def reverse(self):
        return Seq("".join([base for base in self.data[::-1]]))

    def reverse_complemnt(self):
        return Seq("".join([REVC[base] for base in self.data[::-1]]))


if __name__ == "__main__":
    
    test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    print(test_seq)
    
    temp = Seq(test_seq)
    print(temp.reverse_complemnt())