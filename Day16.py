import math
import cProfile
import time 
from inspect import currentframe

def number_str_to_list(number_str, debug_prints = False):

    N = len(number_str)
    number_list = [0] * N
    
    for i in range(N):
        number_list[i] = int(number_str[i])

    return(number_list)
    
def number_list_to_str(number_list, N = -1, debug_prints = False):

    if (N < 0):
        N = len(number_list)
    
    list_of_strings = ["0"] * N

    for i in range(0, N):
        list_of_strings[i] = str(number_list[i])

    return("".join(list_of_strings))

def perform_FFT_phase(number_list, debug_prints = False):

    # number_str = str(number)
    digits = len(number_list)
    if(debug_prints):
        print(f'number length:{digits}')
        
    # initialize to original string to avoid performance hit of resizing
    half_of_digits = int(digits / 2)
    # half_of_digits = digits
    
    computed_FFT_list = list(number_list.copy())
    for i in range (0, half_of_digits):
        if(i % 100 == 0):
            print(f'i:{i}')
        perform_FFT_phase_for_digit(i + 1, number_list, computed_FFT_list, debug_prints)
        
    perform_FFT_phase_for_second_half(half_of_digits, number_list, computed_FFT_list, debug_prints)
    
    if(debug_prints):
        print(computed_FFT_list)
    
    return(computed_FFT_list)

def perform_FFT_phase_for_second_half(start, number_list, computed_FFT_list, debug_prints = False):
    # start with last digit, computing it back up
    
    # N = total digits in input number
    N = len(number_list)
    sum = 0
    
    for index in range (N-1, start-1, -1):
        sum += number_list[index]
        computed_FFT_list[index] = abs(sum) % 10


def perform_FFT_phase_for_digit(digit_number, number_list, computed_FFT_list, debug_prints = False):
    
    # pr = cProfile.Profile()
    # pr.enable()
    if(digit_number == 0):
        print("digit_number needs to be >0")
        return ""
    
    N = len(number_list)
    n = digit_number
    
    # pattern_str = ""
    sum_product = 0
    current_pos = 0
    
    # ignore first (n-1) digits
    current_pos += (n-1)
    # pattern_str = "0" * (n-1)
    
    while(current_pos < N):
        #for next n digits, add to sum_product
        i = 0
        while((current_pos < N) and (i < n)):
            sum_product += number_list[current_pos]
            i += 1
            current_pos += 1
        
        # pattern_str = pattern_str + ("1" * i)
    
        # ignore next n digits
        current_pos += n
        # pattern_str = pattern_str + ("0" * n)
    
        #for next n digits, subtract from sum_product
        i = 0
        while((current_pos < N) and (i < n)):
            sum_product -= number_list[current_pos]
            i += 1
            current_pos += 1
        
        # ignore next n digits
        current_pos += n
        # pattern_str = pattern_str + ("-1" * i)
        
        #repeat
    
    computed_FFT_list[digit_number - 1] = abs(sum_product) % 10
    
    if(debug_prints):
        # (n - 1) + k * (4*n) + x = N
        k = math.floor((N - (n-1))/ (4*n))
        x = N - (n-1) - k * 4*n
        
        expected_zeros = (n-1) + k*2*n
        expected_positive_ones = k*n
        expected_negative_ones = k*n
        if(x > 3*n):
            expected_positive_ones += n
            expected_zeros += n
            expected_negative_ones += n
            expected_zeros += (x - 3*n)
        elif (x > 2*n):
            expected_positive_ones += n
            expected_zeros += n
            expected_negative_ones += (x - 2*n)
        elif (x > n):
            expected_positive_ones += n
            expected_zeros += (x - n)
        else:
            expected_positive_ones += x

        # print(f'index_into_base_sequence_str:{index_into_base_sequence_str}; pattern_str was:{pattern_str}; computed FFT_digit:{FFT_digit}')
        num_zeros_in_pattern = pattern_str.count("0")
        num_negative_1s_in_pattern = pattern_str.count("-")
        num_positive_1s_in_pattern = pattern_str.count("1") - num_negative_1s_in_pattern
        print(f'For digit:{digit_number}\npattern str 0, 1, -1: {num_zeros_in_pattern, num_positive_1s_in_pattern, num_negative_1s_in_pattern}')
        print(f'expected pattern str 0, 1, -1: {expected_zeros, expected_positive_ones, expected_negative_ones}')
        print(f'computed FFT_digit:{FFT_digit}')

    # pr.disable()
    # pr.print_stats(sort='time')
    
