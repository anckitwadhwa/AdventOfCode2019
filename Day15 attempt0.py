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
    
def process_input(input_queue, direction_queue, output_thread, debug_prints_level = 0):
    debug_prints_level -= 1
    
    continue_execution = True
    while(continue_execution):
    
        continue_execution = output_thread.is_alive()
        # yield to let intcode execute a bit
        while((len(input_queue) > 0) and continue_execution):
            
            if(debug_prints_level > 50):
                print("Sleeping in input thread")
            
            time.sleep(0.1)
            
            if(debug_prints_level > 50):
                print("Awake in input thread")
            
        
        input_str = input("Direction And Steps. Q to exit (Ex: E10 OR Q):")
        
        continue_execution = ((input_str != "Q") and (input_str != "q") and output_thread.is_alive())
        
        if(continue_execution != True):
            input_queue.append("0")
            break
        
        
        with open("Day15_all_inputs.txt", "a") as output_file:
            output_file.write(input_str)
            output_file.write("\n")
        
        append_input_queue(input_str, input_queue, direction_queue, debug_prints_level)
        
        
def append_input_queue(input_str, input_queue, direction_queue, debug_prints_level = 0):
    debug_prints_level -= 1

    direction = 0
    
    if((input_str[0] == "N") or (input_str[0] == "n")):
        direction = 1
    elif((input_str[0] == "S") or (input_str[0] == "s")):
        direction = 2
    elif((input_str[0] == "W") or (input_str[0] == "w")):
        direction = 3
    elif((input_str[0] == "E") or (input_str[0] == "e")):
        direction = 4
    

    steps = int(input_str[1:])
    
    for index in range(steps):
        input_queue.append(direction)
        direction_queue.append(direction)

def add_input_from_file(input_queue, direction_queue, debug_prints_level = 0):
    debug_prints_level -= 1
    
    with open("Day15_all_inputs.txt", "r") as input_file:
            input_str = input_file.read()
            
    lines = input_str.splitlines()
    
    for line in lines:
        append_input_queue(line, input_queue, direction_queue, debug_prints_level)
            
        


def process_output(input_queue, output_queue, direction_queue, starting_location, board_state, debug_prints_level = 0):
    debug_prints_level -= 1
    
    last_location = starting_location
    
    
    continue_execution = True
    while(continue_execution):
    
        while(len(output_queue) < 1):
            time.sleep(0.01)
            
        
        if(debug_prints_level > 50):
            print(f'output_queue:{output_queue}')
            print(f'direction_queue:{direction_queue}')
            
        while(len(output_queue) >= 1):
            status = output_queue.popleft()
            
            if(status == 99):
                continue_execution = False;
                break
            
            intended_direction = direction_queue.popleft()
            
            update_location_and_board(status, intended_direction, last_location, board_state, debug_prints_level)
            
            #if hit a wall, empty the input_queue and direction_queue
            # if(status == 0):
                # input_queue.clear()
                # direction_queue.clear()
            
        print_board_state(board_state, last_location, debug_prints_level)
 
def update_location_and_board(status, intended_direction, location, board_state, debug_prints_level = 0):
    debug_prints_level -= 1
    
    x_delta, y_delta = get_x_y_delta(intended_direction, debug_prints_level)
    
    if(status == 0):
        board_state[location.y + y_delta][location.x + x_delta] = "#"

    elif(status == 1):
        board_state[location.y + y_delta][location.x + x_delta] = " "

    elif(status == 2):
        board_state[location.y + y_delta][location.x + x_delta] = "!"

    if(status != 0):
        #update location
        location.x += x_delta
        location.y += y_delta
      
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
   
def print_board_state(board_state, location, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level <= 20):
        return
        
    for y, row in enumerate(board_state):
        line = "".join(row) 
        if(y == location.y):
            line = line[0:location.x] + "@" + line[location.x+1:]
        
        print(line)
        

def solve_day17_puzzle(debug_prints_level = 0):
    debug_prints_level -= 1
    use_threading = True
    
    input_queue = deque()
    output_queue = deque()
    direction_queue = deque()
    N = 100
    starting_location = Point.Point(int(N/2), int(N/2))
    
    board_state = setup_board(N, starting_location, debug_prints_level)
    
    executor = None
    output_thread = None
    input_thread = None
    
    if(use_threading):
        output_thread = threading.Thread(name="output thread", target=process_output, args=([input_queue, output_queue, direction_queue, starting_location, board_state, debug_prints_level]))
        output_thread.start()
        
        add_input_from_file(input_queue, direction_queue, debug_prints_level)
    
        input_thread = threading.Thread(name="input thread", target=process_input, args=([input_queue, direction_queue, output_thread, debug_prints_level]))
        input_thread.start()
        
        executor = IntcodeExecutor.IntcodeExecutor(day15_intcode_program, input_queue, output_queue, None, False)
    else:
        executor = IntcodeExecutor.IntcodeExecutor(day15_intcode_program, None, None, None, False)
    
    
    #wait for threads to join
    executor.thread.join()
    
    if(use_threading):
        if(debug_prints_level > 20):
            print("executor joined, waiting for output")
            
        output_thread.join()
        if(debug_prints_level > 20):
            print("output joined, waiting for input")
        
        input_thread.join()
        



