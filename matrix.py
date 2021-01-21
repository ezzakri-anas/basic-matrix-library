class Interrupt(Exception):
    pass


class InvalidOperation(Exception):
    pass


class InvalidExpression(Exception):
    pass


class NonInvertableMatrix(Exception):
    pass


class Matrix:
    def __init__(self, num_rows, num_cols, content=None):
        self.row_num = int(num_rows)
        self.col_num = int(num_cols)
        self.size = self.row_num, self.col_num
        if content is None:
            matrix = [input().split() for _ in range(self.row_num)]
            for row in range(self.row_num):
                if len(matrix[row]) != self.col_num:
                    raise InvalidExpression
            self.content = matrix
            self.content = self.float()
        else:
            self.content = []
            for row in content:
                self.content.append(row[:])
            self.content = self.float()
        self.rows = self.content
        self.cols = [[self.content[row_in][col_in] for row_in in range(self.row_num)] for col_in in range(self.col_num)]

    def __repr__(self):
        self.print_float()
        return "{}".format("\n".join(str(row).strip("[]").replace(",", "") for row in self.content))

    def __add__(self, other):
        if self.size != other.size:
            raise InvalidOperation
        else:
            res_matrix_content = [[self.content[row][col] + other.content[row][col] for col in range(self.col_num)] for
                                  row in range(self.row_num)]
            return Matrix(self.row_num, self.col_num, res_matrix_content)

    def __mul__(self, other):
        """Return the 'dot product' of rows and columns"""

        if self.col_num != other.row_num:
            raise InvalidOperation
        else:
            res_matrix = list()
            for row_in in range(self.row_num):
                res_matrix.append([])
                for col_in in range(other.col_num):
                    row_cumul = 0
                    for j in range(self.col_num):
                        row_cumul += self.content[row_in][j] * other.content[j][col_in]
                    res_matrix[row_in].append(row_cumul)
            return Matrix(self.row_num, other.col_num, res_matrix)

    def print_float(self):
        res = []
        for row in range(self.row_num):
            res.append([])
            for col in range(self.col_num):
                item = self.content[row][col]
                if item.is_integer():
                    res[row].append(int(item))
                else:
                    res[row].append(float(str(item)[:str(item).find(".") + 4]))
        self.content = res

    def float(self):
        return [[float(item) for item in row] for row in self.content]

    def is_square(self):
        return self.row_num == self.col_num

    def scallar(self, constant):
        res_matrix = [[item * constant for item in row] for row in self.content]
        return Matrix(self.row_num, self.col_num, res_matrix)

    def transpose(self, axe):
        matrix_copy = self.create_copy()
        if axe == "main diagonal":
            return Matrix(matrix_copy.col_num, matrix_copy.row_num, matrix_copy.cols)
        elif axe == "side diagonal":
            matrix_copy.cols.reverse()
            for lst in matrix_copy.cols:
                lst.reverse()
            return Matrix(matrix_copy.col_num, matrix_copy.row_num, matrix_copy.cols)
        elif axe == "vertical line":
            for lst in matrix_copy.content:
                lst.reverse()
            return Matrix(matrix_copy.row_num, matrix_copy.col_num, matrix_copy.content)
        elif axe == "horizontal line":
            matrix_copy.content.reverse()
            return Matrix(matrix_copy.row_num, matrix_copy.col_num, matrix_copy.content)

    def det(self, index):
        if self.col_num == 2:
            return self.content[0][0] * self.content[1][1] - self.content[1][0] * self.content[0][1]
        else:
            if index == 0:
                rest_of_matrix = 0
            else:
                rest_of_matrix = self.det(index - 1)
            return self.content[0][index] * self.cofactor(0, index) + rest_of_matrix

    def create_copy(self, content=None):
        content = self.content if content is None else content
        return Matrix(self.row_num, self.col_num, content)

    def minor(self, *coord):
        row, col = coord
        matrix_copy = self.create_copy()
        matrix_copy.content.remove(matrix_copy.content[row])
        for lst in matrix_copy.content:
            lst.pop(col)
        matrix_copy.row_num -= 1
        matrix_copy.col_num -= 1
        return matrix_copy.det(matrix_copy.col_num - 1)

    def cofactor(self, *coord):
        row, col = coord
        return self.minor(row, col) * (-1)**(row + col)

    def is_inversable(self):
        deter = self.det(self.col_num - 1)
        if deter == 0:
            return False
        return True

    def inverse(self):
        if not self.is_inversable():
            raise NonInvertableMatrix
        deter = self.det(self.col_num - 1)
        n_matrix_content = [[self.cofactor(row, col) for col in range(self.col_num)]for row in range(self.row_num)]
        pre_n_matrix = Matrix(self.row_num, self.col_num, n_matrix_content)
        n_matrix = pre_n_matrix.transpose("main diagonal")
        return n_matrix.scallar(1/deter)


def input_choices():
    print("",
          "1. Add matrices",
          "2. Multiply matrix by a constant",
          "3. Multiply matrices",
          "4. Transpose matrix",
          "5. Calculate a determinant",
          "6. Inverse matrix",
          "0. Exit",
          sep="\n")
    return int(input("Your choice: > "))


def input_axe_choice():
    print("",
          "1. Main diagonal",
          "2. Side diagonal",
          "3. Vertical line",
          "4. Horizontal line",
          sep="\n")
    return int(input("Your choice: > "))


def add_matrices():
    first_matrix, second_matrix = get_operands(2)
    return first_matrix + second_matrix


def multiply_matrices():
    first_matrix, second_matrix = get_operands(2)
    return first_matrix * second_matrix


def mul_by_const():
    _matrix, constant = get_operands(1, 1)
    return _matrix.scallar(constant)


def transpose_func():
    axes = ["main diagonal", "side diagonal", "vertical line", "horizontal line"]
    axe = axes[input_axe_choice() - 1]
    _matrix = get_operands(1)[0]
    return _matrix.transpose(axe)


def determinant():
    _matrix = get_operands(1)[0]
    if not _matrix.is_square():
        raise InvalidOperation
    elif _matrix.col_num == 1:
        return _matrix
    return _matrix.det(_matrix.col_num - 1)


def inverse_func():
    _matrix = get_operands(1)[0]
    if not _matrix.is_square():
        raise InvalidOperation
    return _matrix.inverse()


def get_operands(operands_num=None, const_num=0):
    res = list()
    if operands_num is None or operands_num == 2:
        options = ["first ", "second "]
    else:
        options = [""]
    for order in options:
        row_num, column_num = input("Enter size of {}matrix: > ".format(order)).split()
        print("Enter {}matrix:".format(order))
        res.append(Matrix(row_num, column_num))
    for _ in range(const_num):
        res.append(float(input("Enter constant: > ")))
    return res


def process_choice(choice):
    if choice == 0:
        raise Interrupt
    choices = {
        1: add_matrices,
        2: mul_by_const,
        3: multiply_matrices,
        4: transpose_func,
        5: determinant,
        6: inverse_func
    }
    try:
        return choices[choice]()
    except InvalidExpression:
        print("Invalid expression")
    except InvalidOperation:
        print("The operation cannot be performed.")
    except NonInvertableMatrix:
        print("This matrix doesn't have an inverse.")


while True:
    action = input_choices()
    try:
        result = process_choice(action)
    except Interrupt:
        break
    if result is not None:
        print("The result is: ", result, sep="\n")