def unit_tests():

    print("=" * 75)
    print("Begin unit tests")
    
    input_list = number_str_to_list("12345678")
    output_list = input_list.copy()
    
    perform_FFT_phase_for_digit(1, input_list, output_list, False)
    expected_answer = 4
    actual_answer = output_list[1 - 1]
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    perform_FFT_phase_for_digit(6, input_list, output_list, False)
    expected_answer = 1
    actual_answer = output_list[6 - 1]
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')


    # big_number = "59702216318401831752516109671812909117759516365269440231257788008453756734827826476239905226493589006960132456488870290862893703535753691507244120156137802864317330938106688973624124594371608170692569855778498105517439068022388323566624069202753437742801981883473729701426171077277920013824894757938493999640593305172570727136129712787668811072014245905885251704882055908305407719142264325661477825898619802777868961439647723408833957843810111456367464611239017733042717293598871566304020426484700071315257217011872240492395451028872856605576492864646118292500813545747868096046577484535223887886476125746077660705155595199557168004672030769602168262"
    # big_number_len = len(big_number)
    # expected_answer = "1"
    # for digit_number in range(103, 104):
        # actual_answer = perform_FFT_phase_for_digit(digit_number, big_number, True)
    # if(actual_answer != expected_answer):
        # print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')


    expected_answer = "48226158"
    actual_answer = number_list_to_str(perform_FFT_phase(number_str_to_list("12345678"), False))
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    expected_answer = "03415518"
    actual_answer = number_list_to_str(perform_FFT_phase(number_str_to_list("34040438"), False))
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    expected_answer = "01029498"
    actual_answer = number_list_to_str(perform_FFT_phase(number_str_to_list("03415518"), False))
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    
    expected_answer = "24176176"
    actual_answer = solve_day_16_puzzle("80871224585914546619083218645595", 100, False)
    actual_answer = actual_answer[0:8]
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    expected_answer = "73745418"
    actual_answer = solve_day_16_puzzle("19617804207202209144916044189917", 100, False)
    actual_answer = actual_answer[0:8]
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    expected_answer = "52432133"
    actual_answer = solve_day_16_puzzle("69317163492948606335995924319873", 100, False)
    actual_answer = actual_answer[0:8]
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')


    expected_answer = "84462026"
    actual_answer = solve_day_16_puzzle_b("03036732577212944063491565474664", True)
    actual_answer = actual_answer[0:8]
    if(actual_answer != expected_answer):
        print(f'Unit test failed. Expected:{expected_answer}; actual:{actual_answer}; line#:{currentframe().f_lineno}')

    
    print("Unit tests complete")
    print("=" * 75)


def solve_day_16_puzzle(number_str, num_phases = 100, debug_prints = False):
    print("*" * 75)
    # print(number_str)
    return_val = 0
    number_str_copy = number_str
    number_list = number_str_to_list(number_str, debug_prints)
    
    for i in range(num_phases):
        number_list = perform_FFT_phase(number_list, debug_prints)
        if(i % 20 == 0):
            # print(f'i:{i}; FFT:{number_str}; len:{len(number_str)}')
            print(f'i:{i}; len:{len(number_list)}')
        
    number_str = number_list_to_str(number_list, 8, False)
    
    print(number_str)
    print("$" * 50)
    
    return(number_str)
    

def get_offset(input_str, debug_prints = False):

    return(int(input_str[0:7]))
    
    
