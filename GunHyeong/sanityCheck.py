from collections import namedtuple
import fasta

class SanityCheck:
    def __init__(self, inputfileObject) -> None:
        self._inputfileObject = inputfileObject
        #print(self._inputfileObject)

    def fastaSanityCheck(self) -> bool:
        
        """fastaSanityCheck [summary]

        Verify that the file is a fasta file.

        Returns
        -------
        bool
            [description]

            If it is a fasta file, return true, or false.
        """

        fastaElement : list= ['A','T','G','C','N','R','Y','S','W','K','M','B','D','H','V']

        print(f'file format is fasta. \nStart the sanity check for {self._inputfileObject._filepath}')
        fr :IO = open(self._inputfileObject._filepath,"r")
        for line, value in enumerate(fr, start=1):
            if line % 2 == 1:
                if value[0] == ">":
                    pass
                    print(f'Header : {value}',end='')
                else:
                    #raise Exception(f'헤더를 확인하세요 -> Header : {value[0]}')
                    print(f'Check header -> Header : {value[0]}')
                    return False
            else:
                
                checkbase = [base in fastaElement for base in value.strip()]
                checkbool :bool = all(checkbase)
                #print(checkbool)
                #print(checkbase)
                a =list((filter(lambda x: x, checkbase)))
                if checkbool == False:
                    misbaseList = [ (value[i],i+1) for i, b in enumerate(checkbase) if b == False]
                    #print(misbaseList)
                    print(f'Please enter a valid seq : \n(misbase,seq position. : {misbaseList} \n')
        if checkbool == False:
            print("Check the seq")
            return False
        else:
            print("Seq is normal.")
            return True

    def samSanityCheck(self) -> bool:
        print("파일 포맷은 sam입니다.")
        return 0 

    def fastqSanityCheck(self) -> bool:
        print("파일 포맷은 fastq입니다.")
        return 0
