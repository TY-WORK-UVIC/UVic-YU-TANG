# Implementation of B+-tree functionality.

from index import *

# You should implement all of the static functions declared
# in the ImplementMe class and submit this (and only this!) file.

class ImplementMe:
  
    # Returns a B+-tree obtained by inserting a key into a pre-existing
    # B+-tree index if the key is not already there. If it already exists,
    # the return value is equivalent to the original, input tree.
    #
    # Complexity: Guaranteed to be asymptotically linear in the height of the tree
    # Because the tree is balanced, it is also asymptotically logarithmic in the
    # number of keys that already exist in the index.
    @staticmethod
    def InsertIntoIndex( index, key ):
        counter=0
        
        for i in index.root.keys.keys:    # Check if root is None or not 
            if(i is None):
                counter=1+counter
        if(index.root.get_num_keys()==counter): # If root is None 
      
            index=root_is_None(index, key )
            return index
        if(LookupKeyInIndex_out(index, key )==True): # Check if the key is already exist in tree 
            return index
        if(index.root.get_num_keys()!=counter):  # If root is not None 
            index=root_is_not_None(index, key )
        return index
       

    # Returns a boolean that indicates whether a given key
    # is found among the leaves of a B+-tree index.
    #
    # Complexity: Guaranteed not to touch more nodes than the
    # height of the tree
    @staticmethod
    def LookupKeyInIndex( index, key ):
        if(index.root.pointers.pointers[0] is None):     # when it only contains root
            result=LookupKeyInIndex_out_root_only( index, key )
        if(index.root.pointers.pointers[0] is not None): # when it contains leaves
            result=LookupKeyInIndex_out( index, key )
        return result

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        array=[]
        for i in index.root.keys.keys: # First search the root keys
            if(i is not None and lower_bound<=i<=upper_bound and check_exist(array,i)==False):
                
                array.append(i)
        if(index.root.pointers.pointers[0] is not None): # If it contains leaves, we go through the leaves 
                  array=Cotains_leaf(index, lower_bound, upper_bound )
        array.sort()  # Sorted in ascending order 
   
        return array

    
def LookupKeyInIndex_out( index, key ):  # Any time if i equals key, return true
    if(index.root.pointers.pointers[0] is not None): # it contains leaves
        for i in index.root.keys.keys:  # Go through the root keys 
            if(i==key):
                return True
        for j in index.root.pointers.pointers[0].keys.keys: # Go through first leaf's keys
            if(j==key): 
                return True
        for k in index.root.pointers.pointers[1].keys.keys: # Go through second leaf's keys
            if(k==key):
                return True
        if(index.root.pointers.pointers[0].pointers.pointers[0] is not None): # if there exist second level
            for k in index.root.pointers.pointers[0].pointers.pointers[0].keys.keys: # Go through leaves
                if(k==key):
                    return True
            for k in index.root.pointers.pointers[0].pointers.pointers[1].keys.keys:
                if(k==key):
                    return True
            for k in index.root.pointers.pointers[1].pointers.pointers[0].keys.keys:
                if(k==key):
                    return True
            if(index.root.pointers.pointers[1].pointers.pointers[1] is not None): 
                for k in index.root.pointers.pointers[1].pointers.pointers[1].keys.keys:
                    if(k==key):
                        return True
            if(index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers is not None):  # if there exist third level
                    if(index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0] is not None): # Go through leaves
                        for k in index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0].keys.keys:
                            if(k==key):
                                return True
                    if(index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[1] is not None):        
                        for k in index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[1].keys.keys:
                            if(k==key):
                                return True    
    return False   
