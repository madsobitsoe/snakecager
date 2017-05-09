from fractions import Fraction as F

def frac_matrix_of_string(string_matrix):
    def string_to_frac(fraction_string):
        fraction = fraction_string.split("/")
        if len(fraction) == 2:
            return F(int(fraction[0]), int(fraction[1]))
        return F(fraction_string)
    fracmatrix = [[string_to_frac(ix) for ix in x] for x in string_matrix]
    return fracmatrix

def intmatrix_to_frac_matrix(intmatrix):
    return [[F(ix) for ix in x] for x in intmatrix]


def scale_row(matrix, row, multiplier):
    matrix[row-1] = map(lambda  x: x * multiplier, matrix[row-1])
    return matrix

def add_row(matrix, row1, row2, multiplier):
    for i in range(len(matrix[row1-1])):
        matrix[row2-1][i] = matrix[row2-1][i] + multiplier * matrix[row1-1][i]
    return matrix

def subtract_row(matrix, row1, row2, multiplier):
    for i in range(len(matrix[row1-1])):
        matrix[row2-1][i] = matrix[row2-1][i] - multiplier * matrix[row1-1][i]
    return matrix

def swap_rows(matrix, row1, row2):
    tmp = matrix[row1-1]
    matrix[row1-1] = matrix[row2-1]
    matrix[row2-1] = tmp
    return matrix

def print_matrix(matrix):
    matrix_string = ""
    for row in matrix:
        for col in row:
            matrix_string += " %d" % col
        matrix_string += "\n"
    print matrix_string

def to_latex_matrix(matrix):
    """ """
    matrix_string = "\\left[\n\\begin{array}{%s}\n" % (len(matrix[0]) * "r")
    for row in matrix:
        for col in row:
            matrix_string += " %s &" % col
        matrix_string = matrix_string[:-1]
        matrix_string += " \\\\\n"
    matrix_string = matrix_string[:-5]
    matrix_string += "\n\\end{array}\n\\right]\n"
    return matrix_string

def frac_matrix_to_latex(matrix):
    """Converts a nested list of fractions into a latex-formatted string"""
    matrix_string = "\\left[\n\\begin{array}{%s}\n" % (len(matrix[0]) * "r")
    for row in matrix:
        for col in row:
            matrix_string += " %s &" % frac_to_latex(col)
        matrix_string = matrix_string[:-1]
        matrix_string += " \\\\\n"
    matrix_string = matrix_string[:-5]
    matrix_string += "\n\\end{array}\n\\right]\n"
    return matrix_string

def create_op_string(string_multiplier, row1, row2, operation):
    if operation == "swap":
        return "\\mathbf{r}_%d \\leftrightarrow \\mathbf{r}_%d" % (row1, row2)
    elif operation == "scale":
        if string_multiplier == '1':
            string_multiplier = ""
        if string_multiplier == "-1":
            string_multiplier = "-"
        return "%s\\mathbf{r}_%d \\to \\mathbf{r}_%d" % (string_multiplier, row1, row1)
    return "%s\\mathbf{r}_%d %s \\mathbf{r}_%d \\to \\mathbf{r}_%d" % (string_multiplier,
                                                                       row1,
                                                                       operation,
                                                                       row2,
                                                                       row2)

def print_row_op(matrix, row1, row2, multiplier, operation):
    """Perform a row operation on supplied matrix and
    return it as a latex string"""
    string_multiplier = ""
    if multiplier != 1:
        string_multiplier = frac_to_latex(multiplier)
    latex_string = ("\\setstretch{1.5}\n"
                    "\\setlength{\\jot}{8pt}\n")
    latex_string += "  \\begin{array}{lcl}\n"
    # add first matrix
    latex_string += "%s\n&\n" % frac_matrix_to_latex(matrix)
    # Add row operation line
    latex_string += ("\\xymatrix@C=15ex{\n"
                     "    \\ar[r]^-{\\small\n"
                     "      \\begin{array}{r}\n")
    latex_string += create_op_string(string_multiplier, row1, row2, operation)
    latex_string += "\n      \\end{array}\n} & \n}"
    # add second matrix
    if operation == "+":
        add_row(matrix, row1, row2, multiplier)
    elif operation == "-":
        subtract_row(matrix, row1, row2, multiplier)
    elif operation == "swap":
        swap_rows(matrix, row1, row2)
    elif operation == "scale":
        scale_row(matrix, row1, multiplier)
    latex_string += "\n&\n%s" % frac_matrix_to_latex(matrix)
    latex_string += "\\end{array}"
    return (matrix, latex_string)

def frac_to_latex(frac):
    """Takes a fraction and returns it as a latex-formatted string"""
    split = str(frac).split("/")
    if len(split) == 2:
        return "\\frac{%s}{%s}" % (split[0], split[1])
    return split[0]
