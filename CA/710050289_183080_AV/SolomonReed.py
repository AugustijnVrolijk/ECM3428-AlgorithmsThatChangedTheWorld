import random
from itertools import combinations


"""
lagrangePolgen: generates a lagrange polynomials for a list of points, with 1 point specified as the unit point
for a set of n points, there are n lagrange polynomials, where each one has x intercept at all but one of n points,
and a value of 1 for the last point

i.e. for points: (1,5)(2,3)(3,8)(4,15), unit point (1,5) a lagrange polynomial would have points (1,1)(2,0)(3,0)(4,0)

inputs: toExclude - unit point (x value)
        toInclude - all n points (X values

returns: lagrange polynomial for n points with unit point toExclude
"""
def lagrangePolGen(toExclude:int, toInclude:list) -> list:
    
    #find which x values need to be made 0, i.e. for points mentioned above -> y = c(x-2)(x-3)(x-4)
    #therefore converting x value to negative, to make x intercept for that value
    roots = []
    for int in toInclude:
        if toExclude == int:
            continue
        roots.append(-int)

    #calculate coefficient needed to make unit point have y value 1
    #i.e. for above points: y = c(x-2)(x-3)(x-4)
    #                       1 = c(1-2)(1-3)(1-4)
    #                       c = 1/(1-2)(1-3)(1-4)
    coefficient = 1 
    for int in roots:
        temp = int + toExclude #find (x-a) (toEclude is negative)
        coefficient = coefficient*temp #find (x-a)(x-b)(x-c)
    coefficient = 1/coefficient 

    #finding y = ax^n + ... + bx + c from list roots, which representt each x intercept -> (-1, -2, -3) -> (x-1)(x-2)(x-3)
    #recursively multiply standard polynomial 1, by each group, 1(x-1) -> (x-1)(x-2) -> (x^2-3x+2)(x-3)    
    #position of polynomial determines order of x
    polynomial = [1]
    for root in roots:
        temp = polynomial.copy() #copy polynomial before increasing order, allows to multiply a polynomial by both x, and -1 for (x-1) seperately
        polynomial.append(0) #multiplying by x, increase order of every value, final value has no x value and is therefore 0
        i = 1
        for order in temp:
            order = root*order #multiplying by x intercept value, i.e. -1
            polynomial[i] += order #combining both seperately added polynomials
            i += 1

    
    #multiplying each polynomial coefficient to ensure unit point has value 1
    for i in range(len(polynomial)):
        polynomial[i] = polynomial[i]*coefficient

    return polynomial


"""
calcPol: calculates the lagrange interpolating polynomial, i.e for n points, finds a polynomial of order n-1 which traverses all n points
This has the property of being unique, i.e. no other polynomial of order n-1 can traverse all n points.

done by calculating lagrange polynomials for n points, i.e. n polynomials which have y=0 for all for the x values of n-1 points, and y=1 
for the last point, these have order n-1.

These polynomials are then summed and multiplied by its real corresponding y value

for points (1,3)(2,7)(3,4)
l1 = c1(x-2)(x-3), where l1 = 1 at x = 1
l2 = c2(x-1)(x-3), where l2 = 1 at x = 2
l3 = c3(x-1)(x-2), where l3 = 1 at x = 3

l = 3l1 + 7l2 + 4l3

inputs: list of n points to find lagrange polynomial each point is a tuple (x,y)

returns: lagrange interpolating polynomial
"""

def calcPol(list:list) -> list:

    polynomial = [0] * len(list)

    #x values needed to calculate lagrange polynomials
    roots = []
    for point in list:
        roots.append(point[0])

    for point in list:
        temp = lagrangePolGen(point[0], roots) #calculate lagrange polynomial for specifc unit point
        for index in range(len(temp)):
            polynomial[index] += temp[index]*point[1] #lagrange interpolating polynomial = lagrange polynomial for each point * y value 
    
    for i in range(len(polynomial)):
        polynomial[i] = round(polynomial[i],9) #rounded to remove floating point inaccuracies, needed for the decoder

    return polynomial

