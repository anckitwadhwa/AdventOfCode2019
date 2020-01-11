from collections import deque
import IntcodeExecutor
import Point
import time
from inspect import currentframe


def get_ASCII_input(debug_prints_level = 0):
    debug_prints_level -= 1

    output_queue = deque()
    executor = IntcodeExecutor.IntcodeExecutor(ascii_code_sequence.copy(), None, output_queue, IntcodeExecutor.ASCIIInterpretor(), False)
    
    executor.thread.join()
    
    n = len(output_queue)
    character_list = [""] * (n - 1)
    
    
    for index in range(n):
        output = output_queue.popleft()
        
        if(output == 99):
            break
        
        character_list[index] = output

    return_val = "".join(character_list)
    if(debug_prints_level > 20):
    
        print(return_val)
        
    return(return_val)  


def get_overlap_points(input_str, symbol = "#", debug_prints_level = 0):
    debug_prints_level -= 1
    overlap_points = []
    if(debug_prints_level > 50):
        print(f'input_str:\n{input_str}')
    
    
    input_lines = input_str.splitlines()
    #remove empty last line
    if(input_lines[-1] == ""):
        input_lines = input_lines[:-1]
    
    
    if(debug_prints_level > 90):
        print(f'input_lines:{input_lines}')
    
    
    N = len(input_lines)
    # there are no overlaps in 0th or last lines
    
    for row_num in range(1, N-1):
        line = input_lines[row_num]
    
        #intersection is only possible on when at least 2 symbols occur consecutively, and only on the 2nd symbol
        n = line.count(symbol*2)
        
        if(debug_prints_level > 90):
            print(f'(for row_num: {row_num}; n:{n}')
        
        
        last_col = -2
        for j in range(n):
            col_num = line.find(symbol*2, last_col+2)
            last_col = col_num
        
            if(is_intersection(input_lines, row_num, col_num)):
                overlap_points.append(Point.Point(col_num, row_num))
                
                if(debug_prints_level > 50):
                    print(f'row_num:{row_num}, col_num:{col_num} checks out')
            else:
                if(debug_prints_level > 50):
                    print(f'row_num:{row_num}, col_num:{col_num} doesnt check out')
            
                
                
    if(debug_prints_level > 50):
        print_str =""
        for point in overlap_points:
            print_str += str(point)+";"
        print(print_str)

    return(overlap_points)

def compute_alignment_parameter(points, debug_prints_level = 0):
    debug_prints_level -= 1
    
    alignment_parameter_sum = 0
    for point in points:
        alignment_parameter_sum += (point.x * point.y)
    
    print(alignment_parameter_sum)

def is_intersection(input_lines, row_num, col_num, symbol = "#", debug_prints_level = 0):

    #assume symbol is already present on the left of row_num, col_num
    line_above = input_lines[row_num-1]
    line_below = input_lines[row_num+1]
    line_at = input_lines[row_num]
    
    character_above = line_above[col_num]
    character_below = line_below[col_num]
    character_right = line_at[col_num+1]
    
    return((character_above == symbol) and (character_below == symbol) and (character_right == symbol))

def solve_day17_puzzle(debug_prints_level = 0):
    debug_prints_level -= 1
    
    input_str = get_ASCII_input(0)
    overlap_points = get_overlap_points(input_str, "#", 55)
    compute_alignment_parameter(overlap_points, debug_prints_level)
    
def solve_day17_puzzle_b(debug_prints_level = 0):
    debug_prints_level -= 1
    
    # input_str = input_to_ASCII("Input: ")
    # print(input_str)
    # print(ASCII_to_output(input_str))

    code_sequence = ascii_code_sequence.copy()
    code_sequence[0] = 2
    
    input_queue = deque()
    prepare_input_queue(input_queue, debug_prints_level)
    
    executor = IntcodeExecutor.IntcodeExecutor(code_sequence, input_queue, None, IntcodeExecutor.ASCIIInterpretor(), False)
    # executor = IntcodeExecutor.IntcodeExecutor(code_sequence, None, None, None, False)
    
    
def prepare_input_queue(input_queue, debug_prints_level = 0):
    debug_prints_level -= 1
    
    main_routine = "C,C,A,B,A,B,A,B,A,C\n"

    routine_A = "R,6,R,10,R,12,R,6\n"
    routine_B = "R,10,L,12,L,12\n"
    routine_C = "R,10,L,12,R,6\n"
    
    continuous_feed = input("Continuous Feed:? y/n?") + "\n"
    
    all_inputs = main_routine + routine_A + routine_B + routine_C + continuous_feed


    for index in range(len(all_inputs)):
        input_queue.append(all_inputs[index])

