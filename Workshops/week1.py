import numpy as np

class webPage():
    def __init__(self, selfURL: int, linkURLs: list=[]):
        self.selfURL = selfURL
        self.linkURLs = linkURLs
        if len(self.linkURLs) != 0:
            self.rank = 1/len(self.linkURLs)
        else:
            self.rank = 0

def calculateRank():
    return

def calculateTransitionMatrix(links:list):
    #transitionMatrix (TM) is a modifier to the pang ranks based on how many links a page has.
    TM = []
    for i in range(len(links)):
        TM.append([0]*len(links))

    for page in links:
        for link in page.linkURLs:
            TM[page.selfURL][link.selfURL] = page.rank
    return TM 

def MatrixMultiplication(matrix1,matrix2):
    if not checkValidMatrix(matrix1) and not checkValidMatrix(matrix2):
        print("error multiplying matrices\n %f%f".format(matrix1,matrix2))
        exit
    
    return

def checkValidMatrix(matrix:list):
    length = len(matrix[0])
    for vector in matrix:
        if length != vector:
            return False
        length = len(vector)
    return True

def setup():
    page1 = webPage(1)
    page0 = webPage(0, [page1])
    page3 = webPage(3, [page0])
    page4 = webPage(4, [page3])
    page2 = webPage(2, [page1, page4])
    links = [page0,page1,page2,page3,page4]
    return links

def main():
    links = setup()
    TM = calculateTransitionMatrix(links)
    print(TM)
    return



if __name__ == "__main__":
    main()