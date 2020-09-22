from nonogram import read_puzzle
from state import draw_state, build_init_state
from datetime import datetime
import copy
import numpy as np
import re # regular expression


class StateInfo:
    def __init__(self, state, track_row_constraints):
        self.state = state # string
        # track_row_constraints: list of pairs (in list) [j, k] where for each row i, jth row constraint
        # is the lastest satisfied constraint in that row and k is the last index(position) of
        # that last satisfied constraint
        # the values should initially be [-1, -2]
        self.track_row_constraints = track_row_constraints


def is_valid_col_constraint(puzzle, stateInfo):
    state = stateInfo.state
    track_row_constraints = stateInfo.track_row_constraints
    numCols = puzzle.col
    numRows = puzzle.row

    for col in range(numCols):
        numOnes = 0
        stringToMatch = ""
        for row in range(numRows):
            if state[row*puzzle.col+col] == '1':
                numOnes += 1
                stringToMatch += '1'
            elif state[row*puzzle.col+col] == '0' \
                and ((track_row_constraints[row][0] >= len(puzzle.row_list[row])-1) \
                    or (track_row_constraints[row][1] + 1 >= col)):
                stringToMatch += '0'
            else:
                stringToMatch += '2' # can either be 0 or 1

        requiredOnes = 0
        pattern = ""
        isInit = True
        pattern += "[0,2]*"
        for constraint in puzzle.col_list[col]:
            if not isInit: # need zero(s) only in between constraints
                pattern += "[0,2]+"
            requiredOnes += constraint
            pattern += '[1,2]{' + str(constraint) + '}' # requiring exact numbers of ones
            isInit = False

        pattern += "[0,2]*"

        if numOnes > requiredOnes:
            return False
        
        if not re.match(pattern, stringToMatch):
            return False

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
            newState = turn_on(state.state, rowStart+col, puzzle.row_list[row][constraint_ind])
            newTracker = state.track_row_constraints[:]
            newTracker[row] = [constraint_ind, col + puzzle.row_list[row][constraint_ind]-1]
            successor = StateInfo(newState, newTracker)
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

        if is_valid_col_constraint(puzzle, new_state):
            successors.append(new_state)
        
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
        for x in range(puzzle.row):
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
        if is_goal(puzzle, current_state.state):
            result = current_state.state
            break

        for successorInfo in get_successors(puzzle, current_state):
            if successorInfo.state not in explored:
                frontier.append(successorInfo)
                explored.append(successorInfo.state)

    return result
    
if __name__ == "__main__":
    puzzles = read_puzzle()
    for p in puzzles:
        init = build_init_state(p)
        start=datetime.now()
        solved = solve(p, init)
        print(datetime.now()-start)
        print(draw_state(solved,p))

    # result = re.match("10+1", "1[0-1]1")
    # result = re.match("[1,2]{3}0+1", "10101")
    # result = re.match("[1,2]{3}[0,2]+1", "11101")
    # if result:
    #     print("TRUE")
    # else:
    #     print("FALSE")

    



