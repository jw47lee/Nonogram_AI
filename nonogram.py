

file_name_list = ["10x10_1.txt"]

class Puzzle:

    def __init__(self, row, col, row_list, col_list):
        self.row = row
        self.col = col
        self.row_list = row_list
        self.col_list = col_list

    def __str__(self):
        output = "This puzzle is {0} x {1} puzzle\n".format(self.row, self.col)
        output += "rows:\n"
        for i in self.row_list:
            output += ' '.join([str(elem) for elem in i])
            output += "\n"
        output += "cols:\n"
        for i in self.col_list:
            output += ' '.join([str(elem) for elem in i])
            output += "\n"
        return output

    
# read puzzles and return two lists, constraint for rows, and cols
def read_puzzle():
    class_list = []
    for i in file_name_list:
        row_list = []
        col_list = []
        f = open(i, "r")
        file_info = f.readlines()
        # remove newline char
        for j in range(len(file_info)):
            file_info[j] = file_info[j][:-1]

        row, col = int(file_info[0]), int(file_info[1])

        # row
        #print("row")
        for r in file_info[2:row+2]:
            x = r.split(" ")
            x = [int(j) for j in x]
            row_list.append(x)

        # col
        #print("col")
        for c in file_info[row+2:]:
            x =  c.split(" ")
            x = [int(j) for j in x]
            col_list.append(x)

        class_list.append(Puzzle(row, col, row_list, col_list))
    return class_list


def main():
    puzzles = read_puzzle()
    for i in puzzles:
        print(i)
        print("what is stored in row")
        print(i.row)
        print("what is stored in col")
        print(i.col)

        print("what is stored in row_list")
        print(i.row_list)
        print("what is stored in col_list")
        print(i.col_list)

if __name__ == '__main__':
    main()