ascii_code_sequence = [1,330,331,332,109,3160,1102,1,1182,16,1101,0,1477,24,102,1,0,570,1006,570,36,102,1,571,0,1001,570,-1,570,1001,24,1,24,1106,0,18,1008,571,0,571,1001,16,1,16,1008,16,1477,570,1006,570,14,21101,58,0,0,1105,1,786,1006,332,62,99,21101,0,333,1,21102,73,1,0,1105,1,579,1102,0,1,572,1102,1,0,573,3,574,101,1,573,573,1007,574,65,570,1005,570,151,107,67,574,570,1005,570,151,1001,574,-64,574,1002,574,-1,574,1001,572,1,572,1007,572,11,570,1006,570,165,101,1182,572,127,1002,574,1,0,3,574,101,1,573,573,1008,574,10,570,1005,570,189,1008,574,44,570,1006,570,158,1105,1,81,21101,0,340,1,1105,1,177,21102,477,1,1,1106,0,177,21101,514,0,1,21102,176,1,0,1106,0,579,99,21101,0,184,0,1105,1,579,4,574,104,10,99,1007,573,22,570,1006,570,165,1001,572,0,1182,21101,375,0,1,21102,1,211,0,1105,1,579,21101,1182,11,1,21101,222,0,0,1106,0,979,21102,1,388,1,21102,233,1,0,1105,1,579,21101,1182,22,1,21101,0,244,0,1105,1,979,21101,0,401,1,21102,1,255,0,1106,0,579,21101,1182,33,1,21102,1,266,0,1106,0,979,21102,414,1,1,21102,1,277,0,1105,1,579,3,575,1008,575,89,570,1008,575,121,575,1,575,570,575,3,574,1008,574,10,570,1006,570,291,104,10,21102,1182,1,1,21102,313,1,0,1105,1,622,1005,575,327,1101,1,0,575,21101,327,0,0,1105,1,786,4,438,99,0,1,1,6,77,97,105,110,58,10,33,10,69,120,112,101,99,116,101,100,32,102,117,110,99,116,105,111,110,32,110,97,109,101,32,98,117,116,32,103,111,116,58,32,0,12,70,117,110,99,116,105,111,110,32,65,58,10,12,70,117,110,99,116,105,111,110,32,66,58,10,12,70,117,110,99,116,105,111,110,32,67,58,10,23,67,111,110,116,105,110,117,111,117,115,32,118,105,100,101,111,32,102,101,101,100,63,10,0,37,10,69,120,112,101,99,116,101,100,32,82,44,32,76,44,32,111,114,32,100,105,115,116,97,110,99,101,32,98,117,116,32,103,111,116,58,32,36,10,69,120,112,101,99,116,101,100,32,99,111,109,109,97,32,111,114,32,110,101,119,108,105,110,101,32,98,117,116,32,103,111,116,58,32,43,10,68,101,102,105,110,105,116,105,111,110,115,32,109,97,121,32,98,101,32,97,116,32,109,111,115,116,32,50,48,32,99,104,97,114,97,99,116,101,114,115,33,10,94,62,118,60,0,1,0,-1,-1,0,1,0,0,0,0,0,0,1,0,14,0,109,4,1202,-3,1,586,21001,0,0,-1,22101,1,-3,-3,21101,0,0,-2,2208,-2,-1,570,1005,570,617,2201,-3,-2,609,4,0,21201,-2,1,-2,1106,0,597,109,-4,2106,0,0,109,5,2101,0,-4,630,20102,1,0,-2,22101,1,-4,-4,21102,1,0,-3,2208,-3,-2,570,1005,570,781,2201,-4,-3,652,21002,0,1,-1,1208,-1,-4,570,1005,570,709,1208,-1,-5,570,1005,570,734,1207,-1,0,570,1005,570,759,1206,-1,774,1001,578,562,684,1,0,576,576,1001,578,566,692,1,0,577,577,21102,1,702,0,1106,0,786,21201,-1,-1,-1,1106,0,676,1001,578,1,578,1008,578,4,570,1006,570,724,1001,578,-4,578,21102,731,1,0,1105,1,786,1105,1,774,1001,578,-1,578,1008,578,-1,570,1006,570,749,1001,578,4,578,21101,756,0,0,1105,1,786,1105,1,774,21202,-1,-11,1,22101,1182,1,1,21101,0,774,0,1105,1,622,21201,-3,1,-3,1105,1,640,109,-5,2105,1,0,109,7,1005,575,802,21002,576,1,-6,20101,0,577,-5,1105,1,814,21101,0,0,-1,21101,0,0,-5,21101,0,0,-6,20208,-6,576,-2,208,-5,577,570,22002,570,-2,-2,21202,-5,51,-3,22201,-6,-3,-3,22101,1477,-3,-3,2101,0,-3,843,1005,0,863,21202,-2,42,-4,22101,46,-4,-4,1206,-2,924,21102,1,1,-1,1105,1,924,1205,-2,873,21101,0,35,-4,1106,0,924,1201,-3,0,878,1008,0,1,570,1006,570,916,1001,374,1,374,1201,-3,0,895,1101,2,0,0,1202,-3,1,902,1001,438,0,438,2202,-6,-5,570,1,570,374,570,1,570,438,438,1001,578,558,922,20101,0,0,-4,1006,575,959,204,-4,22101,1,-6,-6,1208,-6,51,570,1006,570,814,104,10,22101,1,-5,-5,1208,-5,33,570,1006,570,810,104,10,1206,-1,974,99,1206,-1,974,1102,1,1,575,21101,973,0,0,1105,1,786,99,109,-7,2106,0,0,109,6,21102,0,1,-4,21102,1,0,-3,203,-2,22101,1,-3,-3,21208,-2,82,-1,1205,-1,1030,21208,-2,76,-1,1205,-1,1037,21207,-2,48,-1,1205,-1,1124,22107,57,-2,-1,1205,-1,1124,21201,-2,-48,-2,1106,0,1041,21101,-4,0,-2,1105,1,1041,21101,0,-5,-2,21201,-4,1,-4,21207,-4,11,-1,1206,-1,1138,2201,-5,-4,1059,2101,0,-2,0,203,-2,22101,1,-3,-3,21207,-2,48,-1,1205,-1,1107,22107,57,-2,-1,1205,-1,1107,21201,-2,-48,-2,2201,-5,-4,1090,20102,10,0,-1,22201,-2,-1,-2,2201,-5,-4,1103,1201,-2,0,0,1106,0,1060,21208,-2,10,-1,1205,-1,1162,21208,-2,44,-1,1206,-1,1131,1105,1,989,21102,1,439,1,1105,1,1150,21102,477,1,1,1105,1,1150,21101,514,0,1,21101,0,1149,0,1106,0,579,99,21102,1157,1,0,1105,1,579,204,-2,104,10,99,21207,-3,22,-1,1206,-1,1138,1202,-5,1,1176,2102,1,-4,0,109,-6,2106,0,0,28,1,50,1,32,7,11,1,32,1,5,1,11,1,32,1,5,1,11,1,7,11,14,1,5,1,11,1,7,1,9,1,14,1,5,1,11,13,5,1,14,1,5,1,19,1,3,1,5,1,14,1,5,1,5,13,1,1,3,1,5,1,14,1,5,1,5,1,11,1,1,1,3,1,5,1,14,1,5,1,5,1,11,1,1,13,12,1,5,1,5,1,11,1,5,1,5,1,1,1,12,1,5,13,5,1,5,1,5,1,1,1,12,1,11,1,5,1,5,1,5,1,5,1,1,1,2,11,11,1,1,11,5,1,5,1,1,1,24,1,1,1,3,1,11,1,5,1,1,1,24,1,1,1,3,1,11,7,1,1,24,1,1,1,3,1,19,1,24,7,15,7,24,1,19,1,3,1,1,1,24,1,1,7,11,1,3,1,1,1,24,1,1,1,5,1,11,1,3,1,1,1,24,1,1,1,5,1,5,11,1,1,24,1,1,1,5,1,5,1,5,1,5,1,24,1,1,1,5,1,5,1,5,1,5,1,24,1,1,1,5,1,5,1,5,1,5,1,24,13,1,1,5,1,5,1,26,1,5,1,3,1,1,1,5,1,5,1,26,1,5,1,3,1,1,13,26,1,5,1,3,1,7,1,32,1,5,13,32,1,9,1,40,11,14]

debug_prints_level = 100
# solve_day17_puzzle(debug_prints_level)
solve_day17_puzzle_b(debug_prints_level)