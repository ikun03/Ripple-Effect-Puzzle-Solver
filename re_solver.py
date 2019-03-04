import copy


class PuzzleCell:
    __slots__ = "row", "column", "value", "id", "region", "isFixedValue", "isValueAssigned", "minRemVals"

    def __init__(self, value, row, column):
        self.value = value
        self.row = row
        self.column = column
        self.id = str(row) + "," + str(column)
        self.isFixedValue = False
        self.isValueAssigned = False
        self.minRemVals = []

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


def inAddedCells(addedCellsDict, rowCounter, columnCounter):
    if str(rowCounter) + "," + str(columnCounter) in addedCellsDict.keys():
        return True
    else:
        return False


def getAllRegionCells(rowCounter, columnCounter, lineArray, lineIndex, charIndex, nodeList):
    # For checking the bottom cell
    lineIndexCounter = lineIndex + 1
    while len(lineArray[lineIndexCounter]) < (charIndex + 1) or lineArray[lineIndexCounter][charIndex] == " ":
        lineIndexCounter += 1
    if lineArray[lineIndexCounter][charIndex] != "-":
        if lineArray[lineIndexCounter][charIndex] == "." or int(lineArray[lineIndexCounter][charIndex]) > 0:
            isPresent = False
            for node in nodeList:
                if node.id == (str(rowCounter + 1) + "," + str(columnCounter)):
                    isPresent = True
                    break
            if not isPresent:
                nodeList.append(PuzzleCell(lineArray[lineIndexCounter][charIndex], rowCounter + 1, columnCounter))
                nodeList = getAllRegionCells(rowCounter + 1, columnCounter, lineArray, lineIndexCounter, charIndex,
                                             nodeList)

    # For checking the top cell
    lineIndexCounter = lineIndex - 1
    while len(lineArray[lineIndexCounter]) < (charIndex + 1) or lineArray[lineIndexCounter][charIndex] == " ":
        lineIndexCounter -= 1
    if lineArray[lineIndexCounter][charIndex] != "-":
        if lineArray[lineIndexCounter][charIndex] == "." or int(lineArray[lineIndexCounter][charIndex]) > 0:
            isPresent = False
            for node in nodeList:
                if node.id == (str(rowCounter - 1) + "," + str(columnCounter)):
                    isPresent = True
                    break
            if not isPresent:
                nodeList.append(PuzzleCell(lineArray[lineIndexCounter][charIndex], rowCounter - 1, columnCounter))
                nodeList = getAllRegionCells(rowCounter - 1, columnCounter, lineArray, lineIndexCounter, charIndex,
                                             nodeList)

    # For checking right cell
    charIndexCounter = charIndex + 1
    while lineArray[lineIndex][charIndexCounter] == " ":
        charIndexCounter += 1
    if lineArray[lineIndex][charIndexCounter] != "|":
        if lineArray[lineIndex][charIndexCounter] == "." or int(lineArray[lineIndex][charIndexCounter]) > 0:
            isPresent = False
            for node in nodeList:
                if node.id == (str(rowCounter) + "," + str(columnCounter + 1)):
                    isPresent = True
                    break
            if not isPresent:
                nodeList.append(PuzzleCell(lineArray[lineIndex][charIndexCounter], rowCounter, columnCounter + 1))
                nodeList = getAllRegionCells(rowCounter, columnCounter + 1, lineArray, lineIndex, charIndexCounter,
                                             nodeList)

    # For checking left cell
    charIndexCounter = charIndex - 1
    while lineArray[lineIndex][charIndexCounter] == " ":
        charIndexCounter -= 1
    if lineArray[lineIndex][charIndexCounter] != "|":
        if lineArray[lineIndex][charIndexCounter] == "." or int(lineArray[lineIndex][charIndexCounter]) > 0:
            isPresent = False
            for node in nodeList:
                if node.id == (str(rowCounter) + "," + str(columnCounter - 1)):
                    isPresent = True
                    break
            if not isPresent:
                nodeList.append(PuzzleCell(lineArray[lineIndex][charIndexCounter], rowCounter, columnCounter - 1))
                nodeList = getAllRegionCells(rowCounter, columnCounter - 1, lineArray, lineIndex, charIndexCounter,
                                             nodeList)

    return nodeList


