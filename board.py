from nonogram import read_puzzle
import copy



def build_init_board(puzzle):
    row, col = puzzle.row, puzzle.col
    return [[0]*col]*row


def draw_board(board, puzzle):
    
    max_row_count = max([len(i) for i in puzzle.row_list])
    max_col_count = max([len(i) for i in puzzle.col_list])
    
    viz = ""
    row_num = 0
    col_constraint = copy.deepcopy(puzzle.col_list)
    # Print col_constraint
    for i in range(0, max_col_count):
        viz += " "*((max_row_count+ max_row_count-1)*2)
        for col in col_constraint:
            if len(col) == max_col_count - row_num:
                viz += str(col[0])
                col.pop(0)
            else:
                viz += " "
        viz += "\n\n"
        row_num += 1
    print(viz[:-2])
    
    # Print row_constraint with puzzle
    
    for i in range(0, puzzle.row):
        viz = ''
    
        if len(puzzle.row_list[i]) < max_row_count:
            viz += ' ' * ((max_row_count - len(puzzle.row_list[i]))*2)
        viz += ' '.join([str(elem) for elem in puzzle.row_list[i]])
        viz += ' '* ((max_row_count+ max_row_count-1)*2 - len(viz))
        
        viz += ''.join(str(elem) for elem in board[i])
            
        print(viz)
                

def main():
    puzzles = read_puzzle()

    for p in puzzles:
        b = build_init_board(p)
        draw_board(b, p)    

if __name__ == '__main__':
    main()

    

    
