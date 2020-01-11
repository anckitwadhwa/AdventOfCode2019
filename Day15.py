from collections import deque
import IntcodeExecutor
import Point
import time
import threading
from inspect import currentframe

def setup_board(N, starting_location, debug_prints_level = 0):
    debug_prints_level -= 1
    
    board_state = [None] * N
    for index in range(N):
        board_state[index] = ["?"] * N
        
        
    board_state[starting_location.y][starting_location.x] = "*"
    
    return(board_state)

def halt_executor(executor, debug_prints_level = 0):

    # executor.input_queue.clear()
    executor.input_queue.append(-1)
    
    
def update_location_and_board(status, intended_direction, location, board_state, debug_prints_level = 0):
    debug_prints_level -= 1
    actual_direction = 0
    
    x_delta, y_delta = get_x_y_delta(intended_direction, debug_prints_level)
    
    if(status == 0):
        board_state[location.y + y_delta][location.x + x_delta] = "#"
        actual_direction = 0

    elif(status == 1):
        board_state[location.y + y_delta][location.x + x_delta] = " "

    elif(status == 2):
        board_state[location.y + y_delta][location.x + x_delta] = "O"

    if(status != 0):
        #update location
        location.x += x_delta
        location.y += y_delta
        
        actual_direction = intended_direction
        
    return(actual_direction)
      
def get_x_y_delta(intended_direction, debug_prints_level = 0):
   debug_prints_level -= 1
    
   x_delta = 0
   y_delta = 0
   
   if(intended_direction == 1):
    #north
    y_delta = -1
    
   elif(intended_direction == 2):
    #south
    y_delta = 1
    
   elif(intended_direction == 3):
    #west
    x_delta = -1
   
   elif(intended_direction == 4):
    #east
    x_delta = 1
    
   
   return(x_delta, y_delta)
   
def print_board_state(board_state, location = None, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level <= 20):
        return
        
    for y, row in enumerate(board_state):
        line = "".join(row) 
        if((location != None) and (y == location.y)):
            line = line[0:location.x] + "@" + line[location.x+1:]
        
        print(line)
        

def print_oxygen_fill_state(oxygen_fill_state, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level <= 20):
        return
        
    for y, row in enumerate(oxygen_fill_state):
        line = [""] * len (row)
        for x, element in enumerate(row):
            line[x] = str(element).rjust(4, " ")
    
        initial_str = str(y) + "#: "
        print(initial_str + "".join(line))
    

def get_user_input(debug_prints_level = 0):
    debug_prints_level -= 1
    is_bad_input = True
    choice = ""
    num_steps = 0
    direction = 0
        
    while(is_bad_input):
        is_bad_input = False
        
        print("A#: Automate '#' steps")
        print("B: Backtrack automatically to last location with multiple paths")
        print("M[N/E/W/S]#: Manual move in specified direction, '#' steps")
        print("MB#: Manually backtrack'#' steps")
        print("Q. Quit")
        
        user_input = input("Your Choice: ")
        
        if(len(user_input) < 1):
            print("bad input")
            is_bad_input = True
        else:
            choice = user_input[0].lower()
        
        if(choice == "q"):
            #Nothing to do
            pass
        
        elif(choice == "a"):
            num_steps = int(user_input[1:])
            
        elif(choice == "m"):
            direction = direction_int_from_str(user_input[1].lower())
            num_steps = int(user_input[2:])
        
        elif(choice == "b"):
            num_steps = -1
            direction = -1
            
        else:
            print("bad input")
            is_bad_input = True
            
    if(debug_prints_level > 90):
        print("*" * 50)
        print(f'choice:{choice}, direction:{direction}, num_steps:{num_steps}')
        
    return(choice, direction, num_steps)
    
def direction_int_from_str(direction_str, debug_prints_level = 0):
    debug_prints_level -= 1
    
    direction_int = 0
    
    if(direction_str[0] == "n"):
        direction_int = 1
    elif(direction_str[0] == "s"):
        direction_int = 2
    elif(direction_str[0] == "w"):
        direction_int = 3
    elif(direction_str[0] == "e"):
        direction_int = 4
    elif(direction_str[0] == "b"):
        #back
        direction_int = -1
    
    return(direction_int)
    
