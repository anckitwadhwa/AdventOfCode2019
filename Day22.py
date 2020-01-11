import math

def read_input_from_file(filename, debug_prints_level = 0):
    debug_prints_level -= 1
    
    with open(filename, "r") as input_file:
        input_str = input_file.read()
            
    lines = input_str.splitlines()
    
    return(lines)
    
def solve_day22_puzzle(perform_shuffles, num_shuffles, num_cards, debug_prints_level = 0):

    input_lines = read_input_from_file("Day22 input.txt")
    num_lines = len(input_lines)
    
    cum_cut_index = 0
    cum_increment = 1
    cum_new_stack = 1
    for line_no, line in enumerate(input_lines):
        if(debug_prints_level > 90):
            print(f'performing shuffle {line_no} of {num_lines}')
        
        if (line[0] == "#"):
            # #indicates comment
            continue
            
        words = line.split(" ")
        
        if(words[0] == "cut"):
            cut_index = int(words[-1])
            cum_cut_index = (cut_index + cum_cut_index) % num_cards
            if(debug_prints_level > 90):
                print(f'cum_cut_index: {cum_cut_index}')
        
        elif(words[-1] == "stack"):
            cum_new_stack *= -1
            cum_cut_index *= -1
            if(debug_prints_level > 90):
                print(f'cum_cut_index: {cum_cut_index}')
        
        else:
            increment = int(words[-1])
            
            cum_increment = (increment * cum_increment) % num_cards
            cum_cut_index = (increment * cum_cut_index) % num_cards
            
            if(cum_new_stack < 0):
                cum_cut_index -= (num_cards+1 - increment)
                
            if(debug_prints_level > 90):
                print(f'cum_cut_index: {cum_cut_index}')
        

        if(debug_prints_level > 90):
            print(card_stack)

    if(debug_prints_level > 70):
        print(card_stack)

    
    cum_cut_index = (num_shuffles * cum_cut_index) % num_cards
    cum_increment = (num_shuffles * cum_increment) % num_cards
    
    if(cum_new_stack == -1):
        if(num_shuffles % 2 == 0):
            cum_new_stack = 1
            
            
    print(f'num_lines:{num_lines}; cum_cut_index:{cum_cut_index}; cum_new_stack:{cum_new_stack}; cum_increment:{cum_increment}')
    
    
    if(perform_shuffles):
        card_stack = [i for i in range(0, num_cards)]
        
        card_stack = deal_with_increment(card_stack, cum_increment, debug_prints_level)
        
        if(cum_new_stack == -1):
            card_stack = deal_into_new_stack(card_stack, debug_prints_level)
        
        card_stack = cut_deck(card_stack, cum_cut_index, debug_prints_level)
        
        print(f'position of card 2019: {card_stack.index(2019)}')
        print(f'card at 2020: {card_stack[2020]}')
        print(f'card at 2019: {card_stack[2019]}')

    return(cum_cut_index, cum_increment, cum_new_stack)
  
def cut_deck(current_deck, cut_index, debug_prints_level = 0):
    debug_prints_level -= 1
    if(debug_prints_level > 90):
        print(f'cutting deck at: {cut_index}')
    cut_index = cut_index % len(current_deck)
    
    new_deck = current_deck[cut_index:] + current_deck[0:cut_index]
    
    return(new_deck)
    
    
def deal_with_increment(current_deck, increment, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level > 90):
        print(f'dealing with increment: {increment}')
        
    num_cards = len(current_deck)
    new_deck = [0] * num_cards
    
    new_location = 0
    for current_location in range(0, num_cards):
        new_deck[new_location] = current_deck[current_location]
        
        new_location = (new_location + increment) % num_cards
        
    return(new_deck)
        

def deal_into_new_stack(current_deck, debug_prints_level = 0):
    debug_prints_level -= 1
    
    if(debug_prints_level > 90):
        print(f'dealing into new stack')
    
    new_deck = current_deck[::-1]
    
    return(new_deck)


def solve_day22_puzzle_b(cum_cut_index, cum_increment, cum_new_stack, num_cards, position, debug_prints_level = 0):
    debug_prints_level -= 1
    
    
    if(cum_new_stack != 1):
        print("alogirthm incomplete. Come back next year. kthxbai")
        return
    
    # for position x, increment m, new position y is given by
    # y = (mx) % n
    # for this puzzle we know y, and need to find x. Instead of solving this equation, find m2, such that it brings the deck back to original position
    m1 = cum_increment
    n = num_cards
    m2 = pow(m1, n-2, n) ## mod inv
    
    # now, y2 = (m2*x2) % n
    # here, y2 = x1 and x2 = y1
    # thus x1 = (m2*y1) % n
    
    y1 = (cum_cut_index + position)
    x1 = (m2 * y1) % n
    
    print (x1)

debug_prints_level = 70
# num_shuffles = 1
# num_shuffles = 2
num_shuffles = 101741582076661
# num_cards = 15
# num_cards = 10007
num_cards = 119315717514047
position = 2020
cum_cut_index, cum_increment, cum_new_stack = solve_day22_puzzle(False, num_shuffles, num_cards, debug_prints_level)

# num_lines:100; cum_cut_index:7249563028840; cum_new_stack:1; cum_increment:46225408621547
# 119315717514047
# 46225408621547  
# 7249563028840

solve_day22_puzzle_b(cum_cut_index, cum_increment, cum_new_stack, num_cards, position-1, debug_prints_level)