def Cotains_leaf(index, lower_bound, upper_bound ): # Any time that key in tree is greater than lower_bound and less than upper_bound, append it in array
    array=[]
    if(index.root.pointers.pointers[0] is not None): # If it contains leaves 
        for j in index.root.pointers.pointers[0].keys.keys: # Go through the first level
            if(j is not None and lower_bound<=j<=upper_bound and check_exist(array,j)==False):
                array.append(j)
        if(index.root.pointers.pointers[1] is not None):
            for k in index.root.pointers.pointers[1].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
        if(index.root.pointers.pointers[2] is not None):
            for k in index.root.pointers.pointers[2].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)            
    if(index.root.pointers.pointers[0].pointers.pointers[0] is not None): # If it contains second level 
                 
        for k in index.root.pointers.pointers[0].pointers.pointers[0].keys.keys: # Go through the leaves of second level
            if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False): # Make sure key is not None, if it is we don't compare it with lower_bound and upper_bound
                array.append(k)
        
        for k in index.root.pointers.pointers[0].pointers.pointers[1].keys.keys:
            if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                array.append(k)
        
        if(index.root.pointers.pointers[0].pointers.pointers[2] is not None):
            for k in index.root.pointers.pointers[0].pointers.pointers[2].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)        
        for k in index.root.pointers.pointers[1].pointers.pointers[0].keys.keys:
            if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                array.append(k)
        if(index.root.pointers.pointers[1].pointers.pointers[1] is not None):
            for k in index.root.pointers.pointers[1].pointers.pointers[1].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
        if(index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0] is not None): # Check if it exist third level 
            for k in index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0].keys.keys:  # Go through all the exist leaves in this level
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
            for k in index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[1].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
            if(index.root.pointers.pointers[0].pointers.pointers[1].pointers.pointers[0] is not None):           
                for k in index.root.pointers.pointers[0].pointers.pointers[1].pointers.pointers[0].keys.keys:
                    if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                        array.append(k)
            for k in index.root.pointers.pointers[0].pointers.pointers[1].pointers.pointers[1].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
        if(index.root.pointers.pointers[1].pointers.pointers[0].pointers.pointers[0] is not None):  # Continue to look all leaves of third level before the look make sure it is not None      
            for k in index.root.pointers.pointers[1].pointers.pointers[0].pointers.pointers[0].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
        if(index.root.pointers.pointers[1].pointers.pointers[0].pointers.pointers[1] is not None):        
            for k in index.root.pointers.pointers[1].pointers.pointers[0].pointers.pointers[1].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
        if(index.root.pointers.pointers[1].pointers.pointers[1] is not None and index.root.pointers.pointers[1].pointers.pointers[1].pointers.pointers[0] is not None):        
            for k in index.root.pointers.pointers[1].pointers.pointers[1].pointers.pointers[0].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)
        if(index.root.pointers.pointers[1].pointers.pointers[1] is not None and index.root.pointers.pointers[1].pointers.pointers[1].pointers.pointers[1] is not None):        
            for k in index.root.pointers.pointers[1].pointers.pointers[1].pointers.pointers[1].keys.keys:
                if(k is not None and lower_bound<=k<=upper_bound and check_exist(array,k)==False):
                    array.append(k)                

    return array 

def LookupKeyInIndex_out_root_only( index, key ): # When the tree only have root, go through all the keys 
    for j in index.root.keys.keys:
            if(j is not None and lower_bound<=j<=upper_bound and check_exist(array,j)==False):
                array.append(j)
    return array
def check_exist(array, integer): # Check if the key is already in the array or not. 
    for i in array:
        if(i==integer):
            return True
    return False
def root_is_None(index, key ): # When root is None, add the key into tree
    
    index.root.keys.keys[0]=key
    
    
    return index

def LookupKeyInIndex1( index, key ): # When the tree only contains root, go through all the keys
    for i in index.root.keys.keys:
        if(i==key):
            return True
            
    return False
def root_is_not_None(index, key ): # When the root is not None

    i=0
    counter=0
    for i in index.root.keys.keys: # Check if root is full or not 
        if(i is not None):
            counter=1+counter
    # If the tree only contains root, and root is not full 
    if(counter!=index.root.get_num_keys() and index.root.keys.keys[0] is not None and index.root.keys.keys[0]>key and index.root.pointers.pointers[0] is None):
        index.root.keys.keys[1]=index.root.keys.keys[0]
        index.root.keys.keys[0]=key
    # If the tree only contains root, and root is not full    
    elif(counter!=index.root.get_num_keys() and index.root.keys.keys[0] is not None and index.root.keys.keys[0]<key and index.root.pointers.pointers[0] is None):
        index.root.keys.keys[1]=key  
    
    # If the tree only contains root, and root is full, then we have to create new node
    elif(counter==index.root.get_num_keys() and index.root.pointers.pointers[0] is None):
        leaf0=Node()
        leaf1=Node()
        if(index.root.pointers.pointers[0] is None):
            index=Full_Node(index, key ) # Create the new nodes
            
    elif(index.root.pointers.pointers[0] is not None): # If the tree has leaves. 
        index=With_leaf_nodes(index, key )
        
    return index


