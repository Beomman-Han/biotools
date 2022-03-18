import os, sys

# VCFv4.3
class varRecord:
    def __init__(
        self,
        chrom: str,
        pos: str,
        ID: str,
        ref: str,
        alt: str,
        qual: str,
        var_filter: str,
        info: str,
        format_header: str = False,
        format_list: list = False,
        sample_name_list: list = False,
    ):
        """_summary_

        Parameters
        ----------
        chrom : str
            _Chromosome_
        pos : int
            _Reference position (1-base coordinate)_
        ID : str
            _Variant identifier_
        ref : str
            _Reference allele_
        alt : str
            _Alternative allele_
        qual : int
            _Variant Quality_
        var_filter : str
            _Filter status_
        info : str
            _Additional information_
        format_header : str, optional
            _description_, by default False
        format_list : list, optional
            _description_, by default False
        sample_name_list : list, optional
            _description_, by default False
        """
        
        self.chrom = chrom
        try: self.pos = int(pos)
        except: sys.exit("POS data must be int type")
        self.ID = ID
        self.ref = ref; self.alt = alt
        try: self.qual = int(qual)
        except: sys.exit("QUAL data must be int type")
        self.filter = var_filter
        
        self.info = {}
        if info.endswith(';'): info = info[:-1]
        for info_data in info.split(';'):
            try: key, value = info_data.split('=')
            except: key = info_data[0]; value = ''
            self.info[key.strip()] = value.strip()
            
        if format_header:
            format_header_dic = {}
            for i, key in enumerate(format_header.split(':')):
                format_header_dic[i] = key
        
        if format_list:
            self.sample_info = { sample_name: {} for sample_name in sample_name_list }
            if len(format_list) != len(sample_name_list):
                sys.exit('The length of "format_list" and the length of "sample_name_list" must be the same.')
                
            for sample_i, sample_info in enumerate(format_list):
                sample_name = sample_name_list[sample_i]
                for i, value in enumerate(sample_info.split(':')):
                    self.sample_info[sample_name][format_header_dic[i]] = value
                    
                    
if __name__ == "__main__":
    sample_list = ["NA00001", "NA00002"]
    test_str = "20\t14370\trs6054257\tG\tA\t29\tPASS\tNS=3;DP=14;AF=0.5;DB;H2\tGT:GQ:DP:HQ\t0|0:48:1:51,51\t1|0:48:8:51,51"
    
    test_info = test_str.split('\t')
    
    test_var = varRecord(*test_info[:8], format_header=test_info[8], format_list=test_info[9:], sample_name_list=sample_list)
    
    from pprint import pprint
    
    print(test_var.chrom)
    pprint(test_var.info)
    pprint(test_var.sample_info)