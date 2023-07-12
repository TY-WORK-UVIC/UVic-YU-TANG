# Counts the number of steps required to decompose a relation into BCNF.

from relation import *
from functional_dependency import *

# You should implement the static function declared
# in the ImplementMe class and submit this (and only this!) file.
# You are welcome to add supporting classes and methods in this file.
class ImplementMe:

    # Returns the number of recursive steps required for BCNF decomposition
    #
    # The input is a set of relations and a set of functional dependencies.
    # The relations have *already* been decomposed.
    # This function determines how many recursive steps were required for that
    # decomposition or -1 if the relations are not a correct decomposition.
    @staticmethod
    def DecompositionSteps( relations, fds ): #I have spread the function to four steps, input will go to specific functions to save some time
        
        result=-1
        
        len_relation=len(relations.relations) # length of relation
        len_fds=len(fds.functional_dependencies) # length of fds
        list_of_fds=seperate(fds) # Sepearte fds
        
        if(len_relation==1 and len_fds==1): # First part, when length of relation and length of fds are both equal to 1.
            result=one_to_one(relations, fds ) 
            
        if(len_relation==1 and len_fds>1): #Second part, when length of relation equal to 1 and length of fds greater than one
            list_of_closure=closure( relations, fds, len_fds,list_of_fds) #Find the closure of all the fds then store them in a list
            
            compare_result=compare(relations,list_of_closure) # Compare the closure with relations to check if they are superkeys
            
            if(compare_result==0): # If all of them are superkey, return 0
                result=0
        if(len_relation>1 and len_fds==1): #Third part, when length of relation >1 and length of fds = 1 
            
            superkey_check=check_superkey(relations, fds, len_fds,list_of_fds) #Check superkey when there are multiple relations
            
            if(superkey_check==0): # If all of them are superkey, return 0
                result=0
                
            else:
                result_compare=more_to_one(relations, fds, len_fds,list_of_fds) # Use more_to_one to find all possible decomposition
                result=check_equality(len_relation,result_compare) # Check if they have eqaul number of fds
                
        if(len_relation>1 and len_fds>1): #The last part, when length of relation >1 and length of fds > 1
            result=more_to_more(relations, fds, len_fds,list_of_fds) # Use more_to_more to find all possible decomposition
        
        return result
    
def more_to_more( relations, fds, len_fds,list_of_fds):
    i=0
    list2=[]
    list7=[]
    result=-1
    counter=1
    relations_unioned=union_relations(relations)
    list_of_closure=closure( relations_unioned, fds, len_fds,list_of_fds)             
    comare_result=compare_relations(  relations_unioned, list_of_closure)#Check if all the closures are superkeys, if they are return 0
    if(comare_result==0): #If all the closures are superkeys, return -1 because all the relations are subset of unioned realtion, so closure will                                 never equal to relations
        result=-1
    else:
        for d in fds.functional_dependencies: # Not all the closures are superkeys, we go through every fds
            set1=d.left_hand_side   
            set2=relations_unioned-list_of_closure[i] #Find all letters which is not in closure
            
            list2.append(i)  # A list which store the index 
            set7=list_of_closure[i] # R1
            list7.append(set7) #A list store R1 and R2
            if(set2 !=set()): # If R1 is not a superkey
                set2=set1.union(set2) # Union R1 with every letters not in R1 
                list7.append(set2)   #R2 in a list
                if(more_relations_compare(relations,list7)!=-1): # check if current R1 and R2 are superkeys for relations
                    result=1   #If it is we return 1 and exit the loop
                    break
                final=decomposes(relations,list_of_fds, i, set2,list2,list_of_closure,list_of_closure[i],counter) #Use decompose to find if all the final decomposition are equal to relations
                
                if(final!=-1): # If everything equal, we return final which is the number of times of decomposition 
                    result=final
                    break
            i=i+1
            
    return result

def decomposes(relations,list_of_fds, i, set2,list2,list_of_closure,set1,counter):
    list9=[]
    list9.append(set1) #A list append R1
    for j in range(len(list_of_fds)):
        set3=list_of_fds[j].left_hand_side.union(list_of_fds[j].right_hand_side) #Union j'th fd
        
        if(j not in list2 and set3.issubset(set2)):# List 2 is a list of index which I use to avoid duplication, if set3 is a subset of set2, it means I can decompose again
            list9.append(set3) # R3
            set4=set2-list_of_closure[j] # Everything not in R3
            set5=list_of_fds[j].left_hand_side
            set6=set4.union(set5)   #R4
            
            list9.append(set6)  #Append R3 R4
            list2.append(j)    #Avoid visit this fd again
          
    if(len(list9)==1): # It means nothing in R2 can be decompose again, so there is only R1 in the list
        list9.append(set2) #Append R2
        result_compare=more_relations_compare(relations,list9) # Compare them with relations if thay are equal return counter
        if(result_compare!= -1):
            counter=1
        else:
            counter=-1
    
    else:
        result_compare=more_relations_compare(relations,list9) #It means therer are multipl relations,so we compare them with input
        if(result_compare!= -1): #If they are equal return counter if not return -1
            counter+=1
        else:
            counter=-1
   
    return counter
            
