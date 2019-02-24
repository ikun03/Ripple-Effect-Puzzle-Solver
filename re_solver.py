class PuzzleCell:
    __slots__ = "row", "column", "value", "id"

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.id = row + column


def inAddedCells(addedCellsDict, rowCounter, columnCounter):
    if rowCounter + columnCounter in addedCellsDict.keys():
        return True
    else:
        return False


def getAllCellsOfRegion(lineIndex, charIndex, lineArray, matrixOfCells):
    pass


def processPuzzleArray(puzzleHeight, puzzleWidth, lineArray):
    rowCounter = 0
    columnCounter = 0
    listOfRegions = []
    addedCellsDict = {}
    regionCounter = 0

    matrixOfCells = []
    for length in range(puzzleHeight):
        matrixOfCells.append([])

    for lineIndex in range(1, len(lineArray) - 1):
        columnCounter = 0
        for charIndex in lineArray[lineIndex]:
            charToCheck = lineArray[lineIndex][charIndex]
            if charToCheck == "." or charToCheck > 0:
                if not inAddedCells(addedCellsDict, rowCounter, columnCounter):
                    puzzleCell = PuzzleCell(rowCounter, columnCounter, int(charToCheck))
                    addedCellsDict[rowCounter + columnCounter] = puzzleCell
                    matrixOfCells.append(puzzleCell)
                    regionList=getAllCellsOfRegion(lineIndex,charIndex,lineArray,matrixOfCells)


def main():
    fileName = "puzzle1.txt"
    file = open(fileName, "r")
    lineArray = []
    size = 0
    inputLine = file.readline().strip("\n").split(" ")

    puzzleHeight = int(inputLine[0])
    puzzleWidth = int(inputLine[1])
    for line in file:
        lineArray.append(line.strip("\n"))
        size += 1

    processPuzzleArray(puzzleHeight, puzzleWidth, lineArray)


main()
