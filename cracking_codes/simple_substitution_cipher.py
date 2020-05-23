from .utils import wordpatterns, makewordpatterns
import re, copy

nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def keyIsValid(key):
    keyList = list(key)
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()

    return keyList == lettersList


def encryptSimpleSubstitutionCipher(key, message):
    return translateSimpleSubstitutionCipher(key, message, 'encrypt')


def decryptSimpleSubstitutionCipher(key, message):
    return translateSimpleSubstitutionCipher(key, message, 'decrypt')


def translateSimpleSubstitutionCipher(key, message, mode):
    translated = ''
    charsA = LETTERS
    charsB = key
    if mode == 'decrypt':
        charsA, charsB = charsB, charsA

    for symbol in message:
        if symbol.upper() in charsA:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            translated += symbol

    return translated


def getRandomKey():
    key = list(LETTERS)
    random.shuffle(key)
    return ''.join(key)

def getBlankCipherletterMapping():
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
       'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
       'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
       'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    for i in range(len(cipherword)):
        if candidate[i] not in letterMapping[cipherword[i]]:
            letterMapping[cipherword[i]].append(candidate[i])


def intersectMappings(mapA, mapB):
    intersectedMapping = getBlankCipherletterMapping()
    for letter in LETTERS:
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    loopAgain = True
    while loopAgain:
        loopAgain = False

        solvedLetters = []
        for cipherletter in LETTERS:
            if len(letterMapping[cipherletter]) == 1:
                solvedLetters.append(letterMapping[cipherletter][0])

        for cipherletter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherletter]) != 1 and s in letterMapping[cipherletter]:
                    letterMapping[cipherletter].remove(s)
                    if len(letterMapping[cipherletter]) == 1:
                        loopAgain = True
    return letterMapping


def hackSimpleSubstitutionCipher(message):
    intersectedMap = getBlankCipherletterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('', message.upper()).split()
    for cipherword in cipherwordList:
        candidateMap = getBlankCipherletterMapping()

        wordPattern = makewordpatterns.getWordPattern(cipherword)
        if wordPattern not in wordpatterns.allPatterns:
            continue 
        for candidate in wordpatterns.allPatterns[wordPattern]:
            addLettersToMapping(candidateMap, cipherword, candidate)

        intersectedMap = intersectMappings(intersectedMap, candidateMap)

    return removeSolvedLettersFromMapping(intersectedMap)


def decryptWithCipherletterMapping(ciphertext, letterMapping):

    key = ['x'] * len(LETTERS)
    for cipherletter in LETTERS:
        if len(letterMapping[cipherletter]) == 1:
            keyIndex = LETTERS.find(letterMapping[cipherletter][0])
            key[keyIndex] = cipherletter
        else:
            ciphertext = ciphertext.replace(cipherletter.lower(), '_')
            ciphertext = ciphertext.replace(cipherletter.upper(), '_')
    key = ''.join(key)

    return decryptSimpleSubstitutionCipher(key, ciphertext)