import fileClass
import sanityCheck

if __name__ == "__main__":

    def main():
        filename = input("filename or abspath or relapath : ")
        inputfile = fileClass.File(filename)
        check = sanityCheck.SanityCheck(inputfile)

        if inputfile.get_fileformat() == ".fasta":
            check.fastaSanityCheck()
        

main()

