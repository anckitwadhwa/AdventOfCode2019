class Node:
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.children = []

        if (parent != None):
            self.distance_from_root = parent.distance_from_root + 1

            parent.children.append(self)

        else:
            self.distance_from_root = 0

    def __str__(self):
        self_as_string = self.name + "," + str(self.distance_from_root) + "("

        for child in self.children:
            self_as_string += str(child) + "; "

        self_as_string += ") "
        return(self_as_string)


    def update_distance_from_root(self, starting_distance = 0):

        self.distance_from_root = starting_distance

        for child in self.children :
            child.update_distance_from_root(self.distance_from_root + 1)



    def find_node(self, name):
        return_node = None

        if (self.name == name):
            return_node = self

        else:
            for child in self.children:
                return_node = child.find_node(name)

                if (return_node != None):
                    break

        return (return_node)

    def distance_sum(self):
        sum = 0

        sum += self.distance_from_root
        for child in self.children:
            sum += child.distance_sum()

        return sum

    def get_earliest_ancestor(self):
        return_node = self

        if (self.parent != None):
            return_node = self.parent.get_earliest_ancestor()

        return(return_node)

    def link_child (self, child_node):
        self.children.append(child_node)
        child_node.parent = self

def handle_parent_child_input(parent_name, child_name, root_node, orphan_list):

    debug_prints = False


    if (parent_name == "63N" or child_name == "63N"):
        debug_prints = True

    if (debug_prints):
        print ("handling parent, child: ", parent_name, child_name)
        print ("*" * 40)
        print ("initial orphan_list: ", [str(child) for child in orphan_list])
        print ("*" * 40)

    #get or create new parent
    if(root_node == None):
        parent_node = Node(parent_name)
        root_node = parent_node
    else:
        parent_node = root_node.find_node(parent_name)

    if (parent_node == None):
        parent_node = find_node_in_list(orphan_list, parent_name)

        if (parent_node == None):
            parent_node = Node(parent_name)
            orphan_list.append(parent_node)

    #get or create new child
    #note child can either be root_node or exist in unparanted list

    if(root_node.name == child_name):
        child_node = root_node
        #if child is the root node, implies that parent is in the unparented list, and we need to remove it from there
        earliest_ancestor = parent_node.get_earliest_ancestor()
        print (parent_name, child_name, str(earliest_ancestor))
        orphan_list.remove(earliest_ancestor)

        parent_node.link_child(child_node)
        root_node = earliest_ancestor

    else:
        child_node = find_node_in_list(orphan_list, child_name)

        if (child_node != None):
            parent_node.link_child(child_node)
            orphan_list.remove(child_node)

        else:
            child_node = Node(child_name, parent_node)

    if (debug_prints):
        print ("resulting orphan_list: ", [str(child) for child in orphan_list])

    return (root_node)


def find_node_in_list(node_list, name):

    #print("Looking for ", name, " in ", [str(node) for node in node_list])
    return_node = None
    for node in node_list:
        return_node = node.find_node(name)
        if (return_node != None):
            break

    #print("Found: ", str(return_node))
    return return_node


def nearest_common_ancestor(node1, node2):
    node1.get_earliest_ancestor().update_distance_from_root()
    node2.get_earliest_ancestor().update_distance_from_root()

    nearest_common_ancestor = None
    while (nearest_common_ancestor == None):

        if (node1 != node2):

            if (node1.distance_from_root > node2.distance_from_root):
                node1 = node1.parent
            else:
                node2 = node2. parent
        else:
            nearest_common_ancestor = node1

    return(nearest_common_ancestor)


def get_parent_child_from_input(input):
    names = list(input.split(")"))
    #TODO: error check

    parent = names[0]
    child = names[1]

    #print(parent, child)
    return(parent, child)

def solve_puzzle(input_list):

    root_node = None

    orphan_list = []

    for input in input_list:
        #print (input)

        parent_name, child_name = get_parent_child_from_input(input)
        updated_root_node = handle_parent_child_input(parent_name, child_name, root_node, orphan_list)
        root_node = updated_root_node

        #print("root_node: ", str(root_node))
        #print("unparented_children: ", ([str(child) for child in unparented_children]))

    root_node.update_distance_from_root()

    print("root_node: ", str(root_node))
    print("orphan_list: ", ([str(child) for child in orphan_list]))
    print("length of orphan_list: ", len(orphan_list))
    print((root_node.distance_sum()))

    node_you = root_node.find_node("YOU")
    node_san = root_node.find_node("SAN")

    distance_you = node_you.distance_from_root
    distance_san = node_san.distance_from_root

    nearest_ancestor = nearest_common_ancestor(node_you, node_san)

    distance_ancestor = nearest_ancestor.distance_from_root

    orbital_transfers = (distance_you - distance_ancestor) + (distance_san - distance_ancestor) - 2

    print ("distance you, distance san, orbital transfers: ", distance_you, distance_san, orbital_transfers)


def unit_tests():
    ancestor = Node("ancestor")
    #print("ancestor:", ancestor)

    child = Node("child1", ancestor)
    #print("ancestor:", ancestor)

    child = Node("child2", ancestor)
    #print("ancestor:", ancestor)

    child = Node("child3", ancestor)
    #print("ancestor:", ancestor)

    grand_child = Node("grandchild", child)
    print("with 1 grandchild:", ancestor)

    grand_child = Node("grandchild2", child)
    print("with 2 grandchildren:", ancestor)

    node = ancestor.find_node("child1")
    offspring_of_node = Node("grandchild3", node)
    print("with 3 grand children:", ancestor)


    node = ancestor.find_node("grandchild2")
    node2 = ancestor.find_node("grandchild")
    nearest_ancestor = nearest_common_ancestor(node, node2)

    print("ancestor: ", str(ancestor))
    print ("nearest ancestor of grandchild2, grandchild: ", str(nearest_ancestor))

#unit_tests()

#f = open("Day6_test_input.txt", "r")
f = open("Day6_input.txt", "r")
puzzle_input = list(f.read().splitlines())
#print (puzzle_input)

solve_puzzle(puzzle_input)





