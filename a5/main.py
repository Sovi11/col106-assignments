
class Heap : 
    # The heap created is max heap
    # This stores tuples with the first element in the tuples as maximum data that can reach that node, the second as the name of that vertex 
    # store all the vertices ordered by their weights ( the first index ) , remove the 'completed' vertices
    def __init__(self):
        # initializes the heap as empty self.ele represents the list representation of the heap
        self.ele = []
    def size(self):
        # this returns the size (number of elements) in the heap
        return len(self.ele)

    def heap_up(self,i):
        # this is the heap up operation.
        # If the heap property is violated at one place, it takes in that index, and fixes it
        while i!=0:
            # until the parent node is reached or the heap is restored, cascade the heap up process
            if self.ele[(i-1)//2] < self.ele[i]:
                # swapping the child with its parent in the heap  
                self.ele[i],self.ele[(i-1)//2] = self.ele[(i-1)//2],self.ele[i]
                i=(i-1)//2
            else:
                break
    ## T.C = O(logn) ; where n is the number of elements in the heap
    def heap_down(self,i):
        # This is the heap down operation
        while 2*i+1 < self.size():
            # if while there is no child of the node to be 'heaped down'
            if 2*i+2 == self.size() :
                # if there does not exists any right child, swap with the left child if possible otherwise break the loop
                if self.ele[2*i + 1] > self.ele[i]:
                    # if the heap property is violated, swap
                    self.ele[i],self.ele[2*i+1] = self.ele[2*i+1],self.ele[i]
                    i=2*i + 1
                else:
                    # if not, break, we are done
                    break
            elif self.ele[2*i+1]>=self.ele[2*i+2]:
                # if the left child is bigger than right, swap with the left child
                if self.ele[2*i+1]> self.ele[i]:
                    # if the heap property is violated, swap
                    self.ele[i],self.ele[2*i+1] = self.ele[2*i+1],self.ele[i]
                    i=2*i + 1
                else:
                    # if not, break, we are done
                    break
            else:
                if self.ele[2*i+2] > self.ele[i]:
                    # if the heap property is violated, swap
                    self.ele[i],self.ele[2*i+2] = self.ele[2*i+2],self.ele[i]
                    i=2*i+2
                else:
                    # if not, break, we are done
                    break
    # T.C = O(logn) ; where n is the number of elements in the heap
    def add(self,element):
        # This is basically adding a element to the heap and restoring the heap property , if it is destroyed
        self.ele.append(element)
        self.heap_up(self.size()-1)
    # T.C = O(logn) ; where n is the number of elements in the heap
    def throw(self):
        # This is removing the top (maximum) element of the heap, also returning the removed value
        temp=self.ele[0]
        self.ele[0]=self.ele[-1]
        # put the last element in place of the first
        self.ele.pop()
        # remove the last element 
        self.heap_down(0)
        # apply heap down to restore the heap property 
        return temp
        # return temp variable ( which had stored the value of the maximum element of the heap)
    # T.C = O(logn) ; where n is the number of elements in the heap

# given the set of edges, translate them into adjacency list representation
# given a list with (a1,a2,weight) add it to a1, a2 

def findMaxCapacity(n,edge_list,source,end):
    if end==source :
        return(float('inf'),[])
    # if the end and the source are the same nodes , return infinity
    # completed list is basically a list with a boolean value for each of the vertices, if the vertices have been processed finally : then mark them as True, else false
    completed = [False for i in range(n)]
    adjacency_list=[[] for i in range(n)]
    # Adjacency list is a matrix with the ith row representing all the vetices, with their corresponding weights adjacent to the vertex i 
    vertex_with_weights=[-1 for i in range(n)]
    # vertex with weights ; this is a list that keeps updating the weights of the vetrex 
    # if a certain vertex is completed, then its weight in the vertex with weights list is its final weight ( here weight is the maximum amount of data reachable in one transmission)
    for (a,b,w) in edge_list:
        # This is how the vertex list is created, for every edge add the corresponding edge in adjacency list of both vertices
        adjacency_list[a].append((w,b))
        adjacency_list[b].append((w,a))
        # Note that the data is stored in adjacency list as (weight, vertex) ; where weight is the weight (or capacity) of the edge connecting a and b 
    # Time complexity = O(m) ; where m is the number of edges

    vertex_with_weights[source]=float('inf') 
    # Initializing as the source node with infinite weight, can transfer data from source to source iself with any 
    h=Heap()
    # an empty heap is created which will store the vertices with their weights
    h.add((float('inf'),source))
    # initially add the source vertex, with weight infinity
    prev=[-1 for i in range(n)]
    # prev is a list that stores the preeceding vertex in the 'best' path 
    # initialized to -1  

    final_weight=0
    # final weight is the value we wish to output as weight
    while h.size()!=0:
        # if the heap is empty implies that all of the vertex in a connected component have been traversed , and because in the problem description the graph is connected => the graph is completed
        k=h.throw()
        # throw the last element
        if completed[k[1]] : continue
        # if the vertex is completed ; restart the loop  
        completed[k[1]]=True 
        # if not, mark the vertex now as completed
        if k[1]==end:
            # if the vertex that is now completed is target vertex, stop 
            final_weight = k[0]
            break
        for (a,b) in (adjacency_list[k[1]]):
            # if not, add all the adjacent vertices for the given vertex
            if not completed[b]:
                # add only if they are not completed
                if vertex_with_weights[b]>=min(a,vertex_with_weights[k[1]]):
                    # if the the weight is already more than what can now be reached no need to update 
                    h.add((vertex_with_weights[b],b))
                else:
                    # if the the weight is more than what can now be reached no need to update 
                    h.add((min(a,vertex_with_weights[k[1]]),b))
                    vertex_with_weights[b]=min(a,vertex_with_weights[k[1]])
                    # the weight of the vertex is updated
                    prev[b]=k[1]
                    # updating prev indicates that a better path can now be chosen
    final_list=[end]
    # the final list is initialised as end
    i=end
    while prev[i]!=source:
        # final list gives the valid path according to maximum data 
        final_list.append(prev[i])
        # add prev
        i=prev[i]
    final_list.append(source)
    return (final_weight,final_list[::-1])
    # return weight , list 
