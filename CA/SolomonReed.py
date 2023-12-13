"""
lagrangePolgen: generates a lagrange polynomials for a list of points, with 1 point specified as the unit point
for a set of n points, there are n lagrange polynomials, where each one has x intercept at all but one of n points,
and a value of 1 for the last point

i.e. for points: (1,5)(2,3)(3,8)(4,15), a lagrange polynomial would have points (1,1)(2,0)(3,0)(4,0)

inputs: toExclude - unit point
        toInclude - all n points

returns: lagrange polynomial for n points with unit point toExclude
"""
def lagrangePolGen(toExclude:int, toInclude:list) -> list:
    
    #find which x values need to be made 0
    roots = []
    for int in toInclude:
        if toExclude == int:
            continue
        roots.append(-int)

    #calculate coefficient needed to make unit point have y value 1
    yIntercept = 1
    for int in roots:
        temp = int + toExclude
        yIntercept = yIntercept*temp
    yIntercept = 1/yIntercept

    polynomial = [1]
    for root in roots:
        temp = polynomial.copy()
        polynomial.append(0)
        i = 1
        for order in temp:
            order = root*order
            polynomial[i] += order
            i += 1

    for i in range(len(polynomial)):
        polynomial[i] = polynomial[i]*yIntercept

    return polynomial

def calcPol(list:list) -> list:
    polynomial = [0] * len(list)
    roots = []
    for i in range(len(list)):
        roots.append(i)
    for index, int in enumerate(list):
        temp = lagrangePolGen(index, roots)
        for index in range(len(temp)):
            polynomial[index] += temp[index]*int
    return polynomial

def calcParityChars(polynomial:list, messageLen: int, codeLen: int) -> list:
    parityBits = []
    for j in range(codeLen):
        x = messageLen + j
        tempBit = 0
        for index, coefficient in enumerate(polynomial):
            tempBit += coefficient*(x**(len(polynomial)-index))
        parityBits.append(int(tempBit))

    return parityBits

def solomonEncoder(message: list, blockLen: int) -> list:

    codeLen = blockLen-len(message)

    polynomial = calcPol(message)
    parityChars = calcParityChars(polynomial, len(message), codeLen)
    
    encodedMessage = message
    for char in parityChars:
        encodedMessage.append(char)
    
    return encodedMessage

def solomonDecoder(encodedMessage: list, messageLen) -> list:
    message = []


    return message

def main():
    print(calcPol([1,5,2,3]))

    message = [1,5,2,3]
    encodedMessage = solomonEncoder(message, 7)
    print(encodedMessage)


if __name__ == "__main__":
    main()