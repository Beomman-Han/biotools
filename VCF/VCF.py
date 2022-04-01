import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from typing import Dict, Generator, List, Literal, Type

from varRecord import varRecord
from File import File
import gzip


class metaFILTER:
    """Class contains 'FILTER' field meta information
    
    Example
    -------
    ##FILTER=<ID=PASS,Description="All filters passed">
    """
    
    def __init__(self,
        id : str,
        desc : str):
        
        self.id = id
        self.desc = desc
        
        return
    
    def __str__(self) -> str:
        return f'<ID={self.id},Description={self.desc}>'


class metaFORMAT:
    """Class contains 'FORMAT' field meta information
    
    Possible Types of FORMAT : Integer, Float, Character, String
    
    Example
    -------
    ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic ..">
    """
    
    TYPES = {'Integer', 'Float', 'Character', 'String'}
    
    def __init__(self,
        id : str,
        number : str,
        type : str,
        desc : str):

        self.id = id
        self.number = number
        self.type = type
        self.desc = desc

        return
    
    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, _type: str):
        if _type not in self.TYPES:
            print(f'[Warning] FORMAT field should have 4 types ({self.TYPES})')
            print(f'This line contains {_type}')
        self._type = _type
        return

    def __str__(self) -> str:
        return f'<ID={self.id},Number={self.number},Type={self.type},Description={self.desc}>'


class metaINFO:
    """Class contains 'INFO' field meta information
    
    Possible Types of INFO : Integer, Float, Flag, Character, String
    
    Example
    -------
    ##INFO=<ID=DP,Number=1,Type=Integer,Description="Approximate...">
    """

    TYPES = {'Integer', 'Float', 'Flag', 'Character', 'String'}


    def __init__(self,
        id : str,
        number : str,
        type : str,
        desc : str):
        
        self.id = id
        self.number = number
        self.type = type
        self.desc = desc
        
        return
    
    @property
    def type(self) -> str:
        return self._type
    
    @type.setter
    def type(self, _type: str):
        if _type not in self.TYPES:
            print(f'[Warning] INFO field should have 5 types ({self.TYPES})')
            print(f'This line contains {_type}')
        self._type = _type
        return
    
    def __str__(self) -> str:
        return f'<ID={self.id},Number={self.number},Type={self.type},Description={self.desc}>'
    

