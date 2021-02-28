from CipherInterface import CipherInterface
from symmetric import CipherUtils
import random
import io

class VernamCipher(CipherInterface):

    def cipher(self, key_filename, clear_text):
        key = self.computeKey(len(clear_text))
        self.writeKeyToFile(key, key_filename)
        char_array = CipherUtils.initializeCharArray()
        return self.getCipherText(key, clear_text, char_array)

    def decipher(self, key_filename, cipher_text):
        key = self.loadKey(key_filename)
        char_array = CipherUtils.initializeCharArray()
        return self.getClearText(key, cipher_text, char_array)

    def computeKey(self, text_length):
        key = []

        for i in range(0, text_length):
            key.append(random.randint(0, 62))

        return key

    def writeKeyToFile(self, key, key_filename):
        file = open(key_filename, 'w+')
        file.write(','.join([str(single_key) for single_key in key]))
        file.close()

    def getCipherText(self, key, clear_text, char_array):
        cipher_text = ''

        for clear_char in clear_text:
            clear_char = CipherUtils.normalizeChar(clear_char)
            char_key = key.pop(0)
            cipher_text = '{}{}'.format(cipher_text, CipherUtils.getCipherChar(char_key, clear_char, char_array))

        return cipher_text

    def loadKey(self, key_filename):
        file = io.open(key_filename, mode='r', encoding='utf-8')
        text = file.read()
        file.close()
        return [int(single_key) for single_key in text.split(',')]

    def getClearText(self, key, cipher_text, char_array):
        clear_text = ''

        for cipher_char in cipher_text:
            char_key = key.pop(0)
            clear_text = '{}{}'.format(clear_text, CipherUtils.getClearChar(char_key, cipher_char, char_array))

        return clear_text
