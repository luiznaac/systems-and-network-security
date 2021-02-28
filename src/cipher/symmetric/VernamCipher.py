from CipherInterface import CipherInterface
import random

class VernamCipher(CipherInterface):

    def cipher(self, key_filename, clear_text):
        key = self.computeKey(len(clear_text))
        self.writeKeyToFile(key, key_filename)
        return self.getCipherText(key, clear_text)

    def decipher(self, key_filename, cipher_text):
        pass

    def computeKey(self, text_length):
        key = ''

        for i in range(0, text_length):
            key = '{}{}'.format(key, chr(random.randint(0, 100)))

        return key

    def writeKeyToFile(self, key, key_filename):
        file = open(key_filename, 'w+')
        file.write(key)
        file.close()

    def getCipherText(self, key, clear_text):
        cipher_text = ''

        for i in range(0, len(clear_text)):
            clear_char = clear_text[i]
            char_key = ord(key[i])
            cipher_char = chr(ord(clear_char) + char_key)
            cipher_text = '{}{}'.format(cipher_text, cipher_char)

        return cipher_text
