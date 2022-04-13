import sys
from typing import List, Dict

__all__ = ('varRecord',)

# VCFv4.3
class varRecord:
    """This class is for storing variant information from VCF.    
    It follows VCFv4.2 specification. Data lines of VCF are 
    tab seperated, and each column represents each information
    related to variant.  For example,
    
    #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO    FORMAT  SAMPLE1...
    
    The first 8 fields are mandatory.
    'CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO'
    
    And most of VCFs produced by normal analysis pipeline have fields
    'FORMAT', 'SAMLE1', 'SAMLE2', ...
    
    Of 9 fields, 'FILTER', 'INFO', and 'FORMAT' fields contain
    more complicated information. For example,
    
    #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
    Y	2728456	rs2058276	T	C	32	.	AC=2;AN=2;DB;DP=182;H2;NS=65
    Y	2734240	.	G	A	31	.	AC=1;AN=2;DP=196;NS=63
    Y	2743242	.	C	T	25	.	AC=1;AN=2;DP=275;NS=66
    Y	2746727	.	A	G	34	.	AC=2;AN=2;DP=179;NS=64
    Y	2777970	.	T	A	67	.	AC=1;AN=2;DP=225;NS=67

    varRecord instance saves content of 'FILTER' field as list,
    content of 'INFO' field as dictionary, and content of 'FORMAT' field
    as dictionary. Other fileds are saved as string or integer.
    
    In the case of the absence of 'FORMAT' field (and following 'SAMPLE' fields),
    'format_headers' and 'sample_info' attributes are saved as None.
    
    Example
    -------    
    >>> sample_list = ["NA00001", "NA00002"]
    >>> test_str = "20\t14370\trs6054257\tG\tA\t29\tPASS\tNS=3;DP=14;AF=0.5;DB;H2\tGT:GQ:DP:HQ\t0|0:48:1:51,51\t1|0:48:8:51,51"
    >>> test_info = test_str.split()
    >>> test_var = varRecord(*test_info[:8], format_header=test_info[8], format_list=test_info[9:], sample_name_list=sample_list)
    >>> from pprint import pprint
    >>> print(test_var.chrom)
    20
    >>> print(test_var.pos)
    14370
    >>> print(test_var.ID)
    rs6054257
    >>> print(test_var.ref)
    G
    >>> print(test_var.alt)
    A
    >>> print(test_var.qual)
    29.0
    >>> print(test_var.filter)
    ['PASS']
    >>> print(test_var.get_column_num())
    10
    """
    
    __slots__ = ('_chrom', '_pos', '_ID',
                 '_ref', '_alt', '_qual',
                 '_filter', '_info',
                 '_format_headers', 'sample_info')
    
    def __init__(self,
        chrom: str,
        pos: str,
        ID: str,
        ref: str,
        alt: str,
        qual: str,
        var_filter: str,
        info: str,
        format_header: str = False,
        format_list: List[str] = False,
        sample_name_list: List[str] = False,
        ) -> None:
        
        """Init instance for each variant

        Parameters
        ----------
        chrom : str
            Chromosome
        pos : int
            Reference position (1-base coordinate)
        ID : str
            Variant identifier
        ref : str
            Reference allele
        alt : str
            Alternative allele
        qual : int
            Variant quality
        var_filter : str
            Filter status
        info : str
            Additional info combined across all samples
        format_header : str, optional
            Header for additional info of each sample, by default False
        format_list : list, optional
            Additional info of each sample_, by default False
        sample_name_list : list, optional
            Sample name list_, by default False
        """
        
        self.chrom = chrom
        self.pos = pos
        self.ID = ID
        self.ref = ref
        self.alt = alt
        self.qual = qual
        self.filter = var_filter
        self.info : Dict[str, str] = info
        
        ## optional attributes
        if format_header and format_list and sample_name_list:
            self.format_headers : Dict[str, str] = format_header
            self.sample_info : Dict[str, Dict[str, str]] = self._parse_sample_format(format_list, sample_name_list)
        else:
            self.format_headers = None
            self.sample_info = None

        return
    
    @property
    def chrom(self) -> str:        
        return self._chrom
    
    @chrom.setter
    def chrom(self, _chrom : str) -> None:
        self._chrom = _chrom.strip()
        return
    
    @property
    def pos(self) -> int:
        return self._pos
    
    @pos.setter
    def pos(self, _pos : str) -> None:
        try:
            self._pos = int(_pos)
        except ValueError:
            sys.exit('POS data must be int type')
        return
    
    @property
    def ID(self) -> str:
        return self._ID
    
    @ID.setter
    def ID(self, _ID : str) -> None:
        self._ID = _ID
        return
    
    @property
    def ref(self) -> str:
        return self._ref
    
    @ref.setter
    def ref(self, _ref : str) -> None:
        self._ref = _ref
        return
    
    @property
    def alt(self) -> str:
        return self._alt
    
    @alt.setter
    def alt(self, _alt : str) -> None:
        self._alt = _alt
        return

    @property
    def qual(self) -> float:
        return self._qual
    
    @qual.setter
    def qual(self, _qual : str) -> None:
        try:
            self._qual = float(_qual)
        except ValueError:
            sys.exit('QUAL data must be float type')
    
    @property
    def filter(self) -> str:
        return self._filter
    
    @filter.setter
    def filter(self, _filter : str) -> None:
        self._filter = []
        if _filter.endswith(';'):
            _filter = _filter[:-1]
        self._filter = _filter.split(';')
        
        return

    @property
    def info(self) -> Dict:
        return self._info
    
    @info.setter
    def info(self, _info : str) -> None:
        self._info = {}
        if _info.endswith(';'):
            _info = _info[:-1]
        for info_data in _info.split(';'):
            try:
                key, value = info_data.split('=')
            except ValueError:
                key = info_data
                value = ''
            self._info[key.strip()] = value.strip()
        return

    @property
    def format_headers(self) -> Dict[str, str]:
        return self._format_headers
    
    @format_headers.setter
    def format_headers(self, _format_header : str) -> None:
        if _format_header:
            format_headers = {}
            for i, key in enumerate(_format_header.split(':')):
                format_headers[i] = key
            self._format_headers = format_headers
        else:
            self._format_headers = dict()
        return

    def _parse_sample_format(self,
        sample_formats : List[str] = False,
        sample_names : List[str] = False
        ) -> Dict[str, Dict[str, str]]:
        
        if sample_formats:
            sample_info = { sample_name : {} for sample_name in sample_names }
            if len(sample_formats) != len(sample_names):
                sys.exit('The number of FORMAT columns and the number of samples must be the same.')
            
            for sample_i, sample_format in enumerate(sample_formats):
                sample_name = sample_names[sample_i]
                for i, value in enumerate(sample_format.split(':')):
                    sample_info[sample_name][self.format_headers[i]] = value
        return sample_info

    def __str__(self) -> str:
        res_str = f'varRecord'
        res_str += f'({self.chrom}, {self.pos}'
        res_str += f', {self.ID}, {self.ref}'
        res_str += f', {self.alt}, {self.qual}'
        res_str += f', {self.filter}, {self.info}'
        if not self.format_headers and not self.sample_info:
            res_str += ')'
            return res_str
        else:
            res_str += f', {self.format_headers}, {self.sample_info})'
            return res_str
    
    def get_column_num(self) -> int:
        """Return # of columns at VCF data line"""
        cols = [ getattr(self, c) for c in self.__slots__ if getattr(self, c) ]
        return len(cols)


def _test():
    """Test function of this code"""
    
    import doctest
    doctest.testmod()
    
    return

if __name__ == "__main__":
    _test()