def execute_user_input(choice, direction, num_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level = 0):
    debug_prints_level -= 1
    is_oxygen_found = False
    
    if(choice != "a"):
        is_oxygen_found = move_on_specified_path(direction, num_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level)
    else:
        is_oxygen_found = explore_and_move(num_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level)
        
    return(is_oxygen_found)

def get_unexplored_directions(executor, board_state, current_location, debug_prints_level = 0):
    debug_prints_level -= 1
    is_oxygen_found = False
    unexplored_directions = []
    
    for direction in range(1, 5):
        intended_direction   = direction
        x_delta, y_delta = get_x_y_delta(intended_direction)
        
        intended_x = current_location.x + x_delta
        intended_y = current_location.y + y_delta
        
        if(board_state[intended_y][intended_x] != "?"):
            continue
            
        is_oxygen_found, actual_direction = attempt_move(intended_direction, executor, board_state, current_location, debug_prints_level)
        
        if(actual_direction == intended_direction):
            # was able to move, now move back
            unexplored_directions.append(actual_direction)
            opposite_direction = get_opposite_direction(actual_direction)
            attempt_move(opposite_direction, executor, board_state, current_location, debug_prints_level)
    
    return(is_oxygen_found, unexplored_directions)

def explore_and_move(num_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level = 0):
    debug_prints_level -= 1
    count = 0
    is_trapped = False
    is_oxygen_found = False
        
    while((count < num_steps) and not(executor.is_halted()) and not(is_trapped) and not (is_oxygen_found)):
    
        is_oxygen_found, unexplored_directions = get_unexplored_directions(executor, board_state, current_location, debug_prints_level)
        
        if(is_oxygen_found):
            break
    
        #we are trapped when there are no possible directions (we skipped the back of last direction intentionally)
        is_deadend = (len(unexplored_directions) == 0)
        is_trapped = is_deadend and (len(unexplored_paths_stack) == 0)
        
        if(is_deadend):
        
            if(is_trapped):
                print("nowhere to go, giving up.")
                break
                
            #return to last known location with multiple paths
            #magic values
            steps_to_back_track = -1
            back_track_direction = -1
            
            #get the direction we need to move in after back tracking. Need to get this now before the value is popped off
            next_direction = unexplored_paths_stack[-1]['direction']
            next_steps = 1
            
            if(debug_prints_level > 20):
                print(f'Trapped. Back tracking {steps_to_back_track} steps. Current state')
                print_board_state(board_state, current_location, debug_prints_level)
             
            move_on_specified_path(back_track_direction, steps_to_back_track, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level)
            move_on_specified_path(next_direction, next_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level)
        
        else:
        
            for index in range(1, len(unexplored_directions)):
                unexplored_paths_stack.append({'offset' : len(direction_stack), 'direction' : unexplored_directions[index]})
                
            #move 1 step in first available direction, preferring the direction we have been moving in
            intended_direction   = unexplored_directions[0]
            is_oxygen_found, actual_direction = attempt_move(intended_direction, executor, board_state, current_location, debug_prints_level)
                
            if(actual_direction != intended_direction):
                #something went pretty wrong
                print("Something bad happened. Likely programming error")
                break
            else:
                direction_stack.append(actual_direction)
        
        
            if(debug_prints_level > 90):
                print(f'count, num_steps, intended_direction, actual_direction, location: {count, num_steps, intended_direction, actual_direction, str(current_location)}')
        
        if((debug_prints_level > 20) and (count % 10 == 0 )):
            print_board_state(board_state, current_location, debug_prints_level)
        
        count += 1
    
    if(debug_prints_level > 20):
        print_board_state(board_state, current_location, debug_prints_level)
        print(f'performed {count} steps of {num_steps} requested')
        print(f'# locations with multiple paths = {len(unexplored_paths_stack)}')
    
    return(is_oxygen_found)

