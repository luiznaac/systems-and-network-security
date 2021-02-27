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
