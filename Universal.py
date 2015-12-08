# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:19:11 2015

@author: sara
"""

# local package import
import random
from copy import deepcopy
from CondensedList import condensed_list_b
from GenomePath import debruijn2

# Find a universal string given k.

def universal(k):
    
    #generate list of possible k-mers
    kmers = condensed_list_b(k)
    
    # Use De Bruijn approach to create adjacency dictionary from list of k-mers
    adj_dict = debruijn2(kmers)    
    
    # Dictionary that tracks remaining edges (those not yet taken),
    # initialized as the input adjacency dict
    remain_d = deepcopy(adj_dict)
    
    # Randomly select a starting node
    node_i = random.choice(range(len(adj_dict)))
    node = adj_dict.items()[node_i][0]
    
    # Initialize string with the starting node
    u_string = node
#    print u_string

    # Continue as long as there are edges that remain untaken    
    while len(remain_d) > 0:

        # Check if any adjacencies remain for the node and if so, how many        
        value = remain_d.get(node)
#        print "value is: ",
#        print value
#        print "node is: "+node
        # If the node has no unused edges, we must be back at V0 (since the 
        # graph is balanced), but we also know there are remaining edges out 
        # there. We need to expand the circle until it encompasses all nodes.
        if value == None:
#            print "Value is none"
            # To do so, iterate through the current "cycle" until we find a 
            # node with an unused edge. Make that the new V0.
            for i, n in enumerate(u_string):
                n = u_string[i:i+k-1]
                if remain_d.get(n) > 0:
                    node = n
                    u_string = u_string[i:]+u_string[:i+k-1]
#                    print "new node is: "+str(node)
#                    print "u_string now is:"+u_string
                    break
                
        # If the node has a single unused edge, simply use it to continue the 
        # cycle by adding it to the list 'cycle' and removing it from the dict
        elif len(value) == 1:   
#            print "Value is one"  
            node = remain_d.pop(node)[0]
            u_string = u_string+node[-1]
#            print u_string
            
        # If the node has multiple unused edges, randomly select one to add to 
        # the cycle and remove it out from the node's list of adjacencies.
        elif len(value) > 1:
#            print "Value is greater than one"  
            random_i = random.randrange(len(value))
            pos_nodes = remain_d[node]
            new_node = pos_nodes.pop(random_i) 
            remain_d[node] = pos_nodes
            node = new_node
            u_string = u_string+node[-1]
#            print u_string
            
    # Since the string is a circle, the last k-1 digits will be a repeat of the 
    # first k-1 digits and thus can be removed.
    return u_string[:-(k-1)]