def seperate(    fds ): # Seperate the fds and store them in a list 
    list1=[]
    for d in fds.functional_dependencies:
        list1.append(d)
    return list1    
                                          
def check_equality(len_relation,result_compare): # Check if the length of relations are equal to number of superkeys
    if(len_relation==result_compare):
        return 1
    else:
        return -1
                                          
def check_superkey(  relations, fds, len_fds,list_of_fds): #Check if the given fds are already all superkeys
    result=1
    relations_unioned=union_relations(relations) #Union relations 
    list_of_closure=closure( relations_unioned, fds, len_fds,list_of_fds) # List of closures
    comare_result=compare_relations(  relations_unioned, list_of_closure) # Compare them if all equal, return 0
    
    if(comare_result==0):
        result=0
    return result    
    
def compare_relations(relations,list_of_closure): # Compare the relation and clousure 
    
    result=0
    
    for i in range(len(list_of_closure)):       
        if(list_of_closure[i]!=relations):
             result=-1
    
    return result
def more_to_one( relations, fds, len_fds,list_of_fds): # When there is multiple relations and one fd
    list1=[]
    i=0
    
    relations_unioned=union_relations(relations) #Union relations
    list_of_closure=closure( relations_unioned, fds, len_fds,list_of_fds) # List of closures
    
    comare_result=compare_relations(  relations_unioned, list_of_closure) # Compare them if all equal, return 0
    if(comare_result!=0):
        for d in fds.functional_dependencies:         
            set1=d.right_hand_side           
            relations_unioned2=Relation(relations_unioned) # Change the type of relation
       
            set1=relations_unioned-set1 #Find the letter not in R1
          
            if(set1 !=set()):
                list1.append(list_of_closure[i]) # Append them in a list 
                list1.append(set1)
            i=i+1
                     
    result_compare=more_relations_compare(relations,list1) # Finally, compare them with relations
    
    return result_compare
                

        
def union_relations(relations): # Union all the relations to a single one 
    i=0
    list1=[]
    
    for e in relations.relations:           
        list1.append(e)     
    
    set3=set()
    for i in range(len(list1)-1):       
        set2=list1[i].attributes.union(list1[i+1].attributes) # Union every relations to a single one and return the set
        
        set3=set3.union(set2)
            
    return set3

def compare(relations,list_of_closure): # Compare relations and closures when there is only one relation
    result=0
   
    for e in relations.relations:
        for i in range(len(list_of_closure)):
            set4=Relation(list_of_closure[i])
            if(set4 != e):
                result=-1
    return result        
def more_relations_compare(relations,list_of_closure): # Compare relatoins with closures when there are multiple relations
    result=0
    
    if(len(list_of_closure)>=len(relations.relations)): # If there is less closure than relations, it means it is not in BCNF
        
        for e in relations.relations:
            for i in range(len(list_of_closure)):          
                set4=Relation(list_of_closure[i])
             
                if(set4 == e):   # Whenever, relations equal to closure we add one
                    
                    result=result+1          
        
    if(result!=len(list_of_closure)): # If final result not equal to length of list of closure, it means there is at least one closure not equal to realtions, it means not in BCNF. 
        result=-1          
            
    return result
def closure( relations, fds, len_fds,list_of_fds): # Find the closures of fds
    list_of_closure=[]
    for i in range(len_fds):
        list1=[]
        set1=list_of_fds[i].left_hand_side.union(list_of_fds[i].right_hand_side) # Union the fd we chosen
        list1.append(i)
        for k in range(len_fds):
            for j in range(len_fds):
                if(j not in list1 and list_of_fds[j].left_hand_side.issubset(set1)): # Go through whole list of fds to find if there is some closures of our chosen fd
                    set2=list_of_fds[j].left_hand_side.union(list_of_fds[j].right_hand_side) # Union the closure we find
                    set1=set1.union(set2)
                    list1.append(j) # Append this fd in a list, then we go to next fd
                    
        list_of_closure.append(set1)  
        
    return list_of_closure
def one_to_one(relations, fds ): # When there is only one relation and fd
    set22=set()
    for e in relations.relations:
        a=e
        for d in fds.functional_dependencies: 
            set1=d.left_hand_side
            set2=d.right_hand_side
            
            set3 = set1.union(set2)
            
            set22=set22.union(set3) #Union all the fds
            
        set4=Relation(set22)
        if(set4==a): # Compare it with relation if they are equal, it means it is a superkey return 0, if not return -1
            return 0
        else:        
            return -1