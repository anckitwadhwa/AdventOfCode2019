from collections import deque
import itertools
import threading
import time

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


def solve_day7_puzzle (instruction_sequence, range_of_phase_values, debug_prints = False):

    number_of_amps = len(range_of_phase_values)
    possible_amp_phase_values = list(itertools.permutations(range_of_phase_values))
    amp_input_value = 0

    input_queue = [deque() for amp_number in range (0, number_of_amps)]
    output_queue = [None] * number_of_amps

    best_phase_combination = []
    max_value = float("-inf")

    for phase_values in possible_amp_phase_values:
        if(debug_prints):
            print("phase_values this iteration: ", phase_values)
            print("Active Threads: ", threading.active_count())

        amp_input_value = 0
        sequence = [instruction_sequence.copy() for amp_number in range (0, number_of_amps)]

        #setup queues and instruction sequences
        for amp_number in range (0, number_of_amps):

            input_queue[amp_number].append(phase_values[amp_number])
            #output of amp A is input for amp B
            output_queue[amp_number] = input_queue [(amp_number + 1) % number_of_amps]

        #for first amp, setup initial signal
        input_queue[0].append(amp_input_value)


        #setup threads
        threads = []
        for amp_number in range (0, number_of_amps):

            thread = threading.Thread(target=run_instructions, args=(sequence[amp_number], input_queue[amp_number], output_queue[amp_number], debug_prints))
            threads.append(thread)

        #start threads, reverse order just for fun
        for amp_number in range (number_of_amps - 1, -1, -1):
            threads[amp_number].start()


        #wait for thread completion
        for amp_number in range (0, number_of_amps):
            threads[amp_number].join()

        #output queue of final amp has the final signal value
        if (debug_prints):
            print(output_queue[-1])

        amp_input_value = output_queue[-1].popleft()

        if (amp_input_value > max_value):
            max_value = amp_input_value
            best_phase_combination = phase_values

    print (best_phase_combination)
    print (max_value)

