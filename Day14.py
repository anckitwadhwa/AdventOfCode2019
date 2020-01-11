import math
from inspect import currentframe

def read_puzzle_input_from_file(filename):
    f = open(filename, "r")
    puzzle_input = list(f.read().splitlines())

    return(puzzle_input)

def get_input_and_product_list(reactions_list, debug_prints = False):
    inputs = []
    products = []

    for index, reaction in enumerate(reactions_list):

        inputs.append(dict())
        products.append(dict())

        chemicals = reaction.split("=>")

        reaction_left_side = chemicals[0]
        reaction_right_side = chemicals[1]

        products[index].update(split_qty_and_chemical(reaction_right_side, False))

        reactants = reaction_left_side.split(",")

        for reactant in reactants:
            qty_and_chemical = split_qty_and_chemical(reactant, False)
            inputs[index].update(qty_and_chemical)

        if(debug_prints):
            print(f'inputs:{inputs}\nproducts:{products}')

    return(inputs, products)


def split_qty_and_chemical(combined_string, debug_prints = False):

    combined_string = combined_string.strip()
    if (debug_prints):
        print(combined_string)

    qty_and_chemical_str = combined_string.split(" ")

    qty = int(qty_and_chemical_str[0])
    chemical = qty_and_chemical_str[1]

    qty_and_chemical_dict = {chemical : qty}
    return(qty_and_chemical_dict)


def find_index_of_product(product_of_interest, products):
    index_of_product = 0

    for index, product in enumerate(products):
        if(product_of_interest in product):
            index_of_product = index
            break
    else:
        print(f'product not found, {product_of_interest, product}')

    return(index_of_product)

def get_multiplier(qty_needed, qty_produced, coerce_up = True):

    multiplier_float = (qty_needed * 1.0) / qty_produced
    if(coerce_up):
        multiplier_int = int(math.ceil(multiplier_float))
    else:
        multiplier_int = int(math.floor(multiplier_float))

    return(multiplier_int)

def decompose_all_reactants(reactant_to_preserve, side_to_decompose, other_side_of_reaction, inputs, products, coerce_up, debug_prints = False):

    # find index of reactant in products, get reactants for reactant from inputs, add to left side, adjust right side with any extra reactant
    decomposition_successful = False

    side_to_decompose_copy = side_to_decompose.copy()
    for reactant in side_to_decompose_copy:
        if(reactant == reactant_to_preserve):
            continue

        decomposition_successful_for_this_reactant = decompose_single_reactant(reactant, side_to_decompose, other_side_of_reaction, inputs, products, coerce_up, debug_prints)
        if(debug_prints):
            print(f'after decomposing {reactant} {side_to_decompose}<=>{other_side_of_reaction}')

        decomposition_successful = decomposition_successful or decomposition_successful_for_this_reactant

    balance_reaction(side_to_decompose, other_side_of_reaction, False)
    if(debug_prints):
        print(f'after 1 round of decomposition {side_to_decompose}<=>{other_side_of_reaction}')


    return(decomposition_successful)

def decompose_single_reactant(reactant, side_to_decompose, other_side_of_reaction, inputs, products, coerce_up, debug_prints = False):
    decomposition_successful = False
    index = find_index_of_product(reactant, products)

    qty_of_reactant_needed = side_to_decompose[reactant]
    qty_of_reactant_produced = products[index][reactant]

    multiplier = get_multiplier(qty_of_reactant_needed, qty_of_reactant_produced, coerce_up)

    if(debug_prints and (reactant == "NZVS")):
        print(f'qty_of_reactant_needed: {qty_of_reactant_needed}; qty_of_reactant_produced:{qty_of_reactant_produced}; multiplier:{multiplier}')

    if (multiplier == 0):
        # cant decompose further
        return(decomposition_successful)

    decomposition_successful = True

    next_level_reactants = inputs[index].copy()

    # add next level reactants to side to decompose
    add_chemicals(multiplier, next_level_reactants, side_to_decompose, debug_prints)

    # If we coerce up, there will be excess reactant on other side, else there will be remaining reactant on side to decompose
    if (coerce_up):
        # add excess reactant produced to rhs
        # if(debug_prints):
        #     print(f'Adding {reactant} : {excess_reactant_produced} to {other_side_of_reaction}')
        excess_reactant_produced = qty_of_reactant_produced * multiplier - qty_of_reactant_needed
        other_side_of_reaction.update({reactant : excess_reactant_produced})
        side_to_decompose[reactant] = 0

    else:
        remaining_reactant = qty_of_reactant_needed - qty_of_reactant_produced * multiplier
        side_to_decompose[reactant] = remaining_reactant

    return(decomposition_successful)

