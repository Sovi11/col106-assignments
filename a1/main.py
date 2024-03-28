class Stack():
    # Implementing the stack class from 'scratch'
    def __init__(self):
        # input is just the instance of the class stack (input can be omitted if function is called by classifying the object first)
        # We initialise the Stack class, with initial size of 8, and all elements empty, hence set to 'None'
        self.ele=[None for i in range(8)]
        # self.ele is initially [None,None,None,None,None,None,None,None]
        self.length_of_stack=0
        # This variable keeps track of the length of the stack, i.e. the number of non None elements in the array
        # Invariant : All the non empty elements of the stack are together in the internal array and start from the beginning of the internal array
        self.length_of_internal_list=8   
        # Internal list is 'assumed' to be 'fixed in length' until it is doubled by a method. Initially is has a size 8
        # because we just need a last in first out data type, there is no need to circularly fill elements in the array
        # This is because the element filling in stack will always start from the start of the internal array. 

        # For eg. if self.ele is [1,2,3,None,None,None,None,None]
        # Then self.length_of_internal_list=8 and self.length_of_stack=3
        # This method changes the stack but returns nothing
    def double(self):
        # input is just the instance of the class stack (input can be omitted if function is called by classifying the object first)
        # This method doubles the length of the internal array, where the stack is implemented.
        s=[None for i in range(2*self.length_of_internal_list)]
        # we make a temporary array of size 2 times the size of the initial internal array (doubling the size)
        for i in range(self.length_of_internal_list):
            # We then copy all  the elements of the original array to the temporary array
            s[i]=self.ele[i]
            # Now the temporary array has first half of the elements filled from original array and latter half of the elements set to none  
        self.ele=s
        # We now assign the reference of the temporary array to the original array
        self.length_of_internal_list*=2
        # We update the size of the length of the internal array to 2 times the previous size
        # This method changes the stack but returns nothing
    def push(self,k):
        # This method takes in the instance of the stack, say l and an integer (in case of this assignment) .
        # Method can be called either as push(l,k) or l.push(k)
        # This method adds element k to the stack 
        if self.length_of_stack==self.length_of_internal_list:
            # If the array is fully filled, we do a doubling of the size of the array
            self.double()
        self.ele[self.length_of_stack]=k
        # We set the smallest indexed (first) element that is None to be equal to k
        self.length_of_stack+=1 
        # We increase the length of the stack variable by 1
        # This method changes the stack but returns nothing
    def pop(self):
        # input is just the instance of the class stack (input can be omitted if function is called by classifying the object first)
        # We set the largest indexed element (last) that is not None to be equal to None
        self.ele[self.length_of_stack-1]=None 
        self.length_of_stack-=1 
        # We decrease the length of the stack variable by 1
        # This method changes the stack but returns nothing
    def top(self):
        # input is just the instance of the class stack (input can be omitted if function is called by classifying the object first)
        # This returns the largest indexed (last) element of the array which is not None 
        return self.ele[self.length_of_stack - 1]
        # This method int object (in case of this assignment) could return any object type
def findPositionandDistance(s):
    # The input of the function is an object of the type string.  
    # This is the main function
    l=Stack()
    # l is the stack
    neg_bool,length_by_drone,x,y,z,i,current_multiplier=0,0,0,0,0,0,1
    # initializing all the variables. 
    # neg_bool keeps track if there is a minus sign before a variable, for eg. -X, -Y
    # length_by_drone keeps track of the length traversed by the drone
    # x,y,z keeps track of the coordinates of the drone. 
    # i is the counter variable
    # current_multiplier keeps track of the total multiplier, this is a dynamic counter whose value increases whenever we encounter a nuew multiplier, and whose value decreases when the brackets close.
    while i <len(s):
        # l is a stack that keeps track of the multipiers
        # it adds a new multiplier, and deletes it when the bracket is closed
        # ***the property of multipliers is that the multiplier added the last, is removed the first.
        if s[i]==')':
            # if the brackets close, then the current variable is reduced by the most recent multiplier
            current_multiplier=current_multiplier//l.top()
            l.pop()
            # We remove the multiplier from the stack now
        elif s[i]=='(' :
            # Opening brackets are not of use, given that the input expression is syntactically correct 
            pass 
        elif s[i]=='-':
            # If a '-' sign appears, => that the neg_bool variable should be converted to 1 to store this fact
            neg_bool=1
        elif s[i]=='+':
            # similarly is a '+' sign appears, => that the neg_bool variable should be converted to 0 to store this fact
            neg_bool=0
        elif s[i]=='X':
            length_by_drone+=current_multiplier 
            # increase the length_by_drone variable by the current multiplier
            x+=current_multiplier if neg_bool==0 else -current_multiplier
            # this is an inline if else statement, which says that if neg_bool is 0, increase the value of x by current_multiplier, otherwise decrease by current_multiplier
        elif s[i]=='Y':
            length_by_drone+=current_multiplier 
            # increase the length_by_drone variable by the current multiplier
            y+=current_multiplier if neg_bool==0 else -current_multiplier
            # this is an inline if else statement, which says that if neg_bool is 0, increase the value of y by current_multiplier, otherwise decrease by current_multiplier
        elif s[i]=='Z':
            length_by_drone+=current_multiplier 
            # increase the length_by_drone variable by the current multiplier
            z+=current_multiplier if neg_bool==0 else -current_multiplier
            # this is an inline if else statement, which says that if neg_bool is 0, increase the value of x by current_multiplier, otherwise decrease by current_multiplier
        else:
            # This section of the code deals with the numeric part of the string
            temp=0
            # this is a temporary variable initialized to 0
            temp+=int(s[i])
            # because s[i] is numeric in nature, we convert it into int(s[i]) and add it to temp
            # it may be the case that s[i+1] is also numeric, like in case of '832' as a multiplier, here '8' '3' and '2' are all numeric
            # but we need to read this as 832 and not separately as 8, 3 and 2
            while s[i+1].isnumeric():
                # Note: isnumeric() tells whether a character belongs to ['0','1','2','3,'..]
                # if the following character is also numeric, then we increase the value of temp, w.r.t the new character
                temp=temp*10 + int(s[i+1])
                i+=1
                # Note that this is the same i as for the initial while loop, hence the T.complexity is O(n) as each character is examined only once.
            current_multiplier=current_multiplier*temp
            l.push(temp)
            # This adds the temp variable as a multiplier to the stack
        i+=1
        # increasing the counter variable
    return [x,y,z,length_by_drone]
    # Output is a list of length 4, with type of the element as integers
    # The ouput is of list format with entries as the final coordinates of the drone and the length of the path traversed