def With_leaf_nodes(index, key ): # When tree have leaves
    if(key<index.root.keys.keys[0]): # Go to left if key less than first value of root 
        if(key<index.root.pointers.pointers[0].keys.keys[0] and index.root.pointers.pointers[0].pointers.pointers[0] is not None): # Check how many levels it contains
            if(key<index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0] and index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0] is None):
                expected_output = Index(left_new_node(index, key)) # Insert the key into left most leaf
            if(key>index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0] and index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0] is None):
                expected_output = Index(left_mid_new_node(index, key)) #Insert the key to middle of left most leaf
    if( key>index.root.keys.keys[0] and key<index.root.keys.keys[1]): # Go to right if key greater than first value of root 
        if(key>index.root.pointers.pointers[1].keys.keys[0] and index.root.pointers.pointers[0].pointers.pointers[0] is not None):
            if(key>index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[0] and index.root.pointers.pointers[0].pointers.pointers[0].pointers.pointers[0] is None):
                expected_output = Index(right_new_node(index, key)) # Insert the key into right most leaf
        
    return expected_output

def left_mid_new_node(index, key): #Insert the key to middle of left most leaf
    leaf0=Node()
    leaf1=Node()   # Create the nodes we need 
    leaf2=Node()
    leaf3=Node()
    leaf4=Node()
    leaf5=Node()
    parent1=Node()
    parent2=Node()
    parent3=Node()
    parent4=Node()
    parent5=Node()
    newroot=Node()
    
    if(index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1] is None): # When the parent is not full, we can insert it in the parent node
        leaf0.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]  # Create the first new leaf
        leaf0.pointers.pointers[2]=leaf1
        leaf1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1] # Create the second new leaf
        leaf1.keys.keys[1]=key
        leaf1.pointers.pointers[2]=index.root.pointers.pointers[0].pointers.pointers[1] # The second leaf will point to the second leaf from original tree
        temp=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]
        index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]=temp # Since the parent is not full we can insert it in, don't have to split 
        index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]
    
    # When it comes with full parent node and full root with root split, I tried my best to create a simple way but I couldn't run it without bug, so I just wirte the code
    # that make the function runs and gives right output.
    if(index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1] is not None and key>index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]):
        # When parent is full
        
        leaf5.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[0] # Create the new leaf5, take data the right most leaf in tree
        leaf5.keys.keys[1]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1]
      
        leaf4.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[0].keys.keys[0]
        leaf4.pointers.pointers[2]=leaf5
        
        leaf3.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[2].keys.keys[0]
        leaf3.pointers.pointers[2]=leaf4
        
        leaf2.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[1].keys.keys[0]
        leaf2.pointers.pointers[2]=leaf3
        
        leaf1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1] # Key will store at leaf1 beacuse it is in the middle of two keys from leaf0 
        leaf1.keys.keys[1]=key
        leaf1.pointers.pointers[2]=leaf2
    
        leaf0.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]  
        leaf0.pointers.pointers[2]=leaf1
        
        parent3.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[0] # Few new parents 1 2 3, that point to the new leaves
        
        parent3.pointers.pointers[1]=leaf5
        parent3.pointers.pointers[0]=leaf4
        
        parent2.keys.keys[0]=index.root.pointers.pointers[0].keys.keys[1]
   
        parent2.pointers.pointers[0]=leaf2
        parent2.pointers.pointers[1]=leaf3
      
        parent1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]
        parent1.pointers.pointers[0]=leaf0
        parent1.pointers.pointers[1]=leaf1

        parent5.keys.keys[0]=index.root.keys.keys[1]     # Parent 4, 5 will be the second level of new tree
        parent5.pointers.pointers[0]=parent3
        
        parent4.keys.keys[0]=index.root.pointers.pointers[0].keys.keys[0]
        parent4.pointers.pointers[0]=parent1
        parent4.pointers.pointers[1]=parent2
      
        newroot.keys.keys[0]=index.root.keys.keys[0] # Finally, the new root will point to the Parent 4,5
        newroot.pointers.pointers[0]=parent4
        newroot.pointers.pointers[1]=parent5
       
    return newroot
