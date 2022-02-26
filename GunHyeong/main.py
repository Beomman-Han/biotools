#import fileClass
import sanityCheck
from fileClass import *

if __name__ == "__main__":

    def main():
        filename = input("filename or abspath or relapath : ")
        inputfile = File(filename)
        check = sanityCheck.SanityCheck(inputfile)

        if inputfile.get_fileformat() == ".fasta":
            check.fastaSanityCheck()
        

main()

