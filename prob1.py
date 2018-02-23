
import numpy as np

class VariableNode:
    def __init__(self, name):
        self.name = name

class FactorNode:
    def __init__(self, name, parents, cpt):
        self.name = name
        self.parents = parents
        self.cpt = cpt

factor_to_node = {}
node_to_factor = {}


def get_message_factor_to_node(factor, node):
    #not sum over node of factor into all other stuff that reached here
        
    p = factor_nodes[factor].parents
    for i in p:
        if(i == node):
            tup = (1, 1)
            key = (factor, node)
            factor_to_node[key] = tup
            return
    
    tup_list = []
    for j in node_to_factor.keys():
        if(j[1] == factor and j[0] != factor):
            tup_list.append(node_to_factor[j])

    f = factor_nodes[factor]
    if(len(tup_list) == 0):

        #print (f.cpt)
        #v = 1.0 - f.cpt
        tup = (f.cpt, (1 - f.cpt))
        key = (factor, node)
        factor_to_node[key] = tup
        return

    elif(len(tup_list) == 1):
        #point to point
        tup = f.cpt
        tup1 = tup_list[0]
        val1 = 0
        for t in tup:
            if(t[0] == 't'):
                val1 = val1 + (t[1] * tup1[0])
            elif(t[0] == 'f'):
                val1 = val1 + (t[1] * tup1[1])
        key = (factor, node)
        tup2 = (val1, 1 - val1)
        factor_to_node[key] = tup2
        return
    
    val1 = 0
    tup1 = tup_list[0]
    tup2 = tup_list[1]
    
    for tup in f.cpt:
        #print (tup)
        if(tup[0] == 't' and tup[1] == 't'):
            val1 = val1 + (tup[2] * tup1[0] * tup2[0])                                        
        elif(tup[0] == 't' and tup[1] == 'f'):
            val1 = val1 + (tup[2] * tup1[0] * tup2[1])
        elif(tup[0] == 'f' and tup[1] == 't'):
            val1 = val1 + (tup[2] * tup1[1] * tup2[0])
        elif(tup[0] == 'f' and tup[1] == 'f'):
            val1 = val1 + (tup[2] * tup1[1] * tup2[1])
    key = (factor, node)
    tup = (val1, 1 - val1)
    factor_to_node[key] = tup
                
def get_message_node_to_factor(node, factor):
    found = 0
    j = []
    for i in factor_to_node.keys():
        if(i[1] == node and i[0] != factor):
            found = found + 1
            j.append(i[0])
    if(found == 0):
        key = (node, factor)
        node_to_factor[key] = (1,)
    else:
        if(found == 1):
            key = (node, factor)
            tup = factor_to_node[j[0], node]
            node_to_factor[key] = tup
        else:
            #point to point multiplication
            #print (tup1, tup2)
            length = len(j)
            if(found == 2 or found == 3):
                tup1 = factor_to_node[j[length - 2], node]
                tup2 = factor_to_node[j[length - 1], node]
                mult = []
                for i in range(2):
                    val1 = tup1[i]*tup2[i]
                    mult.append(val1)
                tup3 = (mult[0], mult[1])
                key = (node, factor)
                node_to_factor[key] = tup3

def get_marginals():
    for i in range(len(nodes)):
        marginal = factor_to_node[i, i][0] * node_to_factor[i, i][0]
        print ("i = ", i, "marginal = ", marginal)
    


nodes = [0, 1, 2, 3, 4]
print (nodes)

variable_nodes = []
for i in nodes:
    a = VariableNode(i)
    variable_nodes.append(a)

all_cpts = []

burglary = (0.001)
all_cpts.append(burglary)

earthquake = (1)
all_cpts.append(earthquake)

alarm = (('t', 't', 0.95), ('t', 'f', 0.94), ('f', 't', 0.29), ('f', 'f', 0.001))
all_cpts.append(alarm)

johncalls = (('t', 0.90), ('f', 0.05))
all_cpts.append(johncalls)

marycalls = (('t', 0.70), ('f', 0.01))
all_cpts.append(marycalls)