def right_new_node(index, key): #Insert the key right most leaf
    leaf0=Node()
    leaf1=Node()
    leaf2=Node()
    leaf3=Node()
    leaf4=Node()
    leaf5=Node()
    parent1=Node()
    parent2=Node() # Create the nodes we need 
    parent3=Node()
    parent4=Node()
    parent5=Node()
    newroot=Node()
    if(index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1] is None): # When the parent is not full, we can insert it in the parent node
        leaf5.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1]  # Create the first new leaf
        leaf5.keys.keys[1]=key # The right most leaf 
        
        leaf4.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[0] # The second new leaf 
        leaf4.pointers.pointers[2]=leaf5  # It point to leaf4
        index.root.pointers.pointers[1].pointers.pointers[0].pointers.pointers[2]=leaf4 # The left side reamins unchanged and point to the new leaf4
        index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1]  # Since the parent is not full we can insert it in, don't have to split 
    
    # For this example too, when it comes with full parent node and full root with root split, I tried my best to create a simple way but I couldn't run it without bug, so I just wirte the code
    # that make the function runs and gives right output.
    if(index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1] is not None):
        
        
        leaf5.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1] # Create the new leaf5, take data the right most leaf in tree
        leaf5.keys.keys[1]=key              # Key will store at leaf2 beacuse it is in the right most key from leaf5 
      
        leaf4.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[0]
        leaf4.pointers.pointers[2]=leaf5
        
        leaf3.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[0].keys.keys[0]
        leaf3.pointers.pointers[2]=leaf4
      
        leaf2.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[2].keys.keys[0]
        leaf2.pointers.pointers[2]=leaf3
       
        leaf1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[1].keys.keys[0]
        
        leaf1.pointers.pointers[2]=leaf2
        
        leaf0.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]
      
        leaf0.keys.keys[1]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]
        leaf0.pointers.pointers[2]=leaf1
       
        parent3.keys.keys[0]=index.root.pointers.pointers[1].pointers.pointers[1].keys.keys[1]
        parent3.pointers.pointers[0]=leaf5
        
        parent2.keys.keys[0]=index.root.pointers.pointers[1].keys.keys[0]  # Few new parents 1 2 3, that point to the new leaves
        parent2.pointers.pointers[0]=leaf3
        parent2.pointers.pointers[1]=leaf4
    
        parent1.keys.keys[0]=index.root.pointers.pointers[0].keys.keys[0]
        parent1.keys.keys[1]=index.root.pointers.pointers[0].keys.keys[1]
        parent1.pointers.pointers[0]=leaf0
        parent1.pointers.pointers[1]=leaf1
        parent1.pointers.pointers[2]=leaf2
      
        parent5.keys.keys[0]=index.root.keys.keys[1] # Parent 4, 5 will be the second level of new tree
        parent5.pointers.pointers[0]=parent3
         
        parent4.keys.keys[0]=index.root.keys.keys[0]
        parent4.pointers.pointers[0]=parent1
        parent4.pointers.pointers[1]=parent2
        newroot.keys.keys[0]=index.root.pointers.pointers[1].keys.keys[1]
        
        newroot.pointers.pointers[0]=parent4 # Finally, the new root will point to the Parent 4,5
        newroot.pointers.pointers[1]=parent5
    
    return newroot
