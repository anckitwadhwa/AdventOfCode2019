from collections import deque
import IntcodeExecutor
import time
from inspect import currentframe


def test_intcode_module():

    
    print("Starting executor")
    executor = IntcodeExecutor.IntcodeExecutor(drone_program_sequence.copy())
    
    print("In main thread, about to call join")
    executor.thread.join()
    
    print("after join")
    

def get_new_board(default_char = ".", height = 10, width = 10):

    board = [None] * height
    for i, row in enumerate(board):
        board[i] = [default_char] * width
    
    return(board)
    
def print_board(board, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level <= 0):
        return

    print("~" * 75)
    for row in board:
        print("".join(row))
        
def process_io(board, x_offset, y_offset, debug_prints_level = 0):
    debug_prints_level -= 1
    
    # start drone program
    input_queue = deque()
    output_queue = deque()
    

    y = 0
    while(y < len(board)):
        if((debug_prints_level > 20) and (y % 10 == 0)):
            print(f'testing: y: {y}')
            
        x = 0
        while(x < len(board[y])):
            if(debug_prints_level > 50):
                    print(f'testing: {x}, {y}')
            input_queue.clear()
            output_queue.clear()
            
            input_queue.append(x + x_offset)
            input_queue.append(y + y_offset)
            
            executor = IntcodeExecutor.IntcodeExecutor(drone_program_sequence.copy(), input_queue, output_queue)
    
        
            while(len(output_queue) < 1):
                time.sleep (0.001)

            drone_status = output_queue.popleft()
            executor.thread.join()
            
            if(drone_status == 1):
                if(debug_prints_level > 20):
                    print(f'#############: {x}, {y}')
                board[y][x] = "#"
                
            x += 1
        y += 1
                
def count_points_affected(board, debug_prints_level = 0):
    debug_prints_level -= 1
    
    counter = 0
    for row in board:
        counter += row.count("#")
        
    return(counter)

def solve_day_19_puzzle(x_offset, y_offset, height, width, debug_prints_level = 0):
    debug_prints_level -= 1

    board = get_new_board(".", height, width)
    
    process_io(board, x_offset, y_offset, debug_prints_level)
    
    print_board(board, debug_prints_level)
    print(count_points_affected(board, debug_prints_level))

def find_earliest_row_given_width(xy_flipped, input_queue, output_queue, x_max = 1000, y_max = 1000, min_width = 100, debug_prints_level = 0):
    debug_prints_level -= 1

    #heuristic
    if(xy_flipped):
        y_start = 6 * min_width
    else:
        y_start = 8 * min_width
        
    y = y_start
    y_earliest = -1
    x_earliest = -1
    count = -1
    while((count < min_width) and (y < y_max)):
        x_earliest, count = get_count_in_row(xy_flipped, y, input_queue, output_queue, x_max, debug_prints_level)
        
        if(debug_prints_level > 20):
            print(f'for y:{y}, count:{count}')
        
        if(count < min_width):
            y += min_width - count
    
    if(count >= min_width):
        # we have a y estimate, back track to find y_earliest
        
        y_earliest = y
        for y in range(y_earliest-1, -1, -1):
            x_earliest, count = get_count_in_row(xy_flipped, y, input_queue, output_queue, x_max, debug_prints_level)
            
            if(debug_prints_level > 20):
                print(f'for y:{y}, count:{count}')
            
            if(count < min_width):
                break
        
        y_earliest = y
        if(count < min_width):
            y_earliest += 1
            
    
    return(x_earliest, y_earliest)

