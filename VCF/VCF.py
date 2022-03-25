import sys, io, gzip, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from typing import Generator, List
from File import File

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
        self.header = ['CHROM', 'POS', 'ID', 'REF', 'ALT',\
                    'QUAL', 'FILTER', 'INFO', 'FORMAT',\
                    'SAMPLE']
        self.vcf = vcf_
        self._compressed = self._chk_compressed(self.vcf)
        self.f_obj = False

        return

    @property
    def vcf(self) -> str:
        return self._vcf

    @vcf.setter
    def vcf(self, path: str) -> None:
        if os.path.isfile(path):
            self._vcf = path
        else:
            print(f'[WARNING] {path} does not exist...')
            self._vcf = path
        return

    def sanity_check(self) -> bool:
        """Check whether self.vcf file has weird format.
        
        > All variant lines have the same # of columns
        > Load ## header lines and check it's ID and Number... etc. is normally matched.
        > Whether REF == ALT allele
        > Check DP == 0
        > Whether chromosome naming is uniform ('chr1' or '1' / 'chrY' or 'chr23' / 'chrM' or 'chrM')
        
        Returns
        -------
        bool
            Is self.vcf normal format
        """
        pass
        return

    def import_from_json(self) -> None:
        pass
        return    

    def export_to_json(self) -> None:
        pass
        return
    
    def reader(self) -> None:
        pass
        return

    def open(self, mode='r') -> io.BufferedReader or io.BufferedWriter:
        """Open self.vcf file (vcf or vcf.gz)

        Parameters
        ----------
        mode: str (default: 'r')
            'r': read, 'w': write

        Returns
        -------
        io.BufferedReader
            io object for reading vcf file
        """

        if self._compressed:
            if mode == 'r':
                mode = 'rb'
            elif mode == 'w':
                mode = 'wb'
            f_obj = gzip.open(self.vcf, mode)
            self.f_obj = f_obj
            return f_obj
        else:
            f_obj = open(self.vcf, mode)
            self.f_obj = f_obj
            return f_obj

    def close(self) -> None:
        """Close self.vcf

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        self.f_obj.close()
        self.f_obj = False
        
        return

    def readline(self, skip_header=True) -> str:
        """Read vcf file by line (~= io.BufferedReader.readline())

        Parameters
        ----------
        skip_header: bool (default: True)
            whether skipping header line which starts '#'

        Returns
        -------
        str
            A line from vcf
        """

        if self._compressed:
            if not self.f_obj:
                self.f_obj = self.open(mode='rb')

            line = self.f_obj.readline().decode()
            if skip_header:
                while line[:2] == '##':
                    line = self.f_obj.readline().decode()
        else:
            if not self.f_obj:
                self.f_obj = self.open(mode='r')
            line = self.f_obj.readline()
            if skip_header:
                while line[:2] == '##':
                    line = self.f_obj.readline()

        ## self.header
        if line == '':
            return line
        
        if line[0] == '#':
            self.header = line[1:].strip('\n').split('\t')
            if skip_header:
                line = self.f_obj.readline().decode() if self._compressed else self.f_obj.readline()

        return line

    def write(self, line: str):
        """Write vcf file by line (~= io.BufferedWriter.write())

        Parameters
        ----------
        line: str
            A line for writing vcf file
        """

        if self._compressed:
            if not self.f_obj:
                self.f_obj = self.open(mode='wb')
            self.f_obj.write(line.encode())
        else:
            if not self.f_obj:
                self.f_obj = self.open(mode='w')
            self.f_obj.write(line)

        return

    def _chk_compressed(self, vcf_: str) -> bool:
        """Check whether vcf is compressed (by extension)

        Parameters
        ----------
        vcf_: str
        > input vcf

        Returns
        -------
        bool
        > is compressed
        """

        extension = vcf_.split('.')[-1]
        if extension == 'gz':
            return True
        elif extension == 'vcf':
            return False
        else:
            print(f'> {self.__class__.__name__} chk_vcf_type()')
            #print(f'> {sys._getframe.f_code.co_name}')
            print('> Only .vcf or .vcf.gz')
            sys.exit()

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
    
    def filter_genotype(self,
        genotypes : List[str]
        ) -> Generator[str, None, None]:
        
        """Bring a variant line not containing input genotypes in 'GT' field.
        
        Parameters
        ----------
        genotype : List[str]
            Input genotype list for checking
        
        Yields
        ------
        Generator[str, None, None]
            Line not containing input genotype
        
        Example
        -------
        >>> proc = VCFProcessor(vcf_path)
        >>> proc.open()
        >>> for line in proc.get_genotype(['0/0'])
        ...     print(line)
        Y	2728456	rs2058276	T	C	32	.	AC=2;AN=2;DB;DP=182;H2;NS=65    GT  0/1
        Y	2728456	rs2058276	T	C	32	.	AC=2;AN=2;DB;DP=182;H2;NS=65    GT  1/1
        Y	2728456	rs2058276	T	C	32	.	AC=2;AN=2;DB;DP=182;H2;NS=65    GT  0/1
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
            
            filt_gt = False
            for spl_idx in range(format_idx+1, len(self.header)):
                spl_genotype = cols[spl_idx].split(':')[gt_idx]
                if spl_genotype in genotypes:
                    filt_gt = True
                    break
            if not filt_gt:
                yield line
                
            line = self.readline()
        
        return
    
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
    
    def is_part_of_genotypes(self, line, genotypes):
        
        if 'FORMAT' not in self.header:
            ## GT info not in VCF
            return

        format_idx = self.header.index('FORMAT')
        cols = line.strip('\n').split('\t')
        format = cols[format_idx].split(':')
        
        try:
            gt_idx = format.index('GT')
        except ValueError:
            ## GT info not in VCF
            return
        
        spl_genotypes = set()
        for spl_idx in range(format_idx+1, len(self.header)):
            spl_genotype = cols[spl_idx].split(':')[gt_idx]
            spl_genotypes.add(spl_genotype)
        if set(genotypes).intersection(spl_genotypes) == spl_genotypes:
            return True
        return False
        
    def _check_header(self, line : str) -> bool:
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
    
    def get_header_line(self):
        
        proc = VCF(self.vcf)
        proc.open()
        line = proc.readline(skip_header=False)
        while line != '':
            if self._check_header(line):
                yield line
            else:
                break
            line = proc.readline(skip_header=False)            
        proc.close()
        
        return

if __name__ == '__main__':
    # vcf = '/Users/hanbeomman/Documents/project/mg-bio/trio.2010_06.ychr.sites.vcf'
    vcf = '/Users/hanbeomman/Documents/project/mg-bio/test.vcf'
    proc = VCF(vcf)
    proc.open()
    # for line in proc.get_genotype('0/0'):
    #     print(line.strip())
    
    # for line in proc.filter_genotype(['.', '0', '0/0']):
    #     print(line.strip())
    
    for line in proc.get_header_line():
        print(line.strip())