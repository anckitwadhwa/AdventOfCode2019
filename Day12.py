# from inspect import currentframe
import copy
import math

class XYZObject:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return(f'{self.x}, {self.y}, {self.z}')

    def __eq__(self, other):
        if isinstance(other, XYZObject):
            return((self.x == other.x) and (self.y == other.y) and (self.z == other.z))
        else:
            return False

    def __hash__(self):
        return(hash((self.x, self.y, self.z)))

    def compute_energy(self):
        return(abs(self.x) + abs(self.y) + abs(self.z))


class UniverseState:
    def __init__(self, positions = None, velocities = None):
        self.positions = positions
        self.velocities = velocities


    def __hash__(self):
        hash_value = 0
        for index in range(len(positions)):
            position = self.positions[index]
            velocity = self.velocities[index]

            hash_value = hash((hash_value, hash(position), hash(velocity)))

        return(hash_value)

    def __str__(self):
        return_val = "Universe State\n"
        return_val = return_val + "positions:" + str([str(position) for position in self.positions]) + "\n"
        return_val = return_val + "velocities:" + str([str(velocity) for velocity in self.velocities])

        return(return_val)

def apply_gravity_for_many(positions, velocities, debug_prints = False):

    # if(len(positions) != len(velocities)):
    #     print("Bad input, exiting.", currentframe().f_lineno)
    #     return

    for i in range(len(positions)):
        position1 = positions[i]
        velocity1 = velocities[i]

        for j in range(i, len(positions)):
            position2 = positions[j]
            velocity2 = velocities[j]

            apply_gravity_for_one_pair(position1, position2, velocity1, velocity2, debug_prints)

def apply_gravity_for_one_pair(position1, position2, velocity1, velocity2, debug_prints = False):
    velocity1.x, velocity2.x = apply_gravity_for_one_pair_in_one_direction(position1.x, position2.x, velocity1.x, velocity2.x, debug_prints)
    velocity1.y, velocity2.y = apply_gravity_for_one_pair_in_one_direction(position1.y, position2.y, velocity1.y, velocity2.y, debug_prints)
    velocity1.z, velocity2.z = apply_gravity_for_one_pair_in_one_direction(position1.z, position2.z, velocity1.z, velocity2.z, debug_prints)

def apply_gravity_for_one_pair_in_one_direction(x1, x2, v1, v2, debug_prints = False):
    return_v1 = v1
    return_v2 = v2

    if(x1 > x2):
        return_v1 -= 1
        return_v2 += 1

    elif(x1 < x2):
        return_v1 += 1
        return_v2 -= 1

    return return_v1, return_v2


def apply_velocity_for_many(positions, velocities, debug_prints = False):

    # if(len(positions) != len(velocities)):
    #     print("Bad input, exiting.", currentframe().f_lineno)
    #     return

    for index in range(len(positions)):
        position = positions[index]
        velocity = velocities[index]

        apply_velocity_for_one(position, velocity, debug_prints)

def apply_velocity_for_one(position, velocity, debug_prints = False):

    position.x += velocity.x
    position.y += velocity.y
    position.z += velocity.z



def compute_energy(positions, velocities, debug_prints = False):
    energy = 0
    for index in range(len(positions)):
        position = positions[index]
        velocity = velocities[index]

        energy = energy + (position.compute_energy() * velocity.compute_energy())

    return energy


def zero_out_axes(xyz_objects, axis_to_retain, debug_prints = False):
    for xyz_object in xyz_objects:

        if(axis_to_retain != 0):
            xyz_object.x = 0

        if(axis_to_retain != 1):
            xyz_object.y = 0

        if(axis_to_retain != 2):
            xyz_object.z = 0

def solve_day12_puzzle(universe_state, number_of_steps, debug_prints = False):

    print("*" * 50)
    positions = universe_state.positions
    velocities = universe_state.velocities

    for i in range(number_of_steps):

        apply_gravity_for_many(positions, velocities, debug_prints)
        apply_velocity_for_many(positions, velocities, debug_prints)

        print(f'step{i}')
        if(debug_prints):
            print(f'positions: {[str(position) for position in positions]}')
            print(f'velocities: {[str(velocity) for velocity in velocities]}')

    energy = compute_energy(positions, velocities, debug_prints)
    print(f'energy: {energy}')

def solve_day12_puzzle_b(original_universe_state, debug_prints = False):

    print("*" * 50)

    has_repeated = False
    original_positions = original_universe_state.positions
    original_velocities = original_universe_state.velocities
    steps_per_axis = []
    for axis in range(0, 3):
        positions = copy.deepcopy(original_positions)
        velocities = copy.deepcopy(original_velocities)
        universe_state = UniverseState(positions, velocities)
        all_hash_values = set()
        all_hash_values.add(hash(universe_state))



        zero_out_axes(positions, axis, debug_prints)
        zero_out_axes(velocities, axis, debug_prints)
        print(str(universe_state))

        has_repeated = False
        step = 0
        while(has_repeated != True):

            if(debug_prints and (step % 100 == 0)):
                print(f'At step#:{step}')

            apply_gravity_for_many(positions, velocities, debug_prints)
            apply_velocity_for_many(positions, velocities, debug_prints)

            step += 1
            all_hash_values.add(hash(universe_state))
            if(len(all_hash_values) != step + 1):
                has_repeated = True

                if(debug_prints):
                    print(str(universe_state))

                continue

        steps_per_axis.append(step)
        print(f'steps it took:{step}')

    lcm_of_steps = int(1)
    for step in steps_per_axis:
        gcd = math.gcd(lcm_of_steps, (step-1))
        lcm_of_steps = int((lcm_of_steps * (step-1) ) / gcd)

    print(f'all steps:{steps_per_axis}\nLCM: {lcm_of_steps}')

# puzzle_test_input =
# <x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>
# positions = [XYZObject(-1, 0, 2), XYZObject(2, -10, -7), XYZObject(4, -8, 8), XYZObject(3, 5, -1)]

# puzzle_input =
# <x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>
positions = [XYZObject(-8, -10, 0), XYZObject(5, 5, 10), XYZObject(2, -7, 3), XYZObject(9, -8, -3)]

# puzzle_input =
#     <x=-5, y=6, z=-11>
#     <x=-8, y=-4, z=-2>
#     <x=1, y=16, z=4>
#     <x=11, y=11, z=-4>

# positions = [XYZObject(-5, 6, -11), XYZObject(-8, -4, -2), XYZObject(1, 16, 4), XYZObject(11, 11, -4)]

velocities = [XYZObject(0, 0, 0), XYZObject(0, 0, 0), XYZObject(0, 0, 0), XYZObject(0, 0, 0)]

print(f'positions: {[str(position) for position in positions]}')
print(f'velocities: {[str(velocity) for velocity in velocities]}')

# solve_day12_puzzle(UniverseState(positions, velocities), 1000, False)
solve_day12_puzzle_b(UniverseState(positions, velocities), True)