def processPuzzleArray(puzzleHeight, puzzleWidth, lineArray):
    rowCounter = 0
    listOfRegions = []
    addedCellsDict = {}
    regionCounter = 0

    matrixOfCells = []
    for length in range(puzzleHeight):
        list = []
        for width in range(puzzleWidth):
            list.append([])
        matrixOfCells.append(list)

    for lineIndex in range(1, len(lineArray) - 1):
        columnCounter = 0
        for charIndex in range(1, len(lineArray[lineIndex]) - 1):
            charToCheck = lineArray[lineIndex][charIndex]
            if charToCheck not in ['|', '-', ' '] and (charToCheck == "." or int(charToCheck) > 0):
                nodeList = []
                if not inAddedCells(addedCellsDict, rowCounter, columnCounter):
                    puzzleCell = PuzzleCell(charToCheck, rowCounter, columnCounter)
                    nodeList = [puzzleCell]
                    nodeList = getAllRegionCells(rowCounter, columnCounter, lineArray, lineIndex, charIndex, nodeList)
                    for node in nodeList:
                        node.region = regionCounter
                        if node.value == ".":
                            node.value = 0
                        else:
                            node.value = int(node.value)
                            node.isFixedValue = True
                        addedCellsDict[str(node.row) + "," + str(node.column)] = node
                        matrixOfCells[node.row][node.column] = node
                if len(nodeList) != 0:
                    listOfRegions.append(nodeList)
                    regionCounter += 1
                columnCounter += 1
        if "." in lineArray[lineIndex]:
            rowCounter += 1
    return matrixOfCells, listOfRegions


def isPlacementLegal(value, row, column, puzzleMatrix, regionList):
    cell = puzzleMatrix[row][column]
    if value > len(regionList[cell.region]):
        return False

    for node in regionList[cell.region]:
        if node.value == value:
            return False

    for index in range(1, value + 1):
        i = row + index
        if (not (i > (len(puzzleMatrix) - 1))) and (puzzleMatrix[i][column].value == value):
            return False

        i = row - index
        if i > -1 and puzzleMatrix[i][column].value == value:
            return False

        i = column + index
        if (not (i > (len(puzzleMatrix[row]) - 1))) and (puzzleMatrix[row][i].value == value):
            return False

        i = column - index
        if i > -1 and puzzleMatrix[row][i].value == value:
            return False

    return True


def solveNextCell(row, column, puzzleMatrix, regionList, maxValue):
    node = puzzleMatrix[row][column]
    if node.isFixedValue:
        value = False
        if row == (len(puzzleMatrix) - 1) and column == (len(puzzleMatrix[0]) - 1):
            if isPlacementLegal(node.value, row, column, puzzleMatrix, regionList):
                return True
            else:
                return False
        if column == (len(puzzleMatrix[0]) - 1):
            newRow = row + 1
            newColumn = 0
            value = solveNextCell(newRow, newColumn, puzzleMatrix, regionList, maxValue)
        else:
            newColumn = column + 1
            value = solveNextCell(row, newColumn, puzzleMatrix, regionList, maxValue)

        if value:
            return True
    elif not node.isFixedValue:
        for num in range(1, len(regionList[node.region]) + 1):
            if isPlacementLegal(num, row, column, puzzleMatrix, regionList):
                puzzleMatrix[row][column].value = num
                if row == (len(puzzleMatrix) - 1) and column == (len(puzzleMatrix[0]) - 1):
                    return True
                if column == (len(puzzleMatrix[0]) - 1):
                    newRow = row + 1
                    newColumn = 0
                    value = solveNextCell(newRow, newColumn, puzzleMatrix, regionList, maxValue)
                else:
                    newColumn = column + 1
                    value = solveNextCell(row, newColumn, puzzleMatrix, regionList, maxValue)

                if value:
                    return True
    if not node.isFixedValue:
        puzzleMatrix[row][column].value = 0
    return False


def solveNextCell2(index, puzzleList, puzzleMatrix, regionList):
    node = puzzleList[index]
    node = puzzleMatrix[node.row][node.column]
    print(index);
    if node.isFixedValue:
        value = False
        if index == len(puzzleList) - 1:
            if isPlacementLegal(node.value, node.row, node.column, puzzleMatrix, regionList):
                return True
            else:
                return False
        else:
            value = solveNextCell2(index + 1, puzzleList, puzzleMatrix, regionList)

        if value:
            return True
    elif not node.isFixedValue:
        for num in range(1, len(regionList[node.region]) + 1):
            if isPlacementLegal(num, node.row, node.column, puzzleMatrix, regionList):
                value = False
                puzzleMatrix[node.row][node.column].value = num
                if index == len(puzzleList) - 1:
                    value = True
                else:
                    value = solveNextCell2(index + 1, puzzleList, puzzleMatrix, regionList)

                if value:
                    return True

    if not node.isFixedValue:
        puzzleMatrix[node.row][node.column].value = 0
    return False


