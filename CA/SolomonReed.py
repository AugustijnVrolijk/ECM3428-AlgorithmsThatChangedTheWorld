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
    
    """
    find which x values need to be made 0
    i.e., for points mentioned above -> y = c(x-2)(x-3)(x-4)
    therefore converting x value to negative, to make x intercept for that value
    """
    roots = []
    for int in toInclude:
        if toExclude == int:
            continue
        roots.append(-int)

    """
    calculate coefficient needed to make unit point have y value 1
    i.e. for above points: y = c(x-2)(x-3)(x-4)
                           1 = c(1-2)(1-3)(1-4)
                           c = 1/(1-2)(1-3)(1-4)
    """
    coefficient = 1 
    for int in roots:
        temp = int + toExclude #find (x-a) (toEclude is negative)
        coefficient = coefficient*temp #find (x-a)(x-b)(x-c)
    coefficient = 1/coefficient 

    """
    finding y = ax^n + ... + bx + c
    for list roots, which representt each x intercept -> (-1, -2, -3) -> (x-1)(x-2)(x-3)
    recursively multiply standard polynomial 1, by each group, 1(x-1) -> (x-1)(x-2) -> (x^2-3x+2)(x-3)
        
    position of polynomial determines order of x
    """
    polynomial = [1]
    for root in roots:
        temp = polynomial.copy() #copy polynomial before increasing order, allows to multiply a polynomial by both x, and -1 for (x-1) seperately
        polynomial.append(0) #multiplying by x, increase order of every value, final value has no x value and is therefore 0
        i = 1
        for order in temp:
            order = root*order #multiplying by x intercept value, i.e. -1
            polynomial[i] += order #combining both seperately added polynomials
            i += 1

    """
    multiplying each polynomial coefficient to ensure unit point has value 1
    """
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

inputs: list of n numbers to find lagrange polynomial to (x values are assumed to be 0, ..., n-1)

returns: lagrange interpolating polynomial
"""

def calcPol(list:list) -> list:

    polynomial = [0] * len(list)

    #x values needed to calculate lagrange polynomials
    roots = []
    for i in range(len(list)):
        roots.append(i)

    for index, int in enumerate(list):
        temp = lagrangePolGen(index, roots) #calculate lagrange polynomial for specifc unit point
        for index in range(len(temp)):
            polynomial[index] += temp[index]*int #lagrange interpolating polynomial = lagrange polynomial for each point * y value 

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
        for index, coefficient in enumerate(polynomial):
            tempBit += coefficient*(x**(len(polynomial)-index)) #calculate y value for specified x value based on polynomial

        parityBits.append(int(tempBit)) #convert to int to remove floating point inaccuracies 

    return parityBits


"""
solomonEncoder: generates a unique polynomial based on a message, calculates parity char based on this polynomial to add to the encoded message

inputs: message - message of length < blocklen to encode
        blockLen - total encoded message length, determines number of parity bits to add

returns: encoded message
"""
def solomonEncoder(message: list, blockLen: int) -> list:

    codeLen = blockLen-len(message) #length of added parity char, more means a safer more protected message

    polynomial = calcPol(message)
    parityChars = calcParityChars(polynomial, len(message), codeLen)
    
    encodedMessage = message
    for char in parityChars:
        encodedMessage.append(char)
    
    return encodedMessage

"""
solomonDecoder: returns original message from an encoded message, reverts errors, 
                protects up to codeLen (len(encodedMessage - messageLen) errors

works by calculating all possible lagrange interpolating polynomials for message len, from the encoded message
as a lagrange interpolating polynomial is unique, all combinations without an error create the same polynomial,
ones with error create a different one

ascertains original message from the most popular polynomial to revert errors.

inputs: encodedMessage: Reed-solomon encoded message
        messageLen: length of the actual message

returns: Original message
"""
def solomonDecoder(encodedMessage: list, messageLen) -> list:
    
    possiblePol = {}
    for i in range(len(encodedMessage)-messageLen):
        
    message = []


    return message

def main():
    message = [1,5,2,3]
    encodedMessage = solomonEncoder(message, 7)
    print(encodedMessage)
    corruptedEncodedMessage = [3,5,2,4,76,305,840]



if __name__ == "__main__":
    main()