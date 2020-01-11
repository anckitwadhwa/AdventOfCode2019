from collections import deque
from inspect import currentframe
import threading
import time
import math

class IntcodeExecutor:
    def __init__(self, instruction_sequence, input_queue = None, output_queue = None, io_interpreter = None, debug_prints = False):

        self.relative_base = 0
        self.instruction_pointer = 0
        self.halted = False
        self.instructions_attempted = 0
        
        if(isinstance(io_interpreter, IOInterpreter) == True):
            self.io_interpreter = io_interpreter
            
        else:
            self.io_interpreter = IOInterpreter()
            
        self.instruction_sequence = instruction_sequence
        self.input_queue = input_queue
        self.output_queue = output_queue

        self.thread = threading.Thread(name="executor", target=self.__run_instructions, args=([debug_prints]))

        self.thread.start()
        
    def __del__(self, debug_prints = False):       
        self.thread.join()

    def is_halted(self, debug_prints = False):
        self.halted = self.halted or not(self.thread.is_alive())
        
        return(self.halted)
    
    def signal_termination(self, debug_prints = False):
        self.halted = True
        
    
    def __fetch_from_instruction_pointer(self, additional_offset = 0):
        return(self.instruction_sequence[self.instruction_pointer + additional_offset])

    def __fetch_from_start(self, additional_offset = 0):
        return(self.instruction_sequence[additional_offset])

    def __increment_instruction_pointer(self, increment):
        self.instruction_pointer += increment

    def __get_modes_and_opcode(self, debug_prints = False):
        modes_and_opcode_str = str(self.__fetch_from_instruction_pointer(0))

        opcode = int(modes_and_opcode_str[-2:])

        modes_str = modes_and_opcode_str[:-2]
        modes = []

        for index in range(1, len(modes_str) + 1):
            mode = int(modes_str[-index])
            modes.append(mode)

        if(debug_prints):
            print ("modes_and_opcode_str, opcode, modes: ", modes_and_opcode_str, opcode, modes)

        return opcode, modes

    def __get_operand(self, parameter_number, modes, debug_prints = False):
        operand = 0
        mode = 0
        relative_base = self.relative_base
        __fetch_from_instruction_pointer = self.__fetch_from_instruction_pointer
        __fetch_from_start = self.__fetch_from_start

        if (parameter_number <= 0):
            print ("Bad Operand Number (must be <=0):", parameter_number)
            return (operand)

        elif (parameter_number <= len (modes)):
            mode = modes[parameter_number - 1]

        if (mode == 1):
            operand = self.__fetch_from_instruction_pointer(parameter_number)

        elif (mode == 0):
            operand = __fetch_from_start(__fetch_from_instruction_pointer(parameter_number) + 0)

        elif (mode == 2):
            operand = __fetch_from_start(__fetch_from_instruction_pointer(parameter_number) + relative_base)

        else:
            print ("Unknown Mode: ", mode)

        if(debug_prints):
            print(f'mode:{mode}, operand: {operand}')
        return (operand)

    def __get_result_position(self, parameter_number, modes):
        mode = 0
        result_position = self.__fetch_from_instruction_pointer(parameter_number)

        if (parameter_number <= 0):
            print ("Bad Operand Number (must be <=0):", parameter_number)

        elif (parameter_number <= len (modes)):
            mode = modes [parameter_number - 1]


        if (mode == 2):
            result_position += self.relative_base

        return(result_position)


    def __run_instructions (self, debug_prints = False):
        # debug_prints = True
        #add 10,000 space for more memory
        self.instruction_sequence.extend([0] * 10000)

        instruction_sequence_length = len(self.instruction_sequence)
        self.instructions_attempted = 0

        while ((self.instruction_pointer < instruction_sequence_length) and (self.halted != True)):
            opcode, modes = self.__get_modes_and_opcode(debug_prints)
            self.__handle_opcode(opcode, modes, debug_prints)
            self.instructions_attempted += 1

        self.halted = True

    def __handle_opcode(self, opcode, modes, debug_prints = False):
        if (debug_prints):
            print ("Instructions Attempted, InstructionPointer, Modes, OpCode, RelativeBase: ", self.instructions_attempted, self.instruction_pointer, modes, opcode, self.relative_base)

        if opcode == 99:
            self.halted = True
            self.__handle_opcode_99(debug_prints)

        elif opcode == 1:
            self.__handle_opcode_1(modes, debug_prints)

        elif opcode == 2:
            self.__handle_opcode_2(modes, debug_prints)

        elif opcode == 3:
            self.__handle_opcode_3(modes, debug_prints)

        elif opcode == 4:
            self.__handle_opcode_4(modes, debug_prints)

        elif opcode == 5:
            self.__handle_opcode_5(modes, debug_prints)

        elif opcode == 6:
            self.__handle_opcode_6(modes, debug_prints)

        elif opcode == 7:
            self.__handle_opcode_7(modes, debug_prints)

        elif opcode == 8:
            self.__handle_opcode_8(modes, debug_prints)

        elif opcode == 9:
            self.__handle_opcode_9(modes, debug_prints)

        else:
            print (f'Unknown Opcode:{opcode}\nExiting')
            print ("Instructions Attempted, InstructionPointer, Modes, OpCode, RelativeBase: ", self.instructions_attempted, self.instruction_pointer, modes, opcode, self.relative_base)
            self.halted = True

    def __handle_opcode_99(self, debug_prints = False):

        if (self.output_queue != None):
            self.output_queue.append(99)

        if (debug_prints):
            print ("Halt")

        self.__increment_instruction_pointer(1)

    def __handle_opcode_1(self, modes, debug_prints = False):

        operand1 = self.__get_operand(1, modes)
        operand2 = self.__get_operand(2, modes)
        result_position = self.__get_result_position(3, modes)

        result = operand1 + operand2
        self.instruction_sequence[result_position] = result

        if (debug_prints):
            print (f'Add.{operand1}, {operand2}. Placing result at position:{result_position}. Result{self.instruction_sequence[result_position]}')

        self.__increment_instruction_pointer(4)

    def __handle_opcode_2(self, modes, debug_prints = False):

        operand1 = self.__get_operand(1, modes)
        operand2 = self.__get_operand(2, modes)
        result_position = self.__get_result_position(3, modes)

        result = operand1 * operand2
        self.instruction_sequence[result_position] = result

        if (debug_prints):
            print (f'Multiply.{operand1}, {operand2}. Placing result at position:{result_position}. Result{self.instruction_sequence[result_position]}')

        self.__increment_instruction_pointer(4)

    def __handle_opcode_3(self, modes, debug_prints = False):

        result_position = self.__get_result_position(1, modes)
        result = 0

        if (self.input_queue != None):
            #wait for element to be added to the queue
            while (not(self.is_halted()) and (len(self.input_queue) < 1)):
                if (debug_prints):
                    print(f'sleeping in {threading.current_thread().name}')
                time.sleep (0.001)

            if(not(self.is_halted())):
                result = self.input_queue.popleft()
        else:
            result = input ("Enter Input:")

        result = self.io_interpreter.interpret_input(result, debug_prints)
        
        self.instruction_sequence[result_position] = int(result)

        if (debug_prints):
            print(f'Input:{result}')

        self.__increment_instruction_pointer(2)

    def __handle_opcode_4(self, modes, debug_prints = False):
        operand1 = self.__get_operand(1, modes)
        
        operand1 = self.io_interpreter.interpret_output(operand1)

        if (self.output_queue != None):
            self.output_queue.append(operand1)

        else:
            print(operand1, end = "")

        if (debug_prints):
            print(f'Output:{operand1}')

        self.__increment_instruction_pointer(2)

    def __handle_opcode_5(self, modes, debug_prints = False):

        operand1 = self.__get_operand(1, modes)
        operand2 = self.__get_operand(2, modes)

        if (operand1 != 0):
            self.instruction_pointer = operand2
        else:
            self.__increment_instruction_pointer(3)

        if (debug_prints):
            print (f'Jump if True. {operand1}, {operand2}. instruction pointer now at:{self.instruction_pointer}')

    def __handle_opcode_6(self, modes, debug_prints = False):

        operand1 = self.__get_operand(1, modes)
        operand2 = self.__get_operand(2, modes)

        if (operand1 == 0):
            self.instruction_pointer = operand2
        else:
            self.__increment_instruction_pointer(3)

        if (debug_prints):
            print (f'Jump if False. {operand1}, {operand2}. instruction pointer now at:{self.instruction_pointer}')

    def __handle_opcode_7(self, modes, debug_prints = False):

        operand1 = self.__get_operand (1, modes)
        operand2 = self.__get_operand (2, modes)
        result_position = self.__get_result_position(3, modes)

        if (operand1 < operand2):
            result = 1
        else:
            result = 0

        self.instruction_sequence[result_position] = result

        if (debug_prints):
            print (f'Is less than.{operand1} < {operand2}?. Placing result at position:{result_position}. Result{self.instruction_sequence[result_position]}')

        self.__increment_instruction_pointer(4)

    def __handle_opcode_8(self, modes, debug_prints = False):

        operand1 = self.__get_operand(1, modes)
        operand2 = self.__get_operand(2, modes)
        result_position = self.__get_result_position(3, modes)

        if (operand1 == operand2):
            result = 1
        else:
            result = 0

        self.instruction_sequence[result_position] = result

        if (debug_prints):
            print (f'Equals {operand1} == {operand2}?. Placing result at position:{result_position}. Result{self.instruction_sequence[result_position]}')

        self.__increment_instruction_pointer(4)

    def __handle_opcode_9(self, modes, debug_prints = False):

        operand1 = self.__get_operand(1, modes)
        self.relative_base += operand1

        if (debug_prints):
            print (f'Update relative base to:{self.relative_base}')

        self.__increment_instruction_pointer(2)
        

class IOInterpreter:
    def interpret_input(self, input_str, debug_prints = False):
        return input_str
        
    def interpret_output(self, output_str, debug_prints = False):
        return output_str
        
class ASCIIInterpretor(IOInterpreter):

    def interpret_input(self, input_char, debug_prints = False):
        return_val = 0
    
        if(input_char == ""):
            return_val = ord("\n")
        else:
            return_val = ord(input_char[0])
    
        if(debug_prints):
            print(f'interpreting {input_char}->{return_val}')
    
        return(return_val)
        
    def interpret_output(self, output_int, debug_prints = False):

        MAX_ASCII_INT = 128
        if(output_int < MAX_ASCII_INT):
            return(chr(output_int))
        else:
            return(output_int)
