import typing

REVC = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
for base in list(REVC.keys()): REVC[base.lower()] = REVC[base].lower()

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
        
    def __repr__(self):
        if len(self.data) < 60:
            return f"Seq({self.data})"
        else:
            start = self.data[:3]
            end = self.data[-3:]
            return f"Seq({start}...{end})"       

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def complement(self):
        return Seq("".join([REVC[base] for base in self.data]))

    def reverse(self):
        return Seq("".join([base for base in self.data[::-1]]))

    def reverse_complemnt(self):
        return Seq("".join([REVC[base] for base in self.data[::-1]]))


if __name__ == "__main__":
    
    test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    print(test_seq)
    
    temp = Seq(test_seq)
    print(temp.reverse_complemnt())