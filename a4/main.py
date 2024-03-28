import random
import math

def hash_val(s,pr):
	# This function calculates the hash value of a string using its conversion to a 26-ary number , modulo a prime
    ans=0
	# The initialization of the value is set to 0, [for horner's rule]
    for i in range(len(s)):
		# This is calculates the summation series, sum [(26**(len(s)-i-1) * s[i])], using horners rule
        ans=(ans*26 + char_val(s[i]))%pr 
			# the value of 'A' is 0, 'B' is 1.... 'Z' is 25  [values bounded between 0 and 25]
			# The value of '?' is assumed to be 0, as we will see why in modpatternmatchWildcard
		# the previous calculation is muliplied by 26, O(1) then the current term is added to it, so on until the complete polynomial is evaluated
    return ans 
	# The time complexity of the function is O(m log q),
	# m because of the loop running m times and log q because modulo operation in b bits takes O(b) time and q integer will be stored using log(q) bits

	# Note : This is the function f that was being refered to in the assignment 

def hash_val_ofm(m,p):
	# this function takes in the input m and evaluates the remainder of 26**m divided by q 
	ans=1
	# initially the answer is set to be 1
	for i in range(m):
		# the method to calculate power is just to repeatedly multiply the current power by 26 and take its remainder with q
		ans=(ans*26)%p 
	return ans
	# The time complexity of the function is O(m log q),
	# m because of the loop running m times and log q because modulo operation in b bits takes O(b) time and q integer will be stored using log(q) bits

def char_val(a):
	if a=='?':
		return 0
	# this just evaluates the position of the letters and ?
	# the value of 'A' is 0, 'B' is 1.... 'Z' is 25  [values bounded between 0 and 25]
	# The value of '?' is assumed to be 0, as we will see why in modpatternmatchWildcard
	return ord(a)-65
	# Time complexity is O(1) as the ord function takes O(1) time

#To generate random prime less than N
def randPrime(N):
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]
	# This function stores in a list of primes from less than N 
	# This then outputs a random prime number in the range
	# The time complexity and space complexity of the function is to be assumed to be O(1)

# To check if a number is prime
def isPrime(q):
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

#pattern matching
def randPatternMatch(eps,p,x):
	N = findN(eps,len(p))
	# O(1) time and space
	q = randPrime(N)
	# O(1) time and space
	return modPatternMatch(q,p,x)
	# O(k+ logn + logq) space ; O(n logq) time 

#pattern matching with wildcard
def randPatternMatchWildcard(eps,p,x):
	N = findN(eps,len(p))
	# O(1) time and space
	q = randPrime(N)
	# O(1) time and space
	return modPatternMatchWildcard(q,p,x)
	# O(k+ logn + logq) space ; O(n logq) time 

def findN(eps,m):
	# Here the value of N is to be calculated such that the probability of false positive is less than eps

	# PROOF of the value of N :
	
	# let a and b be 2 outputs f(s1) and f(s2) ; 
	# for false positives , a != b, but a%q == b%q 
	# => (a-b)%q==0 => (a-b) = n*q 
	# now (a-b) is bounded by 26**m as a and b lie between 0 and 26**m 
	# so (a-b) have atmost log2 (a-b) prime factors  					[ From claim 1 ]
	#  now if q is among one of these log2 (a-b) prime factors , then the function will report a false positive
	# The total number of  prime factors less than N >= N/2*log2(N)  	 [ From claim 2 ]
	# So the probability of q to give false positive atmost  log2(a-b) / ( N/2*log2(N))    [ Notice that the denomiantor is minimised and numerator maximised]
	# as (a-b) < 26**m 
	# => log (a-b) < m *(log2(26))    
	# prob [false +ve] <=  m *(log2(26))/ ( N/2*log2(N))  		 [ the numerator further increased]
	# if hence if we keep eps < prob[false +ve], then we get 
	# eps <=  m *(log2(26))/ ( N/2*log2(N)) 
	# => N/log2(N) >= (m/eps)*(9.4)  [final expression]


	# either N can be calculated using the code given below, approximately correct 
					# N=4 
					# while (N/(math.log2(N)))< (m/eps)*(2*math.log2(26)):
					# 	N=N*2
					# return N
	# or log2(N) <= N**(0.5) for large enough N ; 
	# Hence N/log(N)>= N**(0.5) 
	# if N is kept >= ((9.4)*(m/eps))**2 
	# then the above inequality also holds
	return int (88.36 * (m/eps)*(m/eps))+1 
	# the T.C of the code is O(1) as max is and other operations are also arithemetic hence O(1) ; O(1) space 

