from collections import deque
from inspect import currentframe
import threading
import time

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __hash__(self):
        return(hash((self.x, self.y)))

    def __str__(self):
        return(str(self.x) + "," + str(self.y))

    def __eq__(self, other):
        if isinstance(other, Point):
            return((self.x == other.x) and (self.y == other.y))

        return False


class Location:
    possible_directions = ["up", "left", "down", "right"]

    def __init__(self, coordinates = Point(), head_direction = "up"):

        self.coordinates = coordinates
        self.head_direction = head_direction

    def __str__(self):
        return("coordinates:" + str(self.coordinates) + ", head_direction:" + self.head_direction)

    def __hash__(self):
        return(hash((self.coordinates, self.head_direction)))

    def __eq__(self, other):
        if isinstance(other, Location):
            return((self.coordinates == other.coordinates) and (self.head_direction == other.head_direction))

        return False

    def move_1_step(self):
        if(self.head_direction == "up"):
            self.coordinates.y -= 1

        elif(self.head_direction == "left"):
            self.coordinates.x -= 1

        elif(self.head_direction == "down"):
            self.coordinates.y += 1

        elif(self.head_direction == "right"):
            self.coordinates.x += 1

        else:
            print("bad direction, ignored.")

    def update(self, turn, debug_prints = False):
        current_direction_index = self.possible_directions.index(self.head_direction)

        # 0 == left turn
        if(turn == 0):
            new_direction_index = (current_direction_index + 1) % len(self.possible_directions)

        # 1 == right turn
        elif(turn == 1):
            new_direction_index = (current_direction_index - 1) % len(self.possible_directions)

        else:
            print("bad turn, ignored")
            return

        self.head_direction = self.possible_directions[new_direction_index]

        self.move_1_step()



def get_modes_and_opcode (Number):
    Opcode = Number % 100

    AllModes = int (Number / 100)
    Modes = []

    while (AllModes > 0):
        #print (AllModes)
        Mode = int (AllModes % 10)
        #print (Mode)
        if (Mode > 2):
            print ("Unknown Mode: ", Mode, "Full parameter mode:", int(Number / 100))
            break

        Modes.append(Mode)
        AllModes = int(AllModes / 10)

    #print ("Number, Opcode, Modes: ", Number, Opcode, Modes)
    return Opcode, Modes

def get_operand (ParameterNumber, Modes, InstructionSequence, InstructionPointer, RelativeBase):
    Operand = 0
    Mode = 0

    if (ParameterNumber <= 0):
        print ("Bad Operand Number (must be <=0):", ParameterNumber)
        return (Operand)

    elif (ParameterNumber <= len (Modes)):
        Mode = Modes [ParameterNumber - 1]

    if (Mode == 0):
        Operand = InstructionSequence[InstructionSequence[InstructionPointer + ParameterNumber]]

    elif (Mode == 1):
        Operand = InstructionSequence[InstructionPointer + ParameterNumber]

    elif (Mode == 2):
        Operand = InstructionSequence[InstructionSequence[InstructionPointer + ParameterNumber] + RelativeBase]

    else:
        print ("Unknown Mode: ", Mode)

    return (Operand)

def get_result_position(ParameterNumber, Modes, InstructionSequence, InstructionPointer, RelativeBase):
    Mode = 0
    ResultPosition = InstructionSequence[InstructionPointer + ParameterNumber]

    if (ParameterNumber <= 0):
        print ("Bad Operand Number (must be <=0):", ParameterNumber)

    elif (ParameterNumber <= len (Modes)):
        Mode = Modes [ParameterNumber - 1]


    if (Mode == 2):
        ResultPosition += RelativeBase

    return(ResultPosition)