day15_intcode_program = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,1002,1036,1,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1001,1034,0,1039,1002,1036,1,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,1001,1035,0,1040,102,1,1038,1043,1002,1037,1,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,102,1,1035,1040,1001,1038,0,1043,1002,1037,1,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,5,1032,1006,1032,165,1008,1040,35,1032,1006,1032,165,1102,1,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,38,1044,1106,0,224,1101,0,0,1044,1106,0,224,1006,1044,247,1001,1039,0,1034,1001,1040,0,1035,101,0,1041,1036,102,1,1043,1038,1002,1042,1,1037,4,1044,1106,0,0,4,26,16,55,25,8,4,99,2,21,20,20,56,26,97,81,12,2,4,9,32,7,49,54,5,18,81,16,7,88,4,23,30,66,17,31,27,29,34,26,81,62,27,81,41,84,12,53,90,79,37,22,45,27,17,39,76,1,55,58,44,20,18,57,57,20,76,47,20,44,88,26,43,36,79,12,68,30,19,71,27,21,18,75,18,9,56,29,15,84,8,74,93,1,35,91,39,32,86,9,97,54,4,22,59,13,61,31,19,97,26,82,35,73,23,77,71,59,26,76,78,73,34,85,67,26,1,66,91,79,26,95,5,75,99,29,14,23,26,8,66,97,55,21,25,49,17,99,71,37,62,21,45,46,13,29,30,24,31,63,99,12,12,63,10,64,2,76,3,8,37,94,33,12,47,65,35,65,60,12,88,8,10,49,36,12,14,4,43,82,19,16,51,52,20,17,43,18,33,49,19,93,49,29,86,10,31,92,90,44,26,97,8,63,70,81,28,17,80,23,22,79,56,33,67,61,91,37,4,83,77,16,6,8,33,66,92,46,8,34,23,81,3,93,14,23,72,20,91,16,62,79,7,27,81,10,11,44,65,24,66,77,31,12,53,15,50,84,24,70,29,62,50,5,3,88,13,52,85,42,4,15,39,82,65,18,15,58,37,71,10,13,90,98,29,59,52,3,22,13,59,91,29,23,79,1,7,24,80,79,37,31,77,17,11,64,10,9,8,74,97,6,74,35,73,44,68,29,97,3,45,73,30,28,80,9,48,73,76,7,3,77,83,8,12,41,62,44,10,21,27,74,32,95,73,4,47,71,6,67,17,57,10,67,5,25,74,18,24,57,7,61,66,4,51,14,7,44,29,79,74,11,6,49,75,32,3,98,89,63,5,15,5,74,78,37,7,77,3,13,47,9,33,76,22,47,6,72,12,35,75,39,25,87,83,37,19,91,25,45,22,30,54,83,74,22,71,19,3,3,85,74,37,95,26,67,46,10,12,96,44,50,32,90,3,28,56,24,43,4,1,65,5,9,50,22,44,88,9,48,59,21,24,54,11,35,53,28,7,82,32,24,17,45,88,34,72,95,17,9,39,29,4,55,66,95,22,62,15,71,11,39,51,37,86,49,20,10,63,31,66,59,15,55,93,3,11,28,54,30,41,20,92,7,3,12,54,49,14,33,56,89,21,26,67,20,93,7,64,3,31,60,23,51,36,30,57,20,14,28,88,4,6,69,33,65,98,35,96,80,49,25,68,78,97,30,63,35,73,89,32,64,69,10,68,96,19,89,71,41,32,31,30,90,5,71,20,53,36,51,23,87,19,25,15,34,15,48,19,25,33,14,50,64,11,96,19,34,14,44,33,29,40,16,50,90,22,34,44,17,64,63,18,86,57,29,44,22,98,16,41,20,99,34,14,51,11,4,84,91,66,27,49,6,58,34,95,62,6,45,53,27,72,4,12,40,43,17,41,93,27,30,70,31,47,87,26,64,9,63,59,73,9,11,97,35,56,73,23,58,9,49,13,88,1,87,13,54,21,94,13,69,16,39,2,10,64,13,10,19,96,2,23,1,60,99,47,12,61,37,13,70,24,48,91,7,33,51,10,25,88,33,69,29,98,16,16,60,5,29,44,17,21,41,62,65,8,61,84,27,42,78,72,23,98,16,76,98,77,37,19,49,37,93,83,97,1,63,9,63,27,66,34,74,87,58,3,90,4,48,51,67,32,66,9,56,9,44,1,67,24,49,29,58,20,70,32,73,27,82,0,0,21,21,1,10,1,0,0,0,0,0,0]
debug_prints_level = 50
solve_day17_puzzle(debug_prints_level)
