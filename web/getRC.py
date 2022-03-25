import os, sys
sys.path.append("%s/FASTA"%os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Seq import Seq

def main(seq_list): 
    for sequence in seq_list:
        print(str(Seq(sequence, type="DNA").reverse_complement()))

if __name__ == "__main__":
    main(sys.argv[1:])