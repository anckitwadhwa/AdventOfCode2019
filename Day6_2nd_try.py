def get_orbiter_orbitee_from_input(input):
    names = list(input.split(")"))
    #TODO: error check

    orbitee = names[0]
    orbiter = names[1]

    #print(orbitee, orbiter)
    return(orbitee, orbiter)



def solve_puzzle(input):
    orbitee, orbiter = get_orbiter_orbitee_from_input(input)

    stellar_bodies.index()







f = open("Day6_test_input.txt", "r")
#f = open("Day6_input.txt", "r")
puzzle_input = list(f.read().splitlines())
#print (puzzle_input)

solve_puzzle(puzzle_input)
