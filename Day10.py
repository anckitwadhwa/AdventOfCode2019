import math

def get_number_of_asteroids_visible(asteroid_coordinates, debug_prints = False):
    number_of_asteroids = len(asteroid_coordinates)

    # start with all asteroids marked as visible to each other
    asteroids_visible = [None] * number_of_asteroids

    for i in range(0, number_of_asteroids):
        asteroids_visible[i] = [1] * number_of_asteroids

    # start algorithm
    for i in range(0, number_of_asteroids-2):
        if(debug_prints):
            print(f'For asteroid {i}, initial asteroids_visible: {asteroids_visible[i]}')

        coordinates1 = asteroid_coordinates[i]

        for j in range (i+1, number_of_asteroids - 1):

            if (asteroids_visible[i][j] == 0):
                continue


            coordinates2 = asteroid_coordinates[j]
            line_equation = get_line_equation(coordinates1, coordinates2, False)

            if(debug_prints):
                print("*" * 100)
                print(f'For asteroids at {coordinates1}, {coordinates2}, line equation:{line_equation}')

            for k in range (j+1, number_of_asteroids):

                if (asteroids_visible[i][k] == 0):
                    continue

                coordinates3 = asteroid_coordinates[k]

                if (is_on_line(coordinates3, line_equation, False)):
                    asteroids_visible[i][k] = 0
                    asteroids_visible[k][i] = 0

                    if(debug_prints):
                        if(debug_prints):
                            print(f'Asteroids at {coordinates3}, is on the line')

        if(debug_prints):
            print(f'For asteroid {i}, final asteroids_visible: {asteroids_visible[i]}')
    return(asteroids_visible)

def get_line_equation(coordinates1, coordinates2, debug_prints = False):

    if (coordinates2[0] != coordinates1[0]):
        m = (coordinates2[1] - coordinates1[1]) / (coordinates2[0] - coordinates1[0])
        b = coordinates2[1] - m * coordinates2[0]

    else:
        m = math.inf
        b = coordinates2[0]

    line_equation = {'m': m, 'b':b}
    if debug_prints:
        print(line_equation)
    return(line_equation)

def is_on_line(coordinates, line_equation, debug_prints = False):

    m = line_equation["m"]
    b = line_equation["b"]
    y_computed = math.inf

    return_value = False

    if (m != math.inf):
        y_computed = line_equation["m"] * coordinates[0] + line_equation["b"]
        return_value = math.isclose(coordinates[1], y_computed)
    else:
        return_value = math.isclose(coordinates[0], b)

    if (debug_prints):
        print(f'For {line_equation} and x = {coordinates[0]}, computed y = {y_computed}, actual y = {coordinates[1]}')


    return (return_value)

def get_asteroid_coordinates(asteroid_grid, debug_prints = False):
    asteroid_coordinates = []
    for y, grid_row in enumerate(asteroid_grid):

        x = grid_row.find("#", 0)
        while(x != -1):

            # if (debug_prints):
            #     print("Current coordinate, current grid_row: ", x, y, grid_row)

            asteroid_coordinates.append([x, y])
            x = grid_row.find("#", x + 1)

    return(asteroid_coordinates)



def solve_day10_puzzle(grid_string, debug_prints = False):

    asteroid_coordinates = get_asteroid_coordinates(grid_string, debug_prints)
    asteroids_visible = get_number_of_asteroids_visible(asteroid_coordinates, debug_prints)

    if (debug_prints):
        print(f'raw data: {asteroids_visible}')
        print(f'Summed data: {[sum(i)-1 for i in zip(*asteroids_visible)]}')

    asteroids_visible_summed = [sum(i)-1 for i in zip(*asteroids_visible)]


    max_visible_asteroids = max(asteroids_visible_summed)
    index_of_monitoring_station = asteroids_visible_summed.index(max_visible_asteroids)
    monitoring_station_coordinates = asteroid_coordinates[index_of_monitoring_station]

    print(max_visible_asteroids, monitoring_station_coordinates)


    # begin part 2, I only have a partial algorithm here
    special_vaporization_number = 200
    if(special_vaporization_number > max_visible_asteroids):
        # this will require multiple rotations, and my algorithm doesnt handle that. Just say sorry
        print("Sorry, algorithm not available for this case.kthxbai")

    asteroids_visible_from_station = asteroids_visible[index_of_monitoring_station]
    # for all visible asteroids, compute angle between the vertical and the line connecting them
    x1 = asteroid_coordinates[index_of_monitoring_station][0]
    y1 = asteroid_coordinates[index_of_monitoring_station][1]

    angles = [360] * len(asteroids_visible_from_station)
    for i in range (0, len(asteroids_visible_from_station)):
        #skip not visible asteroids and the station itself
        if((asteroids_visible_from_station[i] == 0) or (i == index_of_monitoring_station)):
            continue
        else:

            x2 = asteroid_coordinates[i][0]
            y2 = asteroid_coordinates[i][1]

            current_angle = math.degrees(math.atan2((x2-x1), (y1-y2)))

            while (current_angle < 0):
                current_angle += 360

            angles[i] = current_angle

    # angles_copy = angles.copy()
    destruction_order = []
    min_angle = min(angles)
    while(min_angle < 360):
        i = angles.index(min_angle)
        destruction_order.append(asteroid_coordinates[i])

        angles[i] += 360
        min_angle = min(angles)


    desired_indices = [1, 2, 3, 10, 20, 50, 100, 150, 199, 200, 201]
    print([destruction_order[i - 1] for i in desired_indices])

def read_puzzle_input_from_file(filename):
    f = open(filename, "r")
    puzzle_input = list(f.read().splitlines())

    return(puzzle_input)



grid_string = read_puzzle_input_from_file("day10_input.txt")
# grid_string = read_puzzle_input_from_file("day10_test_input.txt")
# asteroid_coordinates = get_asteroid_coordinates(grid_string, False)

# line_equation = get_line_equation([2, 0], [2, 1], True)
# print(is_on_line([2, 100], line_equation, True))

# print(asteroid_coordinates)
# print(len(asteroid_coordinates))
solve_day10_puzzle(grid_string, False)