def get_count_in_row(xy_flipped, y, input_queue, output_queue, x_max = 1000, debug_prints_level = 0):
    debug_prints_level -= 1
    
    x_quanta = int(x_max / 100)
    
    # find starting point
    x = 0
    for x in range(0, x_max, x_quanta):
        drone_status = get_drone_status(xy_flipped, x, y, input_queue, output_queue, debug_prints_level)
        
        if(debug_prints_level > 50):
            print(f'for x, y: {x}, {y}; drone_status:{drone_status}')
        
        if(drone_status) == 1:
            break
    
    if(drone_status != 1):
        return 0, 0
    
    x_start = x
    x_stop = x
    if(debug_prints_level > 20):
            print(f'estimated start:{x_start}')
        
    # we have an estimate of starting point, find exact starting point
    for x in range(x_start-1, x_start-x_quanta-1, -1):
        drone_status = get_drone_status(xy_flipped, x, y, input_queue, output_queue, debug_prints_level)
        
        if(debug_prints_level > 50):
            print(f'for x, y: {x}, {y}; drone_status:{drone_status}')
        
        if(drone_status) == 0:
            break
    
    
    x_start = x+1
    if(debug_prints_level > 20):
            print(f'exact start:{x_start}')
    #find stopping point
    for x in range(x_stop+1, x_max):
        drone_status = get_drone_status(xy_flipped, x, y, input_queue, output_queue, debug_prints_level)
        
        if(debug_prints_level > 50):
            print(f'for x, y: {x}, {y}; drone_status:{drone_status}')
        
        if(drone_status) == 0:
            break
        
    x_stop = x-1
    if(debug_prints_level > 20):
            print(f'exact stop:{x_stop}')
        
    return(x_start, x_stop - x_start + 1)

def get_drone_status(xy_flipped, x, y, input_queue, output_queue, debug_prints_level = 0):
    debug_prints_level -= 1
    
    input_queue.clear()
    output_queue.clear()
    
    if(xy_flipped):
        input_queue.append(y)
        input_queue.append(x)
    
    else:
        input_queue.append(x)
        input_queue.append(y)
    
    executor = IntcodeExecutor.IntcodeExecutor(drone_program_sequence.copy(), input_queue, output_queue)

    while(len(output_queue) < 1):
        time.sleep (0.001)

    drone_status = output_queue.popleft()
    executor.thread.join()
    
    if(debug_prints_level > 20):
        print(f'for x, y:{x, y}; drone_status:{drone_status}')
    
    return(drone_status)

def solve_day_19_puzzle_b():
    
    debug_prints_level = 5
    
    height = 20
    width = 200
    
    x_offset = int(1375.625) + 100 - 50
    y_offset = int(1658.625)
    
    solve_day_19_puzzle(x_offset, y_offset, height, width, debug_prints_level)
    
    x_offset = int(1375.625)
    y_offset = int(1658.625) + 100 - 50
    
    solve_day_19_puzzle(x_offset, y_offset, height, width, debug_prints_level)

def solve_day_19_puzzle_b_attempt2(min_width = 100):
    
    debug_prints_level = 51
    
    y_max = 2000
    xy_flipped = False
    
    input_queue = deque()
    output_queue = deque()
    
    drone_status = -1
    closest_x = -1
    closest_y = -1
    for y in range(min_width, y_max, min_width):
        if(debug_prints_level > 20):
            print(f'for y:{y}')
    
        drone_status = -1
        
        x_start = find_starting_x(xy_flipped, y, min_width, input_queue, output_queue, debug_prints_level)
        
        
        x1 = x_start + (min_width-1)
        y1 = y - (min_width-1)
        
        if((x_start < 0) or (y1 < 0)):
            continue
    
        
        drone_status = get_drone_status(xy_flipped, x1, y1, input_queue, output_queue, debug_prints_level)
        if(debug_prints_level > 50):
            print(f'for x, y: {x1}, {y1}; drone_status:{drone_status}')
        
        if(drone_status == 1):
            closest_x = x_start
            closest_y = y - (min_width-1)
            break
            
    if(drone_status) != 1:
        print('Nothing found')
        return
        
    
    # we have an estimate of starting y, find exact y
    y_start = y
    if(debug_prints_level > 20):
            print(f'estimated y:{y_start}')
    for y in range(y_start-1, y_start-min_width-1, -1):
        if(debug_prints_level > 20):
            print(f'for y:{y}')
    
        x_start = find_starting_x(xy_flipped, y, min_width, input_queue, output_queue, debug_prints_level)
        
        
        x1 = x_start + (min_width-1)
        y1 = y - (min_width-1)
        
        if((x_start < 0) or (y1 < 0)):
            break
    
        drone_status = get_drone_status(xy_flipped, x1, y1, input_queue, output_queue, debug_prints_level)
        if(debug_prints_level > 50):
            print(f'for x, y: {x1}, {y1}; drone_status:{drone_status}')
        
        if(drone_status == 0):
            break
            
        closest_x = x_start
        closest_y = y - (min_width-1)
                
    print(f'closest_x, closest_y:{closest_x, closest_y}')
    
    

