import math
from .utils import detect_english

def encryptTranspositionCipher(message, key):
    ciphertext = [''] * key
    
    for column in range(key):
        currentIndex = column
        
        while currentIndex < len(message):
            ciphertext[column] += message[currentIndex]
            currentIndex += key
            
    return ''.join(ciphertext)

def decryptTranspositionCipher(encrypted, key):
    numOfColumns = int(math.ceil(len(encrypted) / float(key)))

    numOfRows = key

    numOfShadedBoxes = (numOfColumns * numOfRows) - len(encrypted)

    plaintext = [''] * numOfColumns

    column = 0
    row = 0
    
    for symbol in encrypted:
        plaintext[column] += symbol
        column += 1 

        if (column == numOfColumns) or (column == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            column = 0
            row += 1

    return ''.join(plaintext)

def hackTranspositionCipher(message):
    for key in range(1, len(message)):
        print(f'Trying key #{key}...')

        decryptedText = decryptTranspositionCipher(message, key)
        
        if detect_english.isEnglish(decryptedText):
            print()
            print('Possible encryption hack:')
            print(decryptedText[:100])
            print()
    print('Done')