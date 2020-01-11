def run_instructions (InstructionSequence):

    InstructionSequenceLength = len(InstructionSequence)

    InstructionPointer = 0
    InstructionsAttempted = 0

    while InstructionPointer < InstructionSequenceLength:
        OpCode = InstructionSequence[InstructionPointer]
        InstructionsAttempted += 1;
        Result = 0
        ResultPosition = 0

        if OpCode == 99:
            #print ("Halt")
            break

        else:
            Operand1 = InstructionSequence[InstructionSequence[InstructionPointer + 1]]
            Operand2 = InstructionSequence[InstructionSequence[InstructionPointer + 2]]
            ResultPosition = InstructionSequence[InstructionPointer + 3]

            if OpCode == 1:
                Result = Operand1 + Operand2
                InstructionPointer += 4
                #print ("Add.", Operand1, "+", Operand2, ".Placing result at position:", ResultPosition)


            elif OpCode == 2:
                Result = Operand1 * Operand2
                InstructionPointer += 4
                #print ("Multiply.", Operand1, "*", Operand2, ".Placing result at position:", ResultPosition, ".Result", InstructionSequence[ResultPosition])

            else:
                print ("Unknown Opcode: ", OpCode, "\nExiting")
                break

        InstructionSequence[ResultPosition] = Result
        #print ("Operand1, Operand2, ResultPosition, Result:", Operand1, Operand2, ResultPosition, InstructionSequence[ResultPosition])
        #print(InstructionSequence)

    return InstructionsAttempted
# end run_instructions
PuzzleInputSequence = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,13,19,1,9,19,23,1,6,23,27,2,27,9,31,2,6,31,35,1,5,35,39,1,10,39,43,1,43,13,47,1,47,9,51,1,51,9,55,1,55,9,59,2,9,59,63,2,9,63,67,1,5,67,71,2,13,71,75,1,6,75,79,1,10,79,83,2,6,83,87,1,87,5,91,1,91,9,95,1,95,10,99,2,9,99,103,1,5,103,107,1,5,107,111,2,111,10,115,1,6,115,119,2,10,119,123,1,6,123,127,1,127,5,131,2,9,131,135,1,5,135,139,1,139,10,143,1,143,2,147,1,147,5,0,99,2,0,14,0]

PuzzleTestSqeuence = [1,9,10,3,2,3,11,0,99,30,40,50]
PuzzleTestSqeuence2 = [1,1,1,4,99,5,6,0,99]
AlarmCodeSequence = PuzzleInputSequence.copy()
AlarmCodeSequence[1] = 12
AlarmCodeSequence[2] = 2

#CopyOfSequenceToRun = AlarmCodeSequence.copy()
#InstructionsAttempted = run_instructions (CopyOfSequenceToRun)

#print ("InstructionsAttempted: ", InstructionsAttempted)
#print ("result in postion 0: ", CopyOfSequenceToRun[0])

Day2BSequence = PuzzleInputSequence.copy()
MAGIC_RESULT = 19690720
ResultFound = False

print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Starting search$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
for Noun in range (0, 100):
    Day2BSequence[1] = Noun

    for Verb in range (0, 100):

        Day2BSequence[2] = Verb
        #print ("Noun+verb:", 100 * Noun + Verb)
        #print (Day2BSequence)

        CopyOfSequenceToRun = Day2BSequence.copy()
        InstructionsAttempted = run_instructions (CopyOfSequenceToRun)

        #print ("InstructionsAttempted: ", InstructionsAttempted)
        #print ("result in postion 0: ", CopyOfSequenceToRun[0])


        if (CopyOfSequenceToRun[0] == MAGIC_RESULT):
            ResultFound = True
            print ("ResultFound:", 100 * Noun + Verb)
            break

    if (ResultFound):
            break
else:
    print("No Noun + Verb combination found")



