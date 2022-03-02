import sys, io, gzip, os
from FileProcessor import FileProcessor

class VCFProcessor(FileProcessor):
	"""Class for processing VCF file
	It provides general VCF process methods.

	Member variables
	----------------
	self.header: list
	> last header of vcf
	self.f_vcf_: str
	> vcf path for processing
	self.compressed: bool
	> is vcf compressed (vcf.gz)
	self.vcf: io.BufferedReader
	> opened file object of self.f_vcf_

	Methods
	-------
	self.chk_compressed()
	self.open()
	self.close()
	self.readline()
	self.extract_dnv()
	self.extract_snv()
	self.reader() (depricated)
	self.read_vcf() (depricated)
	self.read_skipping_header() (depricated)
	self.X_extract_dnv_tmp() (depricated)
	"""

	def __init__(self, vcf_: str) -> None:
		"""Initialize VCFProcessor class
		It sets default self.header, checks compressness, opens vcf.
		It prepares vcf processing jobs.

		Parameters
		----------
		vcf_: str
		> path of vcf for processing

		Returns
		-------
		None
		"""

		self.header = ['CHROM', 'POS', 'ID', 'REF', 'ALT',\
					'QUAL', 'FILTER', 'INFO', 'FORMAT',\
					'SAMPLE']
		self.f_vcf_ = vcf_
		self._compressed = self._chk_compressed(self.f_vcf_)
		#self.vcf = self.open()

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

		if self.compressed:
			if mode == 'r':
				mode = 'rb'
			elif mode == 'w':
				mode = 'wb'
			f_obj = gzip.open(self.f_vcf_, mode)
			self.vcf = f_obj
			return f_obj
		else:
			f_obj = open(self.f_vcf_, mode)
			self.vcf = f_obj
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

		self.vcf.close()

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
			if self.vcf == None:
				self.vcf = self.open(mode='rb')

			line = self.vcf.readline().decode()
			if skip_header:
				while line[:2] == '##':
					line = self.vcf.readline().decode()
		else:
			if self.vcf == None:
				self.vcf = self.open(mode='r')
			line = self.vcf.readline()
			if skip_header:
				while line[:2] == '##':
					line = self.vcf.readline()

		## self.header
		if line[0] == '#':
			self.header = line[1:].strip('\n').split('\t')
			line = self.vcf.readline().decode() if self._compressed else self.vcf.readline()

		return line

	def write(self, line: str):
		"""Write vcf file by line (~= io.BufferedWriter.write())

		Parameters
		----------
		line: str
			A line for writing vcf file
		"""

		if self._compressed:
			if self.vcf == None:
				self.vcf = self.open(mode='wb')
			self.vcf.write(line.encode())
		else:
			if self.vcf == None:
				self.vcf = self.open(mode='w')
			self.vcf.write(line)

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

	@property
	def f_vcf_(self) -> str:
		return self._f_vcf_

	@f_vcf_.setter
	def f_vcf_(self, path: str) -> None:
		if os.path.isfile(path):
			self._f_vcf_ = path
		else:
			print(f'{path} does not exist...')
			sys.exit()
		return