class VCF(File):
    """Class supports various functions for processing VCF file
    It provides general VCF process methods.

    Attributes
    ----------
    To be written...
    
    Methods
    -------
    To be written...
    """

    def __init__(self, vcf_: str) -> None:
        """Initialize VCFProcessor class
        It sets default self.header, checks compressness, opens vcf.
        It prepares vcf processing jobs.

        Parameters
        ----------
        vcf_ : str
            Absolute path of vcf for processing
        """

        ## default header
        self.header = ['CHROM', 'POS', 'ID', 'REF', 'ALT',
                    'QUAL', 'FILTER', 'INFO', 'FORMAT',
                    'SAMPLE']
        self.vcf = vcf_
        self._compressed = self._chk_compressed(self.vcf)
        self.f_obj = False
        self.mode = False

        return

    @property
    def vcf(self) -> str:
        return self._vcf

    @vcf.setter
    def vcf(self, path: str) -> None:
        ## check existence
        if os.path.isfile(path):
            self._vcf = path
        else:
            print(f'[WARNING] {path} does not exist...')
            self._vcf = path
        return

    def _chk_compressed(self, vcf_: str) -> bool:
        """Check whether vcf is compressed (by extension)

        Parameters
        ----------
        vcf_ : str
            Path of input vcf

        Returns
        -------
        bool
            True if compressed, else False
        """

        extension = vcf_.split('.')[-1]
        if extension == 'vcf':
            return False
        elif extension == 'gz':
            return True
        else:
            raise Exception('Check file extension (only .vcf | .vcf.gz)')

    def sanity_check(self) -> bool:
        pass
        return
    
    def parse_meta_info_lines(self) -> Dict[str, List]:
        """Parse meta information lines starting with '##' to save meta info of VCF file.
        Meta information lines must be key=value pairs. Please refer to official VCF format
        document.
        
        Returns
        -------
        Dict[str, List]
            Dictionary containing meta information
        """
        
        meta_info = dict()
        
        ## init new VCF instance
        vcf = VCF(self.vcf)
        vcf.open()
        line = vcf.readline(skip_header=False)
        while line != '':
            if line[:2] != '##':
                break
            
            ## '##FILTER=<...>' -> 'FILTER'
            field = line[2:].strip().split('=')[0]
            if field not in meta_info.keys():
                # meta_info[field] = set()
                meta_info[field] = []
            
            ## '##FILTER=<ID=..,Description="..">' -> '<ID=..,Description="..">'
            contents: str = '='.join(line[2:].strip().split('=')[1:])
            if contents[0] == '<':
                ## '<ID=..,Description=".."">' -> ['ID=..', 'Description=".."']
                temp = contents[1:-1].split(',')
                
                ## 'Description' can have ','
                ## Ex) Description="dbSNP membership, build 129"
                contents_list = []
                for content in temp:
                    if '=' in content:
                        contents_list.append(content)
                    else:
                        contents_list[-1] += f',{content}'

                temp = dict()
                for content in contents_list:
                    # print(content)
                    key = content.split('=')[0]
                    value = content.split('=')[1]
                    ## {'ID':'..', 'Description':'..'}
                    temp[key] = value
                
                ## '##FILTER=<ID=..,Description=..>'
                ## -> {'FILTER': [metaFILTER, ...]}
                if field == 'FILTER':
                    meta_info[field].append(metaFILTER(temp['ID'], temp['Description']))
                elif field == 'FORMAT':
                    meta_info[field].append(metaFORMAT(temp['ID'], temp['Number'],\
                                            temp['Type'], temp['Description']))
                elif field == 'INFO':
                    meta_info[field].append(metaINFO(temp['ID'], temp['Number'],\
                                            temp['Type'], temp['Description']))
                else:
                    ## '##GATKCommandLine=<ID=..,CommandLine=..>'
                    ## -> {'GATKCommandLine': [{'ID':'..', 'CommandLine':'..'}]}
                    meta_info[field].append(temp)
            else:
                ## '##VCFformat=4.2v' -> {'VCFformat':['4.2v']}
                meta_info[field].append(contents)
            line = vcf.readline(skip_header=False)
        
        return meta_info
    
    def reader(self) -> Generator[varRecord, None, None]:
        """Generator function read vcf file line by line.
        
        Yields
        ------
        varRecord
            varRecord parsed from each vcf line
        """
        
        if not self.f_obj:
            print(f'[ERROR] {self.vcf} is not opened.')
            return
        
        line = self.readline()
        while line != '':
            cols = line.strip().split('\t')
            if len(cols) < 9:
                yield varRecord(*cols[:8])
            else:
                yield varRecord(*cols[:8], cols[8], cols[9:], self.header)
            line = self.readline()

        return

    def open(self,
        mode : Literal['r', 'w'] = 'r'
        ) -> None:
        
        """Open self.vcf (.vcf or .vcf.gz path) and
        save TextIOWrapper instance by attribute (self.f_obj).

        Parameters
        ----------
        mode: str (default: 'r')
            'r': read, 'w': write
        """
        
        if mode not in {'r', 'w'}:
            raise Exception('Only \'r\' and \'w\' mode supports')

        ## .vcf.gz case
        if self._compressed:
            mode = 'rb' if mode == 'r' else 'wb'
            f_obj = gzip.open(self.vcf, mode)
            self.mode = mode
        else:
            f_obj = open(self.vcf, mode)
            self.mode = mode
        self.f_obj = f_obj
        return

    def close(self) -> None:
        """Close self.vcf"""
        
        self.f_obj.close()
        self.f_obj = False
        
        return

    def readline(self, skip_header=True) -> str:
        """Read vcf file by one line (~= TextIOWrapper.readline())

        Parameters
        ----------
        skip_header : bool, optional
            Boolean val whether skip header line which starts with '#', by default True

        Returns
        -------
        str
            A line from vcf
        """

        if not self.f_obj:
            self.open(mode='r')

        if self._compressed:
            line = self.f_obj.readline().decode()
            if skip_header:
                while line[:2] == '##':
                    line = self.f_obj.readline().decode()
        else:
            line = self.f_obj.readline()
            if skip_header:
                while line[:2] == '##':
                    line = self.f_obj.readline()

        if line == '':
            return line
        
        if line[0] == '#' and line[:2] != '##':
            self.header = line[1:].strip('\n').split('\t')
            if skip_header:
                line = self.f_obj.readline().decode() if self._compressed else self.f_obj.readline()

        return line

    def write(self, line : str) -> None:
        """Write an input line at self.vcf file.
        This method check input line whether it contains
        proper columns for vcf format comparing to 'self.header'.
        
        Examples
        --------
        >>> vp = VCF('test.vcf')
        ...
        >>> vp.header
        ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'SAMPLE']
        >>> line = 'Line with improper format'
        >>> vp.write(line)  ## do not write improper format line
        >>> 
        >>> line = '##Line with proper format'
        >>> vp.write(line)  ## recognize as header line
        >>> line = 'chr1\t10000\t.\tA\tT\t32\t.\tAC=2;AN=2\tGT:GQ\t1/1:12\n'
        >>> vp.write(line)  ## write one line containing variant info
        >>> vp.close()
        $ cat test.vcf
        ##Line with proper format
        chr1\t10000\t.\tA\tT\t32\t.\tAC=2;AN=2\tGT:GQ\t1/1:12\n
        $

        Parameters
        ----------
        line : str
            A line for writing vcf file
        """

        ## check input line if it has proper format
        if line[:2] != '##':
            if line[0] == '#':
                self.header = line[1:].strip('\n').split('\t')
            else:
                cols = line.strip('\n').split('\t')
                if len(cols) != len(self.header):
                    print('Skip improper formatted line')
                    return
        
        if not self.f_obj:
            self.open(mode='w')

        if line[-1] != '\n':
            line += '\n'
        
        if self._compressed:
            self.f_obj.write(line.encode())
        else:
            self.f_obj.write(line)

        return

    def is_indel(self, line: str) -> bool:
        """Return whether a variant(line) is indel or not"""

        A_allele_idx = self.header.index('REF')
        B_allele_idx = self.header.index('ALT')

        cols     = line.strip('\n').split('\t')
        A_allele = cols[A_allele_idx]
        B_allele = cols[B_allele_idx]

        return (len(A_allele) != len(B_allele))

    def is_snp(self, line: str) -> bool:
        """Return whether a variant(line) is snp or not"""

        A_allele_idx = self.header.index('REF')
        B_allele_idx = self.header.index('ALT')

        cols     = line.strip('\n').split('\t')
        A_allele = cols[A_allele_idx]
        B_allele = cols[B_allele_idx]

        return (len(A_allele) == 1 and len(B_allele) == 1)

    def is_mnp(self, line: str) -> bool:
        """Return whether a variant(line) is mnp or not (snp included)"""

        A_allele_idx = self.header.index('REF')
        B_allele_idx = self.header.index('ALT')

        cols = line.strip('\n').split('\t')
        A_allele = cols[A_allele_idx]
        B_allele = cols[B_allele_idx]

        return (len(A_allele) == len(B_allele))
        
    def get_genotype(self,
        genotypes : List[str]
        ) -> Generator[str, None, None]:
        
        """Bring a variant line containing input genotype in 'GT' field.
        
        Parameters
        ----------
        genotype : List[str]
            Input genotype list for checking
        
        Yields
        ------
        Generator[str, None, None]
            Line containing input genotype
        
        Example
        -------
        >>> proc = VCFProcessor(vcf_path)
        >>> proc.open()
        >>> for line in proc.get_genotype(['0/0'])
        ...     print(line)
        Y	2728456	rs2058276	T	C	32	.	AC=2;AN=2;DB;DP=182;H2;NS=65    GT  0/0
        """
        
        if not self.f_obj:
            ## Open VCF first
            return
        
        if 'FORMAT' not in self.header:
            ## GT info not in VCF
            return

        format_idx = self.header.index('FORMAT')
        line = self.readline()
        while line != '':
            cols = line.strip('\n').split('\t')
            format = cols[format_idx].split(':')
            try:
                gt_idx = format.index('GT')
            except ValueError:
                ## GT info not in VCF
                return
            
            chk_gt = False
            for spl_idx in range(format_idx+1, len(self.header)):
                spl_genotype = cols[spl_idx].split(':')[gt_idx]
                if spl_genotype in genotypes:
                    chk_gt = True
            if chk_gt:
                yield line
            line = self.readline()
        
        return

    def _is_header(self, line : str) -> bool:
        """Check whether input line is vcf header line.
        
        Parameters
        ----------
        line : str
            Input vcf line for checking
        
        Returns
        -------
        bool
            Whether line is header line
        """
        
        return line[0] == '#'