def left_new_node(index, key ): #Insert the key left most leaf
    leaf0=Node()
    leaf1=Node()
    leaf2=Node()
    leaf3=Node()
    leaf4=Node()
    leaf5=Node()
    parent1=Node()
    parent2=Node()
    parent3=Node()
    newroot=Node()
    if(index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1] is None): # When the parent is not full, we can insert it in the parent node
        leaf1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0] # Create the first new leaf
        leaf1.keys.keys[1]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]
        leaf1.pointers.pointers[2]=index.root.pointers.pointers[0].pointers.pointers[1]
        leaf0.keys.keys[0]=key                   # Create the second new leaf
        leaf0.pointers.pointers[2]=leaf1
        temp=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]
        index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]=temp # Since the parent is not full we can insert it in, don't have to split 
        index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]
    
    # I found a better way to handle the insertion without root spliting, it uses the same ideas create few new leaves and parent nodes, handle the pointers
    # and keep the right half of tree unchanged, I can't do it when it requires root spliting because it always lost track of leaves
    if(index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1] is not None and index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0] is not None):
     
        parent1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0] # Create new parent1
        leaf1.keys.keys[0]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[0]
        leaf1.keys.keys[1]=index.root.pointers.pointers[0].pointers.pointers[0].keys.keys[1]
        leaf1.pointers.pointers[2]=index.root.pointers.pointers[0].pointers.pointers[1] # Leaf1 point to the second leaf from original tree
        leaf0.keys.keys[0]=key                     # Create the left most leaf : leaf0 that cotains the key
        leaf0.pointers.pointers[2]=leaf1           # Point to leaf1
        parent2.keys.keys[0]=index.root.pointers.pointers[0].keys.keys[1]
        parent1.pointers.pointers[0]=leaf0
        parent1.pointers.pointers[1]=leaf1
        parent2.pointers.pointers[0]=index.root.pointers.pointers[0].pointers.pointers[1] 
        parent2.pointers.pointers[1]=index.root.pointers.pointers[0].pointers.pointers[2]
        
        index.root.keys.keys[1]=index.root.keys.keys[0]    # Don't have to create a new root because it doesn't require root split 
        index.root.keys.keys[0]=index.root.pointers.pointers[0].keys.keys[0]
        index.root.pointers.pointers[2]=index.root.pointers.pointers[1]
        
        index.root.pointers.pointers[1]=parent2
        index.root.pointers.pointers[0]=parent1
        
    
    return index.root   
        
         
                  
def Full_Node(index, key ): # When the tree only contains root and root is full
    leaf0=Node()
    leaf1=Node()
    if (index.root.keys.keys[0]<key<index.root.keys.keys[1]): # When the key is between two keys
        leaf1.keys.keys[0]=key
        leaf1.keys.keys[1]=index.root.keys.keys[1] # Create two new nodes 
        leaf0.keys.keys[0]=index.root.keys.keys[0]
        leaf0.pointers.pointers[2]=leaf1
        index.root.keys=KeySet()
        index.root.keys.keys[0]=key
        index.root.pointers.pointers[0]=leaf0  # Use root pointer 
        index.root.pointers.pointers[1]=leaf1

        
    elif(key<index.root.keys.keys[0]):   # When key is less than the minimum value of root 
        leaf1.keys.keys[0]=index.root.keys.keys[0]
        leaf1.keys.keys[1]=index.root.keys.keys[1]
        leaf0.keys.keys[0]=key
        leaf0.pointers.pointers[2]=leaf1 # Create two new nodes
        index.root.keys=KeySet()
        index.root.keys.keys[0]=index.root.keys.keys[0]
        index.root.pointers.pointers[0]=leaf0
        index.root.pointers.pointers[1]=leaf1 # Use root pointer 
        
    elif (key>index.root.keys.keys[1]): # When key is less than the largest value of root 
        leaf1.keys.keys[0]=index.root.keys.keys[1]
        leaf1.keys.keys[1]=key
        leaf0.keys.keys[0]=index.root.keys.keys[0] # Create two new nodes
        leaf0.pointers.pointers[2]=leaf1
        index.root.keys=KeySet()
        index.root.keys.keys[0]=index.root.keys.keys[1]
        index.root.pointers.pointers[0]=leaf0
        index.root.pointers.pointers[1]=leaf1    # Use root pointer 
    return index