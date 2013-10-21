import os


string = """#Stephen Wolfram's Rule 110
NN 2 
#How many nearest neighbors in rules (must be even)

#BEGIN Rules
#Rule structure 
#R specifies rules, colon starts rule input
#Left hand side of semicolon is previous states
#Right hand side of semicolon is resultant states
R : 1, 1, 1 ; 0
R : 1, 1, 0 ; 0
R : 1, 0, 1 ; 1
R : 1, 0, 0 ; 1
R : 0, 1, 1 ; 0
R : 0, 1, 0 ; 1
R : 0, 0, 1 ; 1
R : 0, 0, 0 ; 0
#END Rules"""

def get_bit(number, bitlocation):
	if((number & 2**bitlocation) != 0):
		return 1
	else:
		return 0

for i in range(0, 256):
	rule = "Rule"+str(i)+".txt"
	if os.path.isfile(rule):
		pass
	else:
		with open(rule, 'w') as f:
			f.write("#Stephen Wolfram's Rule "+str(i)+"\n")
			f.write("NN 2\n")
			f.write("#How many nearest neighbors in rules (must be even)\n\n#BEGIN Rules\n#Rule structure\n#R specifies rules, colon starts rule input\n")
			f.write("#Left hand side of semicolon is previous states\n#Right hand side of semicolon is resultant states\n")
			for j in range(0, 8):
				f.write("R : "+ str(get_bit(j, 2)) + ", " + str(get_bit(j, 1)) + ", " + str(get_bit(j, 0)) + " ; " + str(get_bit(i, j)) + "\n")
			f.write("#END Rules\n")