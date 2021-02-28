def initializeCharArray():
    char_array = getCharsInRange(ord('A'), ord('Z'))
    char_array += getCharsInRange(ord('a'), ord('z'))
    char_array += getCharsInRange(ord('0'), ord('9'))

    return char_array


def getCharsInRange(initial_value, final_value):
    chars = []

    for char_value in range(initial_value, final_value + 1):
        chars.append(chr(char_value))

    return chars


def normalizeChar(char):
    if isCapitalLetter(char):
        char = chr(ord(char) + 32)

    return higienizeChar(char)


def isCapitalLetter(char):
    return ord('A') <= ord(char) <= ord('Z')


def higienizeChar(char):
    char_map = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'Á': 'a', 'À': 'a', 'Ã': 'a', 'Â': 'a',
        'é': 'e', 'ê': 'e',
        'É': 'e', 'Ê': 'e',
        'í': 'i',
        'Í': 'i',
        'ó': 'o', 'õ': 'o', 'ô': 'o',
        'Ó': 'o', 'Õ': 'o', 'Ô': 'o',
        'ú': 'u',
        'Ú': 'u',
        'ç': 'c',
        'Ç': 'c',
    }

    if char in char_map:
        return char_map[char]

    return char


def getCipherChar(key, char, char_array):
    if not shouldApplyKeyToChar(char):
        return char

    clear_char_index = char_array.index(char)
    cipher_char_index = getCipherCharIndex(
        key,
        clear_char_index,
        len(char_array)
    )

    return char_array[cipher_char_index]


def getCipherCharIndex(key, clear_char_index, char_array_length):
    key = int(key) % char_array_length
    cipher_char_index = clear_char_index + key

    if cipher_char_index >= char_array_length:
        return cipher_char_index - char_array_length

    return cipher_char_index


def getClearChar(key, char, char_array):
    if not shouldApplyKeyToChar(char):
        return char

    cipher_char_index = char_array.index(char)
    clear_char_index = getClearCharIndex(
        key,
        cipher_char_index,
        len(char_array)
    )

    return char_array[clear_char_index]


def getClearCharIndex(key, cipher_char_index, char_array_length):
    key = int(key) % char_array_length
    clear_char_index = cipher_char_index - key

    if clear_char_index < 0:
        return char_array_length + clear_char_index

    return clear_char_index


def shouldApplyKeyToChar(char):
    char_value = ord(char)
    return (ord('a') <= char_value <= ord('z')) or \
           (ord('A') <= char_value <= ord('Z')) or \
           (ord('0') <= char_value <= ord('9'))
