__author__ = "Kunal Shitut(ks6807)"
"""
CSCI-630-02: Assignment 1
Author=Kunal Shitut(ks6807), Ruta Kulkarni(rk6930)

This is a program that implements two solvers 
for a Ripple Effect puzzle. The first is a brute
force solve and the second is a intelligent solver

"""

import copy
import time

# Counter variable to keep track of recursive calls
counter = 0


class PuzzleCell:
    """
    The class represents a puzzle cell of the ripple effect puzzle
    """
    __slots__ = "row", "column", "value", "id", "region", "isFixedValue", "isValueAssigned", "minRemVals"

    def __init__(self, value, row, column):
        """
        The constructor for creating a cell object
        :param value: The value of the puzzle cell
        :param row: The row in which the cell is located
        :param column: The column in which the cell is located
        """
        self.value = value
        self.row = row
        self.column = column
        self.id = str(row) + "," + str(column)
        self.isFixedValue = False
        self.isValueAssigned = False
        self.minRemVals = []

    def __str__(self):
        """
        Returns a string representation of the Puzzle cell
        :return: String representing value of the cell
        """
        return str(self.value)

    def __repr__(self):
        """
        Returns a representation of the puzzle cell
        :return: The string representing the puzzle cell
        """
        return str(self.value)


def inAddedCells(addedCellsDict, rowCounter, columnCounter):
    """
    Check if a given cell is already present in the row and column
    :param addedCellsDict: The dictionary of all added cells
    :param rowCounter: The row of the cell to check
    :param columnCounter: The column of the cell to check
    :return: True if cell is present
    """
    if str(rowCounter) + "," + str(columnCounter) in addedCellsDict.keys():
        return True
    else:
        return False


def getAllRegionCells(rowCounter, columnCounter, lineArray, lineIndex, charIndex, nodeList):
    """
    Get all cells in a given cell's region
    :param rowCounter: The row of the cell
    :param columnCounter: The column of the cell
    :param lineArray: The puzzle input file representation
    :param lineIndex: The index of the line in the puzzle file
    :param charIndex: The index of a character in the line
    :param nodeList: The list of all nodes in the region
    :return: The updated list of all cells in the region
    """
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
    """
    Process the puzzle file array into the representation of the puzzle
    :param puzzleHeight: The height of the puzzle
    :param puzzleWidth: The width of the puzzle
    :param lineArray: The puzzle file
    :return: The puzzle matrix and the region list of the puzzle
    """
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
    """
    Determines if the given value can be placed at that cell or not.
    :param value: The value to check
    :param row: The row to check
    :param column: The column to check
    :param puzzleMatrix: The matrix of the puzzle
    :param regionList: The list of the puzzle region
    :return: True if value placement is legal
    """
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


def solveNextCell(row, column, puzzleMatrix, regionList):
    """
    Solve the puzzle using Bruteforce appraoch
    :param row: The row of the cell to start from
    :param column: The column of the cell to start from
    :param puzzleMatrix: The puzzle matrix
    :param regionList: The region list of the puzzle
    :return: True if the puzzle has been solved
    """
    global counter
    counter += 1

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
            value = solveNextCell(newRow, newColumn, puzzleMatrix, regionList)
        else:
            newColumn = column + 1
            value = solveNextCell(row, newColumn, puzzleMatrix, regionList)

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
                    value = solveNextCell(newRow, newColumn, puzzleMatrix, regionList)
                else:
                    newColumn = column + 1
                    value = solveNextCell(row, newColumn, puzzleMatrix, regionList)

                if value:
                    return True
    if not node.isFixedValue:
        puzzleMatrix[row][column].value = 0
    return False


def getPuzzleList(regionList):
    """
    Get a list of all cells
    :param regionList: The region list to copy from
    :return: The list of cells
    """
    list = []
    for region in regionList:
        for cell in region:
            list.append(cell)

    return list


def assignCellsMRV(regionList):
    """
    Assign the MRV to all cells in the regionList
    :param regionList: The region list
    :return: None
    """
    for region in regionList:
        for puzzleCell in region:
            cell = puzzleCell
            for i in range(1, len(regionList[cell.region]) + 1):
                cell.minRemVals.append(i)


def forwardCheck(cell, regionList, puzzleMatrix):
    """
    Forward check and eliminate invalid MRVs
    :param cell: The cell to forward check
    :param regionList: The list of regions
    :param puzzleMatrix: The puzzle matrix
    :return: list of all cells that were forward checked
    """
    listOfCheckedNodes = []

    value = cell.value
    for othCells in regionList[cell.region]:
        if value in othCells.minRemVals and othCells.id != cell.id:
            othCells.minRemVals.remove(value)
            listOfCheckedNodes.append(othCells)

    # clear columns
    for i in range(1, value + 1):
        index = cell.column - i
        if index >= 0:
            changedCell = puzzleMatrix[cell.row][index]
            if value in changedCell.minRemVals:
                changedCell.minRemVals.remove(value)
                listOfCheckedNodes.append(changedCell)

        index = cell.column + i
        if index < len(puzzleMatrix[0]):
            changedCell = puzzleMatrix[cell.row][index]
            if value in changedCell.minRemVals:
                changedCell.minRemVals.remove(value)
                listOfCheckedNodes.append(changedCell)

        index = cell.row - i
        if index >= 0:
            changedCell = puzzleMatrix[index][cell.column]
            if value in changedCell.minRemVals:
                changedCell.minRemVals.remove(value)
                listOfCheckedNodes.append(changedCell)

        index = cell.row + i
        if index < len(puzzleMatrix):
            changedCell = puzzleMatrix[index][cell.column]
            if value in changedCell.minRemVals:
                changedCell.minRemVals.remove(value)
                listOfCheckedNodes.append(changedCell)

    return listOfCheckedNodes