def modPatternMatch(q,p,x):
	# This takes in 3 inputs : q => the prime number ; p => the pattern ; x => the larger string  
	m=len(p)
	# store m as the length of the pattern, it will be useful in analysing the time complexity of the function
	r=hash_val(p,q)
	# r is the hash value, the 26-ary number modulo q of the pattern p. The helper function called takes O(m log q) time to compute it
	k=hash_val_ofm(m-1,q)
	# k is the remainder of 26**(m-1) when divided by q
	# It will be helpful to keep it calculated as it will be repeatedly be used in the rolling hash
	roll_hash=hash_val(x[0:m],q)
	# This is the initial value of rolling hash (stored in the rolling hash variable) [the hash value of first m element substring in x]
	i=0 
	ans_list=[]
	# ans list is the final list that will store all the indices of matches of the f(q) value with f(p)
	if roll_hash==r:
		# if the initial rolling hash is equal to the required rolling hash, then the index 0 can be appended to it
		ans_list.append(0)
	while i < len(x)-m:
		# for the entire range of i such that there is a continuous substring of length m in n, we update the roliing hash 
		# we do this by using the similar idea as horner rule we subtract the Most significant element, multiply by 26, add the smallest back again
		roll_hash= ((roll_hash-k*(char_val(x[i])))*26 + char_val(x[i+m]) + (26*26)*q) %q
		# the loop runs n-m times, and each step takes O(log q) time
		i+=1
		if roll_hash==r:
			# if the rolling hash matches with the precomputed hash of pattern, then we append the index in the final list
			ans_list.append(i)
	return ans_list
	# we output the final list such that it contains all the occurences where f(pattern) % q == f(substring) % q
	# The time complexity is O(3 * m log q + O(m-n *log q)) = O(n log q )  [ as m<=n]
	# The extra space required is to store [working space] consists of counters (in logn time), to store hash values (log q) [ the value is bounded by q] 
	# also the ans_list takes O(k) space  ;
	# The total space complexity is hence, O(log n + log q + k) 

def modPatternMatchWildcard(q,p,x):
	# The basic idea is that we neglect '?' and for doing so ; we remove the corresponding character in the text too, and by this, we compare the hash value of just the rest of the substring

	# This takes in 3 inputs : q => the prime number ; p => the pattern ; x => the larger string  
	m=len(p)
	# store m as the length of the pattern, it will be useful in analysing the time complexity of the function
	# here the pattern contains exactly one occurence of '?'
	question_pos=-1
	# this is set to store the value of the index where the question mark is put, this will be helpful in calculating rolling hash
	for i in range(m):
		if p[i]=='?':
			question_pos=i
			break 
	# whereever we see that p[i] is '?', we break the loop and report the value
	r=hash_val(p,q)
	# this is the hash value of the pattern, '?' assumed to be 0 in value
	k1=hash_val_ofm(m-1,q)
	# this is the remainder of 26**(m-1) when divided by q ; Time complexity is O(m log q)
	k2=hash_val_ofm(m-question_pos-1,q)
	# this is the remainder of 26**(m-question_pos-1) when divided by p ; the time complexity is O(m log q ) [ as m-ques_pos < m]
	roll_hash=(hash_val(x[0:m],q)-k2*char_val(x[question_pos])+26*q)%q
	# The rolling hash is initially set as the hash value of the starting substring excluding the value at question_pos
	i=0
	ans_list=[]
	# this list will store the indices where the mod value of hash functions match
	if roll_hash==r:
		# if th initial hash compares, then index 0 is included in our answer
		ans_list.append(0)
	while i < len(x)-m:
		roll_hash= ((roll_hash-k1*(char_val(x[i])))*26 + char_val(x[i+m]) + 26*k2*char_val(x[i+question_pos]) - k2* char_val(x[question_pos+i+1])+ (50*26)*q) %q
		# this step is the rolling hash step and takes  O(log q) time. Here 2 values are added and 2 subtracted [ the main idea is similar to horners rule]
		i+=1
		if roll_hash==r:
			# if the hash matches, append index value to the list
			ans_list.append(i)
	return ans_list
	# we output the final list such that it contains all the occurences where f(pattern) % q == f(substring) % q
	# The time complexity is O(3 * m log q + O(m-n *log q)) = O(n log q )  [ as m<=n]
	# The extra space required is to store [working space] consists of counters (in logn time), to store hash values (log q) [ the value is bounded by q] 
	# also the ans_list takes O(k) space  ;
	# The total space complexity is hence, O(log n + log q + k) 
