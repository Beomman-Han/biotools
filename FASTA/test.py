import FASTA

fasta_dict = FASTA.to_dict(open('RGS14_cDNA.fasta'))
print(list(fasta_dict.keys()))

for seq_name in fasta_dict:
    print(seq_name)
    record = fasta_dict[seq_name]
    print(record.description)
    seq = record.seq
    s_seq = str(seq)
    r_seq = seq.reverse()
    c_seq = seq.complement()
    rc_seq = seq.reverse_complemnt()
    print(s_seq[:10])
    print(repr(seq))
    print(repr(r_seq))
    print(repr(c_seq))
    print(repr(rc_seq))
    
    #print(seq, len(seq))
    #print(type(seq.to_string()))
    #print(rc_seq, len(rc_seq))
    break
    