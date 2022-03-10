from typing import Dict, Type

class Seq:
    def __init__(self,
<<<<<<< Updated upstream
        type : str,
        data : str
=======
        data : str,
        type : str = "DNA",
>>>>>>> Stashed changes
        ) -> None:
        
        """Initializae Seq class with type, sequence.

        Parameters
        ----------
        type : str
<<<<<<< Updated upstream
            Type of sequence ('DNA' or 'RNA' or 'Protein')
=======
            Type of sequence ('DNA' or 'RNA' or 'Protein'), by default True
>>>>>>> Stashed changes
        data : str
            Sequence string
        """
        
        self.type = type
        self.data = data    
    
    def check(self) -> bool:
        """Check whether initialization is normal.

        Returns
        -------
        bool
            Is it normal content
        """
        ## IUPAC info was referred from http://www.incodom.kr/IUPAC
        BASE_IUPAC = {
            'A', 'C', 'G', 'T',
            'U', 'R', 'Y', 'M',
            'K', 'W', 'S', 'B',
            'D', 'H', 'V', 'N'
        }
        AMINO_ACID_IUPAC = {
            'A', 'R', 'N', 'D',
            'C', 'Q', 'E', 'G',
            'H', 'I', 'L', 'K',
            'M', 'F', 'P', 'S',
            'T', 'W', 'Y', 'V',
            'B', 'Z', 'X'
        }
        if self.type == 'DNA':
            DNA_IUPAC = BASE_IUPAC - {'U'}
            bases = list(set(self.data.upper()))
            for base in bases:
                if base not in DNA_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is DNA sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        elif self.type == 'RNA':
            RNA_IUPAC = BASE_IUPAC - {'T'}
            bases = list(set(self.data.upper()))
            for base in bases:
                if base not in RNA_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is RNA sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        elif self.type == 'Protein':
            amino_acids = list(set(self.data.upper()))
            for amino in amino_acids:
                if amino not in AMINO_ACID_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is Protein sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        else:
            print('[WARNING] It only supports DNA/RNA/Protein sequences.')
            return False
        return True
        
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

    def complement(self) -> Type['Seq']:
        """Make complementary sequence of self.data.
        If Seq type is not DNA or RNA, it returns replicate object.
<<<<<<< Updated upstream

        Returns
        -------
        Seq
            Seq object which contains complementary sequence
        """
        
        IUPAC_PAIR = {"R": "Y", "Y": "R", "M": "K", "K": "M", "W": "W",
                    "S": "S", "B": "V", "V": "B", "D": "H", "H": "D"}
        if self.type == 'DNA':
            # watson_crick = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
            DNA_PAIR = {**{"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(DNA_PAIR)
            return Seq(self.type, "".join([DNA_PAIR[base] for base in self.data]))
        elif self.type == 'RNA':
            # watson_crick = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
            RNA_PAIR = {**{"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(RNA_PAIR)
            return Seq(self.type, "".join([RNA_PAIR[base] for base in self.data]))
        else:
            print('[WARNING] Only DNA or RNA sequence can get complement seq.')
            ## return replicate Seq object
            return Seq(self.type, self.data)

    def reverse(self) -> Type['Seq']:
        """Make reverse sequence of self.data.

        Returns
        -------
        Seq
            Seq object which contains reverse sequence
        """

        return Seq(self.type, self.data[::-1])

    def get_data(self) -> str:
        return self.data

    def reverse_complement(self) -> Type['Seq']:
        """Make reverse complement sequence of self.data.
        If Seq type is not DNA or RNA, it returns reverse sequence.

        Returns
        -------
        Seq
            Seq object which contains reverse complement sequence
        """
        
        if self.type in ('DNA', 'RNA'):
            rev_com = self.complement().get_data()[::-1]
        else:
            rev_com = self.data[::-1]
        return Seq(self.type, rev_com)
    
    def _warn_iupac(self) -> None:
        """Warn if self.data has more than 'ACGT(U)' base,
        it contains undecided IUPAC codes."""
        
        if self.type == 'DNA':
            if len(set(self.data) - {'A', 'C', 'G', 'T'}) != 0:
                # print('[WARNING] Sequence has more than A/C/G/T bases.')
                print('[WARNING] Sequence has undecided IUPAC codes.')
        elif self.type == 'RNA':
            if len(set(self.data) - {'A', 'C', 'G', 'U'}) != 0:
                # print('[WARNING] Sequence has more than A/C/G/U bases.')
                print('[WARNING] Sequence has undecided IUPAC codes.')
        return
    
    def count(self, char : str, verbose=True) -> int:
        """Count input char from self.data sequence.
        In case of DNA/RNA, it is recommended that 
        self.data have only 'ACGT(U)' not IUPAC character.

        Parameters
        ----------
        char : str
            Base or amino acid for counting
        verbose : bool, optional
            True, print warning message, by default True

        Returns
        -------
        int
            Count number
        """
        
        if verbose:
            self._warn_iupac()
        return self.data.upper().count(char.upper())
        
    def cal_gc_ratio(self, verbose=True) -> float or None:
        """Calculate GC ratio of self.data (only for DNA/RNA).
        GC ratio = ( count of G + count of C ) / length of seq

        Parameters
        ----------
        verbose : bool, optional
            True, print warning message, by default True

        Returns
        -------
        float or None
            GC ration or None for protein
        """
        
        if self.type == 'Protein':
            return None
        
        gc_count = self.count('G', verbose=False) + self.count('C', verbose=False)
        if verbose:
            self._warn_iupac()
        return gc_count / len(self.data)

    def _add_lower_case(self,
        dict : Dict[str, str]
        ) -> None:
        """Add lower case of keys at input dictionary.
        
        Example
        -------
        >>> dict
        {'A': 'T'}
        >>> self._add_lower_case(dict)
        >>> dict
        {'A': 'T', 'a': 't'}
        
        Parameters
        ----------
        dict : Dict[str, str]
            input dict like DNA_PAIR, RNA_PAIR, DNA_RNA_PAIR, etc.
        """
        
        for key in list(dict.keys()):
            dict[key.lower()] = dict[key].lower()

        return
        
    def transcribe(self, verbose=True) -> Type['Seq'] or None:
        """Transcribe DNA sequence to RNA sequence.
        
        Parameters
        ----------
        verbose : bool, optional
            Print warning message, by default True
        
        Returns
        -------
        Seq or None
            Seq object containing trancript or None
        """
        
        if self.type != 'DNA':
            if verbose:
                print('[WARNING] Transcription is only for DNA')
            return None
        if verbose:
            self._warn_iupac()
        IUPAC_PAIR = {"R": "Y", "Y": "R", "M": "K", "K": "M", "W": "W",
                    "S": "S", "B": "V", "V": "B", "D": "H", "H": "D"}
        DNA_RNA_PAIR = {**{'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}, **IUPAC_PAIR}
        self._add_lower_case(DNA_RNA_PAIR)
        
        return Seq('RNA', ''.join([DNA_RNA_PAIR[base] for base in self.data])[::-1])
    
    def translate(self, verbose=True) -> Type['Seq'] or None:
        """Translate RNA sequence to protein sequence.
        
        Parameters
        ----------
        verbose : bool, optional
            Print warning message, by default True

        Returns
        -------
        Seq or None
            Seq object containing protein or None
        """
        
        if self.type != 'RNA':
            if verbose:
                print('[WARNING] Translation is only for RNA')
            return None
        if verbose:
            self._warn_iupac()
        
        CODON_TABLE = {
            "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
            "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
            "UAU": "Y", "UAC": "Y", "UAA": "", "UAG": "",
            "UGU": "C", "UGC": "C", "UGA": "", "UGG": "W",
            "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
            "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
            "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
            "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
            "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
            "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
            "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
            "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
            "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
            "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
            "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
            "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
        }
        IUPAC_TABLE = {"R": ["A", "G"],
                       "Y": ["C", "U"],
                       "M": ["C", "A"],
                       "K": ["U", "G"],
                       "W": ["U", "A"],
                       "S": ["C", "G"],
                       "B": ["C", "U", "G"],
                       "D": ["A", "U", "G"],
                       "H": ["A", "U", "C"],
                       "V": ["A", "C", "G"],
                       "N": ["A", "C", "G", "U"]                       
                       }
        
        ## find first 'AUG' sequence
        upper_data = self.data.upper()
        if len(set(upper_data) - {'A', 'C', 'G', 'U'}) != 0:
            return None
        
        start_idx = upper_data.index('AUG')
        protein = ""
        for i in range(start_idx, len(upper_data), 3):
            codon = upper_data[i:i+3]
            try:
                amino_acid = CODON_TABLE[codon]
                protein += amino_acid
                if amino_acid == "":
                    break
            except KeyError:
                break
        
        return Seq('Protein', protein)

=======

        Returns
        -------
        Seq
            Seq object which contains complementary sequence
        """
        
        IUPAC_PAIR = {"R": "Y", "Y": "R", "M": "K", "K": "M", "W": "W",
                    "S": "S", "B": "V", "V": "B", "D": "H", "H": "D"}
        if self.type == 'DNA':
            # watson_crick = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
            DNA_PAIR = {**{"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(DNA_PAIR)
            return Seq(self.type, "".join([DNA_PAIR[base] for base in self.data]))
        elif self.type == 'RNA':
            # watson_crick = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
            RNA_PAIR = {**{"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(RNA_PAIR)
            return Seq(self.type, "".join([RNA_PAIR[base] for base in self.data]))
        else:
            print('[WARNING] Only DNA or RNA sequence can get complement seq.')
            ## return replicate Seq object
            return Seq(self.type, self.data)

    def reverse(self) -> Type['Seq']:
        """Make reverse sequence of self.data.

        Returns
        -------
        Seq
            Seq object which contains reverse sequence
        """

        return Seq(self.type, self.data[::-1])

    def get_data(self) -> str:
        return self.data

    def reverse_complement(self) -> Type['Seq']:
        """Make reverse complement sequence of self.data.
        If Seq type is not DNA or RNA, it returns reverse sequence.

        Returns
        -------
        Seq
            Seq object which contains reverse complement sequence
        """
        
        if self.type in ('DNA', 'RNA'):
            rev_com = self.complement().get_data()[::-1]
        else:
            rev_com = self.data[::-1]
        return Seq(self.type, rev_com)
    
    def _warn_iupac(self) -> None:
        """Warn if self.data has more than 'ACGT(U)' base,
        it contains undecided IUPAC codes."""
        
        if self.type == 'DNA':
            if len(set(self.data) - {'A', 'C', 'G', 'T'}) != 0:
                # print('[WARNING] Sequence has more than A/C/G/T bases.')
                print('[WARNING] Sequence has undecided IUPAC codes.')
        elif self.type == 'RNA':
            if len(set(self.data) - {'A', 'C', 'G', 'U'}) != 0:
                # print('[WARNING] Sequence has more than A/C/G/U bases.')
                print('[WARNING] Sequence has undecided IUPAC codes.')
        return
    
    def count(self, char : str, verbose=True) -> int:
        """Count input char from self.data sequence.
        In case of DNA/RNA, it is recommended that 
        self.data have only 'ACGT(U)' not IUPAC character.

        Parameters
        ----------
        char : str
            Base or amino acid for counting
        verbose : bool, optional
            True, print warning message, by default True

        Returns
        -------
        int
            Count number
        """
        
        if verbose:
            self._warn_iupac()
        return self.data.upper().count(char.upper())
        
    def cal_gc_ratio(self, verbose=True) -> float or None:
        """Calculate GC ratio of self.data (only for DNA/RNA).
        GC ratio = ( count of G + count of C ) / length of seq

        Parameters
        ----------
        verbose : bool, optional
            True, print warning message, by default True

        Returns
        -------
        float or None
            GC ration or None for protein
        """
        
        if self.type == 'Protein':
            return None
        
        gc_count = self.count('G', verbose=False) + self.count('C', verbose=False)
        if verbose:
            self._warn_iupac()
        return gc_count / len(self.data)

    def _add_lower_case(self,
        dict : Dict[str, str]
        ) -> None:
        """Add lower case of keys at input dictionary.
        
        Example
        -------
        >>> dict
        {'A': 'T'}
        >>> self._add_lower_case(dict)
        >>> dict
        {'A': 'T', 'a': 't'}
        
        Parameters
        ----------
        dict : Dict[str, str]
            input dict like DNA_PAIR, RNA_PAIR, DNA_RNA_PAIR, etc.
        """
        
        for key in list(dict.keys()):
            dict[key.lower()] = dict[key].lower()

        return
        
    def transcribe(self, verbose=True) -> Type['Seq'] or None:
        """Transcribe DNA sequence to RNA sequence.
        
        Parameters
        ----------
        verbose : bool, optional
            Print warning message, by default True
        
        Returns
        -------
        Seq or None
            Seq object containing trancript or None
        """
        
        if self.type != 'DNA':
            if verbose:
                print('[WARNING] Transcription is only for DNA')
            return None
        if verbose:
            self._warn_iupac()
        IUPAC_PAIR = {"R": "Y", "Y": "R", "M": "K", "K": "M", "W": "W",
                    "S": "S", "B": "V", "V": "B", "D": "H", "H": "D"}
        DNA_RNA_PAIR = {**{'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}, **IUPAC_PAIR}
        self._add_lower_case(DNA_RNA_PAIR)
        
        return Seq('RNA', ''.join([DNA_RNA_PAIR[base] for base in self.data])[::-1])
    
    def translate(self, verbose=True) -> Type['Seq'] or None:
        """Translate RNA sequence to protein sequence.
        
        Parameters
        ----------
        verbose : bool, optional
            Print warning message, by default True

        Returns
        -------
        Seq or None
            Seq object containing protein or None
        """
        
        if self.type != 'RNA':
            if verbose:
                print('[WARNING] Translation is only for RNA')
            return None
        if verbose:
            self._warn_iupac()
        
        CODON_TABLE = {
            "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
            "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
            "UAU": "Y", "UAC": "Y", "UAA": "", "UAG": "",
            "UGU": "C", "UGC": "C", "UGA": "", "UGG": "W",
            "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
            "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
            "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
            "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
            "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
            "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
            "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
            "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
            "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
            "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
            "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
            "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
        }
        IUPAC_TABLE = {"R": ["A", "G"],
                       "Y": ["C", "U"],
                       "M": ["C", "A"],
                       "K": ["U", "G"],
                       "W": ["U", "A"],
                       "S": ["C", "G"],
                       "B": ["C", "U", "G"],
                       "D": ["A", "U", "G"],
                       "H": ["A", "U", "C"],
                       "V": ["A", "C", "G"],
                       "N": ["A", "C", "G", "U"]                       
                       }
        
        ## find first 'AUG' sequence
        upper_data = self.data.upper()
        if len(set(upper_data) - {'A', 'C', 'G', 'U'}) != 0:
            return None
        
        start_idx = upper_data.index('AUG')
        protein = ""
        for i in range(start_idx, len(upper_data), 3):
            codon = upper_data[i:i+3]
            try:
                amino_acid = CODON_TABLE[codon]
                protein += amino_acid
                if amino_acid == "":
                    break
            except KeyError:
                break
        
        return Seq('Protein', protein)

>>>>>>> Stashed changes
    
if __name__ == "__main__":
    
    test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    print(test_seq)
    
<<<<<<< HEAD
    test1_seq = Seq('AAAAAAAA')
    test2_seq = Seq('GGGGGGGG')

    print(test1_seq, test1_seq.complement())
    print(test2_seq, test2_seq.complement())
    print((test1_seq + test2_seq))
    print((test1_seq + test2_seq).reverse())
    print((test1_seq + test2_seq).complement())
    print((test1_seq + test2_seq).reverse_complement())
    
    print(test1_seq.concatenate(test2_seq))
    print(test1_seq.concatenate("ATGACGTACGTAGCT"))
    
    print(test1_seq + 'AGCTAGCTGATCGTGGGCTAGTCGTAGCTG')
    #print(test1_seq + 1)
    
    #temp = Seq(test_seq)
    #print(temp.reverse_complemnt())
<<<<<<< Updated upstream
=======
=======
    '''
>>>>>>> Stashed changes
    temp = Seq('DNA', test_seq)
    print(temp.check())
    print(temp.complement())
    print(temp.reverse())
    print(temp.reverse_complement())
    print(temp.count('a'))
    print(temp.cal_gc_ratio())
    print(temp.transcribe())
    
    test_seq = 'AAAAAAAAAUGAUGAUGAUGUGAAAAAA'
    temp = Seq('RNA', test_seq)
    print(temp.translate())
<<<<<<< Updated upstream
>>>>>>> b2bbd9c0a112aebdac6d48e617711f82032faa18
=======
    '''
>>>>>>> Stashed changes
