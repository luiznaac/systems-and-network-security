from CrackInterface import CrackInterface
from symmetric import CipherUtils
from symmetric.CesarCipher import CesarCipher


class CesarCrack(CrackInterface):

    def crack(self, cipher_text):
        cipher_frequency = self.getCipherFrequency(cipher_text)
        sorted_cipher_frequency = self.sortCipherFrequency(cipher_frequency)
        char_with_most_occurrences = sorted_cipher_frequency.pop()

        return self.getClearText(cipher_text, char_with_most_occurrences)

    def getCipherFrequency(self, cipher_text):
        cipher_frequecy = {}

        for char in cipher_text:
            if not self.shouldConsiderChar(char):
                continue

            char_frequency = cipher_frequecy[char] if char in cipher_frequecy else 0
            char_frequency += 1
            cipher_frequecy.update({char: char_frequency})

        return cipher_frequecy

    def shouldConsiderChar(self, char):
        char_value = ord(char)
        return (ord('a') <= char_value <= ord('z')) or \
               (ord('A') <= char_value <= ord('Z')) or \
               (ord('0') <= char_value <= ord('9'))

    def sortCipherFrequency(self, cipher_frequency):
        sorted_frequency = {k: v for k, v in sorted(cipher_frequency.items(), key=lambda item: item[1])}
        i = sorted_frequency.__len__() - 1

        for char in sorted_frequency.keys():
            sorted_frequency.update({char: i})
            i -= 1

        return list(sorted_frequency)

    def getClearText(self, cipher_text, char_with_most_occurrences):
        cracked_key = self.crackKey(char_with_most_occurrences)

        return CesarCipher().decipher(cracked_key, cipher_text)

    def crackKey(self, char_with_most_occurrences):
        char_array = CipherUtils.initializeCharArray()
        cipher_index = char_array.index(char_with_most_occurrences)
        clear_index = char_array.index(self.getMostOccuryingClearLetter())

        return abs(cipher_index - clear_index)

    def getClearChar(self, cipher_char, cipher_frequency):
        if not self.shouldConsiderChar(cipher_char):
            return cipher_char

        clear_frequency = self.getClearFrequencyReference()
        index = cipher_frequency.get(cipher_char)

        return clear_frequency[index] if index < len(clear_frequency) else '?'

    def getMostOccuryingClearLetter(self):
        return 'a'

    def getClearFrequencyReference(self):
        clear_frequency = [
            'y', 'w', 'k', 'x', 'j', 'z', 'f', 'b', 'q', 'h', 'g', 'v', 'p',
            'l', 'c', 't', 'u', 'm', 'd', 'n', 'i', 'r', 's', 'o', 'e', 'a'
        ]

        clear_frequency.reverse()

        return clear_frequency
