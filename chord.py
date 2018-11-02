'''
Implemented from the research paper:
    Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications
    Ion Stoica, Robert Morris, David Liben-Nowell, David R. Karger, M. Frans Kaashoek, Frank Dabek, Hari Balakrishnan
'''
import time
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
        if self.suc <= self.node_value:
            if (self.node_value < id <= (2**hash_size) -1) or (0 <= id <= self.suc):
                return self.suc
            else:
                n1 = self.closest_preceding_node(id)
                n1_node = get_object_from_value(n1)
                return n1_node.find_successor(id)
        else:
            if (self.node_value < id <= self.suc):
                return self.suc
            else:
                n1 = self.closest_preceding_node(id)
                # print("preceding node",n1)
                n1_node = get_object_from_value(n1)
                return n1_node.find_successor(id)

    def closest_preceding_node(self, id):
        for i in range(hash_size-1,-1,-1):
            if (self.node_value < id):
                if (id > self.finger_table[i] > self.node_value):
                    return self.finger_table[i]
            else:
                if ((2**hash_size) -1 >= self.finger_table[i] > self.node_value) or (0 <= self.finger_table[i] < self.node_value):
                    return self.finger_table[i]
        return self.node_value

    def join(self,n1):
        self.pre = None
        n1_node = get_object_from_value(n1)
        temp = n1_node.find_successor(self.node_value)
        self.suc = temp
        self.finger_table[0] = temp

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
        if not any(x.node_value == self.pre for x in list_of_nodes):
            self.pre = None
        if not any(x.node_value == self.suc for x in list_of_nodes):
            self.suc = self.node_value
        suc_node = get_object_from_value(self.suc)
        # print("------------------------------", suc_node)
        if suc_node == None:
            x = None
        else:
            x = suc_node.pre
        if x != None:
            if self.suc <= self.node_value:
                if (self.node_value < x <= (2**hash_size) - 1) or (0 <= x < self.suc):
                    self.suc = x
                    self.finger_table[0] = x
                    suc_node = get_object_from_value(self.suc)
            else:
                if (self.node_value < x < self.suc):
                    self.suc = x
                    self.finger_table[0] = x
                    suc_node = get_object_from_value(self.suc)
        if suc_node != None:
            suc_node.notify(self.node_value)

    def notify(self,n1):
        '''
        // n1 thinks it might be our predecessor.
        n.notify(n1)
            if (predecessor is nil or n1 ∈ (predecessor, n))
                predecessor = n1;
        '''
        if self.pre == None:
            self.pre = n1
        elif self.node_value <= self.pre:
            if (self.pre < n1 <= (2**hash_size) - 1) or (0 <= n1 < self.node_value):
                self.pre = n1
        else:
            if self.pre < n1 < self.node_value:
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
            temp = self.find_successor((self.node_value + 2**i)%(2**hash_size))
            self.finger_table[i] = temp
            if i == 0:
                self.suc = temp

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
isWrongInput = False
input1 = sys.argv[1]
if input1 == '-i':
    file_name = sys.argv[2]
    hash_size = sys.argv[3]
else:
    hash_size = input1
# convert hash_size to integer
try:
    hash_size = int(hash_size)
    if (hash_size<=0):
        a = 1/0
    if (type(hash_size) != type(1)):
        a = 1/0
except:
    print("\nERROR: invalid hash_size", hash_size)
    isWrongInput = True

input_from_file = False
if 'file_name' in globals():
    # we have a file input
    print(file_name)
    file = open(file_name, 'r')
    lines = file.readlines()
    input_from_file = True
    line_index = -1

while True:
    if isWrongInput:
        break
    if input_from_file:
        curr_input = lines[line_index]
        line_index += 1
        if line_index >= len(lines):
            break
    else:
        # take input manually from the user
        curr_input = input()
    '''
    Switch Cases:
    '''
    try:
        if curr_input == "end":
            # Exit from the program
            break
        elif curr_input.startswith("add"):
            node_val = int((curr_input.split())[1])
            if any(x.node_value == node_val for x in list_of_nodes):
                print("ERROR: Node",node_val,"exists")
            if node_val < 0 or node_val >= 2**hash_size:
                print("ERROR: node id must be in [0,"+str(2**hash_size)+")")
            else:
                new_node = node_class(node_val, hash_size)
                list_of_nodes.append(new_node)
                print("Added node", node_val)

        elif curr_input.startswith("drop"):
            node_val = int((curr_input.split())[1])
            deleted_node = None
            for i, o in enumerate(list_of_nodes):
                if o.node_value == node_val:
                    deleted_node = o.node_value
                    # list_of_nodes[(i-1)%(len(list_of_nodes))].suc = list_of_nodes[i].suc
                    # list_of_nodes[(i-1)%(len(list_of_nodes))].finger_table[0] = list_of_nodes[i].suc
                    # list_of_nodes[(i-1)%(len(list_of_nodes))].pre = list_of_nodes[i].pre
                    del list_of_nodes[i]
                    break
            print("Dropped node", node_val)

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

        elif curr_input.startswith("list"):
            list_of_nodes.sort(key=lambda x: x.node_value)
            print("Nodes: ", end='')
            temp_list = []
            for node in list_of_nodes:
                temp_list.append(node.node_value)
            print(*temp_list, sep = ", ")

        elif curr_input.startswith("showall"):
            for node in list_of_nodes:
                print("Node " + str(node.node_value) + ": suc "+ str(node.suc) + ", pre "+str(node.pre)+", finger ", end="")
                print(*node.finger_table, sep=", ")
        elif curr_input.startswith("show"):
            node_val = int((curr_input.split())[1])
            node = get_object_from_value(node_val)
            if node == None:
                print("ERROR: Node",node_val,"does not exist")
            else:
                print("Node " + str(node.node_value) + ": suc "+ str(node.suc) + ", pre "+str(node.pre)+", finger ", end="")
                print(*node.finger_table, sep=", ")
    except ValueError:
        print("ERROR: invalid integer", (curr_input.split())[1])
    except:
        print("ERROR: Wrong Input")
