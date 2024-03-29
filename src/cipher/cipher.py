import sys
import io

from CipherInterface import CipherInterface
from symmetric.CesarCipher import CesarCipher
from symmetric.VernamCipher import VernamCipher


options = {
    '-c': 'cipher',
    '-d': 'decipher',
}

CIPHERTYPE = 1
USEROPTION = 2
USERKEY = 4
INPUTTEXT = 5
OUTPUTTEXT = 6


def main():
    cipher = getCipherInstance()
    option = getUserOption(cipher)
    key = getUserKey()
    input_text = getInputText()
    output_text = option(key, input_text)
    writeToFile(output_text)


def getCipherInstance() -> CipherInterface:
    cipher_name = getCipherClassName()
    return globals()[cipher_name]()


def getCipherClassName():
    cipher_name = sys.argv[CIPHERTYPE]
    return "{}Cipher".format(cipher_name.capitalize())


def getUserOption(cipher):
    option_param = sys.argv[USEROPTION]
    return getattr(cipher, options[option_param])


def getUserKey():
    return sys.argv[USERKEY]


def getInputText():
    filename = sys.argv[INPUTTEXT]
    file = io.open(filename, mode='r', encoding='utf-8')
    text = file.read()
    file.close()
    return text


def writeToFile(output_text):
    filename = '{}_{}'.format(getCipherClassName(), sys.argv[OUTPUTTEXT])
    file = open(filename, 'w+')
    file.write(output_text)
    file.close()


if __name__ == '__main__':
    main()
