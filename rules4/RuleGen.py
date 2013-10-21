import os


#Use this program to build rules for nearest four neighbors.
#Rules variants run from MIN to MAX

NN = 4
MIN = 0
MAX = 1024


def get_bit(number, bitlocation):
	if((number & 2**bitlocation) != 0):
		return 1
	else:
		return 0

for i in range(MIN, MAX):
	rule = "Rule"+str(i)+".txt"
	if os.path.isfile(rule):
		pass
	else:
		with open(rule, 'w') as f:
			f.write("#RPC's Rule "+str(i)+"\n")
			f.write("NN "+str(NN)+"\n")
			f.write("#How many nearest neighbors in rules (must be even)\n\n#BEGIN Rules\n#Rule structure\n#R specifies rules, colon starts rule input\n")
			f.write("#Left hand side of semicolon is previous states\n#Right hand side of semicolon is resultant states\n")
			for j in range(0, 2**(NN+1)):
				outstr = "R : "
				for k in range(NN, -1, -1):
					 outstr += str(get_bit(j, k)) + ", "
				outstr = outstr[:-2]
				outstr += " ; " + str(get_bit(i, j)) + "\n"
				f.write(outstr)
			f.write("#END Rules\n")
