import unittest
import rowop
import re

class add_row_tests(unittest.TestCase):
    def test_one(self):
        a = [[1]]
        expected = [[2]]
        actual = rowop.add_row(a,1,1,1)
        self.failUnless(actual == expected)

    def test_two(self):
        a = [[1],[1]]
        expected = [[2],[1]]
        actual = rowop.add_row(a,2,1,1)
        self.failUnless(actual == expected)

    def test_three(self):
        a = [[rowop.F(-1) for xi in range(3)] for x in range(3)]
        expected = [[-2,-2,-2],[-1,-1,-1],[-1,-1,-1]]
        actual = rowop.add_row(a,2,1,1)
        self.failUnless(actual == expected)

    def test_four(self):
        a = [[rowop.F(1,2) for xi in range(10)] for x in range(2)]
        expected = [[1 for xi in range(10)],[rowop.F(1,2) for x in range(10)]]
        actual = rowop.add_row(a,2,1,1)
        self.failUnless(actual == expected)

class subtract_row_tests(unittest.TestCase):
    def test_one(self):
        a = [[1]]
        expected = [[0]]
        actual = rowop.subtract_row(a,1,1,1)
        self.failUnless(actual == expected)

    def test_two(self):
        a = [[1],[1]]
        expected = [[0],[1]]
        actual = rowop.subtract_row(a,2,1,1)
        self.failUnless(actual == expected)

    def test_three(self):
        a = [[1, -1, rowop.F(-1,2)],[1,1,1]]
        expected = [[0,-2,rowop.F(-3,2)],[1,1,1]]
        actual = rowop.subtract_row(a,2,1,1)
        self.failUnless(actual == expected)
    
class swap_row_tests(unittest.TestCase):
    def test_one(self):
        a = [[1],[0]]
        expected = [[0],[1]]
        actual = rowop.swap_rows(a,1,2)
        self.failUnless(actual == expected)

    def test_two(self):
        a = [[1],[9],[0]]
        expected = [[0],[9],[1]]
        actual = rowop.swap_rows(a,1,3)
        self.failUnless(actual == expected)

    def test_three(self):
        """ Same as test_two, but with flipped rows in input"""
        a = [[1],[9],[0]]
        expected = [[0],[9],[1]]
        actual = rowop.swap_rows(a,3,1)
        self.failUnless(actual == expected)


class scale_row_tests(unittest.TestCase):
    def test_one(self):
        a = [[1]]
        expected = [[2]]
        actual = rowop.scale_row(a, 1, 2)
        self.failUnless(actual == expected)

    def test_two(self):
        a = [[1]]
        expected = [[rowop.F(1,7)]]
        actual = rowop.scale_row(a, 1, rowop.F(1,7))
        self.failUnless(actual == expected)


        
class frac_to_string_tests(unittest.TestCase):
    def test_one(self):
        expected = "\\frac{2}{3}"
        actual = rowop.frac_to_latex(rowop.F(2,3))
        self.failUnless(actual == expected)
    def test_two(self):
        expected = "1"
        actual = rowop.frac_to_latex(rowop.F(2,2))
        self.failUnless(actual == expected)
    def test_three(self):
        expected = "\\frac{-2}{3}"
        actual = rowop.frac_to_latex(rowop.F(-2,3))
        self.failUnless(actual == expected)
    def test_four(self):
        expected = "-17"
        actual = rowop.frac_to_latex(rowop.F(-17,1))
        self.failUnless(actual == expected)

class op_string_tests(unittest.TestCase):
    def test_one(self):
        string_multiplier = ""
        row1 = 1
        row2 = 2
        operation = "+"
        expected = "\\mathbf{r}_1 + \\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

    def test_two(self):
        string_multiplier = ""
        row1 = 2
        row2 = 1
        operation = "+"
        expected = "\\mathbf{r}_2 + \\mathbf{r}_1 \\to \\mathbf{r}_1"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

    def test_three(self):
        string_multiplier = "-1"
        row1 = 1
        row2 = 2
        operation = "+"
        expected = "-\\mathbf{r}_1 + \\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

    def test_three_2(self):
        string_multiplier = "1"
        row1 = 1
        row2 = 2
        operation = "+"
        expected = "\\mathbf{r}_1 + \\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

        
    def test_four(self):
        string_multiplier = rowop.frac_to_latex(rowop.F(-1,17))
        row1 = 1
        row2 = 2
        operation = "+"
        expected = "\\frac{-1}{17}\\mathbf{r}_1 + \\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)


    def test_five(self):
        string_multiplier = rowop.frac_to_latex(rowop.F(2))
        row1 = 1
        # row2 is irrelevant here
        row2 = -1
        operation = "scale"
        expected = "2\\mathbf{r}_1 \\to \\mathbf{r}_1"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

        
    def test_six(self):
        string_multiplier = rowop.frac_to_latex(rowop.F(-1))
        row1 = 1
        # row2 is irrelevant here
        row2 = -1
        operation = "scale"
        expected = "-\\mathbf{r}_1 \\to \\mathbf{r}_1"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

    def test_seven(self):
        string_multiplier = rowop.frac_to_latex(rowop.F(1))
        row1 = 2
        # row2 is irrelevant here
        row2 = -1
        operation = "scale"
        expected = "\\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)


    def test_eight(self):
        string_multiplier = rowop.frac_to_latex(rowop.F(-1))
        row1 = 1
        # row2 is irrelevant here
        row2 = -1
        operation = "scale"
        expected = "-\\mathbf{r}_1 \\to \\mathbf{r}_1"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

    def test_nine(self):
        string_multiplier = "-1"
        row1 = 1
        row2 = 2
        operation = "-"
        expected = "-\\mathbf{r}_1 - \\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)

    def test_nine_2(self):
        string_multiplier = "1"
        row1 = 1
        row2 = 2
        operation = "-"
        expected = "\\mathbf{r}_1 - \\mathbf{r}_2 \\to \\mathbf{r}_2"
        actual = rowop.create_op_string(string_multiplier, row1, row2, operation)
        self.failUnless(actual == expected)


        
        
def main():
    unittest.main()

if __name__ == "__main__":
    main()