def move_on_specified_path(intended_direction, num_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level = 0):
    debug_prints_level -= 1
    
    is_oxygen_found = False
    is_at_wall = False
    count = 0
    is_backtracking = (intended_direction == -1)
    input_queue = executor.input_queue
    output_queue = executor.output_queue
    
    if(is_backtracking):
        if((num_steps < 0) and (len(unexplored_paths_stack) > 0)):
            num_steps = len(direction_stack) - unexplored_paths_stack.pop()['offset']
        else:
            num_steps = min(len(direction_stack), num_steps)
        
    while((count < num_steps) and not(is_at_wall) and not(executor.is_halted())):
    
        if(is_backtracking):
            intended_direction = get_opposite_direction(direction_stack.pop())
        

        is_oxygen_found, actual_direction = attempt_move(intended_direction, executor, board_state, current_location, debug_prints_level)
        
        if(debug_prints_level > 90):
            print(f'count, num_steps, intended_direction, actual_direction, location: {count, num_steps, intended_direction, actual_direction, str(current_location)}')

        if((debug_prints_level > 20) and (count % 10 == 0 )):
            print_board_state(board_state, current_location, debug_prints_level)
        
        is_at_wall = (actual_direction != intended_direction)
        count += 1
        
        if(not(is_backtracking) and not(is_at_wall)):
            direction_stack.append(actual_direction)
        
        
        
    if(debug_prints_level > 20):
        print_board_state(board_state, current_location, debug_prints_level)
        print(f'performed {count} steps of {num_steps} requested')
        print(f'# locations with multiple paths = {len(unexplored_paths_stack)}')
        
    return(is_oxygen_found)

def attempt_move(intended_direction, executor, board_state, current_location, debug_prints_level = 0):
    debug_prints_level -= 1
    is_oxygen_found = False
    
    if(debug_prints_level > 90):
        print(f'intended_direction, current_location:{intended_direction, current_location}')
    
    input_queue = executor.input_queue
    output_queue = executor.output_queue

    input_queue.append(intended_direction)
            
    while(not(executor.is_halted()) and (len(output_queue) < 1)):
        if(debug_prints_level > 90):
            print("sleeping in attempt_move")
        
        time.sleep(0.01)
        
        
    status = output_queue.popleft()
    is_oxygen_found = (status == 2)
    
    if(is_oxygen_found):
        #found oxygen tank, halt execution
        print("Found oxygen tank. Quitting")
    
    if(debug_prints_level > 90):
        print("awake in attempt_move")
        
    actual_direction = update_location_and_board(status, intended_direction, current_location, board_state, debug_prints_level)
    
    if(debug_prints_level > 90):
        print_board_state(board_state, current_location, debug_prints_level)
    
    
    return(is_oxygen_found, actual_direction)    

def get_opposite_direction(direction, debug_prints_level = 0):
    debug_prints_level -= 1
    
    opposite_direction = 0
    
    if(direction == 1):
        opposite_direction = 2
    elif(direction == 2):
        opposite_direction = 1
        
    elif(direction == 3):
        opposite_direction = 4
    elif(direction == 4):
        opposite_direction = 3
    
    return(opposite_direction)
 

def solve_day17_puzzle(debug_prints_level = 0):
    debug_prints_level -= 1
    use_threading = True
    
    input_queue = deque()
    output_queue = deque()
    direction_stack = []
    unexplored_paths_stack = []
    N = 41
    current_location = Point.Point(21, 21)
    
    board_state = setup_board(N, current_location, debug_prints_level)
    executor = IntcodeExecutor.IntcodeExecutor(day15_intcode_program, input_queue, output_queue, None, False)
    
    continue_execution = True
    
    while(continue_execution):
        choice, direction, num_steps = get_user_input(debug_prints_level)
        
        continue_execution = (choice != "q")
        
        if(continue_execution):
            is_oxygen_found = execute_user_input(choice, direction, num_steps, executor, direction_stack, unexplored_paths_stack, board_state, current_location, debug_prints_level)
            # continue_execution = not(is_oxygen_found) and not(executor.is_halted())
            continue_execution = not(executor.is_halted())
        
    #force intcode to exit
    halt_executor(executor, debug_prints_level)
    executor.thread.join()
    
    print(f'len(direction_stack): {len(direction_stack)}; len(unexplored_paths_stack): {len(unexplored_paths_stack)}')
    
