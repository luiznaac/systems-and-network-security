from CipherInterface import CipherInterface


class CesarCipher(CipherInterface):

    @staticmethod
    def cipher(key, clear_text):
        return CesarCipher.getCipherText(key, clear_text)

    @staticmethod
    def decipher(key, cipher_text):
        return 'Decipher Cesar'

    @staticmethod
    def getCipherText(key, clear_text):
        cipher_text = ''

        for char in clear_text:
            cipher_text = '{}{}'.format(cipher_text, CesarCipher.getCipherChar(key, char))

        return cipher_text

    @staticmethod
    def getCipherChar(key, char):
        if not CesarCipher.shouldCharBeCiphered(char):
            return char

        char_value = ord(char)

        return chr(CesarCipher.getCipherCharValue(key, char_value))

    @staticmethod
    def shouldCharBeCiphered(char):
        char_value = ord(char)
        return (65 <= char_value <= 90) or (97 <= char_value <= 122)

    @staticmethod
    def getCipherCharValue(key, char_value):
        base_value = 96
        if 65 <= char_value <= 90:
            base_value = 64

        cipher_value = char_value + int(key) - base_value

        if cipher_value > 26:
            return char_value + int(key) - 26 + base_value

        return cipher_value + base_value
