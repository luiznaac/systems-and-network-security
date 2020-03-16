from CipherInterface import CipherInterface


class CesarCipher(CipherInterface):

    def cipher(self, key, clear_text):
        return self.getCipherText(key, clear_text)

    def decipher(self, key, cipher_text):
        return 'Decipher Cesar'

    def getCipherText(self, key, clear_text):
        cipher_text = ''

        for char in clear_text:
            cipher_text = '{}{}'.format(cipher_text, self.getCipherChar(key, char))

        return cipher_text

    def getCipherChar(self, key, char):
        if not self.shouldCharBeCiphered(char):
            return char

        char_value = ord(char)

        return chr(self.getCipherCharValue(key, char_value))

    def shouldCharBeCiphered(self, char):
        char_value = ord(char)
        return (65 <= char_value <= 90) or (97 <= char_value <= 122)

    def getCipherCharValue(self, key, char_value):
        base_value = 96
        if self.isCapitalLetter(char_value):
            base_value = 64

        cipher_value = char_value + int(key) - base_value

        if cipher_value > 26:
            return char_value + int(key) - 26 + base_value

        return cipher_value + base_value

    def isCapitalLetter(self, char_value):
        return 65 <= char_value <= 90