if __name__ == '__main__':
    # vcf = '/Users/hanbeomman/Documents/project/mg-bio/trio.2010_06.ychr.sites.vcf'
    # vcf = '/Users/hanbeomman/Documents/project/mg-bio/test.vcf'
    # proc = VCF(vcf)
    # proc.open()
    
    # for line in proc.get_genotype('0/0'):
    #     print(line.strip())
    
    # for line in proc.filter_genotype(['.', '0', '0/0']):
    #     print(line.strip())
    
    # for line in proc.get_header_line():
    #     print(line.strip())
    
    ## test 'readline' method
    # print(proc.readline())
    # print(proc.readline())
    # print(proc.readline())
    
    # proc.open()
    # print(proc.readline(skip_header=False))
    # print(proc.readline(skip_header=False))
    # print(proc.readline(skip_header=False))
    # print(proc.f_obj.mode)
    
    ## test 'write' method
    # path = '/Users/hanbeomman/Documents/project/mg-bio/test.vcf.gz'
    # proc = VCF(vcf)
    # proc.open(mode='w')
    # proc.write('##Test vcf file')
    # proc.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tTEST')
    # proc.write('chrM\t73\t.\tA\tG\t1551\tPASS\tSNVHPOL=3;MQ=60\tGT:GQ:GQX:DP:DPF:AD:ADF:ADR:SB:FT:PL\t1/1:12:9:5:0:0,5:0,5:0,0:0.0:PASS:111,15,0\n')
    # proc.close()
    
    ## test 'parse_meta_info_lines' method
    path = '/Users/hanbeomman/Documents/project/mg-bio/trio.2010_06.ychr.sites.vcf'
    vcf = VCF(path)
    # meta_info = vcf.parse_meta_info_lines()
    # # print(meta_info)
    # for key in meta_info.keys():
    #     print(f'{key}:{[str(e) for e in meta_info[key]]}')
    
    ## test 'reader' method
    vcf.open()
    for variant in vcf.reader():
        print(variant)