def balance_reaction(one_side, other_side, debug_prints = False):

    reactants = set(one_side.keys())
    products = set(other_side.keys())

    common_chemicals = reactants.intersection(products)

    for chemical in common_chemicals:
        min_qty = min(one_side[chemical], other_side[chemical])
        one_side[chemical] -= min_qty
        other_side[chemical] -= min_qty

    remove_keys_with_zero_value(one_side)
    remove_keys_with_zero_value(other_side)


    if(debug_prints):
        print("=" * 25, "after balancing", "=" * 25)
        print(f'{one_side} <=> {other_side}')

def remove_keys_with_zero_value(dictionary):

    # cant modify dictionary while iterating, create a copy
    dictionary_copy = dictionary.copy()

    for key in dictionary_copy:
        if(dictionary_copy[key] == 0):
            del dictionary[key]


def solve_day14_puzzle(filename, debug_prints = False):
    coerce_up = True
    reactions_list = read_puzzle_input_from_file(filename)
    inputs, products = get_input_and_product_list(reactions_list)
    if(debug_prints):
        print("*" * 50)
        for index in range(len(inputs)):
            print(f'{inputs[index]} => {products[index]}')

    index_of_fuel = find_index_of_product("FUEL", products)

    print(inputs[index_of_fuel])

    left_side_of_reaction = inputs[index_of_fuel].copy()

    # right_side_of_reaction = dict()
    right_side_of_reaction = products[index_of_fuel].copy()

    counter = 0
    update_frequency = 1

    decomposition_successful = True
    while(decomposition_successful):
        if(debug_prints and (counter % update_frequency == 0)):
            print(f'(about to decompose {left_side_of_reaction}=>{right_side_of_reaction}')

        counter += 1
        decomposition_successful = decompose_all_reactants("ORE", left_side_of_reaction, right_side_of_reaction, inputs, products, coerce_up, debug_prints)

    print(f'final reaction {left_side_of_reaction}=>{right_side_of_reaction}')


    #only ores should be present on left side now
    number_of_ores_needed = left_side_of_reaction['ORE']
    print(number_of_ores_needed)

    solve_day14_puzzle_b(left_side_of_reaction, right_side_of_reaction, inputs, products, False)


def solve_day14_puzzle_b(left_side_base_equation, right_side_base_equation, inputs, products, debug_prints = False):
    ORE_AMOUNT = int(1e12)
    if(debug_prints):
        print('b' * 50)

    current_left_side = left_side_base_equation.copy()
    current_right_side = right_side_base_equation.copy()

    ore_quanta = left_side_base_equation['ORE']

    decomposition_successful = True
    while(decomposition_successful):

        ore_available = ORE_AMOUNT - current_left_side['ORE']

        multiplier = get_multiplier(ore_available, ore_quanta, False)
        if(debug_prints):
            print(f'ore_available:{ore_available}; ore_quanta:{ore_quanta}; multiplier:{multiplier}')

        add_chemicals(multiplier, left_side_base_equation, current_left_side, debug_prints)
        add_chemicals(multiplier, right_side_base_equation, current_right_side, debug_prints)

        decomposition_successful = decompose_all_reactants("FUEL", current_right_side, current_left_side, inputs, products, False, debug_prints)

    print(f'final equation {current_left_side}=>{current_right_side}')
    #add ORE 1 more time, this time with a forced multiplier of 1.0  and see if we can decompose to get below the ORE_AMOUNT limit
    multiplier = 1
    add_chemicals(multiplier, left_side_base_equation, current_left_side, debug_prints)
    add_chemicals(multiplier, right_side_base_equation, current_right_side, debug_prints)

    decomposition_successful = True
    while(decomposition_successful):

        decomposition_successful = decompose_all_reactants("FUEL", current_right_side, current_left_side, inputs, products, False, debug_prints)

    print(f'final equation {current_left_side}=>{current_right_side}')


    #add ORE 1 more time, this time with a forced multiplier of 1.0  and see if we can decompose to get below the ORE_AMOUNT limit
    multiplier = 1
    add_chemicals(multiplier, left_side_base_equation, current_left_side, debug_prints)
    add_chemicals(multiplier, right_side_base_equation, current_right_side, debug_prints)

    decomposition_successful = True
    while(decomposition_successful):

        decomposition_successful = decompose_all_reactants("FUEL", current_right_side, current_left_side, inputs, products, False, debug_prints)

    print(f'final equation {current_left_side}=>{current_right_side}')


