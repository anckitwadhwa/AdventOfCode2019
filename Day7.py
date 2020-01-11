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
        if (Mode > 1):
            print ("Unknown Mode: ", Mode, "Full parameter mode:", int(Number / 100))
            break

        Modes.append(Mode)
        AllModes = int(AllModes / 10)

    print ("Number, Opcode, Modes: ", Number, Opcode, Modes)
    return Opcode, Modes

def get_operand (OperandNumber, Modes, InstructionSequence, InstructionPointer):
    Operand = 0
    Mode = 0

    if (OperandNumber <= 0):
        print ("Bad Operand Number (must be <=0):", OperandNumber)
        return (Operand)

    elif (OperandNumber <= len (Modes)):
        Mode = Modes [OperandNumber - 1]

    if (Mode == 0):
        Operand = InstructionSequence[InstructionSequence[InstructionPointer + OperandNumber]]

    elif (Mode == 1):
        Operand = InstructionSequence[InstructionPointer + OperandNumber]

    else:
        print ("Unknown Mode: ", Mode)

    return (Operand)


def run_instructions (InstructionSequence, input_queue = None, output_queue = None, debug_prints = False):

    InstructionSequenceLength = len(InstructionSequence)

    InstructionPointer = 0
    InstructionsAttempted = 0
    InstructionSize = 0
    while InstructionPointer < InstructionSequenceLength:
        OpCode, Modes = get_modes_and_opcode (InstructionSequence[InstructionPointer])
        #print ("InstructionPointer, Modes, OpCode:", InstructionPointer, Modes, OpCode)
        InstructionsAttempted += 1;
        Result = 0
        ResultPosition = 0

        if OpCode == 99:
            InstructionSize = 1
            #print ("Halt")
            break

        elif OpCode == 1: #Add
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer)
            ResultPosition = InstructionSequence[InstructionPointer + 3]

            Result = Operand1 + Operand2
            InstructionSequence[ResultPosition] = Result
            #print ("Add.", Operand1, "+", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])


        elif OpCode == 2: #Multiply
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer)
            ResultPosition = InstructionSequence[InstructionPointer + 3]

            Result = Operand1 * Operand2
            InstructionSequence[ResultPosition] = Result
            #print ("Multiply.", Operand1, "*", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

        elif OpCode == 3: #Get Input
            InstructionSize = 2
            ResultPosition = InstructionSequence[InstructionPointer + 1]

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

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)

            # if (debug_prints):
            #     print ("InstructionPointer for opcode == 4: ", InstructionPointer)


            if (output_queue != None):
                output_queue.append(Operand1)

            else:
                print(Operand1)


        elif OpCode == 5: #jump-if-true
            InstructionSize = 3

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer)

            if (Operand1 != 0):
                InstructionPointer = Operand2
                #hack since Instruction pointer is already updated
                InstructionSize = 0

        elif OpCode == 6: #jump-if-false
            InstructionSize = 3

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer)

            if (Operand1 == 0):
                InstructionPointer = Operand2

                #hack since Instruction pointer is already updated
                InstructionSize = 0

        elif OpCode == 7: #less than
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer)
            ResultPosition = InstructionSequence[InstructionPointer + 3]

            if (Operand1 < Operand2):
                Result = 1
            else:
                Result = 0

            InstructionSequence[ResultPosition] = Result
            #print ("Less Than.", Operand1, "<", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

        elif OpCode == 8: #equals
            InstructionSize = 4

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            Operand2 = get_operand (2, Modes, InstructionSequence, InstructionPointer)
            ResultPosition = InstructionSequence[InstructionPointer + 3]

            if (Operand1 == Operand2):
                Result = 1
            else:
                Result = 0

            InstructionSequence[ResultPosition] = Result
            if(debug_prints):
                print ("Equals.", Operand1, "==", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

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







PuzzleInputSequence = [3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99]

PuzzleTestSqeuence = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
PuzzleTestSqeuence2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
PuzzleTestSqeuence3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

PuzzleTestSqeuence4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
PuzzleTestSqeuence5 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

AlarmCodeSequence = PuzzleInputSequence.copy()
AlarmCodeSequence[1] = 12
AlarmCodeSequence[2] = 2

#CopyOfSequenceToRun = AlarmCodeSequence.copy()
#InstructionsAttempted = run_instructions (CopyOfSequenceToRun)

#print ("InstructionsAttempted: ", InstructionsAttempted)
#print ("result in postion 0: ", CopyOfSequenceToRun[0])

#get_modes_and_opcode (11002)
#get_modes_and_opcode (1002)
#get_modes_and_opcode (1101)

run_instructions(PuzzleTestSqeuence5.copy(), debug_prints=True)

#run_instructions(PuzzleInputSequence.copy(), None, None, True)

# range_of_phase_values = range(0, 5)
# range_of_phase_values = range(5, 10)

# solve_day7_puzzle (PuzzleInputSequence.copy(), range_of_phase_values, True)