PuzzleInputSequence = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,1,1021,1101,28,0,1010,1101,36,0,1002,1101,0,39,1014,1101,34,0,1018,1101,0,32,1001,1102,22,1,1017,1102,1,26,1000,1102,1,27,1013,1101,829,0,1022,1102,29,1,1005,1102,1,681,1024,1102,1,510,1029,1101,0,676,1025,1101,31,0,1016,1101,0,716,1027,1101,0,38,1019,1102,21,1,1009,1102,1,0,1020,1102,1,33,1012,1102,1,723,1026,1101,826,0,1023,1101,0,23,1003,1101,0,37,1008,1101,35,0,1007,1102,24,1,1015,1101,25,0,1011,1101,0,30,1004,1101,20,0,1006,1102,519,1,1028,109,19,21102,40,1,-4,1008,1015,40,63,1005,63,203,4,187,1106,0,207,1001,64,1,64,1002,64,2,64,109,-12,21108,41,41,8,1005,1015,229,4,213,1001,64,1,64,1105,1,229,1002,64,2,64,109,6,21107,42,43,4,1005,1017,247,4,235,1105,1,251,1001,64,1,64,1002,64,2,64,109,-8,1201,2,0,63,1008,63,37,63,1005,63,271,1105,1,277,4,257,1001,64,1,64,1002,64,2,64,109,-4,2102,1,0,63,1008,63,32,63,1005,63,299,4,283,1105,1,303,1001,64,1,64,1002,64,2,64,109,2,1208,2,29,63,1005,63,325,4,309,1001,64,1,64,1106,0,325,1002,64,2,64,109,18,1206,0,341,1001,64,1,64,1106,0,343,4,331,1002,64,2,64,109,-19,2101,0,4,63,1008,63,20,63,1005,63,365,4,349,1105,1,369,1001,64,1,64,1002,64,2,64,109,10,1207,-4,38,63,1005,63,391,4,375,1001,64,1,64,1106,0,391,1002,64,2,64,109,-5,21107,43,42,5,1005,1012,407,1106,0,413,4,397,1001,64,1,64,1002,64,2,64,109,1,2102,1,-2,63,1008,63,19,63,1005,63,433,1106,0,439,4,419,1001,64,1,64,1002,64,2,64,109,12,1205,0,455,1001,64,1,64,1105,1,457,4,445,1002,64,2,64,109,-9,1206,9,475,4,463,1001,64,1,64,1105,1,475,1002,64,2,64,109,7,21102,44,1,1,1008,1019,43,63,1005,63,495,1106,0,501,4,481,1001,64,1,64,1002,64,2,64,109,11,2106,0,-1,4,507,1001,64,1,64,1106,0,519,1002,64,2,64,109,-27,21101,45,0,9,1008,1011,47,63,1005,63,543,1001,64,1,64,1106,0,545,4,525,1002,64,2,64,109,-7,1202,5,1,63,1008,63,25,63,1005,63,569,1001,64,1,64,1105,1,571,4,551,1002,64,2,64,109,15,2107,22,-1,63,1005,63,591,1001,64,1,64,1105,1,593,4,577,1002,64,2,64,109,4,2108,33,-7,63,1005,63,609,1105,1,615,4,599,1001,64,1,64,1002,64,2,64,109,2,21101,46,0,0,1008,1016,46,63,1005,63,637,4,621,1106,0,641,1001,64,1,64,1002,64,2,64,109,-6,2101,0,-2,63,1008,63,40,63,1005,63,661,1106,0,667,4,647,1001,64,1,64,1002,64,2,64,109,14,2105,1,0,4,673,1105,1,685,1001,64,1,64,1002,64,2,64,109,-16,1207,-5,22,63,1005,63,701,1106,0,707,4,691,1001,64,1,64,1002,64,2,64,109,15,2106,0,4,1001,64,1,64,1105,1,725,4,713,1002,64,2,64,109,-21,1202,3,1,63,1008,63,29,63,1005,63,751,4,731,1001,64,1,64,1106,0,751,1002,64,2,64,109,7,1201,-5,0,63,1008,63,30,63,1005,63,773,4,757,1105,1,777,1001,64,1,64,1002,64,2,64,109,-10,2107,25,1,63,1005,63,799,4,783,1001,64,1,64,1105,1,799,1002,64,2,64,109,15,1205,7,817,4,805,1001,64,1,64,1106,0,817,1002,64,2,64,109,6,2105,1,3,1106,0,835,4,823,1001,64,1,64,1002,64,2,64,109,-16,21108,47,45,8,1005,1012,851,1106,0,857,4,841,1001,64,1,64,1002,64,2,64,109,1,1208,4,18,63,1005,63,877,1001,64,1,64,1106,0,879,4,863,1002,64,2,64,109,-1,2108,21,5,63,1005,63,901,4,885,1001,64,1,64,1106,0,901,4,64,99,21101,27,0,1,21101,915,0,0,1105,1,922,21201,1,37229,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,942,0,0,1105,1,922,21201,1,0,-1,21201,-2,-3,1,21101,0,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22101,0,-2,-2,109,-3,2105,1,0]

PuzzleTestSqeuence = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
PuzzleTestSqeuence2 = [1102,34915192,34915192,7,4,7,99,0]
PuzzleTestSqeuence3 = [104,1125899906842624,99]
PuzzleTestSqeuence4 = [1,9,10,3,2,3,11,0,99,30,40,50]

# AlarmCodeSequence = PuzzleInputSequence.copy()
# AlarmCodeSequence[1] = 12
# AlarmCodeSequence[2] = 2

#CopyOfSequenceToRun = AlarmCodeSequence.copy()
#InstructionsAttempted = run_instructions (CopyOfSequenceToRun)

#print ("InstructionsAttempted: ", InstructionsAttempted)
#print ("result in postion 0: ", CopyOfSequenceToRun[0])

#get_modes_and_opcode (11002)
#get_modes_and_opcode (1002)
#get_modes_and_opcode (1101)


#run_instructions(PuzzleInputSequence.copy(), None, None, True)

# range_of_phase_values = range(0, 5)
# range_of_phase_values = range(5, 10)

#solve_day7_puzzle (PuzzleInputSequence.copy(), range_of_phase_values, True)


print("*" * 50)
run_instructions(PuzzleInputSequence, None, None, False)

# print(PuzzleInputSequence[0:50])