"""
calcParityChars: calculates parity characters based on a polynomial defined by the message to add to the message

inputs: polynomial - list of coefficients, position and length determine order, i.e [1,-5,3.5,2] = x^3 -5x^2 + 3.5x + 2
        messageLen - message length n
        codeLen - number of parity char to calculate
returns: list of parity characters to add to message
"""
def calcParityChars(polynomial:list, messageLen: int, codeLen: int) -> list:
    parityBits = []
    for j in range(codeLen):
        x = messageLen + j #message represents x values 0 -n-1, therefore calculate parity char from n onwards
        tempBit = 0
        order = 1
        for coefficient in polynomial:
            tempBit += coefficient*(x**(len(polynomial)-order)) #calculate y value for specified x value based on polynomial
            order += 1
        parityBits.append(round(tempBit)) #round to remove floating point inaccuracies 

    return parityBits


"""
solomonEncoder: generates a unique polynomial based on a message, calculates parity char based on this polynomial to add to the encoded message

inputs: message - message of length < blocklen to encode
        blockLen - total encoded message length, determines number of parity bits to add

returns: encoded message
"""
def solomonEncoder(message: list, blockLen: int, isWord:bool = False) -> list:

    if isWord:
        temp = []
        for letter in message:
            temp.append(ord(letter)) #find ASCII code for a symbol, convert string to array of numbers
        message = temp

    codeLen = blockLen-len(message) #length of added parity char, more means a safer more protected message

    messagePoints = [] #convert each char in a message into a point, value is y value, order is x value
    for i in range(len(message)):
        messagePoints.append((i,message[i]))

    polynomial = calcPol(messagePoints)
    parityChars = calcParityChars(polynomial, len(message), codeLen)
    
    encodedMessage = message.copy()
    for char in parityChars:
        encodedMessage.append(char)
    
    return encodedMessage

"""
calcParityChars: calculates parity characters based on a polynomial defined by the message to add to the message

inputs: polynomial - list of coefficients, position and length determine order, i.e [1,-5,3.5,2] = x^3 -5x^2 + 3.5x + 2
        messageLen - message length n
returns: list of parity characters to add to message
"""
def calcOriginalMessage(polynomial:list, messageLen: int) -> list:
    message = []
    for x in range(messageLen):
        tempBit = 0
        order = 1
        for coefficient in polynomial:
            tempBit += coefficient*(x**(len(polynomial)-order)) #calculate y value for specified x value based on polynomial
            order += 1
        message.append(round(tempBit)) #round to remove floating point inaccuracies 

    return message


"""
solomonDecoder: returns original message from an encoded message, reverts errors, 
                protects up to codeLen (len(encodedMessage - messageLen) errors

works by calculating all possible lagrange interpolating polynomials for message len, from the encoded message
as a lagrange interpolating polynomial is unique, all combinations without an error create the same polynomial,
ones with error create a different one

ascertains original message from the most popular polynomial to revert errors.

inputs: encodedMessage: Reed-solomon encoded message
        messageLen: length of the actual message
        isWord: boolean if message is array of numbers or a string

returns: Original message
"""
def solomonDecoder(encodedMessage: list, messageLen, isWord:bool = False) -> list:
    
    messagePoints = [] #convert each char in a message into a point, value is y value, order is x value
    for i in range(len(encodedMessage)):
        messagePoints.append((i,encodedMessage[i]))

    possiblePol = {}
    possibleCombinations = list(combinations(messagePoints, messageLen)) #find all combinations of potential messages

    #for every possible message combination, calculate its lagrange interpolating polynomial, if a message has no error each subset
    #will result in the same polynomial. Counting them results in the most probable correct polynomial to correct potential errors
    for possible in possibleCombinations:
        pol = tuple(calcPol(possible))
        if pol in possiblePol.keys():
            possiblePol[pol] += 1
            continue
        possiblePol[pol] = 1
    
    polynomial = max(possiblePol, key=possiblePol.get)
    message = calcOriginalMessage(polynomial, messageLen)

    if isWord:
        temp = ""
        for i in range(len(message)):
            temp += chr(message[i])
        message = temp

    return message

    """
    corrupter: corrupts a number of characters in a message to random integers

    inputs: message - list of integers, represent original encoded message
            numberOfCorruptions - int, represents number of integers to be randomly changed

    returns: corrupted message - corrupted copy of the encoded message
    """