def run_instructions (InstructionSequence, input_queue = None, output_queue = None, debug_prints = False):

    InstructionSequenceLength = len(InstructionSequence)

    #add 10,000 space for more memory
    InstructionSequence.extend([0] * 10000)

    InstructionSequenceLength = len(InstructionSequence)
    InstructionPointer = 0
    InstructionsAttempted = 0
    InstructionSize = 0

    RelativeBase = 0
    while InstructionPointer < InstructionSequenceLength:
        OpCode, Modes = get_modes_and_opcode (InstructionSequence[InstructionPointer])
        if (debug_prints):
            print ("InstructionPointer, Modes, OpCode, RelativeBase: ", InstructionPointer, Modes, OpCode, RelativeBase)

        InstructionsAttempted += 1;
        Result = 0
        ResultPosition = 0

        if OpCode == 99:
            InstructionSize = 1

            if (output_queue != None):
                output_queue.append(99)

            if (debug_prints):
                print ("Halt")
            break


        elif OpCode == 1: #Add
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            ResultPosition = get_result_position(3, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            Result = Operand1 + Operand2
            InstructionSequence[ResultPosition] = Result
            if (debug_prints):
                print ("Add.", Operand1, "+", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])


        elif OpCode == 2: #Multiply
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            ResultPosition = get_result_position(3, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            Result = Operand1 * Operand2
            InstructionSequence[ResultPosition] = Result
            if (debug_prints):
                print ("Multiply.", Operand1, "*", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

        elif OpCode == 3: #Get Input
            InstructionSize = 2
            ResultPosition = get_result_position(1, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            if (input_queue != None):

                #wait for element to be added to the queue
                while (len(input_queue) < 1):
                    if (debug_prints):
                        print ("Sleeping in :", threading.current_thread())

                    time.sleep (0.01)

                UserInput = input_queue.popleft()
            else:
                UserInput = input ("Enter Input:")

            # if (debug_prints):
            #     print("InstructionPointer for opcode == 3, UserInput", InstructionPointer, UserInput)

            InstructionSequence[ResultPosition] = int(UserInput)

        elif OpCode == 4: #Output
            InstructionSize = 2

            Operand1 = get_operand(1, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            # if (debug_prints):
            #     print ("InstructionPointer for opcode == 4: ", InstructionPointer)


            if (output_queue != None):
                output_queue.append(Operand1)

            else:
                print(Operand1)


        elif OpCode == 5: #jump-if-true
            InstructionSize = 3

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            if (Operand1 != 0):
                InstructionPointer = Operand2
                #hack since Instruction pointer is already updated
                InstructionSize = 0

        elif OpCode == 6: #jump-if-false
            InstructionSize = 3

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            if (Operand1 == 0):
                InstructionPointer = Operand2

                #hack since Instruction pointer is already updated
                InstructionSize = 0

        elif OpCode == 7: #less than
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            ResultPosition = get_result_position(3, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            if (Operand1 < Operand2):
                Result = 1
            else:
                Result = 0

            InstructionSequence[ResultPosition] = Result
            #print ("Less Than.", Operand1, "<", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

        elif OpCode == 8: #equals
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            ResultPosition = get_result_position(3, Modes, InstructionSequence, InstructionPointer, RelativeBase)

            if (Operand1 == Operand2):
                Result = 1
            else:
                Result = 0

            InstructionSequence[ResultPosition] = Result
            #print ("Equals.", Operand1, "==", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

        elif OpCode == 9: #update relative base
            InstructionSize = 2

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer, RelativeBase)
            RelativeBase += Operand1
            if (debug_prints):
                print("Update relative base to: ", RelativeBase)


        else:
            print ("Unknown Opcode: ", OpCode, "\nExiting")
            break

        InstructionPointer += InstructionSize

        #print ("Operand1, Operand2, ResultPosition, Result:", Operand1, Operand2, ResultPosition, InstructionSequence[ResultPosition])
        #print(InstructionSequence)

    return InstructionsAttempted
# end run_instructions


def run_instructions_in_thread(instruction_sequence, input_queue, output_queue, debug_prints = False):
    thread = threading.Thread(target=run_instructions, args=(instruction_sequence, input_queue, output_queue, debug_prints))

    thread.start()
    return(thread)


def perform_io(input_queue, output_queue, hull_state, location, debug_prints = False):
    halted = False
    all_coordinates = set()

    while (halted != True):

        while(len(output_queue) < 1):
            time.sleep(0.01)

        color_to_paint = output_queue.popleft()

        if (color_to_paint == 99):
            halted = True
            continue


        while(len(output_queue) < 1):
            time.sleep(0.01)

        next_turn = output_queue.popleft()

        if (next_turn == 99):
            halted = True
            continue

        all_coordinates.add(location.coordinates)
        update_hull_state(hull_state, location.coordinates, color_to_paint, False)
        location.update(next_turn, debug_prints)


        panel_color = get_color_at_location(hull_state, location.coordinates, debug_prints)
        input_queue.append(panel_color)

        if(debug_prints):
            print(f'color_to_paint:{color_to_paint}, next_turn:{next_turn}, panel_color:{panel_color}')

    print(len(all_coordinates))
    with open("Day11_output.txt", "w") as f:
        for row in hull_state:
            string = ""
            for number in row:
                if(number == 0):
                    string += " "
                else:
                    string += "1"
            f.write(string + "\n")






def update_hull_state(hull_state, coordinates, new_color, debug_prints = False):

    hull_state[coordinates.y][coordinates.x] = new_color


def get_color_at_location(hull_state, coordinates, debug_prints = False):

    color = hull_state[coordinates.y][coordinates.x]
    return (color)


def run_io_thread(input_queue, output_queue, hull_state, location, debug_prints = False):
    thread = threading.Thread(target=perform_io, args=(input_queue, output_queue, hull_state, location, debug_prints))
    thread.start()
    return(thread)



def solve_day_11_puzzle(instruction_sequence, debug_prints = False):

    #assume a 1000 X 1000 hul
    hull_width = 700
    hull_height = 700
    hull_state = [None] * hull_height
    for j in range(len(hull_state)):
        hull_state[j] = [0] * hull_width

    robot_location = Location(Point(500, 500), "up")

    # print(hull_state)
    # print(robot_location)

    input_queue = deque()
    output_queue = deque()
    input_queue.append(1)

    instruction_thread = run_instructions_in_thread(instruction_sequence, input_queue, output_queue, False)
    io_thread = run_io_thread(input_queue, output_queue, hull_state, robot_location, debug_prints)

    instruction_thread.join()
    io_thread.join()


def unit_tests():
    left_turn = 0
    right_turn = 1

    location = Location(Point(0, 0), "up")
    location.update(left_turn)

    if(location != Location(Point(-1, 0), "left")):
        print("Unit test failed", currentframe().f_lineno)
        print(location)


    location.update(right_turn)

    if(location != Location(Point(-1, -1), "up")):
        print("Unit test failed", currentframe().f_lineno)
        print(location)


PuzzleInputSequence = [3,8,1005,8,311,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,29,1006,0,98,2,1005,8,10,1,1107,11,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,62,1006,0,27,2,1002,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,90,1,1006,1,10,2,1,20,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,121,1,1003,5,10,1,1003,12,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,151,1006,0,17,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,175,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,197,2,6,14,10,1006,0,92,1006,0,4,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,229,1006,0,21,2,102,17,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,259,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,280,1006,0,58,1006,0,21,2,6,11,10,101,1,9,9,1007,9,948,10,1005,10,15,99,109,633,104,0,104,1,21101,937150919572,0,1,21102,328,1,0,1105,1,432,21101,0,387394675496,1,21102,1,339,0,1106,0,432,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,46325083283,1,1,21102,1,386,0,1106,0,432,21101,0,179519401051,1,21102,397,1,0,1106,0,432,3,10,104,0,104,0,3,10,104,0,104,0,21102,1,868410348308,1,21102,1,420,0,1105,1,432,21102,718086501140,1,1,21102,1,431,0,1105,1,432,99,109,2,22101,0,-1,1,21101,40,0,2,21101,0,463,3,21101,453,0,0,1106,0,496,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,458,459,474,4,0,1001,458,1,458,108,4,458,10,1006,10,490,1101,0,0,458,109,-2,2105,1,0,0,109,4,2102,1,-1,495,1207,-3,0,10,1006,10,513,21102,0,1,-3,22102,1,-3,1,22102,1,-2,2,21102,1,1,3,21102,1,532,0,1105,1,537,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,560,2207,-4,-2,10,1006,10,560,22101,0,-4,-4,1105,1,628,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,1,579,0,1105,1,537,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,598,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,620,22102,1,-1,1,21102,1,620,0,105,1,495,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

print("*" * 50)
# unit_tests()
solve_day_11_puzzle(PuzzleInputSequence, False)
# run_instructions(PuzzleInputSequence, None, None, False)
