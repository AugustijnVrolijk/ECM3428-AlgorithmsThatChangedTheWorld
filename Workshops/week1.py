import numpy as np

class webPage():
    def __init__(self, selfURL: str, linkURLs: list=[]):
        self.selfURL = selfURL
        self.linkURLs = linkURLs
        self.rank = 1/len(self.linkURLs)
    
def calculateRank():
    return


def main():
    links = []
    size = 5
    page2 = webPage("2")
    page1 = webPage("1", [page2])
    page4 = webPage("4", [page1])
    page5 = webPage("5", [page4])
    page3 = webPage("3", [page2, page5])
    return



if __name__ == "__main__":
    main()