def corrupter(message: list, numberOfCorruptions: int):
    
    if numberOfCorruptions >= len(message): #check valid number of corruptions
        print("Too many corruptions")
        return message

    corruptedMessage = message

    i = 0
    corruptedIndexes = []
    while i < numberOfCorruptions:  #corrupt specified of numberOfCorruptions indexes from message
        index = random.randint(0 , len(message)-1)
        
        if index in corruptedIndexes:
            continue
        
        corruptedMessage[index] = random.randint(0,255)
        corruptedIndexes.append(index)
        i += 1        

    return corruptedMessage

    """
    test: test function to allow encoding and decoding of message, also allowing to corrupt message to ensure the Reed-Solomon codes work

    inputs: message             - original message to encode and decode
            blocklen            - int, length of desired encoded message
            isWord              - bool, is the message a string or an array of numbers
            toCorrupt           - bool, whether to corrupt the message or not
            numberOfCorruptions - int, if to corrupt, how many values to corrupt

    returns: nothing
    """
def test(message, blockLen, isWord: bool = False, toCorrupt: bool = False, numberOfCorruptions: int = 0):
    
    #check valid messagelength
    if len(message) >= blockLen:
        print("MessageLength must be greater than message")
        return
    
    #encode message and print resulting encoded message
    encodedMessage = solomonEncoder(message, blockLen, isWord)
    print("The original message '{}' is encoded as '{}'".format(message, encodedMessage))

    #randomly corrupt message
    if toCorrupt:
        encodedMessage = corrupter(encodedMessage, numberOfCorruptions)

    decodedMessage = solomonDecoder(encodedMessage, len(message), isWord)
    if toCorrupt:
        print("The corrupted encoded message '{}' is decoded as '{}'\n".format(encodedMessage, decodedMessage))
    else:
        print("The encoded message '{}' is decoded as '{}'\n".format(encodedMessage, decodedMessage))

    return

def main():

    #test(message, codedMessageLength, isWord, toCorrupt, NumberOfCorruptions)
    test([1,5,2,3,7], 8, False, True, 2)
    """
    64-bit solomon reed encoding, of which 24 are needed as parity bits to protect up to 16 contiguous bit flips in the best case 
    along 2 integers, or 2 bits in the worst case.
    this is a (5,3) (message length, parity char) or (40,64) (messagelength, codelength) solomon-reed encoded 
    """
    test("Hello", 8, True, True, 2)
    """
    64-bit solomon reed encoding, of which 24 are needed as parity bits to protect up to 16 contiguous bit flips in the best case 
    along 2 character, or 2 bits in the worst case.
    this is a (5,3) (message length, parity char) or (40,64) (messagelength, codelength) solomon-reed encoded 
    """
    test ("Hello world", 16, True, False)
    print("retesting adding corruption to the message\n")
    test ("Hello world", 16, True, True, 1)
    """
    #This is probably due to rounding errors at high numbers, i'm rounding to 9 decimal places, whereas the lagrange polynomials for a sentence
    of 11 characters is of order 10. Therefore has a x^10 variable, when multiplied by large parity chars it is messing with the rounding.
    This is why  only "hello wor" is correctly transcribed when no corruptions are present, values at lower x values of the lagrange polynomial 
    (0-9) are not corrupted, but those at higher x values, 10-11 are.

    In actually implemented Reed-solomon codes, galois fields are used to work under finite field arithmetic, usually a Galois field of 2^8,
    or 256 this overcomes the obstacle of floating point inaccuracies and rounding errors
    This also ensures every encoded parity character remains a normal ASCII Character, unlike some I generated when encoding "Hello world", 
    where the highest reached 33388952, which would need at least 25 bits to encode, therefore 32 when encoded as a long long. This would make
    the spacial efficacy of this encoding quite poor compared to a regular 8 bit char

    128-bit solomon reed encoding, of which 40 are needed as parity bits to protect up to 24 contiguous bit flips in the best case 
    along 3 characters, or 3 bits in the worst case. Would need to work under a galois field in order to work
    this is a (11,5) (message length, parity char) or (88,40) (messagelength, codelength) solomon-reed encoded 
    """

if __name__ == "__main__":
    main()