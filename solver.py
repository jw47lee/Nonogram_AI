from nonogram import read_puzzle
from state import draw_state, build_init_state
from datetime import datetime
import copy
import numpy as np



class StateInfo:
    def __init__(self, state, track_row_constraints):
        self.state = state # string
        # track_row_constraints: list of pairs (in list) [j, k] where for each row i, jth row constraint
        # is the lastest satisfied constraint in that row and k is the last index(position) of
        # that last satisfied constraint
        # the values should initially be [-1, -2]
        self.track_row_constraints = track_row_constraints
    
        

def isValidColConstraint(puzzle, stateinfo):
  
    falseCount = 0
    state = stateinfo.state
#     print(draw_state(state,puzzle))


    for j in range(puzzle.col):
        constraint = puzzle.col_list[j]

        col = ""
          
        # Find consecutive 0's 1's
        #if 01011001110 => [1,1,1,2,2,3,1]
        #                  [0,1,2,3,4,5,6]
        # ones = [1,3,5] len(ones) = 3
        
        #if 0000 => [4]
        #if 1111 => [4]
        first = state[j]
        prev = first
        repeated_len = [] 
        count = 1
        for i in range(1,puzzle.row):
            cell = state[i*puzzle.col + j]
            if cell == prev: count +=1
            else:
                repeated_len.append(count)
                count = 1
                prev = cell
        repeated_len.append(count)

        ones = []
        if first == "1":
            ones = list(np.arange(0,len(repeated_len),2))
        else:
            ones = list(np.arange(1,len(repeated_len),2))
          
        
        #case1: number of coloured block group > number of constraints in that col => INVALID
        if len(ones) > len(constraint): 
#             print("Case1"+ " at "+ str(j) + "th row invalid")
            return False

        #  number of coloured block group <= number of constraints
        for i in range(len(ones)):
            diff = constraint[i] - repeated_len[ones[i]]
            #case2: constraint < len(coloured blocks)  => INVALID
            if diff < 0: 
#                 print("Case2 - diff:" + str(diff)+ " at "+ str(j) + "th row invalid")
                return False
                  
            #case3: less number of blocks are coloured than constraint 
            if diff > 0:

                # Find the row index (n) where we need to investigate
                n = 0
                for k in range(ones[i]):
                    n += repeated_len[k] 
                    
                #if stateinfo.track_row_constraint.find([-1,2]) < n
                if [-1,-2] in stateinfo.track_row_constraints:
                    if stateinfo.track_row_constraints.index([-1,-2])< n: break
                                  
                #case3.0: extra required spaces to be coloured is less than the remaining spaces => INVALID
                if (n + diff - 1) >= puzzle.row: 
#                     print("Case3.0 - diff:" + str(n + diff - 1)+ " at "+ str(j) + "th row invalid")
                    return False
                  
                # the n-th (n+0, ... n+delta th) row need to be investigated to judge if the state is valid 
                # if not coloured cells that should be colured by constraints is known to be empty cell in this state, we will return False
                for delta in range(diff):
                    row = n+delta
                    #case3.1: a cell in previous column & same row has coloured (for sure this cell is empty) => INVALID
                    if j > 1 and state[row*puzzle.col+j-1] == '1': 
#                         print("Case3.1:"+ " at "+ str(j) + "th row invalid")
                        return False

                    #case3.2: at least one cell in any following columns has coloured (for sure this cell is empty) => INVALID
                    if j < puzzle.col-1:
                        following_cells = state[row*puzzle.col+j+1: row*(puzzle.col+1)]
                        if following_cells.find('1') != -1 : 
#                             print("Case3.2:"+ " at "+ str(j) + "th row invalid")
                            return False

                    #for m in range(j+1, puzzle.col):
                    #if state[n*puzzle.col+m] == '1': return False

                
        #case4: Valid cases (coloured blocks satisfy all column constraint OR we check invalid/incomplete row states above)
        if len(ones) > 0: continue
        
        #case5: nothing coloured in this column
        if first == 0 and repeated_cell[0] == puzzle.row:
          
          
            if [-1,-2] not in stateinfo.track_row_constraints: 
#                 print("Case5:"+ " at "+ str(j) + "th row invalid")
                return False
              
