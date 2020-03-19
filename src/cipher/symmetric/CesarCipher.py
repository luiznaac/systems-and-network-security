from CipherInterface import CipherInterface


class CesarCipher(CipherInterface):

    def cipher(self, key, clear_text):
        char_array = self.initializeCharArray()
        return self.getCipherText(key, clear_text, char_array)

    def decipher(self, key, cipher_text):
        char_array = self.initializeCharArray()
        return self.getClearText(key, cipher_text, char_array)

    def initializeCharArray(self):
        char_array = self.getCharsInRange(ord('a'), ord('z'))
        char_array += self.getCharsInRange(ord('A'), ord('Z'))
        char_array += self.getCharsInRange(ord('0'), ord('9'))

        return char_array

    def getCharsInRange(self, initial_value, final_value):
        chars = []

        for char_value in range(initial_value, final_value + 1):
            chars.append(chr(char_value))

        return chars

    def getCipherText(self, key, clear_text, char_array):
        cipher_text = ''

        for char in clear_text:
            cipher_text = '{}{}'.format(cipher_text, self.getCipherChar(key, char, char_array))

        return cipher_text

    def getCipherChar(self, key, char, char_array):
        if not self.shouldApplyKeyToChar(char):
            return char

        clear_char_index = char_array.index(char)
        cipher_char_index = self.getCipherCharIndex(
            key,
            clear_char_index,
            char_array.__len__()
        )

        return char_array[cipher_char_index]

    def getCipherCharIndex(self, key, clear_char_index, char_array_length):
        key = int(key) % char_array_length
        char_array_length -= 1
        cipher_char_index = clear_char_index + key

        if cipher_char_index > char_array_length:
            return cipher_char_index - char_array_length

        return cipher_char_index

    def getClearText(self, key, cipher_text, char_array):
        clear_text = ''

        for char in cipher_text:
            clear_text = '{}{}'.format(clear_text, self.getClearChar(key, char, char_array))

        return clear_text

    def getClearChar(self, key, char, char_array):
        if not self.shouldApplyKeyToChar(char):
            return char

        cipher_char_index = char_array.index(char)
        clear_char_index = self.getClearCharIndex(
            key,
            cipher_char_index,
            char_array.__len__()
        )

        return char_array[clear_char_index]

    def getClearCharIndex(self, key, cipher_char_index, char_array_length):
        key = int(key) % char_array_length
        char_array_length -= 1
        clear_char_index = cipher_char_index - key

        if clear_char_index < 0:
            return char_array_length + clear_char_index

        return clear_char_index

    def shouldApplyKeyToChar(self, char):
        char_value = ord(char)
        return (ord('a') <= char_value <= ord('z')) or \
               (ord('A') <= char_value <= ord('Z')) or \
               (ord('0') <= char_value <= ord('9'))
