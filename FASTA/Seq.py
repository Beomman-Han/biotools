import typing

REVC = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
for base in list(REVC.keys()): REVC[base.lower()] = REVC[base].lower()

class Seq:
    def __init__(self, data: str) -> str:
        """_summary_

        Parameters
        ----------
        data : str
            _description_

        Returns
        -------
        str
            _description_
        """
        
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
    
    def __add__(self, other_seq):
        if type(Seq('A')) == type(other_seq):
            add_seq = str(other_seq)
        elif type('A') == type(other_seq):
            add_seq = other_seq
        else:
            raise TypeError('The type of "other_seq" must be str or Seq() type.')
        return Seq(self.data + add_seq)

    def concatenate(self, other_seq):
        return self.__add__(other_seq)

    def complement(self):
        return Seq("".join([REVC[base] for base in self.data]))

    def reverse(self):
        return Seq("".join([base for base in self.data[::-1]]))

    def reverse_complemnt(self):
        return Seq("".join([REVC[base] for base in self.data[::-1]]))


if __name__ == "__main__":
    
    test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    print(test_seq)
    
    test1_seq = Seq('AAAAAAAA')
    test2_seq = Seq('GGGGGGGG')

    print(test1_seq, test1_seq.complement())
    print(test2_seq, test2_seq.complement())
    print((test1_seq + test2_seq))
    print((test1_seq + test2_seq).reverse())
    print((test1_seq + test2_seq).complement())
    print((test1_seq + test2_seq).reverse_complemnt())
    
    print(test1_seq.concatenate(test2_seq))
    print(test1_seq.concatenate("ATGACGTACGTAGCT"))
    
    print(test1_seq + 'AGCTAGCTGATCGTGGGCTAGTCGTAGCTG')
    print(test1_seq + 1)
    
    #temp = Seq(test_seq)
    #print(temp.reverse_complemnt())