def solve_day17_puzzle_b(debug_prints_level = 0):
    debug_prints_level -= 1
    
    board_state = read_board_state("Day15_area.txt", debug_prints_level)
    
    if(debug_prints_level > 90):
        print_board_state(board_state, debug_prints_level=debug_prints_level)
        
    oxygen_fill_state = [None] * len(board_state)
    
    for y, row in enumerate(board_state):
        oxygen_fill_state[y] = [-1] * len(row)
        
        for x, element in enumerate(row):
        
            if(element != " "):
                oxygen_fill_state[y][x] = float("Inf")
        
    
    print_oxygen_fill_state(oxygen_fill_state, debug_prints_level)
    
    # starting_location = get_oxygen_tank_location(board_state, debug_prints_level)
    starting_location = Point.Point(5, 35)
    
    locations_to_fill = deque()
    locations_to_fill.append({'location' : starting_location, 'value': 0})
    
    compute_oxygen_fill_time(locations_to_fill, oxygen_fill_state, debug_prints_level)
    print_oxygen_fill_state(oxygen_fill_state, debug_prints_level)
    


def read_board_state(filename, debug_prints_level = 0):
    debug_prints_level -= 1
    
    with open(filename, "r") as input_file:
        input_str = input_file.read()
            
    lines = input_str.splitlines()
    
    board_state = [None] * len(lines)
    
    for y, line in enumerate(lines):
        board_state[y] = [" "] * len(line)
        
        for x, element in enumerate(line):
            board_state[y][x] = element

    return(board_state)
    
def compute_oxygen_fill_time(locations_to_fill, oxygen_fill_state, debug_prints_level = 0):
    debug_prints_level -= 1
    
    count = 0
    num_steps = 0
    user_input = ""
    while((user_input != "q") and (len(locations_to_fill) > 0)):
        element = locations_to_fill.popleft()
        
        x = element['location'].x
        y = element['location'].y
        value = element['value']
        
        oxygen_fill_state[y][x] = value
        
        for direction in range(1, 5):
            x_delta, y_delta = get_x_y_delta(direction)
            
            updated_x = x + x_delta
            updated_y = y + y_delta
            
            updated_location = Point.Point(updated_x, updated_y)
            
            if(oxygen_fill_state[updated_y][updated_x] == -1):
                locations_to_fill.append({'location' : updated_location, 'value': value+1})
        
        if(count == num_steps):
            if(debug_prints_level > 50):
                print_oxygen_fill_state(oxygen_fill_state, debug_prints_level)
                print(f'remaining # of locations:{len(locations_to_fill)}')
                
            print("C#: compute next # steps")
            print("Q: Quit")
            user_input = input("Your Input: ")
            
            if(len(user_input) > 1):
                num_steps = int(user_input[1:])
            
            count = 0
        
        else:
            count += 1
    
    

    