def get_relevant_mesage_signal(base_signal, num_repetitions, debug_prints = False):

    N_base_signal = len(base_signal)
    
    message_offset = get_offset(base_signal, debug_prints)
    N_relevant_message_signal = N_base_signal * num_repetitions - message_offset
    
    if(debug_prints):
        print(f':message_offset{message_offset}; N_base_signal:{N_base_signal}; N_relevant_message_signal:{N_relevant_message_signal}')
    
    # fill with base_input_str starting at appropriate offset
    relevant_message_signal = base_signal[message_offset % N_base_signal : ]
    
    # then put 'k' copies of base signal
    current_len = len(relevant_message_signal)
    k = int((N_relevant_message_signal - current_len) / N_base_signal)
    relevant_message_signal += base_signal * k

    return(relevant_message_signal)


def solve_day_16_puzzle_b(input_str, num_phases = 100, debug_prints = False):
    relevant_message_signal = get_relevant_mesage_signal(input_str, 10000, False)
    
    number_list = number_str_to_list(relevant_message_signal)
    N = len(number_list)
    
    if(debug_prints):
        print(f'length:{N}\n')
    
    FFT_list = []
    for i in range(num_phases):
        FFT_list = number_list.copy()
        sum = 0
        
        for j in range(N-1, -1, -1):
            sum += number_list[j]
            number_list[j] = abs(sum) % 10
            
        # number_list = FFT_list
            
    
    FFT_str = number_list_to_str(number_list[0:8])
    print(FFT_str)
    
    
def do_profile():
    
    base_signal = "03036732577212944063491565474664"
    solve_day_16_puzzle_b(base_signal, 2, False)
    
    # relevant_message_signal = get_relevant_mesage_signal(base_signal, 10000, True)
    
    # perform_FFT_phase_for_digit(1, relevant_message_signal, False)
    
    # for digit in range(1, 101):
        # if(digit % 10 == 0):
            # print(f'digit:{digit}')
        # perform_FFT_phase_for_digit(digit, relevant_message_signal, False)
    
    # perform_FFT_phase(relevant_message_signal, False)
    
       
 
# unit_tests()
# cProfile.run('do_profile()')

# do_profile()
# puzzle_input = "1234567"
# solve_day_16_puzzle(puzzle_input, 5, True)


# puzzle_input = "80871224585914546619083218645595"
# solve_day_16_puzzle(puzzle_input)

# puzzle_input = "19617804207202209144916044189917"
# solve_day_16_puzzle(puzzle_input)

# puzzle_input = "69317163492948606335995924319873"
# solve_day_16_puzzle(puzzle_input)

# puzzle_input = "5970221631840183175251610967181290911775951636526944023125778800845375673482782647623990522649358900"
# solve_day_16_puzzle(puzzle_input, 1, True)

# puzzle_input = "59702216318401831752516109671812909117759516365269440231257788008453756734827826476239905226493589006960132456488870290862893703535753691507244120156137802864317330938106688973624124594371608170692569855778498105517439068022388323566624069202753437742801981883473729701426171077277920013824894757938493999640593305172570727136129712787668811072014245905885251704882055908305407719142264325661477825898619802777868961439647723408833957843810111456367464611239017733042717293598871566304020426484700071315257217011872240492395451028872856605576492864646118292500813545747868096046577484535223887886476125746077660705155595199557168004672030769602168262"
# solve_day_16_puzzle(puzzle_input)


# puzzle_input = "12340000"
# solve_day_16_puzzle(puzzle_input)

# puzzle_input = "00005678"
# solve_day_16_puzzle(puzzle_input)

# puzzle_input = "12345678"
# solve_day_16_puzzle(puzzle_input)

# puzzle_input = "03036732577212944063491565474664"
# solve_day_16_puzzle_b(puzzle_input, 100, True)

puzzle_input = "59702216318401831752516109671812909117759516365269440231257788008453756734827826476239905226493589006960132456488870290862893703535753691507244120156137802864317330938106688973624124594371608170692569855778498105517439068022388323566624069202753437742801981883473729701426171077277920013824894757938493999640593305172570727136129712787668811072014245905885251704882055908305407719142264325661477825898619802777868961439647723408833957843810111456367464611239017733042717293598871566304020426484700071315257217011872240492395451028872856605576492864646118292500813545747868096046577484535223887886476125746077660705155595199557168004672030769602168262"
solve_day_16_puzzle_b(puzzle_input, 100, True)
    

