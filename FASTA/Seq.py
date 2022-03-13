from typing import Dict, Type
from Constant import *

class Seq:
    def __init__(self,
        data : str,
        type : str = 'DNA'
        ) -> None:
        
        """Initialize Seq class with type, sequence.
        
        Parameters
        ----------
        data : str
            Sequence string
        type : str, optional
            Type of sequence ('DNA' or 'RNA' or 'Protein'), by default 'DNA'
        """

        self.type = type
        self.data = data
        
        return
    
    def check(self) -> bool:
        
        """Check whether initialization is normal.
        
        Returns
        -------
        bool
            Is it normal content
        """
        
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
        
        """Represent Seq object by printing it's summary sequence data.
        
        Returns
        -------
        str
            Summary sequence data
        """
        
        if len(self.data) <= 60:
            return f"Seq({self.data})"
        else:
            ## it would be better printing 60 char
            start = self.data[:30]
            end = self.data[-30:]
            return f"Seq({start}...{end})"

    def __len__(self) -> int:
        
        """Return the length of self.data (len(Seq)).
        
        Returns
        -------
        int
            Length of self.data
        """
        
        return len(self.data)

    def __str__(self) -> str:
        
        """Transform Seq object to string object (str(Seq)).
        
        Returns
        -------
        str
            String format of Seq object
        """
        
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
            # watson_crick = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
            DNA_PAIR = {**{"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(DNA_PAIR)
            return Seq("".join([DNA_PAIR[base] for base in self.data]), self.type)
        elif self.type == 'RNA':
            # watson_crick = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
            RNA_PAIR = {**{"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(RNA_PAIR)
            return Seq("".join([RNA_PAIR[base] for base in self.data]), self.type)
        else:
            print('[WARNING] Only DNA or RNA sequence can get complement seq.')
            ## return replicate Seq object
            return Seq(self.data, self.type)

    def reverse(self) -> Type['Seq']:
        
        """Make reverse sequence of self.data.
       
        Returns
        -------
        Seq
            Seq object which contains reverse sequence
        """

        return Seq(self.data[::-1],  self.type)

    def get_data(self) -> str:
        
        """Getter method of self.data attribute
        
        Returns
        -------
        str
            self.data
        """
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
        return Seq(rev_com, self.type)

    def _has_iupac(self, seq : str) -> bool:
        
        """Does sequence have IUPAC character not 'ACGT(U)' base.

        Parameters
        ----------
        seq : str
            Input sequence for checking

        Returns
        -------
        bool
            True if self.data has more than 'ACGT'
        """
        
        if self.type == 'DNA':
            if len(set(seq.upper()) - {'A', 'C', 'G', 'T'}) != 0:
                return True
        elif self.type == 'RNA':
            if len(set(seq.upper()) - {'A', 'C', 'G', 'U'}) != 0:
                return True
        return False
    
    def _warn_iupac(self, seq : str = '') -> None:
        
        """Warn if sequence has more than 'ACGT(U)' base,
        it contains undecided IUPAC codes.
        Default sequence is self.data sequence.
        
        Parameters
        ----------
        seq : str, optional
            Input sequence for warning, by default ''
        """
        
        if seq == '':
            seq = self.data

        if self._has_iupac(seq):
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
        
    def transcribe(self,
        start_idx : int = 0,
        verbose : bool = True
        ) -> Type['Seq'] or None:
        
        """Transcribe DNA sequence to RNA sequence.
        
        Example
        -------
        >>> s = Seq('ACGTACGTACGT')
        >>> s.transcribe()
        ACGUACGUACGU
        >>>     
        >>> s = Seq('ACGUACGUACGU', 'RNA')
        >>> s.transcribe()
        [WARNING] Transcription is only for DNA
        None
        
        Parameters
        ----------
        start_idx : int, optional
            Start index for transcription, by default 0
        verbose : bool, optional
            Print warning message, by default True
        
        Returns
        -------
        Seq or None
            Seq object containing trancript (RNA) or None
        """
        
        if self.type != 'DNA':
            if verbose:
                print('[WARNING] Transcription is only for DNA')
            return None

        template_dna = self.data[start_idx:]
        if verbose:
            self._warn_iupac(template_dna)

        DNA_RNA_PAIR = {**{'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}, **IUPAC_PAIR}
        self._add_lower_case(DNA_RNA_PAIR)
        
        return Seq(''.join([DNA_RNA_PAIR[base] for base in template_dna])[::-1], 'RNA')

    def reverse_transcribe(self,
        start_idx : int = 0,
        verbose : bool = True
        ) -> Type['Seq'] or None:
        
        """Reverse transcribe RNA sequence to DNA sequence.
        
        Parameters
        ----------
        start_idx : int, optional
            Start index for reverse transcription, by default 0
        verbose : bool, optional
            Print warning message or not, by default True
        
        Returns
        -------
        Seq or None
            Seq object containing DNA sequence        
        """
        
        if self.type != 'RNA':
            if verbose:
                print('[WARNING] Reverse transcription is only for RNA')
            return None

        template_rna = self.data[start_idx:]
        if verbose:
            self._warn_iupac(template_rna)

        RNA_DNA_PAIR = {**{'A': 'T', 'C': 'G', 'G': 'C', 'U': 'A'}, **IUPAC_PAIR}
        self._add_lower_case(RNA_DNA_PAIR)
        
        return Seq(''.join([RNA_DNA_PAIR[base] for base in template_rna])[::-1], 'DNA')
    
    def translate(self,
        start_idx : None or int = None,
        verbose : bool = True
        ) -> Type['Seq'] or None:
        
        """Translate RNA sequence to protein sequence with start index.
        If start index is None, then find ORF and translate with ORF.
        If start index is None and no ORF, return None.

        start_idx  (direction) ->->
        0123 ->->      None(16)          -5  -1
        ||||            |                 |   |
        ACGUACGUACGUACGUAUGAAACCCGGGAUGACGUUACG... (RNA)
                        |-> (ORF)
        
        Example
        -------
        >>> s = Seq('AAUGAUGAUGAUGUGAAAAAA', 'RNA')
        >>> s.translate()
        MMMM
        >>> s.translate(0)
        NDDDVKK
        >>> s.translate(-3)
        K
        >>> s.translate(-6)
        KK
        
        Parameters
        ----------
        start_idx : int, optional
            Start index for translation, by default None
        verbose : bool, optional
            Print warning message, by default True
            
        Returns
        -------
        Seq
            Seq object containing protein or None
        """
        
        if self.type != 'RNA':
            if verbose:
                print('[WARNING] Translation is only for RNA')
            return None

        ## find first 'AUG' sequence (ORF)
        if start_idx == None:
            start_idx = self.data.upper().find('AUG')
        template_rna = self.data[start_idx:].upper()
        if self._has_iupac(template_rna):
            if verbose:
                self._warn_iupac(template_rna)
            return None

        step = 3        
        protein = ""
        for i in range(0, len(template_rna), step):
            codon = template_rna[i:i+3]
            try:
                amino_acid = CODON_TABLE[codon]
                protein += amino_acid
                if amino_acid == "":
                    break
            except KeyError:
                break

        return Seq(protein, 'Protein')

    def find_orf(self) -> int or None:
        
        """Find ORF frame index from self.data.
        
                |
        12312312312312312312312312312312
        ACGUACGUAUGAAACCCAAACCCCCCAUGUGA

        Returns
        -------
        int or None
            Frame index (1 or 2 or 3 or -1 or -2 or -3),
            if there is no ORF, return None
        """
        
        try:
            start_idx = self.data.index('AUG')
            return start_idx % 3 + 1
        except ValueError:
            try:
                start_idx = self.data[::-1].index('AUG')
                return -1*(start_idx % 3 + 1)
            except ValueError:
                return None
        
    
if __name__ == "__main__":
    
    # test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    # print(test_seq)
    
    # temp = Seq(test_seq, 'DNA')
    # print(temp.check())
    # print(temp.complement())
    # print(temp.reverse())
    # print(temp.reverse_complement())
    # print(temp.count('a'))
    # print(temp.cal_gc_ratio())
    # print(temp.transcribe(-1))
    # print(temp._has_iupac())
    
    test_seq = 'AAUGAUGAUGAUGUGAAAAAA'
    # # test_seq = 'AUGAAAAAAAAAAUAA'
    # # test_seq = 'AAAAAAAAGUAAA'
    # # test_seq = 'AAAAAAAAAAAAC'
    temp = Seq(test_seq, 'RNA')
    # print(temp.translate())
    # print(temp.translate(1))
    # print(temp.translate(3))
    # print(temp.translate(-3))
    # print(temp.find_orf())
    print(temp.reverse_transcribe().get_data())