day15_intcode_program = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,1002,1036,1,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1001,1034,0,1039,1002,1036,1,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,1001,1035,0,1040,102,1,1038,1043,1002,1037,1,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,102,1,1035,1040,1001,1038,0,1043,1002,1037,1,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,5,1032,1006,1032,165,1008,1040,35,1032,1006,1032,165,1102,1,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,38,1044,1106,0,224,1101,0,0,1044,1106,0,224,1006,1044,247,1001,1039,0,1034,1001,1040,0,1035,101,0,1041,1036,102,1,1043,1038,1002,1042,1,1037,4,1044,1106,0,0,4,26,16,55,25,8,4,99,2,21,20,20,56,26,97,81,12,2,4,9,32,7,49,54,5,18,81,16,7,88,4,23,30,66,17,31,27,29,34,26,81,62,27,81,41,84,12,53,90,79,37,22,45,27,17,39,76,1,55,58,44,20,18,57,57,20,76,47,20,44,88,26,43,36,79,12,68,30,19,71,27,21,18,75,18,9,56,29,15,84,8,74,93,1,35,91,39,32,86,9,97,54,4,22,59,13,61,31,19,97,26,82,35,73,23,77,71,59,26,76,78,73,34,85,67,26,1,66,91,79,26,95,5,75,99,29,14,23,26,8,66,97,55,21,25,49,17,99,71,37,62,21,45,46,13,29,30,24,31,63,99,12,12,63,10,64,2,76,3,8,37,94,33,12,47,65,35,65,60,12,88,8,10,49,36,12,14,4,43,82,19,16,51,52,20,17,43,18,33,49,19,93,49,29,86,10,31,92,90,44,26,97,8,63,70,81,28,17,80,23,22,79,56,33,67,61,91,37,4,83,77,16,6,8,33,66,92,46,8,34,23,81,3,93,14,23,72,20,91,16,62,79,7,27,81,10,11,44,65,24,66,77,31,12,53,15,50,84,24,70,29,62,50,5,3,88,13,52,85,42,4,15,39,82,65,18,15,58,37,71,10,13,90,98,29,59,52,3,22,13,59,91,29,23,79,1,7,24,80,79,37,31,77,17,11,64,10,9,8,74,97,6,74,35,73,44,68,29,97,3,45,73,30,28,80,9,48,73,76,7,3,77,83,8,12,41,62,44,10,21,27,74,32,95,73,4,47,71,6,67,17,57,10,67,5,25,74,18,24,57,7,61,66,4,51,14,7,44,29,79,74,11,6,49,75,32,3,98,89,63,5,15,5,74,78,37,7,77,3,13,47,9,33,76,22,47,6,72,12,35,75,39,25,87,83,37,19,91,25,45,22,30,54,83,74,22,71,19,3,3,85,74,37,95,26,67,46,10,12,96,44,50,32,90,3,28,56,24,43,4,1,65,5,9,50,22,44,88,9,48,59,21,24,54,11,35,53,28,7,82,32,24,17,45,88,34,72,95,17,9,39,29,4,55,66,95,22,62,15,71,11,39,51,37,86,49,20,10,63,31,66,59,15,55,93,3,11,28,54,30,41,20,92,7,3,12,54,49,14,33,56,89,21,26,67,20,93,7,64,3,31,60,23,51,36,30,57,20,14,28,88,4,6,69,33,65,98,35,96,80,49,25,68,78,97,30,63,35,73,89,32,64,69,10,68,96,19,89,71,41,32,31,30,90,5,71,20,53,36,51,23,87,19,25,15,34,15,48,19,25,33,14,50,64,11,96,19,34,14,44,33,29,40,16,50,90,22,34,44,17,64,63,18,86,57,29,44,22,98,16,41,20,99,34,14,51,11,4,84,91,66,27,49,6,58,34,95,62,6,45,53,27,72,4,12,40,43,17,41,93,27,30,70,31,47,87,26,64,9,63,59,73,9,11,97,35,56,73,23,58,9,49,13,88,1,87,13,54,21,94,13,69,16,39,2,10,64,13,10,19,96,2,23,1,60,99,47,12,61,37,13,70,24,48,91,7,33,51,10,25,88,33,69,29,98,16,16,60,5,29,44,17,21,41,62,65,8,61,84,27,42,78,72,23,98,16,76,98,77,37,19,49,37,93,83,97,1,63,9,63,27,66,34,74,87,58,3,90,4,48,51,67,32,66,9,56,9,44,1,67,24,49,29,58,20,70,32,73,27,82,0,0,21,21,1,10,1,0,0,0,0,0,0]
debug_prints_level = 50
solve_day17_puzzle(debug_prints_level)
# solve_day17_puzzle_b(debug_prints_level)