parents = {}
parents[0] = []
parents[1] = []
parents[2] = [0, 1]
parents[3] = [2]
parents[4] = [2]


factor_nodes = []
for i in range (len(nodes)):
    a = FactorNode(nodes[i], parents[nodes[i]], all_cpts[i])
    factor_nodes.append(a)

'''
0 = burglary
1 = earthquake
2 = alarm
3 = johncalls
4 = marycalls
'''


for i in factor_nodes:    
    print (i.name)
    print (i.parents)
    print (i.cpt)


connect_factors = {}
connect_nodes = {}
#factors
connect_factors[0] = [0]
connect_factors[1] = [1]
connect_factors[2] = [0, 1, 2]
connect_factors[3] = [2, 3]
connect_factors[4] = [2, 4]
#nodes
connect_nodes[0] = [0, 2]
connect_nodes[1] = [1, 2]
connect_nodes[2] = [2, 3, 4]
connect_nodes[3] = [3]
connect_nodes[4] = [4]

#fa, fb, fc, fd, fe, x1, x2, x3, x4, x5
msgs_received = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
msgs_to_be_send = [1, 1, 3, 2, 2, 2, 2, 3, 1, 1]

receive_from_factor = np.zeros((5, 5))
receive_from_node = np.zeros((5, 5))

messages_factor_to_node = np.zeros((5, 5))
messages_node_to_factor = np.zeros((5, 5))

for i in range(5):
    #print (msgs_to_send)
    #print (msgs_received)
    print ("Step = ", i)
    temp_send = []
    temp_receive = []
    index_tup_factor = []
    index_tup_node = []

    flag = 0
    
    for j in range (10):
        temp_index1 = []
        temp_index2 = []
        #print("once = ", j)
        #print (msgs_to_send[j], "and", msgs_received[j])
        if((msgs_to_be_send[j] - msgs_received[j]) == 1):
            flag = 1
            #print ("value of j = ", j)
            temp_send.append(j)
            if(j < 5):
                for iter_factor in connect_factors[j]:
                    if(receive_from_node[j][iter_factor] == 0):
                        print ("send from factor", j, "to node ", iter_factor)
                        get_message_factor_to_node(j, iter_factor) 
                        temp_receive.append(iter_factor+5)
                        tup = (iter_factor, j)
                        index_tup_factor.append(tup)
                        #receive_from_factor[iter_factor][j] = 1
            else:
                k = j - 5
                for iter_node in connect_nodes[k]:
                    if(receive_from_factor[k][iter_node] == 0):
                        print ("send from node ", k, "to factor ", iter_node)
                        get_message_node_to_factor(k, iter_node)
                        temp_receive.append(iter_node)
                        tup = (iter_node, k)
                        index_tup_node.append(tup)
                        #receive_from_node[iter_node][k] = 1
    if(flag == 0):
        for j in range(10):
            if(j < 5):
                if(msgs_received[j] == len(connect_factors[j])):
                    for iter_factor in connect_factors[j]:
                        if(receive_from_factor[iter_factor][j] != 1):
                            print("send from factor ", j, "to node ", iter_factor)
                            get_message_factor_to_node(j, iter_factor)
                            
                            temp_send.append(j)
                            temp_receive.append(iter_factor+5)
                            tup = (iter_factor, j)
                            index_tup_factor.append(tup)
            else:
                k = j - 5
                if(msgs_received[j] == len(connect_nodes[k])):
                    for iter_node in connect_nodes[k]:
                        if(receive_from_node[iter_node][k] != 1):
                            print ("send from node ", k, "to factor ", iter_node)
                            get_message_node_to_factor(k, iter_node)
                            temp_send.append(j)
                            temp_receive.append(iter_node)
                            tup = (iter_node, k)
                            index_tup_node.append(tup)
    for i in index_tup_factor:
        receive_from_factor[i[0]][i[1]] = 1
    for i in index_tup_node:
        receive_from_node[i[0]][i[1]] = 1
    
    for j in temp_send:
        msgs_to_be_send[j] = msgs_to_be_send[j] - 1
    for j in temp_receive:
        msgs_received[j] = msgs_received[j] + 1

get_marginals()