#             #for rc in state.track_row_constraints:
#             for row in range(puzzle.row):
#                 #case5.1: a cell in previous column & same row has coloured (for sure this cell is empty) => INVALID
#                 if j > 1 and state[n*puzzle.col+j-1] == '1': falseCount += 1
                          
#                 #case5.2: at least one cell in any following columns has coloured (for sure this cell is empty) => 
#                 if j < puzzle.col-1:
#                     following_cells = state[row*puzzle.col+j+1: row*(puzzle.col+1)]
#                     if following_cells.find('1') != -1 : falseCount += 1
                      
    #if falseCount == puzzle.row: return False
        
    return True

    
# toggle a cell in the state
def turn_on(state, start, num):
    return state[:start] + '1'*num + state[start+num:]
         

def generate_possible_successors(puzzle, state):
    successors = []
    tracked_records = state.track_row_constraints
    for row in range(puzzle.row):
        # get inds from records
        constraint_ind = tracked_records[row][0] + 1
        startCol = tracked_records[row][1] + 2
        if constraint_ind >= len(puzzle.row_list[row]): # all constraints are satisfied for this row
            continue

        colsLeft = puzzle.col - startCol
        requiredSpaces = 0
        for constraint in puzzle.row_list[row][constraint_ind:]: # checking all constraint on the same row
            requiredSpaces += constraint + 1
        requiredSpaces -= 1 # removing extra + 1 at the end

        for col in range(startCol, puzzle.col):
            if colsLeft < requiredSpaces:
                break
            rowStart = row * puzzle.col
            successor = StateInfo(copy.deepcopy(state.state), copy.deepcopy(state.track_row_constraints))
            successor.state = turn_on(successor.state, rowStart+col, puzzle.row_list[row][constraint_ind])
            successor.track_row_constraints[row] = [constraint_ind, col + puzzle.row_list[row][constraint_ind]-1]
            successors.append(successor)
            colsLeft -= 1

    return successors

def get_initial_track_row_constraint(numRows):
    return [[-1,-2] for i in range(numRows)]
 
#state = string 101110101 (board)
#row_list & col_list = list of list(row and column)
def get_successors(puzzle, stateInfo):
  
    successors = []
    possible_successors = generate_possible_successors(puzzle, stateInfo)
    
    for new_state in possible_successors:    
        if isValidColConstraint(puzzle, new_state):
            successors.append(new_state)
            #print(draw_state(new_state.state,puzzle))
            #print(new_state.track_row_constraints)
        
    return successors

        
  
  
def check_row_or_col(state, row_const):
    row_result = []
    check_state = state.split("0")
    for i in check_state:
        n = len(i)
        if(n != 0):
            row_result.append(n)

    return row_result == row_const


# Jiwon
# input: defined puzzle & current state
# output: True if state is the goal state
def is_goal(puzzle, state):
    result = True

    for i in range(puzzle.row):
        r = state[i*puzzle.col:(i+1)*puzzle.col]
        result = check_row_or_col(r, puzzle.row_list[i])
        if(not result):
            return False

    for j in range(puzzle.col):
        r = ""
        for x in range(puzzle.col):
            r += state[x * puzzle.col + j]
        result = check_row_or_col(r, puzzle.col_list[j])
        if(not result):
            return False
    return result



# input: current state and r,c number to change toggle a cell in the state
#def turn_on(state, row, col, num):
    #global cost
    #cost += 1
    
def solve(puzzle, initial_state):
    frontier = []
    frontier.append(StateInfo(initial_state, get_initial_track_row_constraint(puzzle.row)))

    explored = []
    explored.append(initial_state)
    result = ""
    while len(frontier) > 0:
        current_state = frontier.pop()
        #print(draw_state(current_state.state,puzzle))
        #print(current_state.track_row_constraints)
        if is_goal(puzzle, current_state.state):
            result = current_state.state
            break

        for successorInfo in get_successors(puzzle, current_state):
            if successorInfo.state not in explored:
                frontier.append(successorInfo)

    return result
    
if __name__ == "__main__":
    puzzles = read_puzzle()
    for p in puzzles:
        init = build_init_state(p)
        start=datetime.now()
        solved = solve(p, init)
        print(datetime.now()-start)
        print(draw_state(solved,p))

    




