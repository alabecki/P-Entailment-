#/usr/bin/python3

# P-Implication Solver ___________________________________________________________________________________________________________
# Author: Adam Labecki (2017)
# This program, is free software. Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), to deal in the Software 
#without restriction, including without limitation the rights to use, copy, modify, merge, publish, 
#distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software 
#is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial 
#portions of the Software.

# For further details see LICENSE 



 #Libraries______________________________________________________________________________________________________________________
from sympy import Symbol
from sympy.abc import*
from sympy.logic.boolalg import to_cnf
from sympy.logic.boolalg import Not, And, Or
from sympy.logic.inference import satisfiable, valid
from mpmath import*
from itertools import product
import sys
import os
from copy import deepcopy
from shutil import copyfile
from itertools import*
import re

from p_functions import*
from p_classes import*


options = {
	"1": "Check if 'a |- b' obtains by p-entailment",
	"2": "Return to previous..."
}


while(True):

	res = base()

	file = res[0]
	file_name = res[1]

	file.seek(0)
	propositions = obtain_atomic_formulas(file)
	#for p in propositions:					#fetches all atomic formulas found in a rule or constraint
		#print (p)
	file.seek(0)
	#rules = {}
	rules = construct_rules_dict(file)		# parses input text, make a Rule object for each rule, saves objects in dictionary
	file.seek(0)
	print("Rules:")
	for r, rule in sorted(rules.items()):
		print(r, rule.item)
	
	constraints = add_constraints(file)
	file.close()
	print ("Constraints:")
	for c, con in sorted(constraints.items()):
		print(c, con.item)
	print("\n")


	while True:
		opt = " "
		print("\n")
		print("____________________________________________________________________")
		while opt not in options.keys():
			print("What would you like to do?\n")
			for k, v in sorted(options.items()):
				print("%s: %s" % (k, v))
			print("____________________________________________________________________")
			print("\n")
			opt = input()
		if opt == "1":

			a = input("Please type in the 'a' formula \n")
			b = input("Please type in the 'b' formula \n")
			res = entailment_0Z(a, b, rules, constraints)
			print("\n")
			if res == True:
				print("####################################################################\n")
				print("%s p-entails %s " % (a, b))
				print("####################################################################")

			else:
				print("####################################################################\n")
				print("%s does not p-entail %s" % (a, b))
				print("####################################################################")

		if opt == "2":
			print("....\n")
			break