def sortRegionList(regionList, puzzleMatrix):
    for i in range(0, len(regionList) - 1):
        minimumIndex = i
        for j in range(i + 1, len(regionList)):
            if len(regionList[j]) < len(regionList[minimumIndex]):
                minimumIndex = j
        temp = regionList[minimumIndex]
        regionList[minimumIndex] = regionList[i]
        regionList[i] = temp
    for i in range(0, len(regionList)):
        for node in regionList[i]:
            node.region = i
            puzzleMatrix[node.row][node.column].region = i


def getPuzzleList(regionList):
    list = []
    for region in regionList:
        for cell in region:
            list.append(cell)

    return list


def assignCellsMRV(regionList, puzzleMatrix):
    for region in regionList:
        for puzzleCell in region:
            cell = puzzleCell
            for i in range(1, len(regionList[cell.region]) + 1):
                cell.minRemVals.append(i)
                # puzzleMatrix[cell.row][cell.column].minRemVals.append(i)


def forwardCheck(cell, regionList, puzzleMatrix):
    value = cell.value
    for othCells in regionList[cell.region]:
        if value in othCells.minRemVals and othCells.id != cell.id:
            othCells.minRemVals.remove(value)

    # clear columns
    for i in range(1, value + 1):
        index = cell.column - i
        if index >= 0:
            if value in puzzleMatrix[cell.row][index].minRemVals:
                puzzleMatrix[cell.row][index].minRemVals.remove(value)

        index = cell.column + i
        if index < len(puzzleMatrix[0]):
            if value in puzzleMatrix[cell.row][index].minRemVals:
                puzzleMatrix[cell.row][index].minRemVals.remove(value)

        index = cell.row - i
        if index >= 0:
            if value in puzzleMatrix[index][cell.column].minRemVals:
                puzzleMatrix[index][cell.column].minRemVals.remove(value)

        index = cell.row + i
        if index < len(puzzleMatrix):
            if value in puzzleMatrix[index][cell.column].minRemVals:
                puzzleMatrix[index][cell.column].minRemVals.remove(value)


def fixedValueMRVAdjust(regionList, puzzleMatrix):
    for region in regionList:
        for cell in region:
            if cell.isFixedValue:
                cell.isValueAssigned = True
                forwardCheck(cell, regionList, puzzleMatrix)


def solveOneValMRV(regionList, puzzleMatrix):
    for region in regionList:
        if len(region) == 1:
            region[0].value = 1
            region[0].isValueAssigned = True
            forwardCheck(region[0], regionList, puzzleMatrix)


def findMinMRV(puzzleMatrix):
    minCell = PuzzleCell(0, -1, -1)
    for row in puzzleMatrix:
        for cell in row:
            if (not cell.isFixedValue) and (not cell.isValueAssigned):
                if minCell.row == -1:
                    minCell = cell
                elif len(minCell.minRemVals) > len(cell.minRemVals):
                    minCell = cell
    return minCell


def intelligentSolver(regionList, puzzleMatrix):
    cell = findMinMRV(puzzleMatrix)
    print(str(cell.id))
    if cell.row == -1:
        for line in puzzleMatrix:
            print(line)
        return True
    else:
        if len(cell.minRemVals) == 0:
            return False
        else:
            for cellValue in cell.minRemVals:

                newCell = copy.deepcopy(cell)
                newCell.value = cellValue
                newCell.isValueAssigned = True
                newRegionList = copy.deepcopy(regionList)
                newPuzzleMatrix = copy.deepcopy(puzzleMatrix)
                cellRegion = newRegionList[newCell.region]

                for val in range(0, len(cellRegion)):
                    if cellRegion[val].row == cell.row and cellRegion[val].column == cell.column:
                        newRegionList[newCell.region][val] = newPuzzleMatrix[newCell.row][newCell.column] = newCell
                        break
                forwardCheck(newCell, newRegionList, newPuzzleMatrix)

                result = intelligentSolver(newRegionList, newPuzzleMatrix)
                if result:
                    return True

            return False


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

    puzzleMatrix, regionList = processPuzzleArray(puzzleHeight, puzzleWidth, lineArray)
    # print(puzzleMatrix)
    # print(regionList)

    # We have the puzzle, now check if a particular number placement is legal
    value = 1
    row = 0
    column = 0
    maxValue = 324

    # isPlacementLegal(value, row, column, puzzleMatrix, regionList)
    # solveNextCell(row, column, puzzleMatrix, regionList, maxValue)
    # for line in puzzleMatrix:
    #     print(line)

    # Intelligent solver with MRV and Forward checking
    # First fill in MRV for all cells
    assignCellsMRV(regionList, puzzleMatrix)

    # Handle regions with fixed value
    fixedValueMRVAdjust(regionList, puzzleMatrix)
    solveOneValMRV(regionList, puzzleMatrix)
    for line in puzzleMatrix:
        print(line)
    intelligentSolver(regionList, puzzleMatrix)
    # print("Done")


main()
