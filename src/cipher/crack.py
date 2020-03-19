import sys

from CrackInterface import CrackInterface
from symmetric.crack.CesarCrack import CesarCrack


CIPHERTYPE = 1
INPUTTEXT = 2
OUTPUTTEXT = 3


def main():
    crack = getCrackInstance()
    input_text = getInputText()
    output_text = crack.crack(input_text)
    writeToFile(output_text)


def getCrackInstance() -> CrackInterface:
    crack_name = getCrackClassName()
    return globals()[crack_name]()


def getCrackClassName():
    crack_name = sys.argv[CIPHERTYPE]
    return "{}Crack".format(crack_name.capitalize())


def getInputText():
    filename = sys.argv[INPUTTEXT]
    file = open(filename, 'r+')
    text = file.read()
    file.close()
    return text


def writeToFile(output_text):
    filename = '{}_{}'.format(getCrackClassName(), sys.argv[OUTPUTTEXT])
    file = open(filename, 'w+')
    file.write(output_text)
    file.close()


if __name__ == '__main__':
    main()
