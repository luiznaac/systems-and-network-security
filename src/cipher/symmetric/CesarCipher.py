from CipherInterface import CipherInterface
from symmetric import CipherUtils


class CesarCipher(CipherInterface):

    def cipher(self, key, clear_text):
        char_array = CipherUtils.initializeCharArray()
        return self.getCipherText(key, clear_text, char_array)

    def decipher(self, key, cipher_text):
        char_array = CipherUtils.initializeCharArray()
        return self.getClearText(key, cipher_text, char_array)

    def getCipherText(self, key, clear_text, char_array):
        cipher_text = ''

        for char in clear_text:
            char = CipherUtils.normalizeChar(char)
            cipher_text = '{}{}'.format(cipher_text, CipherUtils.getCipherChar(key, char, char_array))

        return cipher_text

    def getClearText(self, key, cipher_text, char_array):
        clear_text = ''

        for char in cipher_text:
            clear_text = '{}{}'.format(clear_text, CipherUtils.getClearChar(key, char, char_array))

        return clear_text