def find_starting_x(xy_flipped, y, min_width = 100, input_queue = None, output_queue = None, debug_prints_level = 0):
    debug_prints_level -=1
    x_max = 2000
    
    for x in range(min_width, x_max, min_width):
        drone_status = get_drone_status(xy_flipped, x, y, input_queue, output_queue, debug_prints_level)
            
        if(debug_prints_level > 50):
            print(f'for x, y: {x}, {y}; drone_status:{drone_status}')
        
        if(drone_status == 1):
            break
    
    if(drone_status != 1):
        return -1
        
    # we have an estimate of x, find exact x
    x_start = x
    if(debug_prints_level > 20):
            print(f'estimated x:{x_start}')
        
    for x in range(x_start-1, x_start-min_width-1, -1):
        drone_status = get_drone_status(xy_flipped, x, y, input_queue, output_queue, debug_prints_level)
        
        if(debug_prints_level > 50):
            print(f'for x, y: {x}, {y}; drone_status:{drone_status}')
        
        if(drone_status == 0):
            break
    
        
    x_start = x+1
    if(debug_prints_level > 20):
            print(f'exact x:{x_start}')
            
    return(x_start)
    
def check_nearest(width, height, min_width = 100, debug_prints_level = 0):
    debug_prints_level -= 1
    xy_flipped = False
    print("x:")
    x_input = int(input())
    
    print("y:")
    y_input = int(input())
    
    nearest = []
    
    for x in range(x_input, x_input-width, -1):
        for y in range(y_input, y_input-height, -1):
        
            if(check_farthest_corners (x, y, min_width, debug_prints_level)):
                nearest.append(x*10000 + y)
                print("adding x, y:{x, y} to nearest list")
    
    print(nearest)

def check_farthest_corners(x = -1, y = -1, min_width = 100, debug_prints_level = 0):
    debug_prints_level -= 1
    xy_flipped = False
    
    if(x == -1):
        print("x:")
        x = int(input())
        
    if(y == -1):
        print("y:")
        y = int(input())
    
    input_queue = deque()
    output_queue = deque()
    
    x1 = x + (min_width - 1)
    y1 = y + (min_width - 1)
    
    #check x1, y and x, y1
    drone_status = get_drone_status(xy_flipped, x1, y, input_queue, output_queue, debug_prints_level)
    if(drone_status == 1):
        drone_status = get_drone_status(xy_flipped, x, y1, input_queue, output_queue, debug_prints_level)
    
    return(drone_status == 1)

def solve_day_19_puzzle_main():

    debug_prints_level = 50
    choice = ""
    min_width = 100
    while(choice != "0"):
        print("1: Puzzle b\n2: Get drone status at x, y\n3: Check for nearest in 20 X 20 grid")
        print(f'4. Check farthest corners for x,y\n5. Change min width. Current:{min_width}\n0. Quit')
        choice = input()
        
        if(choice == "1"):
            solve_day_19_puzzle_b_attempt2(min_width)
        elif(choice == "2"):
            executor = IntcodeExecutor.IntcodeExecutor(drone_program_sequence.copy(), None, None)
            executor.thread.join()
        elif(choice == "3"):
            check_nearest(20, 20, min_width, debug_prints_level)
        elif(choice == "4"):
            if(check_farthest_corners(-1, -1, min_width, debug_prints_level)):
                print("Checks out")
            else:
                print("doesnt check out")
        elif(choice == "5"):
            min_width = int(input())
        

