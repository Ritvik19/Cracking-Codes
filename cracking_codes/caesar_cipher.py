SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def encryptCaesarCipher(message, key):
    translated = ''
    for symbol in message:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = (symbolIndex + key)%len(SYMBOLS)
            translated = translated + SYMBOLS[translatedIndex]
        else:
            translated = translated + symbol
    return translated

def decryptCaesarCipher(encrypted, key):
    translated = ''
    for symbol in encrypted:
        if symbol in SYMBOLS:
            symbolIndex = SYMBOLS.find(symbol)
            translatedIndex = (symbolIndex - key)%len(SYMBOLS)
            translated = translated + SYMBOLS[translatedIndex]
        else:
            translated = translated + symbol
    return translated

def hackCaesarCipher(encrypted):
    for key in range(len(SYMBOLS)):
        translated = ''
        for symbol in encrypted:
            if symbol in SYMBOLS:
                symbolIndex = SYMBOLS.find(symbol)
                translatedIndex = (symbolIndex - key)%len(SYMBOLS)
                translated = translated + SYMBOLS[translatedIndex]
            else:
                translated = translated + symbol
        print('Key', key, ':', translated)