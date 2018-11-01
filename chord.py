'''
Implemented from the research paper:
    Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications
    Ion Stoica, Robert Morris, David Liben-Nowell, David R. Karger, M. Frans Kaashoek, Frank Dabek, Hari Balakrishnan
'''

list_of_nodes = []
'''
Define the node class and its functionalities
'''
class node_class:
    node_value = None
    pre = None
    suc = None
    def __init__(self, node_val, length):
        self.node_value = node_val
        self.pre = None
        self.suc = node_val
        self.finger_table = []
        for i in range(0, length):
            self.finger_table.append(node_val)

    # update the successor of a node
    def find_successor(self,id):
        # print("find successor")
        # print("id ",id, " ", self.node_value, " ", self.suc)
        if (self.node_value < id <= self.suc) or (self.node_value > self.suc and (self.node_value < id < 2**hash_size or 0 <= id < self.suc)):
            return self.suc
        elif self.node_value == self.suc and self.suc == id:
            return id
        else:
            n1 = self.closest_preceding_node(id)
            n1_node = get_object_from_value(n1)
            return n1_node.find_successor(id)

    def closest_preceding_node(self, id):
        for i in range(hash_size-1,-1,-1):
            if (self.node_value < self.finger_table[i] < id) or (self.node_value > id and (self.node_value < self.finger_table[i] < 2**hash_size or 0 <= self.finger_table[i] < id )):
                return self.finger_table[i]
        return self.node_value

    def join(self,n1):
        self.pre = None
        n1_node = get_object_from_value(n1)
        self.suc = n1_node.find_successor(self.node_value)

    def stabilize(self):
        '''
        // called periodically. verifies n’s immediate
        // successor, and tells the successor about n.
        n.stabilize()
            x = successor.predecessor;
            if (x ∈ (n,successor))
                successor = x;
            successor.notify(n);
        '''
        suc_node = get_object_from_value(self.suc)
        x = suc_node.pre
        if x != None:
            if (self.node_value < x < self.suc) or (self.node_value > self.suc and (self.node_value < x < 2**hash_size or 0 <= x < self.suc)):
                self.suc = x
                suc_node = get_object_from_value(self.suc)
        suc_node.notify(self.node_value)

    def notify(self,n1):
        '''
        // n1 thinks it might be our predecessor.
        n.notify(n1)
            if (predecessor is nil or n1 ∈ (predecessor, n))
                predecessor = n1;
        '''
        print("in notify")
        if self.pre == None or ((self.pre < n1 < self.node_value) or (self.pre > self.node_value and (self.pre < n1 < 2**hash_size or 0 <= n1 < self.node_value))):
            print("setting pre to", n1)
            self.pre = n1

    def fix_fingers(self):
        '''
        // called periodically. refreshes finger table entries.
        // next stores the index of the next finger to fix.
        n.fix fingers()
            next = next + 1 ;
            if (next > m)
                next = 1 ;
            finger[next] = find successor(n + 2^(next−1));
        '''
        for i in range(0,hash_size):
            self.finger_table[i] = self.find_successor((self.node_value + 2**i)%(2**hash_size))

    def check_predecessor(self):
        for object in list_of_nodes:
            if object.pre == self.pre:
                return
        self.pre = None


'''
The main program
'''

def get_object_from_value(n):
    for obj in list_of_nodes:
        if obj.node_value == n:
            return obj
    return None

import sys

input1 = sys.argv[1]
if input1 == '-i':
    file_name = sys.argv[2]
    hash_size = sys.argv[3]
else:
    hash_size = input1
# convert hash_size to integer
try:
    hash_size = int(hash_size)
except:
    raise Exception("\n\n Wrong Input \n\n")


input_from_file = False
if 'file_name' in globals():
    # we have a file input
    print(file_name)
    lines = [line.rstrip('\n') for line in file]
    input_from_file = True
    line_index = 0


max_nodes = 0
while True:
    if input_from_file:
        if line_index >= len(lines):
            break
        curr_input = lines[line_index]
        line_index += 1
    else:
        # take input manually from the user
        curr_input = input()

    '''
    Switch Cases:
    '''
    if curr_input == "end":
        # Exit from the program
        break
    elif curr_input.startswith("add"):
        max_nodes += 1
        if max_nodes > 2**hash_size:
            printk("Maximum number of nodes reached. Can't add any more")
        else:
            node_val = int((curr_input.split())[1])
            new_node = node_class(node_val, hash_size)
            list_of_nodes.append(new_node)
            print("Added node ", node_val)

    elif curr_input.startswith("drop"):
        node_val = int((curr_input.split())[1])
        for i, o in enumerate(list_of_nodes):
            if o.node_value == node_val:
                del list_of_nodes[i]
                break

    elif curr_input.startswith("join"):
        curr_input = curr_input.split()
        node_1 = int(curr_input[1])
        node_2 = int(curr_input[2])
        get_object_from_value(node_1).join(node_2)


    elif curr_input.startswith("fix"):
        node_val = int((curr_input.split())[1])
        get_object_from_value(node_val).fix_fingers()


    elif curr_input.startswith("stab"):
        node_val = int((curr_input.split())[1])
        get_object_from_value(node_val).stabilize()

    elif curr_input == "list":
        list_of_nodes.sort(key=lambda x: x.node_value)
        print("Nodes: ", end='')
        for node in list_of_nodes:
            print(node.node_value," ", end='')
        print()

    elif curr_input.startswith("showall"):
        for node in list_of_nodes:
            print("Node ", node.node_value, ": suc", node.suc, ", pre", node.pre, ", finger ", end="")
            for finger in node.finger_table:
                print(finger, " ", end="")
            print()
    elif curr_input.startswith("show"):
        node_val = int((curr_input.split())[1])
        node = get_object_from_value(node_val)
        print("Node ", node.node_value, ": suc", node.suc, ", pre", node.pre, ", finger ", end="")
        for finger in node.finger_table:
            print(finger, " ", end="")
        print()
