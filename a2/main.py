# The main idea will be described here:
# Using time of collisions as the thing to be built into a heap
# The least time of collision is used and 2 of the adjacent times of collision updated
# To keep track of which collisions are 'adjacent', a index list is maintained, which stores which indices go where after heap transformation
class heap():
    # Heap is made of the elements which are list. The dictionary ordering is used as the natural ordering in lists
    # This is the heap class, it takes in 2 inputs, elements ( the thing to be input to the heap)
    # and a index_list, which just stores the position of where the element which was initially at i, now is.
    def __init__(self,elements,index_list):
        self.ele=elements # elements are basically a list of list. The smaller list are a list of length 2, the first element being time and second being the index 
        self.build_heap(index_list)
        # we build a heap with the 'elements' and index_list being a parameter  
        self.index=index_list
        
    def size(self):
        # this returns the size (number of elements) in the heap
        return len(self.ele)
    def height(self):
        # this outputs the height of the heap ( because it is almost complete => it has a fixed length)
        j=0
        while 2**j < self.size() :
            j+=1
        if self.size() == 2**j -1 :
            return (j)
        else:
            return (j+1)
    def child(self,i):
        # This outputs the value of the child of the i th element in the heap
        # if no children exist, return infinity value
        # inf has the property, that min(a,inf) = a
        if 2*i + 1 >= self.size():
            return [[float('inf'),-1],[float('inf'),-1]]
        elif 2*i + 2 >= self.size():
            return [self.ele[2*i +1],[float('inf'),-1]]
        return [self.ele[2*i+1],self.ele[2*i+2]]
    def parent(self,i):
        # This gives the parent of the i th element of the heap
        if i==0:
            # there is no parent for the root
            return None
        else:
            return self.ele[(i-1)//2]
    def swap(self,i,j,index_list):
        # this is a function that swaps indices
        # it also makes the relevant changes in the index list (which keeps track of the position)
        self.ele[i],self.ele[j] = self.ele[j],self.ele[i]
        index_list[self.ele[i][1]],index_list[self.ele[j][1]] = index_list[self.ele[j][1]], index_list[self.ele[i][1]]
        # O(1)
    def heap_up(self,i,index_list):
        # this is the heap up operation.
        # If the heap property is violated at one place, it takes in that index, and fixes it
        while self.parent(i)!=None:
            if self.parent(i) > self.ele[i]:
                self.swap((i-1)//2,i,index_list)
                i=(i-1)//2
            else:
                break
        # O(log(n))
    def heap_down(self,i,index_list):
        # This is the heap down operation
        while self.child(i)!=[[float('inf'),-1],[float('inf'),-1]]:
            if self.child(i)[1]==[float('inf'),-1] :
                if self.child(i)[0] < self.ele[i]:
                    self.swap(i,2*i+1,index_list)
                    i=2*i + 1
                else:
                    break
            elif self.child(i)[0]<=self.child(i)[1]:
                if self.child(i)[0]< self.ele[i]:
                    self.swap(i,2*i+1,index_list)
                    i=2*i + 1
                else:
                    break
            else:
                if self.child(i)[1] < self.ele[i]:
                    self.swap(i,2*i+2,index_list)
                    i=2*i+2
                else:
                    break
        # O(log(n))
        # It essentially checks if the element can be heaped down
        # If so, it takes that element and heaps it down to where it satisfies the heap property
    def change_key(self,j,t,index_list):
        # t is Time_heap new time value
        # it changes the value of the first index at a position j and makes the structure heap back again
        if self.ele[j][0]==t:
            pass 
        elif self.ele[j][0]>t:
            self.ele[j][0]=t 
            self.heap_up(j,index_list)
        else:
            self.ele[j][0]=t  
            self.heap_down(j,index_list)
        # O(log(n))
    def build_heap(self,index_list):
        for i in range(self.size()-1,-1,-1):
            self.heap_down(i,index_list)
    # This builds the heap in O(n) time,
    # it makes use of the fact that a heap has a large number of heaps and heap down on them will save a lot of time. ( low height travel)

# previous_time, M, v, x are in same order as physical world
# This means that i th index of these above list is directly correlated to the ith block in the physical world.
def v_after_collision(i,M,v):
    # velocity of particle i and particle i+1 change after they collide
    # these formulas are the velocity after collisions of i th and i+1 th blocks, if the ith and i+1 th block have collided
    t1= (((2*M[i])/(M[i]+M[i+1]))*(v[i]) - (((M[i]-M[i+1])*v[i+1])/(M[i]+M[i+1])))
    t2= ((((M[i]-M[i+1])*v[i])/(M[i]+M[i+1])) +  ((2*M[i+1]/(M[i]+M[i+1]))*(v[i+1])))
    v[i] =t2
    v[i+1] = t1 
    # O(1)
def x_after_collision(i,x,v,running_time,previous_time):
    # position of all balls change, but only those have been updated which collided
    x[i] = x[i] + (running_time- previous_time[i])*v[i]
    x[i+1] = x[i+1] + (running_time - previous_time[i+1])*v[i+1]
    # the previous time refers to the last instance when they collided
    # O(1)
def time_after_collision(index_list,time_list,Time_heap,k1,k2):
    # This takes in the parameters k1 and k2, which are temporary variables defined in collision function
    if k1!=None:
        Time_heap.change_key(index_list[time_list[0][1]-1], k1,index_list)
    if k2!=None:
        Time_heap.change_key(index_list[time_list[0][1]+1] , k2,index_list)
    # it changes the collision time for i-1 and i block collision,
    # it changes the collision time for i+1 and i+2 block collision.

    Time_heap.change_key(index_list[time_list[0][1]],float('inf'),index_list)
    # O(log(n))
    # Because i and i+1 have just collided, they cannot collide again, hence the time is set to infinity
def collision(i,M,x,v,index_list,time_list,running_time,ans,previous_time,Time_heap):
    # This function takes in all the relevant parameters and simulates the whole collision
    A,B=((running_time,time_list[0][1]))
    # stores the current time and index of collision initially
    x_after_collision(i,x,v,running_time,previous_time)
    # updates the coordinates of ith and i+1 th block
    k1,k2=None,None
    if i>0:
        # if it is an inner block that has collided => there exists a i-1 block
        x1new = x[i-1] + v[i-1]*(running_time - previous_time[i-1])
        # coordinate updation for the i-1 th block
    if i < len(x) -2:  
        # if it is an inner block that has collided => there exists a i+1 block
        x2new = x[i+2] + v[i+2]*(running_time - previous_time[i+2])
        # coordinate updation of the i+2 th block
    v_after_collision(i,M,v)
    # update the velocities after collision
    if i>0:
        # 
        if v[i-1]==v[i]:
            # if velocities are in opposite direction => will never collide => infinite time 
            k1=float('inf')
            # k1 is the time of collision of i-1 and i th block
        elif - (x1new - x[i])/(v[i-1]-v[i]) < 0 :
            k1= float('inf')
        else:
            k1=  - (x1new - x[i])/(v[i-1]-v[i]) + running_time
    if i<len(x) - 2:
        # if velocities are in opposite direction => will never collide => infinite time 
        if v[i+2]==v[i+1]:
            # k2 is the time of collision of i+1 and i+2 th block
            k2=float('inf')
        elif - (x2new - x[i])/(v[i+2]-v[i+1]) < 0 :
            k2= float('inf')
        else:
            k2=  - (x2new - x[i])/(v[i+2]-v[i+1]) + running_time
    
    time_after_collision(index_list,time_list,Time_heap,k1,k2) # O(log(n))
    # update the times after collision (of i-1 and i+2 block next collision)
    
    previous_time[i]=running_time
    # change the last time they collided to the current time for i and i+1 blocks
    previous_time[i+1] = running_time
    ans.append((A,B,x[i]))
    # append a time, index and coordinate pair to the final list
    # O(log(n))
def initial_time(i,x,v):
    # this function calculates the initial time of collision between i and i+1 for any index i
    if v[i+1]!=v[i]:
        t= -((x[i+1]-x[i])/(v[i+1]-v[i]))
        if t>=0:
            return (t)
    return float('inf')
    # O(1)
def listCollisions(M,x,v,m,T):
    # This is the final function
    # It inputs mass, position, velocity, collision limit and time limit 
    # outputs a list of collisions in the form, (t,i,x)
    n=len(M)
    # n be the number of blocks
    running_time=0
    # running time be the current time
    cnt_coll=0
    # cnt_coll counts the total number of collisions occured
    previous_time = [0 for i in range(n)]
    # previous time stores the time, when the block i collided
    time_list = [[initial_time(i,x,v),i] for i in range(n-1)]
    # O(n)
    # its i th index keeps track of when will i and i+1 blocks collide 
    index_list = [i for i in range(n-1)]
    # it keeps track of where the time information of the ith index currently is
    Time_heap = heap(time_list,index_list) # O(n)
    # This makes a heap of list of 2 elements, first time, and second index
    ans=[]
    # initializing the final list to be empty
    while running_time<=T and cnt_coll<m :
        # the loop terminates if either the time exceeds time cap or the number of collisions exceed their upper bound
        if Time_heap.ele[0][0]==float('inf'):
            # If the root of the heap is inf => the Heap is empty and no more collisions are possible.
            break
        running_time =Time_heap.ele[0][0]
        # running time can be updated to when the collision happens
        if running_time>T:
            # if the time exceeds running time, then the loop should be terminates
            break
        i=Time_heap.ele[0][1]
        # i is the index of the colliding block
        collision(i,M,x,v,index_list,time_list,running_time,ans,previous_time,Time_heap)  # O(log(n))
        # run the collision function
        cnt_coll+=1
        # increase collision count by 1
    return ans
    # return a list of collisions represented by 3 tuples (i,t,x)

    # Analysing the time complexity.
    # velocity updation takes O(1) time
    # position updation takes O(1) time
    # finding adjacent index takes O(1) time
    # time updation takes O(log(n)) time => due to the fact that key has to be changes
    # time is updated atmost m times.
    # => all collision updation takes O(m*logn) time
    # building the initial heap takes O(n) time
    # creating finite number of lists with length n or n-1 => O(n)
    # The total time is hence O(n + m*logn)