def _unit_tests():

    input_queue = deque()
    output_queue = deque()
    
    xy_flipped = False
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    y = 12
    expected_answer = 2
    x_earliest, actual_answer = get_count_in_row(xy_flipped, y, input_queue, output_queue, 1000, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    y = 841
    expected_answer = 99
    x_earliest, actual_answer = get_count_in_row(xy_flipped, y, input_queue, output_queue, 1000, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    y = 842
    expected_answer = 100
    x_earliest, actual_answer = get_count_in_row(xy_flipped, y, input_queue, output_queue, 1000, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    min_width = 100
    expected_answer = 842
    x_earliest, actual_answer = find_earliest_row_given_width(xy_flipped, input_queue, output_queue, 1000, 1000, min_width, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    print(f'x_earliest, y_earliest, width:{x_earliest, actual_answer, min_width}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    xy_flipped = True
    y = 17
    expected_answer = 3
    x_earliest, actual_answer = get_count_in_row(xy_flipped, y, input_queue, output_queue, 1000, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    y = 658
    expected_answer = 99
    x_earliest, actual_answer = get_count_in_row(xy_flipped, y, input_queue, output_queue, 1000, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    y = 659
    expected_answer = 100
    x_earliest, actual_answer = get_count_in_row(xy_flipped, y, input_queue, output_queue, 1000, 0)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    
    print(f'Executing unit test at line#:{currentframe().f_lineno}')
    min_width = 100
    expected_answer = 659
    x_earliest, actual_answer = find_earliest_row_given_width(xy_flipped, input_queue, output_queue, 2000, 2000, min_width, 20)
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')
    print(f'x_earliest, y_earliest, height:{actual_answer, x_earliest, min_width}')
    


drone_program_sequence = [109,424,203,1,21101,11,0,0,1105,1,282,21102,18,1,0,1105,1,259,1201,1,0,221,203,1,21102,1,31,0,1105,1,282,21101,38,0,0,1105,1,259,20102,1,23,2,21202,1,1,3,21102,1,1,1,21101,0,57,0,1106,0,303,1201,1,0,222,21001,221,0,3,21002,221,1,2,21101,0,259,1,21102,80,1,0,1106,0,225,21102,1,93,2,21101,0,91,0,1105,1,303,2102,1,1,223,21002,222,1,4,21101,0,259,3,21102,225,1,2,21101,0,225,1,21102,1,118,0,1105,1,225,21001,222,0,3,21101,0,73,2,21101,133,0,0,1105,1,303,21202,1,-1,1,22001,223,1,1,21101,148,0,0,1106,0,259,2102,1,1,223,20101,0,221,4,21001,222,0,3,21102,1,11,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,195,1,0,105,1,109,20207,1,223,2,21002,23,1,1,21101,-1,0,3,21101,214,0,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,22101,0,-3,1,22101,0,-2,2,21201,-1,0,3,21101,250,0,0,1106,0,225,22101,0,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2105,1,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22101,0,-2,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21202,-2,1,3,21102,1,343,0,1106,0,303,1106,0,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21102,1,384,0,1105,1,303,1105,1,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21202,1,1,-4,109,-5,2105,1,0]

# test_intcode_module()
debug_prints_level = 10
# solve_day_19_puzzle(0, 0, 25, 25, debug_prints_level)
# _unit_tests()
# solve_day_19_puzzle_b()
solve_day_19_puzzle_main()
