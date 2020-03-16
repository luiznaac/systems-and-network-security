from CipherInterface import CipherInterface


class CesarCipher(CipherInterface):

    def cipher(self, key, clear_text):
        return self.getCipherText(key, clear_text)

    def decipher(self, key, cipher_text):
        return self.getClearText(key, cipher_text)

    def getCipherText(self, key, clear_text):
        cipher_text = ''

        for char in clear_text:
            cipher_text = '{}{}'.format(cipher_text, self.getCipherChar(key, char))

        return cipher_text

    def getCipherChar(self, key, char):
        if not self.shouldApplyKeyToChar(char):
            return char

        char_value = ord(char)

        return chr(self.getCipherCharValue(key, char_value))

    def getCipherCharValue(self, key, char_value):
        base_value = 96
        if self.isCapitalLetter(char_value):
            base_value = 64

        cipher_value = char_value + int(key) - base_value

        if cipher_value > 26:
            return cipher_value - 26 + base_value

        return cipher_value + base_value

    def getClearText(self, key, cipher_text):
        clear_text = ''

        for char in cipher_text:
            clear_text = '{}{}'.format(clear_text, self.getClearChar(key, char))

        return clear_text

    def getClearChar(self, key, char):
        if not self.shouldApplyKeyToChar(char):
            return char

        char_value = ord(char)

        return chr(self.getClearCharValue(key, char_value))

    def getClearCharValue(self, key, char_value):
        base_value = 96
        if self.isCapitalLetter(char_value):
            base_value = 64

        clear_value = char_value - int(key) - base_value

        if clear_value < 1:
            return 26 + clear_value + base_value

        return clear_value + base_value

    def shouldApplyKeyToChar(self, char):
        char_value = ord(char)
        return (65 <= char_value <= 90) or (97 <= char_value <= 122)

    def isCapitalLetter(self, char_value):
        return 65 <= char_value <= 90
