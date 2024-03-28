
def highest_pow_2(n):
    # This function calculates the highest power of 2 in the prime factorisation of n
    i=1
    while n%(2**i)==0:
        i+=1
    return i-1
    # it checks for atmost log(n) values of i, for which it finds the highest power
    # T.C = O(log(n))
def merge(a,b,c,d,temp,m,t):
    # This basically takes 4 indices of a list and merges it to make it sorted (given that the earlier indices had sorted subarrays between them)
    i=a
    j=c
    b = min(b,len(m[0]))
    d= min(d,len(m[0]))
    while i<b and j<d:
        # This is the similar algorithm that is used while sorting an array using mergesort
        # this is the algorithm which has 2 pointers and chooses the smaller value amongst the 2 
        if m[t-1][i][1]<m[t-1][j][1]:
            temp.append(m[t-1][i])
            i+=1
        else:
            temp.append(m[t-1][j])
            j+=1 
    if j<d:
        while j<d:
            temp.append(m[t-1][j])
            j+=1

    if i<b:
        while i<b:
            temp.append(m[t-1][i])
            i+=1
    # Time complexity = O(b-a + d-c)
    # O(sum of length of the small lists )
def binary_search_aux_l(a,b,m,key,toggle,layer):
    # This is the binary search for a sorted array to find out where key should have been
    # This is an auxiallry function
    # It is slightly modified for left index
    leftt=a 
    rightt = b 
    while rightt-leftt>1:
        x = (leftt + rightt)//2 
        if m[layer][x][toggle]== key:
            return x 
        elif m[layer][x][toggle]<key :
            leftt = x 
        else:
            rightt = x 
    if rightt == leftt:
        if key <= m[layer][leftt][toggle]:
            return leftt 
        else:
            return leftt+1 
    else:
        if key <= m[layer][leftt][toggle]:
            return leftt
        elif key > m[layer][rightt][toggle]:
            return rightt+1 
        else:
            return rightt
    # TC = O(log(n))
    # where n is the length of the array
def binary_search_l(m,key,toggle,layer):
    # this just fixes 2 values in binary search aux array
    return(binary_search_aux_l(0,len(m[0])-1,m,key,toggle,layer))
    # Time complexity = O(log(n))
def binary_search_aux_r(a,b,m,key,toggle,layer):
    # This is the binary search for a sorted array to find out where key should have been
    # This is an auxiallry function
    # It is slightly modified for right index
    leftt=a 
    rightt = b 
    while rightt-leftt>1:
        x = (leftt + rightt)//2 
        if m[layer][x][toggle]== key:
            return x 
        elif m[layer][x][toggle]<key :
            leftt = x 
        else:
            rightt = x 
    if rightt == leftt:
        if key == m[layer][leftt][toggle]:
            return leftt 
        elif key < m[layer][leftt][toggle]:
            return leftt - 1 
        else:
            return leftt
    else:
        if key < m[layer][leftt][toggle]:
            return leftt - 1
        elif key > m[layer][rightt][toggle]:
            return rightt
        elif key== m[layer][rightt][toggle]:
            return rightt
        elif key >= m[layer][leftt][toggle]:
            return leftt 
        else:
            return leftt
def binary_search_r(m,key,toggle,layer):
    # this just fixes 2 values in binary search aux array
    return(binary_search_aux_r(0,len(m[0])-1,m,key,toggle,layer))
    # T.C = O(log(n))
class PointDatabase:
    # This is the class PointDatabase
    def __init__(self,l):
        # Init makes the given list into a matrix of with number of rows log(n) and each row of length n 
        # each row is basically partially sorted w.r.t y, given it was initially sorted w.r.t x
        n=len(l)
        l.sort()
        # This is the first row, completely x-sorted
        m=[l,]
        i=1
        while 2**(i-1)<n:
            temp=[]
            j = 0
            while j<n:
                merge(j,j+2**(i-1),j+2**(i-1),j+2**i,temp,m,i)
                j+= 2**i
            m.append(temp)
            i+=1
        self.matrix = m
        # This takes a space complexity of O(n log(n))
        # and it takes time complexity of O(nlog(n))
        # Because merge will take O(n) time at worst case and it is applied for every iteration when i< log(n)
        # Hence the T.c of construction is O(nlog(n))
    def searchNearby(self,point,d):
        # This searches and outputs all the points within the range x-d,x+d and y-d,y+d
        ans=[]
        if self.matrix==[[]]:
            # To avoid error in binary search, if the matrix is empty (no points n==0), return empty ans
            return ans 
        else:
            a,b = point[0]-d , point[0]+d
            # These are the endpoints of x coordinates in the search
            index_start = binary_search_l(self.matrix,a,0,0)
            index_end = binary_search_r(self.matrix,b,0,0)
            # above are the starting and the ending index in the x sorted list
            # We break the found out region into chunks of power of 2 and find in sorted y in the correspoding level 
            while index_start<=index_end:
                # p1 will give the highest power of index
                if index_start==0:
                    p1 = highest_pow_2(len(self.matrix[0])) + 1
                    # set to a large arbitrary value if start index is 0
                else:
                    p1 = highest_pow_2(index_start)
                if index_start!=index_end:
                    while index_start + (2**p1)> index_end:
                        # if the p1 is too large, make it small to fit it in the end index range
                        p1-=1
                else:
                    p1=0
                # Apply binary search on y in the corresponding depth
                a1 = binary_search_aux_l(index_start,min(index_start-1+2**p1,index_end),self.matrix,point[1]-d,1,p1)
                a2 = binary_search_aux_r(index_start,min(index_start-1+2**p1,index_end),self.matrix,point[1]+d,1,p1)
                # this search takes O(log(n)) time and this while loop runs for log(n) iterations 
                # So the total time complexity of this process is O(logn*logn)
                for ii in range(a1,a2+1):
                    if ii<=index_end:
                        # append if the index is valid
                        ans.append(self.matrix[p1][ii])
                        # Here appending takes O(m) time
                index_start+=2**p1
                # increase the index value by 2**p1
            return ans
            # The final time complexity is hence O(m + log(n)**2)
