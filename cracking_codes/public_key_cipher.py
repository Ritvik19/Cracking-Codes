from .utils import primenum, cryptomath
import os, sys, random, math

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def generateKey(keySize):
    p = 0
    q = 0
    print('Generating p and q prime...')
    while p == q:
        p = primenum.generateLargePrime(keySize)
        q = primenum.generateLargePrime(keySize)
    n = p * q

    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    print('Public key:', publicKey)
    print('Private key:', privateKey)

    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):
    if os.path.exists(f'{name}_pubkey.txt') or os.path.exists(f'{name}_privkey.txt'):
        sys.exit('WARNING: The files already exists! Use a different name or delete these files and rerun this program.')

    publicKey, privateKey = generateKey(keySize)

    print()
    print(f'The public key is a {len(str(publicKey[0]))} and a {len(str(publicKey[1]))} digit number.')
    print(f'Writing public key to file {name}_pubkey.txt...')
    with open(f'{name}_pubkey.txt', 'w') as f:
        f.write(f'{keySize},{publicKey[0]},{publicKey[1]}')

    print()
    print(f'The private key is a {len(str(publicKey[0]))} and a {len(str(publicKey[1]))} digit number.')
    print(f'Writing private key to file {name}_privkey.txt...')
    with open(f'{name}_privkey.txt', 'w') as f:
        f.write(f'{keySize},{privateKey[0]},{privateKey[1]}')
        
def getBlocksFromText(message, blockSize):
    for character in message:
        if character not in SYMBOLS:
            print(f'ERROR: The symbol set does not have the character {character}')
            sys.exit()
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(message))):
            blockInt += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize):
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    with open(keyFilename) as f:
        content = f.read()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=None):

    keySize, n, e = readKeyFile(keyFilename)
    if blockSize == None:
        blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size.')
    
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    encryptedContent = f'{len(message)}_{blockSize}_{encryptedContent}'
    with open(messageFilename, 'w') as f:
        f.write(encryptedContent)
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    keySize, n, d = readKeyFile(keyFilename)

    with open(messageFilename) as f:
        content = f.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit('ERROR: Block size is too large for the key and symbol set size.')

    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    return decryptMessage(encryptedBlocks, messageLength, (n, d),blockSize)