def fixedValueMRVAdjust(regionList, puzzleMatrix):
    """
    Adjust MRV for fixed value cells
    :param regionList: The region list
    :param puzzleMatrix: The puzzle matrix
    :return:
    """
    for region in regionList:
        for cell in region:
            if cell.isFixedValue:
                cell.isValueAssigned = True
                forwardCheck(cell, regionList, puzzleMatrix)


def solveOneValMRV(regionList, puzzleMatrix):
    """
    Solve all cells with only 1 possible value
    :param regionList: The region list
    :param puzzleMatrix: The puzzle matrix
    :return: None
    """
    global counter

    for region in regionList:

        if len(region) == 1:
            counter += 1
            region[0].value = 1
            region[0].isValueAssigned = True
            forwardCheck(region[0], regionList, puzzleMatrix)


def findMinMRV(puzzleMatrix):
    """
    Find the cell with least number of remaining values
    :param puzzleMatrix: The puzzle matrix
    :return: The minimum cell
    """
    minCell = PuzzleCell(0, -1, -1)
    for row in puzzleMatrix:
        for cell in row:
            if not (cell.isFixedValue or cell.isValueAssigned):
                if minCell.row == -1:
                    minCell = cell
                elif len(minCell.minRemVals) > len(cell.minRemVals):
                    minCell = cell
    return minCell


def intelligentSolver(regionList, puzzleMatrix):
    """
    The implementation of the intelligent solver using MRV and Forward checking
    :param regionList: The region list
    :param puzzleMatrix: The puzzleMatrix
    :return: True if puzzle solved
    """
    global counter
    counter += 1

    cell = findMinMRV(puzzleMatrix)
    # print(str(cell.id)+" "+str(puzzleMatrix[4][4].minRemVals))
    # print(str(cell.id))
    if cell.row == -1:
        return True
    else:
        if len(cell.minRemVals) == 0:
            return False
        else:
            cellMinRemList = copy.deepcopy(cell.minRemVals)
            for value in cellMinRemList:

                cell.value = value
                cell.isValueAssigned = True
                cell.minRemVals.remove(value)
                listOfCheckedCells = forwardCheck(cell, regionList, puzzleMatrix)
                truthVal = intelligentSolver(regionList, puzzleMatrix)
                if truthVal:
                    return True
                cell.isValueAssigned = False
                cell.value = 0
                cell.minRemVals.append(value)
                for listCell in listOfCheckedCells:
                    puzCell = puzzleMatrix[listCell.row][listCell.column]
                    if value not in puzCell.minRemVals:
                        puzCell.minRemVals.append(value)

                    for regCell in regionList[listCell.region]:
                        if regCell.id == listCell.id:
                            if value not in regCell.minRemVals:
                                regCell.minRemVals.append(value)
                                break

    return False


def main():
    """
    The main method
    :return: None
    """
    global counter
    nextIter = True
    while nextIter:
        # Set the global counter
        counter = 0

        fileName = input("Please enter the name of the puzzle file: ")
        file = open(fileName, "r")
        lineArray = []
        size = 0
        inputLine = file.readline().strip("\n").split(" ")

        puzzleHeight = int(inputLine[0])
        puzzleWidth = int(inputLine[1])
        for line in file:
            lineArray.append(line.strip("\n"))
            size += 1

        print("Processing Puzzle File....")
        puzzleMatrix, regionList = processPuzzleArray(puzzleHeight, puzzleWidth, lineArray)
        print("Puzzle file processed")
        print(" ")
        print(" Please enter the kind of solver you want to use")
        solverType = input("Enter 'B' for Brute Force or 'I' for intelligent ")
        if solverType == 'B':
            row = 0
            column = 0
            start = time.time()
            value = solveNextCell(row, column, puzzleMatrix, regionList)
            if value:
                end = time.time()
                for line in puzzleMatrix:
                    print(line)
                print("===========")
                print("Time taken: " + str((end - start) * 1000) + " milliseconds")
                print("===========")
                print("===========")
                print("Count of recursive calls: " + str(counter))
                print("===========")
            else:
                print("Puzzle cannot be solved")
        elif solverType == 'I':
            # Intelligent solver with MRV and Forward checking
            # First fill in MRV for all cells
            assignCellsMRV(regionList)
            #
            # # Handle regions with fixed value
            fixedValueMRVAdjust(regionList, puzzleMatrix)
            start = time.time()
            solveOneValMRV(regionList, puzzleMatrix)
            value = intelligentSolver(regionList, puzzleMatrix)
            if value:
                end = time.time()
                for line in puzzleMatrix:
                    print(line)
                print("===========")
                print("Time taken: " + str((end - start) * 1000) + "  milliseconds")
                print("===========")
                print("===========")
                print("Count of recursive calls: " + str(counter))
                print("===========")
            else:
                print("Puzzle cannot be solved")
        else:
            print("Wrong input")
        again = input("Would you like to try again ?(y/n) ")
        if not again == "y":
            nextIter = False


main()
