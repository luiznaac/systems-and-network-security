from CrackInterface import CrackInterface


class CesarCrack(CrackInterface):

    def crack(self, cipher_text):
        cipher_frequency = self.getCipherFrequency(cipher_text)
        cipher_frequency = self.sortCipherFrequency(cipher_frequency)

        return self.getClearText(cipher_text, cipher_frequency)

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
        i = 0

        for char in sorted_frequency.keys():
            sorted_frequency.update({char: i})
            i += 1

        return sorted_frequency

    def getClearText(self, cipher_text, cipher_frequency):
        clear_text = ''

        for cipher_char in cipher_text:
            clear_text = '{}{}'.format(clear_text, self.getClearChar(cipher_char, cipher_frequency))

        return clear_text

    def getClearChar(self, cipher_char, cipher_frequency):
        if not self.shouldConsiderChar(cipher_char):
            return cipher_char

        clear_frequency = self.getClearFrequencyReference()
        index = cipher_frequency.get(cipher_char)

        return clear_frequency[index]

    def getClearFrequencyReference(self):
        return [
            'y', 'w', 'k', 'x', 'j', 'z', 'f', 'b', 'q', 'h', 'g', 'v', 'p',
            'l', 'c', 't', 'u', 'm', 'd', 'n', 'i', 'r', 's', 'o', 'e', 'a'
        ]
