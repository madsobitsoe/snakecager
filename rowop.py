#!/usr/bin/env python

# Requires this in preamble of latex doc
#\usepackage[all]{xy}
#\usepackage{setspace}
# Only works with integers

matrix = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

def addRow(matrix, row1, row2, multiplier):
    for i in range(len(matrix[row1])-1):
        matrix[row2-1][i] = matrix[row2-1][i] + multiplier * matrix[row1-1][i]
    return matrix

def subtractRow(matrix, row1, row2, multiplier):
    for i in range(len(matrix[row1])-1):
        matrix[row2-1][i] = matrix[row2-1][i] - multiplier * matrix[row1-1][i]
    return matrix

def swapRows(matrix, row1, row2):
    tmp = matrix[row1-1]
    matrix[row1-1] = matrix[row2-1]
    matrix[row2-1] = tmp
    return matrix

def printMatrix(matrix):
    s = ""
    for row in matrix:
        for col in row:
            s +=  " %d" % col
        s += "\n"
    print s

def toLatexMatrix(matrix):
    m = len(matrix)
    n = len(matrix[0])
    
    s = "\\left[\n\\begin{array}{%s}\n" % (n * "r")
    for row in matrix:
        for col in row:
            s += " %d &" % col
        s = s[:-1]    
        s += " \\\\\n"
    s = s[:-5]
    s += "\n\\end{array}\n\\right]\n"
    return s

def createOpString(stringMultiplier, row1, row2, op):
    s = ""
    if (op == "swap"):
        s = "\\mathbf{r}_%d \\leftrightarrow \\mathbf{r}_%d" % (row1, row2)
    else:
        s += "%s\\mathbf{r}_%d %s \\mathbf{r}_%d \\to \\mathbf{r}_%d" % (stringMultiplier, row1, op, row2, row2)
    return s


def printRowOp(matrix, row1, row2, multiplier, op):
    stringMultiplier = ""
    if (multiplier > 1 or multiplier < 0):
        stringMultiplier = "%d" % multiplier
    s = ("\\setstretch{1.5}\n"
         "\\setlength{\\jot}{8pt}\n")
    s += "  \\begin{array}{lcl}"
    # add first matrix"
    s += "%s\n&\n" % toLatexMatrix(matrix)
    # Add rowop line
    s +=   ("\\xymatrix@C=15ex{\n"
            "    \\ar[r]^-{\\small\n"
            "      \\begin{array}{r}\n")
#    s += "        %s\\mathbf{r}_%d %s \\mathbf{r}_%d \\to \\mathbf{r}_%d" % (stringMultiplier, row1, op, row2, row2)
    s += createOpString(stringMultiplier, row1, row2, op)
    s += "\n      \end{array}\n} & \n}"
    # add second matrix
    if (op == "+"):
        addRow(matrix, row1, row2, multiplier)
    elif (op == "-"):
        subtractRow(matrix, row1, row2, multiplier)
    elif (op == "swap"):
        swapRows(matrix, row1, row2)
    s += "\n&\n%s" % toLatexMatrix(matrix)
    s += "\\end{array}"
    print s
    
# Do some matrix operations
if __name__ == "__main__":
    printRowOp(matrix, 1, 3, 0, "swap")
    printRowOp(matrix, 1, 2, -2, "-")
    printRowOp(matrix, 1, 3, -2, "+")
    
