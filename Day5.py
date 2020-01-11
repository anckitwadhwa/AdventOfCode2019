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

    #print ("Number, Opcode, Modes: ", Number, Opcode, Modes)
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


def run_instructions (InstructionSequence):

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

            UserInput = input ("Enter Input:")
            InstructionSequence[ResultPosition] = int(UserInput)

        elif OpCode == 4: #Output
            InstructionSize = 2

            Operand1 = get_operand (1, Modes, InstructionSequence, InstructionPointer)
            print (Operand1)


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
            #print ("Equals.", Operand1, "==", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

        else:
            print ("Unknown Opcode: ", OpCode, "\nExiting")
            break

        InstructionPointer += InstructionSize

        #print ("Operand1, Operand2, ResultPosition, Result:", Operand1, Operand2, ResultPosition, InstructionSequence[ResultPosition])
        #print(InstructionSequence)

    return InstructionsAttempted
# end run_instructions
PuzzleInputSequence = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,83,20,225,1102,55,83,224,1001,224,-4565,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,1101,52,15,225,1102,42,92,225,1101,24,65,225,101,33,44,224,101,-125,224,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1001,39,75,224,101,-127,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,2,14,48,224,101,-1300,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1002,139,79,224,101,-1896,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,24,92,225,1101,20,53,224,101,-73,224,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,1101,70,33,225,1101,56,33,225,1,196,170,224,1001,224,-38,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,50,5,225,102,91,166,224,1001,224,-3003,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,344,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,359,101,1,223,223,107,677,677,224,1002,223,2,223,1006,224,374,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,389,101,1,223,223,108,677,226,224,102,2,223,223,1006,224,404,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,419,1001,223,1,223,7,677,226,224,102,2,223,223,1005,224,434,101,1,223,223,1008,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,464,101,1,223,223,1108,677,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,107,226,226,224,1002,223,2,223,1005,224,494,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,509,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,524,101,1,223,223,1007,226,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,107,677,226,224,102,2,223,223,1006,224,554,101,1,223,223,1107,677,226,224,1002,223,2,223,1006,224,569,1001,223,1,223,1008,226,677,224,102,2,223,223,1006,224,584,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,599,1001,223,1,223,7,677,677,224,1002,223,2,223,1005,224,614,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,629,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,644,1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,659,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226]

PuzzleTestSqeuence = [1,9,10,3,2,3,11,0,99,30,40,50]
PuzzleTestSqeuence2 = [1,1,1,4,99,5,6,0,99]
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

run_instructions(PuzzleInputSequence)