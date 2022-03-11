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

IUPAC_PAIR = {"R": "Y", "Y": "R", "M": "K", "K": "M", "W": "W",
            "S": "S", "B": "V", "V": "B", "D": "H", "H": "D"}

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
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"}

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
                "N": ["A", "C", "G", "U"]}