def add_chemicals(multiplier, reactants_to_add, current_reactants, debug_prints = False):
    reactants_to_add_copy = reactants_to_add.copy()

    for reactant in reactants_to_add_copy:
        reactants_to_add_copy[reactant] *= multiplier

        # dictionary update will overite existing keys. If the next level reactant is already in lhs, update qty to its final qty
        if(reactant in current_reactants):
            reactants_to_add_copy[reactant] += current_reactants[reactant]


    current_reactants.update(reactants_to_add_copy)


def unit_tests():
    product = '653 C'
    qty_and_chemical = split_qty_and_chemical(product)
    expected_qty_and_chemical = {'C':653}

    if(qty_and_chemical != expected_qty_and_chemical):
        print(f'unit test failed. Expected: {expected_qty_and_chemical}, got: {qty_and_chemical}, line#: {currentframe().f_lineno}')



    reactions_list = ["7 A, 1 E => 1 FUEL", "7 A, 1 D => 1 E"]
    inputs, products = get_input_and_product_list(reactions_list, False)


    expected_inputs_0 = {'A' : 7, 'E' : 1}
    expected_inputs_1 = {'A' : 7, 'D' : 1}
    expected_products_0 = {'FUEL' : 1}
    expected_products_1 = {'E' : 1}

    if((inputs[0] != expected_inputs_0) or (inputs[1] != expected_inputs_1) or (products[0] != expected_products_0) or (products[1] != expected_products_1)):
        print(f'Unit test failed. \nExpected Inputs:{[expected_inputs_0, expected_inputs_1]}, \nActual Inputs: {inputs}, \nExpected Products:{[expected_products_0, expected_products_1]}, \nActual Products:{products}\nline#:{currentframe().f_lineno}')


    left_side_of_reaction = expected_inputs_0.copy()
    right_side_of_reaction = expected_products_0.copy()
    right_side_of_reaction.update(expected_products_1)

    balance_reaction(left_side_of_reaction, right_side_of_reaction)

    if((left_side_of_reaction != {'A' : 7}) or (right_side_of_reaction != {'FUEL' : 1})):
        print(f'Unit test failed. \nExpected LHS:A : 7, \nActual LHS: {left_side_of_reaction}, \nExpected RHS:FUEL : 1, \nActual RHS:{right_side_of_reaction}\nline#:{currentframe().f_lineno}')

    left_side_of_reaction = expected_inputs_0.copy()
    left_side_of_reaction['E'] += 1

    right_side_of_reaction = expected_products_0.copy()
    right_side_of_reaction.update(expected_products_1)

    balance_reaction(left_side_of_reaction, right_side_of_reaction)

    if((left_side_of_reaction != {'A' : 7, 'E' : 1}) or (right_side_of_reaction != {'FUEL' : 1})):
        print(f'Unit test failed. \nExpected LHS: A : 7, E : 1, \nActual LHS: {left_side_of_reaction}, \nExpected RHS:FUEL : 1\nActual RHS:{right_side_of_reaction}\nline#:{currentframe().f_lineno}')





unit_tests()

# filename = "Day14_test_input.txt"
filename = "Day14_input.txt"
solve_day14_puzzle(filename, False)


